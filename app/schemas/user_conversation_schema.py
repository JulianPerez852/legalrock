from pydantic import BaseModel
from typing import Optional

class UserConversationSchema(BaseModel):
    id_user: int
    id_conversation: Optional[int] = None
    conversation_kind: Optional[str] = "demanda_electrodomesticos"
    user_text: Optional[str] = None
    conversation_need: Optional[str] = None
    conversation_line: Optional[str] = None
    obtained_data: Optional[str] = None
    personality: Optional[str] = None
    temperature: Optional[float] = None
    obtained_files: Optional[str] = None
    historic_chat: Optional[list] = []
    is_finish: Optional[bool] = None
