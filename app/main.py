import logging

from fastapi import FastAPI

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
app.include_router(counseling_type_router.router, prefix="/counseling-types", tags=["Counseling Types"])
app.include_router(counseling_type_group_router.router, prefix="/counseling-type-groups", tags=["Counseling Type Groups"])
app.include_router(websocket_router.router, prefix="/ws", tags=["Counseling Chat Logs"])
