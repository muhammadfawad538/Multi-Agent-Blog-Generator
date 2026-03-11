from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class SupportContext(BaseModel):
    """
    Shared context object for the customer support team
    """
    customer_query: str = ""
    intent: Optional[str] = None
    knowledge_docs: List[Dict[str, Any]] = []
    solution: Optional[str] = None
    escalation_required: bool = False
    response: Optional[str] = None
    customer_info: Optional[Dict[str, Any]] = None
    conversation_history: List[Dict[str, str]] = []
    ticket_id: Optional[str] = None