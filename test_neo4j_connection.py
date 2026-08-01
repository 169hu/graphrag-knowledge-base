import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

with driver.session() as session:
    result = session.run("MATCH (n) RETURN count(n) AS count")
    print("节点数量:", result.single()["count"])

driver.close()