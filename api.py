import os
import logging
from dotenv import load_dotenv
from google.adk.cli.fast_api import get_fast_api_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


session_db_url = os.getenv("SESSION_DB_URL")

if not session_db_url:
    logger.warning("SESSION_DB_URL not found in .env file. Using InMemorySessionService.")
    session_db_url = ""

logger.info(f"Using Session DB URL: {'InMemory' if not session_db_url else session_db_url.split('@')[0] + '@...'}") # Avoid logging full credentials


agent_dir = "." # Current directory

app = get_fast_api_app(
    agent_dir=agent_dir,
    session_db_url=session_db_url,
    allow_origins=["*"],
    web=True
)

logger.info("FastAPI app created. Run with: uvicorn api:app --reload --port 8001")