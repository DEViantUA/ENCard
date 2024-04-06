from pydantic import BaseModel
from typing import List,Optional
from PIL import Image

class EnkaCard(BaseModel):
    id: Optional[int]
    name: Optional[str]
    element: Optional[str]
    icon: Optional[str]
    card: Image.Image
    color: tuple
    class Config:
        arbitrary_types_allowed = True

class EnkaNetworkCard(BaseModel):
    uid: Optional[int]
    name: Optional[str]
    lang: Optional[str]
    card: List[EnkaCard]


class EnkaProfileCharter(BaseModel):
    id: int
    name: str
    icon: str
    element: str

class EnkaProfile(BaseModel):
    uid: int
    name: str
    lang: str
    charter: List[EnkaProfileCharter]
    character_name: str
    character_id: str
    card: Image.Image
    class Config:
        arbitrary_types_allowed = True