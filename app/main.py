import logging
from typing import List, Any, Optional, Union

from fastapi import FastAPI

# from app.routers import institution_router, language_router, language_group_router, language_group_mapping_router, counselor_router, pairing_router
from .routers import *


app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

app.include_router(institution_router.router, prefix="/institutions", tags=["Institutions"])
app.include_router(language_router.router, prefix="/languages", tags=["Languages"])
app.include_router(language_group_router.router, prefix="/language-groups", tags=["Language Groups"])
app.include_router(language_group_mapping_router.router, prefix="/language-group-mappings", tags=["Language Group Mappings"])
app.include_router(counselor_router.router, prefix="/counselors", tags=["Counselors"])
app.include_router(pairing_router.router, prefix="/pairings", tags=["Pairings"])
app.include_router(counseling_session_router.router, prefix="/counseling-sessions", tags=["Counseling Sessions"])
app.include_router(counseling_summary_router.router, prefix="/counseling-summaries", tags=["Counseling Summaries"])
app.include_router(counseling_chat_log_router.router, prefix="/counseling-chat-logs", tags=["Counseling Chat Logs"])
