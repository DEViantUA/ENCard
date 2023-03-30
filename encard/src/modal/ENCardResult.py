from pydantic import BaseModel
from typing import List
from PIL import Image

class EnkaCard(BaseModel):
    id: int
    name: str
    element: str
    card: Image.Image
    class Config:
        arbitrary_types_allowed = True

class EnkaNetworkCard(BaseModel):
    uid: int
    name: str
    lang: str
    card: List[EnkaCard]