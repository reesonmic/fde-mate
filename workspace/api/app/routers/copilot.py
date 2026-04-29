"""
Copilot Router - /api/v1/copilot/* (SSE)
"""
import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_async_session
from app.schemas.copilot import ChatRequest, PreviewActionRequest, ExecuteActionRequest
from app.services.copilot_service import CopilotService
from app.services.action_service import ActionService

router = APIRouter()


def get_copilot_service(session: AsyncSession = Depends(get_async_session)) -> CopilotService:
    return CopilotService(session)


def get_action_service() -> ActionService:
    return ActionService()


@router.post("/chat")
async def chat(req: ChatRequest, svc: CopilotService = Depends(get_copilot_service), user_id: int = 1):
    async def event_stream():
        try:
            async for chunk in svc.chat_stream(req, user_id):
                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/sessions")
async def list_sessions(svc: CopilotService = Depends(get_copilot_service), user_id: int = 1):
    return await svc.list_sessions(user_id)


@router.get("/sessions/{session_id}")
async def get_session(session_id: int, svc: CopilotService = Depends(get_copilot_service), user_id: int = 1):
    return await svc.get_session(session_id, user_id)


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: int, svc: CopilotService = Depends(get_copilot_service), user_id: int = 1):
    return await svc.delete_session(session_id, user_id)


@router.post("/preview-action")
async def preview_action(req: PreviewActionRequest, action_svc: ActionService = Depends(get_action_service), user_id: int = 1):
    return await action_svc.preview_action(req.tool_name, req.args, user_id)


@router.post("/execute-action")
async def execute_action(req: ExecuteActionRequest, action_svc: ActionService = Depends(get_action_service), user_id: int = 1):
    return await action_svc.execute_action(req.action_id, user_id)


@router.post("/cancel-action")
async def cancel_action(req: ExecuteActionRequest, action_svc: ActionService = Depends(get_action_service), user_id: int = 1):
    return await action_svc.cancel_action(req.action_id, user_id)


@router.post("/feedback")
async def feedback(body: dict, user_id: int = 1):
    return {"submitted": True}
