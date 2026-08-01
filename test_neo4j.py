xiimport os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
username = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "")

driver = GraphDatabase.driver(uri, auth=(username, password))

# 测试连接
def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'Connected successfully!' AS message")
        print(result.single()["message"])

if __name__ == "__main__":
    test_connection()
    driver.close()