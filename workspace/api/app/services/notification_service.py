"""
Notification Service - 钉钉/邮件/站内信.
"""
import logging

from app.integrations.dingtalk_client import DingTalkClient

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, dingtalk_client: DingTalkClient | None = None):
        self.dingtalk = dingtalk_client

    async def send_dingtalk(self, user_id: int, title: str, content: str) -> bool:
        try:
            if self.dingtalk:
                await self.dingtalk.send_message(user_id, title, content)
            logger.info(f"DingTalk notification sent to user {user_id}: {title}")
            return True
        except Exception as e:
            logger.error(f"Failed to send DingTalk notification: {e}")
            return False

    async def send_email(self, email: str, subject: str, body: str) -> bool:
        # Placeholder - would use SMTP client in production
        logger.info(f"Email notification to {email}: {subject}")
        return True

    async def send_in_app(self, user_id: int, title: str, content: str) -> bool:
        # Placeholder - would store in notification table in production
        logger.info(f"In-app notification to user {user_id}: {title}")
        return True

    async def notify_task_assigned(self, user_id: int, task_title: str) -> bool:
        return await self.send_dingtalk(user_id, "任务指派", f"您被指派了新任务: {task_title}")

    async def notify_project_update(self, user_id: int, project_name: str, update: str) -> bool:
        return await self.send_dingtalk(user_id, "项目更新", f"项目 {project_name} 有更新: {update}")

    async def notify_risk_alert(self, user_id: int, project_name: str, risk_title: str) -> bool:
        return await self.send_dingtalk(user_id, "风险预警", f"项目 {project_name} 新增风险: {risk_title}")
