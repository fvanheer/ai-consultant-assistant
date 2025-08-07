from logging import getLogger
import asyncio

from fastapi import FastAPI
from fastapi import HTTPException

from app.models import chat_request
from app.tasks import run_agent_task

logger = getLogger(__name__)

app = FastAPI()


@app.get("/health")
async def health_check():
    try:
        # Add any health checks here (database connection, etc.)
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )

# add response from ADK to the API call. 
@app.post("/api/v1/research")
async def process_document(request: chat_request):
    message = request.message

    try:
        logger.info("Starting document processing for message: %s",
                    message)
        asyncio.create_task(
            run_agent_task,
            message=message
        )
        return {"status": "Response processing"}
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the response"
        )