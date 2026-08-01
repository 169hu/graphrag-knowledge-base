import os
from openai import OpenAI
from dotenv import load_dotenv
from graph_retriever import retrieve_from_graph, format_results

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def graph_qa(question):
    results = retrieve_from_graph(question)
    context = format_results(results)

    prompt = f"""基于以下从知识图谱中检索到的信息回答问题。

【图谱检索信息】
{context}

【用户问题】
{question}

【回答规则】
- 基于检索到的信息回答
- 如果信息不完整，可以补充你的知识
- 回答简洁、直接

【回答】
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    questions = [
        "DeepSeek 的总部在哪里？",
        "DeepSeek 开发了什么模型？",
        "梁文锋是谁？"
    ]
    for q in questions:
        print("\n" + "=" * 50)
        print(f"❓ {q}")
        print(f"🤖 {graph_qa(q)}")