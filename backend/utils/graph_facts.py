from graph.db_connector import neo4j_connector
from typing import List


def get_graph_facts(node_id: str) -> List[str]:
    """
    Retrieve human-readable graph facts for a given node ID.
    For example: 'kitkat' -> ['KitKat is a product', 'KitKat is a brand of Nestlé']
    """
    query = """
    MATCH (a {id: $id})-[r]->(b)
    RETURN a.name AS source, type(r) AS relation, b.name AS target
    """
    results = neo4j_connector.execute_read(query, {"id": node_id})

    facts = []
    for row in results:
        source = row.get("source")
        relation = row.get("relation").replace("_", " ").lower()
        target = row.get("target")
        facts.append(f"{source} {relation} {target}")
    return facts
