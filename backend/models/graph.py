from pydantic import BaseModel


class GraphNode(BaseModel):
    id: str
    label: str
    name: str


class GraphEdge(BaseModel):
    source_id: str
    target_id: str
    relation: str
