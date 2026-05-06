"""
Copilot Router - /api/v1/copilot/* (SSE)
"""
import asyncio
import json
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_async_session
from app.schemas.copilot import ChatRequest, PreviewActionRequest, ExecuteActionRequest
from app.services.copilot_service import CopilotService
from app.services.action_service import ActionService
from app.deps.auth import UserContext, current_user

router = APIRouter()


def get_copilot_service(session: AsyncSession = Depends(get_async_session)) -> CopilotService:
    return CopilotService(session)


def get_action_service() -> ActionService:
    return ActionService()


@router.post("/chat")
async def chat(
    request: Request,
    req: ChatRequest,
    svc: CopilotService = Depends(get_copilot_service),
    user: UserContext = Depends(current_user),
):
    trace_id = getattr(request.state, "trace_id", "unknown")

    async def event_stream():
        try:
            async for chunk in svc.chat_stream(req, user.id):
                yield f"data: {json.dumps({**chunk, 'traceId': trace_id}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except asyncio.CancelledError:
            # Client disconnected
            return
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e), 'traceId': trace_id})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "X-Trace-Id": trace_id,
        },
    )


@router.get("/sessions")
async def list_sessions(svc: CopilotService = Depends(get_copilot_service), user: UserContext = Depends(current_user)):
    return await svc.list_sessions(user.id)


@router.get("/sessions/{session_id}")
async def get_session(session_id: int, svc: CopilotService = Depends(get_copilot_service), user: UserContext = Depends(current_user)):
    return await svc.get_session(session_id, user.id)


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: int, svc: CopilotService = Depends(get_copilot_service), user: UserContext = Depends(current_user)):
    return await svc.delete_session(session_id, user.id)


@router.post("/preview-action")
async def preview_action(req: PreviewActionRequest, action_svc: ActionService = Depends(get_action_service), user: UserContext = Depends(current_user)):
    return await action_svc.preview_action(req.tool_name, req.args, user.id)


@router.post("/execute-action")
async def execute_action(req: ExecuteActionRequest, action_svc: ActionService = Depends(get_action_service), user: UserContext = Depends(current_user)):
    return await action_svc.execute_action(req.action_id, user.id)


@router.post("/cancel-action")
async def cancel_action(req: ExecuteActionRequest, action_svc: ActionService = Depends(get_action_service), user: UserContext = Depends(current_user)):
    return await action_svc.cancel_action(req.action_id, user.id)


@router.post("/feedback")
async def feedback(body: dict, user: UserContext = Depends(current_user)):
    return {"submitted": True, "userId": user.id}
