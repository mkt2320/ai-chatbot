from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


class Neo4jConnector:
    def __init__(self, uri=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD):
        if not all([uri, username, password]):
            raise ValueError("Neo4j credentials are not set properly in .env")
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        if self.driver:
            self.driver.close()

    def execute_write(self, query: str, parameters: dict = {}):
        """Execute a write (CREATE, MERGE, DELETE) Cypher query."""
        with self.driver.session() as session:
            return session.execute_write(lambda tx: tx.run(query, **parameters).data())

    def execute_read(self, query: str, parameters: dict = {}):
        """Execute a read (MATCH, RETURN) Cypher query."""
        with self.driver.session() as session:
            return session.execute_read(lambda tx: tx.run(query, **parameters).data())


# Singleton instance to be reused across your API
neo4j_connector = Neo4jConnector()
