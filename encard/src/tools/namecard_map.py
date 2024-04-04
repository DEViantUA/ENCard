import json
from typing import Any, Literal

import aiohttp


PATH = "ENCard/encard/src/assets/maps/namecard_map.json"

class Get:
    def __init__(self,charter_id) -> None:
        self.charter_id = str(charter_id)
        with open(PATH) as f:
            self._mapping = json.load(f)
        
    def __getattr__(self, name: str) -> Any:
        if self.charter_id in self._mapping:
            return self._mapping[self.charter_id][name]
        else:
            return {
                "id": 210001,
                "icon": "https://api.ambr.top/assets/UI/namecard/UI_NameCardIcon_0.png",
                "image": "https://api.ambr.top/assets/UI/namecard/UI_NameCardPic_0_P.png",
            }[name]

async def update_data() -> None:
    result: dict[str, dict[Literal["id", "icon", "image"]]] = {}
    namecards_data = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/namecards.json"
    characters_data = "https://raw.githubusercontent.com/seriaati/enka-py-assets/main/data/characters.json"
    all_characters = "https://api.ambr.top/v2/en/avatar"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(namecards_data) as response:
            namecards: dict[str, dict[Literal["icon"], str]] = json.loads(await response.text())
        
        async with session.get(characters_data) as response:
            characters: dict[str, dict[str, Any]] = json.loads(await response.text())
            
        async with session.get(all_characters) as response:
            all_characters: dict[str, dict[str, Any]] = await response.json()
            
    namecard_map: dict[str, str] = {
        namecard["icon"]: namecard_id for namecard_id, namecard in namecards.items()
    }
    
    for character_id, character in characters.items():
        namecard_icon: str | None = character.get("NamecardIcon")
        if namecard_icon is not None:
            result[character_id] = {
                "id": namecard_map[namecard_icon],
                "icon": f"https://api.ambr.top/assets/UI/namecard/{namecard_icon.replace('Icon', 'Pic').replace('_P', '')}.png",
                "image": f"https://api.ambr.top/assets/UI/namecard/{namecard_icon}.png",
            }
    
    # Travelers
    for character_id in all_characters["data"]["items"]:
        if character_id not in result:
            result[character_id] = {
                "id": 210001,
                "icon": "https://api.ambr.top/assets/UI/namecard/UI_NameCardIcon_0.png",
                "image": "https://api.ambr.top/assets/UI/namecard/UI_NameCardPic_0_P.png",
            }
            
    with open(PATH, "w") as f:
        json.dump(result, f)