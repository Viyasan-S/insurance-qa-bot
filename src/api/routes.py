
from fastapi import APIRouter, HTTPException

from src.api.schemas import QuestionRequest, QuestionResponse
from src.retrieval.retriever import retrieve_policy
from src.generation.llm import generate_answer
from fastapi import APIRouter, HTTPException, Depends
from src.security.auth import verify_api_key

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Global Life Assurance Policy Assistant",
    }


@router.post("/ask", response_model=QuestionResponse)
def ask_policy(
    request: QuestionRequest,
    authenticated: bool = Depends(verify_api_key)
):  
    try:
        passages = retrieve_policy(request.question, top_k=3)

        if not passages:
            return QuestionResponse(
                question=request.question,
                answer=(
                    "I could not find sufficient information "
                    "in the available policy document."
                ),
                sources=[],
                notice=(
                    "This is a fictional insurance policy "
                    "for demonstration purposes only."
                ),
            )

        answer = generate_answer(request.question, passages)

        # Return unique source-page references.
        sources = []
        seen = set()

        for item in passages:
            key = (item["source"], item["page"])

            if key not in seen:
                seen.add(key)
                sources.append({
                    "source": item["source"],
                    "page": item["page"],
                })

        return QuestionResponse(
            question=request.question,
            answer=answer,
            sources=sources,
            notice=(
                "Illustrative answer based on a fictional "
                "insurance policy. Actual benefits depend "
                "on the applicable contract."
            ),
        )

    except Exception:
        # Do not expose internal exception details to API clients.
        raise HTTPException(
            status_code=503,
            detail="The policy assistant is temporarily unavailable.",
        )
