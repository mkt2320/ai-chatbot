from fastapi import APIRouter, HTTPException
from typing import Optional
from graph.db_connector import neo4j_connector
from models.graph import GraphNode, GraphEdge

router = APIRouter()


@router.post("/graph/add-node")
def add_node(node: GraphNode):
    query = f"""
    MERGE (n:{node.label} {{id: $id}})
    SET n.name = $name
    RETURN n
    """
    result = neo4j_connector.execute_write(query, {"id": node.id, "name": node.name})
    if result:
        return {"message": "Node added", "node": result[0]}
    raise HTTPException(status_code=400, detail="Failed to add node")


@router.post("/graph/add-edge")
def add_edge(edge: GraphEdge):
    query = f"""
    MATCH (a {{id: $source_id}}), (b {{id: $target_id}})
    MERGE (a)-[r:{edge.relation.upper()}]->(b)
    RETURN type(r)
    """
    result = neo4j_connector.execute_write(
        query, {"source_id": edge.source_id, "target_id": edge.target_id}
    )
    if result:
        return {"message": "Edge added", "relation": result[0]}
    raise HTTPException(status_code=400, detail="Failed to create edge")


@router.get("/graph/query")
def query_graph(label: Optional[str] = None):
    query = "MATCH (n) RETURN n" if not label else f"MATCH (n:{label}) RETURN n"
    result = neo4j_connector.execute_read(query)
    return {"nodes": result}
