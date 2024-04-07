import aiohttp
import json

file_path = "encard/src/assets/data/namecard.json"

with open(file_path, "r") as file:
   mapping = json.load(file)

async def update_namecard(character_id):
   async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.ambr.top/v2/ru/avatar/{character_id}") as response:
            return await response.json()
         
class Get:
   def __init__(self,charter_id) -> None:
      self.charter_id = str(charter_id)
        
   async def __getattr__(self,name):
      if self.charter_id  in mapping:
            return mapping[self.charter_id].get(name)
      else:
            data = await update_namecard(self.charter_id)
            if data["data"]["other"] is None:
               mapping[self.charter_id] = {
                  "id": 210192,
                  "icon": f"https://api.ambr.top/assets/UI/namecard/UI_NameCardPic_OST4_P.png",
                  "image": f"https://api.ambr.top/assets/UI/namecard/UI_NameCardPic_OST4_P.png"
               }
            else:
               name_card_icon = data["data"]["other"]["nameCard"]["icon"]
               name_card_icon_image = data["data"]["other"]["nameCard"]["icon"].replace("NameCardIcon","NameCardPic")
               mapping[self.charter_id] = {
                  "id": data["data"]["other"]["nameCard"]["id"],
                  "icon": f"https://api.ambr.top/assets/UI/namecard/{name_card_icon}.png",
                  "image": f"https://api.ambr.top/assets/UI/namecard/{name_card_icon_image}_P.png"
               }
               
            with open(file_path, "w") as file:
               json.dump(mapping, file, indent=4)

            if self.charter_id  in mapping:
               return mapping[self.charter_id].get(name)
            else:
               raise AttributeError(f"'{type(self)}' object has no attribute '{self.charter_id}'")
