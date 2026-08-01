import os
from neo4j import GraphDatabase
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "")

CYPHER_GENERATION_PROMPT = """
你是一个 Neo4j 专家。请根据用户的问题，生成一个 Cypher 查询语句。

重要规则：
1. 只返回 Cypher 查询语句，不要返回任何其他文字。
2. 查询语句必须符合 Neo4j 语法。

当前知识图谱的 Schema：
- 实体标签：Entity
- 实体属性：name（名称）、type（实体类型）
- 关系类型：RELATION
- 关系属性：type（关系类型，如"总部位于"、"开发了"、"是创始人"）

生成规则（参考示例）：
- 问"XX的总部在哪里" → MATCH (n {{name: 'XX'}})-[r:RELATION {{type: '总部位于'}}]->(m) RETURN m.name AS 地点
- 问"XX开发了什么" → MATCH (n {{name: 'XX'}})-[r:RELATION {{type: '开发了'}}]->(m) RETURN m.name AS 产品
- 问"XX是谁" → MATCH (n {{name: 'XX'}}) RETURN n.name AS 名称, n.type AS 类型

用户问题：{question}

Cypher 查询：
"""

def generate_cypher(question):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": CYPHER_GENERATION_PROMPT.format(question=question)}],
        temperature=0.1
    )
    cypher = response.choices[0].message.content.strip()
    cypher = cypher.replace("```cypher", "").replace("```", "").strip()
    return cypher

def execute_cypher(cypher_query):
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    results = []
    with driver.session() as session:
        result = session.run(cypher_query)
        for record in result:
            for key in record.keys():
                results.append(record[key])
    driver.close()
    return results

def format_results(results):
    if not results:
        return "未找到相关信息。"
    return "\n".join([str(r) for r in results])

def retrieve_from_graph(question):
    print(f"🔍 问题：{question}")
    cypher = generate_cypher(question)
    print(f"📝 生成的 Cypher：{cypher}")
    try:
        results = execute_cypher(cypher)
        print(f"📊 查询到 {len(results)} 条结果")
        return results
    except Exception as e:
        print(f"❌ 查询失败：{e}")
        return []

if __name__ == "__main__":
    test_question = "DeepSeek 的总部在哪里？"
    results = retrieve_from_graph(test_question)
    print("\n" + "=" * 40)
    print(format_results(results))