import os
import json
from neo4j import GraphDatabase
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

genxinURI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "")


# ===== 1. 增强版实体/关系抽取 =====
def extract_entities_and_relations(text):
    """用 LLM 从文本中抽取实体和关系（增强版：8 种实体类型 + 多种关系）"""

    prompt = f"""你是一个知识图谱抽取专家。请从以下文本中抽取实体和关系。

**实体类型（必须从以下选择）：**
- 人物：真实或虚构的人
- 组织：公司、机构、团队、政府部门
- 地点：城市、国家、区域、地标、地址
- 产品：软件、硬件、服务、品牌、商品
- 技术：编程语言、框架、协议、算法、标准
- 日期：具体日期、年份、时间段
- 事件：会议、比赛、发布、收购、签约
- 概念：抽象概念、理论、术语、行业名词

**关系类型（从以下选择或自定义）：**
- 总部位于、成立于、位于、位于附近
- 开发了、发布了、推出了、创建了
- 创始人是、CEO是、董事长是、员工是
- 收购了、投资了、合作了、合并了
- 属于、包含、隶属于、关联
- 提高了、降低了、实现了、推动了
- 参与了、主导了、负责了

**输出格式：** 必须为 JSON 数组，每个元素包含：
{{
  "entity": "实体名称",
  "entity_type": "实体类型（从上面选择）",
  "relation": "关系名称（从上面选择或自定义）",
  "target_entity": "目标实体名称",
  "target_type": "目标实体类型（从上面选择）"
}}

**示例：**
文本："阿里巴巴集团由马云于1999年在杭州创立，总部位于中国杭州，主要产品包括淘宝和阿里云。"
输出：
[
  {{"entity": "阿里巴巴集团", "entity_type": "组织", "relation": "成立于", "target_entity": "1999年", "target_type": "日期"}},
  {{"entity": "阿里巴巴集团", "entity_type": "组织", "relation": "总部位于", "target_entity": "杭州", "target_type": "地点"}},
  {{"entity": "阿里巴巴集团", "entity_type": "组织", "relation": "位于", "target_entity": "中国", "target_type": "地点"}},
  {{"entity": "马云", "entity_type": "人物", "relation": "是创始人", "target_entity": "阿里巴巴集团", "target_type": "组织"}},
  {{"entity": "阿里巴巴集团", "entity_type": "组织", "relation": "开发了", "target_entity": "淘宝", "target_type": "产品"}},
  {{"entity": "阿里巴巴集团", "entity_type": "组织", "relation": "开发了", "target_entity": "阿里云", "target_type": "产品"}}
]

现在请处理以下文本：
{text}

**重要：** 只输出 JSON 数组，不要添加任何解释或额外文字。
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    try:
        content = response.choices[0].message.content
        # 清理可能的 markdown 标记
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        result = json.loads(content)
        return result
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        print(f"原始输出: {content}")
        return []


# ===== 2. 入库函数（存储实体类型） =====
def add_to_neo4j(triples):
    """将抽取的三元组存入 Neo4j，实体类型作为节点属性"""
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    def _create_tx(tx, triple):
        query = """
        MERGE (e1:Entity {name: $entity})
        SET e1.type = $entity_type
        MERGE (e2:Entity {name: $target_entity})
        SET e2.type = $target_type
        MERGE (e1)-[r:RELATION {type: $relation}]->(e2)
        RETURN e1, r, e2
        """
        result = tx.run(query, **triple)
        return result.single()

    with driver.session() as session:
        for triple in triples:
            # 设置默认值，防止 None
            triple['entity_type'] = triple.get('entity_type', '未知类型')
            triple['target_type'] = triple.get('target_type', '未知类型')
            try:
                session.execute_write(_create_tx, triple)
                print(
                    f"✅ 已创建: {triple['entity']} ({triple['entity_type']}) -[{triple['relation']}]-> {triple['target_entity']} ({triple['target_type']})")
            except Exception as e:
                print(f"❌ 创建失败: {e}")

    driver.close()


# ===== 3. 主函数 =====
def build_graph_from_text(text):
    """从文本构建知识图谱"""
    triples = extract_entities_and_relations(text)
    if not triples:
        print("❌ 未抽取到有效三元组")
        return

    print(f"\n📊 抽取到 {len(triples)} 个三元组")
    for t in triples:
        print(f"  {t['entity']} ({t['entity_type']}) -[{t['relation']}]-> {t['target_entity']} ({t['target_type']})")

    print("\n开始入库...")
    add_to_neo4j(triples)
    print("\n✅ 知识图谱构建完成！")


# ===== 4. 清空图谱函数（可选） =====
def clear_graph():
    """清空所有节点和关系"""
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    driver.close()
    print("✅ 图谱已清空")


# ===== 5. 测试 =====
if __name__ == "__main__":
    test_text = """
    DeepSeek 是一家中国人工智能公司，总部位于杭州。
    它开发了 DeepSeek-V2 和 DeepSeek-V3 模型。
    梁文锋是 DeepSeek 的创始人。
    """
    build_graph_from_text(test_text)