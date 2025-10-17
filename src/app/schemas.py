from pydantic import BaseModel, Field
from typing import Optional, List

# FAQ Schemas
class FAQBase(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="Question text")
    answer: str = Field(..., min_length=1, max_length=2000, description="Answer text")

class FAQCreate(FAQBase):
    pass

class FAQ(FAQBase):
    id: int = Field(..., gt=0, description="FAQ record ID")

    class Config:
        from_attributes = True

# Program Schemas
class ProgramBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Program name")
    description: Optional[str] = Field(None, max_length=1000, description="Program description")
    cost: Optional[int] = Field(None, ge=0, description="Program cost in rubles")

class ProgramCreate(ProgramBase):
    pass

class Program(ProgramBase):
    id: int = Field(..., gt=0, description="Program record ID")

    class Config:
        from_attributes = True

# Document Schemas
class DocumentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Document name")
    required: bool = Field(default=True, description="Whether the document is required")

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int = Field(..., gt=0, description="Document record ID")

    class Config:
        from_attributes = True

# Step Schemas
class StepBase(BaseModel):
    step_number: int = Field(..., ge=1, le=100, description="Sequential step number")
    description: str = Field(..., min_length=1, max_length=500, description="Step description")

class StepCreate(StepBase):
    pass

class Step(StepBase):
    id: int = Field(..., gt=0, description="Step record ID")

    class Config:
        from_attributes = True

# RAG Search Schemas
class RAGQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="Search query")

class RAGContext(BaseModel):
    source: str = Field(..., min_length=1, description="Source of the context")
    text: str = Field(..., min_length=1, description="Context text content")
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score between 0 and 1")

class RAGResponse(BaseModel):
    contexts: List[RAGContext] = Field(default=[], description="List of relevant contexts")
