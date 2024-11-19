import asyncio,random
from PIL import ImageDraw,Image
from ..tools import git, pill,EnkanetworkApi
from ..modal import ENCardResult

_gitFile = git.openFile()


positions = [
    (3,303),
    (142,303),
    (281,303),
    (420,303),

    (3,473),
    (142,473),
    (281,473),
    (420,473),
]

async def get_element_icon(element):
    if element == "Fire":
        return await _gitFile.COLOR_PYRO
    elif element== "Grass":
        return await _gitFile.COLOR_DENDRO
    elif element == "Electric":
        return await _gitFile.COLOR_ELECTRO
    elif element == "Water":
        return await _gitFile.COLOR_HYDRO 
    elif element == "Wind":
        return await _gitFile.COLOR_ANEMO
    elif element== "Rock":
        return await _gitFile.COLOR_GEO
    else:
        return await _gitFile.COLOR_CRYO 


class ProfileOne:
    def __init__(self, **items):
        self.lang = items.get('lang', "ru")
        self.hide = items.get('hide')
        self.agent = items.get('agent')
        self.uid = items.get('uid')
        self.translation = items.get('translation')


    async def creat_namecard(self):
        namecard = self.info.namecard.banner.url
        namecard = await pill.get_dowload_img(namecard, size=(528, 201))
        namecard_frame = await _gitFile.BANNER_FRAME
        namecard.alpha_composite(namecard_frame, (0,0))
        return namecard
    
    async def creat_profil_pictures(self):
        background_avatart = await _gitFile.AVATAR
        mask_avatart = await _gitFile.AVATAR_MASK
        avatar = self.info.avatar.icon.url
        avatar = await pill.get_dowload_img(avatar, size=(163, 163))
        avatar = Image.composite(background_avatart, avatar, mask_avatart.convert("L"))
        background_avatart.alpha_composite(avatar, (0,0))

        return background_avatart


    async def creat_left(self):
        left_background = Image.new("RGBA", (574,657), (255,255,255,0))
        banner, pictures = await asyncio.gather(self.creat_namecard(), self.creat_profil_pictures())

        left_background.alpha_composite(banner,(35,9))
        left_background.alpha_composite(pictures,(218,98))

        font = await pill.get_font(19)
        draw = ImageDraw.Draw(left_background)

        if self.hide:
            random_num = random.randint(100000000, 999999999)
            draw.text((219,32), f"UID:{random_num}", font= font, fill=(255,255,255,255))
        else:
            draw.text((219,32), f"UID:{self.uid}", font= font, fill=(255,255,255,255))
        
        font = await pill.get_font(29)
        size = int(font.getlength(self.info.nickname))
        draw.text((int(299-size/2),290), self.info.nickname, font= font, fill=(71,81,106,255))

        font = await pill.get_font(25)
        draw.text((71,365), f"{self.translation.AR}:", font= font, fill=(255,255,255,255))
        size = int(font.getlength(str(self.info.level)))
        draw.text((int(522-size),365), str(self.info.level), font= font, fill=(255,255,255,255))
        
        draw.text((71,417), f"{self.translation.WL}:", font= font, fill=(255,255,255,255))
        size = int(font.getlength(str(self.info.world_level)))
        draw.text((int(522-size),417), str(self.info.world_level), font= font, fill=(255,255,255,255))

        signature = await pill.create_image_with_text(self.info.signature,25,max_width = 450, color = (124,112,96,255))

        left_background.alpha_composite(signature,(74,480))

        return left_background


    async def creat_charters_stand(self,charter):
        background = await _gitFile.CHARTER_BACKGROUND
        background = background.copy()
        CHARTER_MASK = await _gitFile.CHARTER_MASK
        charter_image = await pill.get_dowload_img(charter.icon.url, size=(119, 120))
        character_level = await EnkanetworkApi.get_charters(charter.id)
        if character_level.rarity == 5:
            character_level = await _gitFile.CHARTER_5
        else:
            character_level = await _gitFile.CHARTER_4
        character_level = character_level.copy()
        icon_elemnt = await get_element_icon(charter.element)
        icon_elemnt = icon_elemnt.resize((30,30))
        charter_image = Image.composite(character_level, charter_image, CHARTER_MASK.convert("L"))
        charter_image.alpha_composite(icon_elemnt,(0,4))
        character_level.alpha_composite(charter_image,(0,0))
        background.alpha_composite(character_level,(5,5))

        font = await pill.get_font(16)
        draw = ImageDraw.Draw(background)
        size = int(font.getlength(f"{self.translation.lvl} {charter.level}"))
        draw.text((int(63-size/2),128), f"{self.translation.lvl} {charter.level}", font= font, fill=(78,83,103,255))

        return background
        

    async def creat_right(self):
        right_background = Image.new("RGBA", (574,644), (255,255,255,0))

        font = await pill.get_font(16)
        draw = ImageDraw.Draw(right_background)
        
        size = int(font.getlength(self.translation.MP))
        draw.text((int(164-size/2),49), self.translation.MP, font= font, fill=(128,98,68,255))
        size = int(font.getlength(self.translation.NC))
        draw.text((int(386-size/2),49), self.translation.NC, font= font, fill=(128,98,68,255))

        font = await pill.get_font(19)
        draw.text((115,144), self.translation.AC, font= font, fill=(71,81,106,255))
        draw.text((391,144), self.translation.AB, font= font, fill=(71,81,106,255))

        font = await pill.get_font(31)
        draw.text((115,170), str(self.info.achievement), font= font, fill=(71,81,106,255))
        draw.text((391,170), f"{self.info.abyss_floor}-{self.info.abyss_room}", font= font, fill=(71,81,106,255))

        font = await pill.get_font(23)
        draw.text((43,245), self.translation.CS, font= font, fill=(128,98,68,255))
        

        tasks = [asyncio.create_task(self.creat_charters_stand(charters)) for charters in self.info.characters_preview]

        charters = await asyncio.gather(*tasks)

        for i,key in enumerate(charters):
            right_background.alpha_composite(key,positions[i])
            if i == 7:
                break

        return right_background

    async def profile(self):
        PROFILE_BACKGROUND = await _gitFile.PROFILE_BACKGROUND
        PROFILE_BACKGROUND = PROFILE_BACKGROUND.convert("RGBA")
        left_background = await self.creat_left()
        right_background = await self.creat_right()

        PROFILE_BACKGROUND.alpha_composite(left_background,(0,0))
        PROFILE_BACKGROUND.alpha_composite(right_background,(624,0))

        return PROFILE_BACKGROUND

    async def info_charter(self):
        charter_list = []
        character_name = ""
        character_id = ""
        for key in self.info.characters_preview:
            charter_list.append({"id": key.id, "name": key.name, "icon": key.icon.url, "element": str(key.element)})
            character_name += f"{key.name}, "
            character_id += f"{key.id}, "

        return charter_list,character_name,character_id

    async def start(self):
        info = await EnkanetworkApi.get_full_info(self.agent,self.lang,self.uid)
        self.info = info.player
        user_data = {
            "uid": self.uid,
            "name": info.player.nickname,
            "lang": self.lang,
            "charter": [],
            "character_name": "",
            "character_id": "",
            "card": None,
        }

        result = await asyncio.gather(self.profile(),self.info_charter())

        user_data["card"],user_data["charter"],user_data["character_name"],user_data["character_id"] = result[0],result[1][0],result[1][1],result[1][2]

        return ENCardResult.EnkaProfile(**user_data)

