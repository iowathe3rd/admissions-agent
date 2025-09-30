from pydantic import BaseModel
from typing import Optional, List
import datetime

# FAQ Schemas
class FAQBase(BaseModel):
    question: str
    answer: str

class FAQCreate(FAQBase):
    pass

class FAQ(FAQBase):
    id: int

    class Config:
        from_attributes = True

# Program Schemas
class ProgramBase(BaseModel):
    name: str
    description: Optional[str] = None
    cost: Optional[int] = None

class ProgramCreate(ProgramBase):
    pass

class Program(ProgramBase):
    id: int

    class Config:
        from_attributes = True

# Document Schemas
class DocumentBase(BaseModel):
    name: str
    required: bool = True

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int

    class Config:
        from_attributes = True

# Step Schemas
class StepBase(BaseModel):
    step_number: int
    description: str

class StepCreate(StepBase):
    pass

class Step(StepBase):
    id: int

    class Config:
        from_attributes = True

# RAG Search Schemas
class RAGQuery(BaseModel):
    query: str

class RAGContext(BaseModel):
    source: str
    text: str
    score: float

class RAGResponse(BaseModel):
    contexts: List[RAGContext]
