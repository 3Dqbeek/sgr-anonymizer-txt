from pydantic import BaseModel, Field
from typing import List

class IpExtraction(BaseModel):
    """
    IP-адреса: '192.168.1.1', '2001:db8::1'
    """
    raw_ips: List[str] = Field(default_factory=list)
    justification: str = Field(default="", description="Почему IP — ПДн по ФЗ-152?")
    fragments_to_replace: List[str] = Field(default_factory=list)