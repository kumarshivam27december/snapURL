from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Image(BaseModel):
    filename: str
    url: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    description: Optional[str] = None
    size: Optional[int] = None
    content_type: Optional[str] = None
