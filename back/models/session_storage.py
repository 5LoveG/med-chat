import json
import os
from fastapi import HTTPException
from typing import List, Dict
from uuid import uuid4
from config import SESSION_STORAGE_DIR


class FileSessionStorage:
    def __init__(self):
        self.storage_dir = SESSION_STORAGE_DIR
        self._ensure_storage_dir()

    def _ensure_storage_dir(self):
        """确保存储目录存在"""
        os.makedirs(self.storage_dir, exist_ok=True)

    def _get_session_path(self, session_id: str) -> str:
        """获取会话文件路径"""
        return os.path.join(self.storage_dir, f"{session_id}.json")

    def create_session(self) -> str:
        """创建新会话"""
        session_id = str(uuid4())
        session_path = self._get_session_path(session_id)

        # 创建空会话文件
        with open(session_path, 'w') as f:
            json.dump([], f)

        return session_id

    def get_history(self, session_id: str) -> List[Dict]:
        """获取会话历史"""
        session_path = self._get_session_path(session_id)

        if not os.path.exists(session_path):
            return []

        try:
            with open(session_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to read session data: {str(e)}"
            )

    def add_message(self, session_id: str, role: str, content: str):
        """添加消息到会话"""
        session_path = self._get_session_path(session_id)

        if not os.path.exists(session_path):
            raise HTTPException(status_code=404, detail="Session not found")

        try:
            # 读取现有数据
            with open(session_path, 'r') as f:
                messages = json.load(f)

            # 添加新消息
            messages.append({"role": role, "content": content})

            # 写入更新后的数据
            with open(session_path, 'w') as f:
                json.dump(messages, f, indent=2)

        except (json.JSONDecodeError, IOError) as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update session data: {str(e)}"
            )

    def delete_session(self, session_id: str):
        """删除会话"""
        print(session_id)
        session_path = self._get_session_path(session_id)

        if os.path.exists(session_path):
            try:
                os.remove(session_path)
            except IOError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to delete session: {str(e)}"
                )
        else:
            raise HTTPException(status_code=404, detail="Session not found")
