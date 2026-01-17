# backend/app/schemas/msg.py
from pydantic import BaseModel

class Msg(BaseModel):
    """
    Pydantic model for simple message responses.
    """
    msg: str