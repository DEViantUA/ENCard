import aiohttp
import asyncio

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"Error: {response.status}")
                return None


link_image = "https://api.ambr.top/assets/UI/namecard/{image}.png"
link_icon = "https://api.ambr.top/assets/UI/namecard/{icon}.png"
default_icon = "https://api.ambr.top/assets/UI/namecard/UI_NameCardIcon_0.png"
default_image = "https://api.ambr.top/assets/UI/namecard/UI_NameCardPic_0_P.png"

json_new = {}

async def main():
    charter_list = await fetch_data("https://api.ambr.top/v2/ru/avatar?vh=42F2")
    for key in charter_list["data"]["items"]:
        data_charter = await fetch_data(f"https://api.ambr.top/v2/ru/avatar/{key}?vh=42F2")
        if data_charter["data"]["other"] is None:
            json_new[key] = {"id": 210001, "icon": default_icon, "image": default_image}       
            continue
        output_string = data_charter["data"]["other"]["nameCard"]["icon"].replace("Icon_", "Pic_")
        output_string += "_P"
        json_new[key] = {"id": data_charter["data"]["other"]["nameCard"]["id"], "icon": link_icon.format(icon = data_charter["data"]["other"]["nameCard"]["icon"]), "image": link_image.format(image = output_string)}       
        
    print(json_new)

if __name__ == '__main__':
    asyncio.run(main())
