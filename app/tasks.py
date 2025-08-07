import os
import uuid
from logging import getLogger

from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

from agents.researcher import root_agent as researcher_agent

logger = getLogger(__name__)

SESSION_DATABASE_URL = os.getenv('CORTEX_DATABASE_URL')
session_service_stateful = DatabaseSessionService(db_url=SESSION_DATABASE_URL)

async def delete_session(runner: Runner, app_name: str, user_id: str, session_id: str):
    try:
        await runner.session_service.delete_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
    except Exception as ex:
        logger.error(ex)
        logger.error("Delete session failed. Moving on...")
        pass

#add user_id from chainlit
async def run_agent_task(message: str = None):
    user_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    app_name = "researchAgent"

    new_message = types.Content(
        role="user",
        parts=[types.Part(
            text=f"message:{message}")],
    )
    try:
        runner = Runner(
            agent=researcher_agent,
            app_name=app_name,
            session_service=session_service_stateful,
        )

        await delete_session(runner, app_name, user_id, session_id)
        await runner.session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )

        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=new_message):
            logger.info("Processing event: %s", event)

    except Exception as e:
        logger.error(f"Error in background task: {str(e)}")
        raise