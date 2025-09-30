from fastapi import APIRouter

from app.schemas import RAGQuery, RAGResponse
from src.rag.retriever import retrieve_context

router = APIRouter()

@router.post("/rag", response_model=RAGResponse)
async def search_rag(query: RAGQuery):
    """
    (Debug endpoint) Takes a query and returns the raw context chunks 
    retrieved from the RAG pipeline before they are sent to the LLM.
    """
    contexts = retrieve_context(query.query)
    return RAGResponse(contexts=contexts)
