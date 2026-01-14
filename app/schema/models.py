from pydantic import BaseModel
from typing import List, Optional

class IngestRequest(BaseModel):
    documents: List[str]
    metadata: Optional[dict] = None

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]