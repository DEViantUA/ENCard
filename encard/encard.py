from enkanetwork import EnkaNetworkAPI
import asyncio,os,datetime
import random

from .src.teamplate import style_one
from .src.teamplate  import generation_profile_one
from .src.tools import translation
from .src.modal import ENCardResult

        
class InvalidValueError(ValueError):
    pass


def check_UID_and_template(UID, template):

    """
    A function that checks the UID and pattern for compliance.
    The UID must only be a number with type str or int.
    The template must be a number with type str or int.
    If both parameters meet the requirements, the function returns True,
    otherwise it returns a string with information about an invalid parameter.
    """

    if not isinstance(UID, (str, int)):
        return "The UID must be a string or a number"
    
    if isinstance(UID, str) and not UID.isdigit():
        return "The UID should only contain numbers"
    
    if not isinstance(template, (str, int)):
        return "The template must be a string or a number."
    
    if isinstance(template, str) and not template.isdigit():
        return "The template should only contain numbers."
    
    return True

async def get_character_art(character_art):
    processed_dict = {}
    for key, value in character_art.items():
        if isinstance(value, list):
            processed_dict[key] = random.choice(value)
        else:
            processed_dict[key] = value

    if processed_dict != {}:
        return processed_dict
    return None

async def get_color_user(color):
    processed_dict = {}
    for key, value in color.items():
        if isinstance(value, tuple):
            if len(value) >= 3 and len(value) <= 4:
                if all(0 <= x <= 255 for x in value):
                    processed_dict[key] = value
    if processed_dict != {}:
        return processed_dict
    return None

def check_ENCard_params(parameters):

    """
    ENCard parameter check.
    lang - must be a string and it must match the following data ["ru", "en"]
    character_image - must be a dictionary {"character_id": Link_to_image, "character_id": Link_to_image, ...}
    character_id - comma separated character id line
    adapt - True/False
    hide - True/False
    save - True/False
    nameCards - True/False
    agent - line
    """

    if not isinstance(parameters.lang, str):
        raise InvalidValueError("The lang parameter must be a string")
    
    if parameters.lang not in translation.supportLang:
        raise InvalidValueError(f"Invalid value for lang: {parameters.lang}")
    
    if not parameters.character_image is None:
        if not isinstance(parameters.character_image, dict):
            raise InvalidValueError("The character_image parameter must be a dictionary.")

        for key, value in parameters.character_image.items():
            if not isinstance(key, str):
                raise InvalidValueError("The keys in the character_image parameter must be strings.")
            if not isinstance(value, (str, str, list)):
                raise InvalidValueError(f"Invalid value for the key '{key}' in the character_image parameter")
    
    if not parameters.character_id is None:
        if not isinstance(parameters.character_id, str):
            raise InvalidValueError("The character_id parameter must be a string.")
   
    if not isinstance(parameters.adapt, bool):
       raise InvalidValueError("The parameter adapt must be a Boolean value")
   
    if not isinstance(parameters.hide, bool):
       raise InvalidValueError("The hide parameter must be a boolean value.")
   
    if not isinstance(parameters.save, bool):
        raise InvalidValueError("The save parameter must be a boolean value.")
    
    if not isinstance(parameters.agent, str):
        raise InvalidValueError("The agent parameter must be a string")
    
    return True


async def save_banner(uid,res,name):
        data = datetime.datetime.now().strftime("%d_%m_%Y %H_%M")
        path = os.getcwd()
        try:
            os.mkdir(f'{path}/EnkaImg')
        except:
            pass
        try:
            os.mkdir(f'{path}/EnkaImg/{uid}')
        except:
            pass
        res.save(f"{path}/EnkaImg/{uid}/{name}_{data}.png")

class ENCard:
    def __init__(self, lang="ru", character_image = None, character_id = None, adapt=False,
                 hide=False, save=False, agent= "Library: 0.0.1_Beta", color = None):
        """
        :param lang: str, What language to receive information supported:  en, ru, vi, th, pt, kr, jp, zh, id, fr, es, de, chs, cht.
        :param character_image: dict, Dictionary: {"character_id_1": "image_link","character_id_2": "image_link",...}.
        :param character_id: str, If we want to get certain characters: "character_id_1, character_id_1, character_id_1" Character names must be in the same language as in the lang parameter.
        :param adapt: bool, Adapt colors to custom image.
        :param hide: bool, Display UID.
        :param save: bool, Save images or not.
        :param agent: str, USER-AGENT to send requests.
        :param color: dict, Dictionary: {"character_id_1": (255,255,255,255), "character_id_2": (0,0,0,255),...}.

        """

        self.lang = lang
        self.translator = translation.Translator(lang)
        self.character_image = character_image or None
        self.character_id = character_id or None
        self.adapt = adapt
        self.hide = hide
        self.save = save
        self.agent = agent
        self.color = color or None
        
        check = check_ENCard_params(self)
        if check is True:
            pass
        else:
            return check

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass
    
    async def create_profile(self, uid, style=1):
        check = check_UID_and_template(uid, style)

        if check is not True:
            return check
        else:
            if style == 1:
                result = await generation_profile_one.ProfileOne(translation = self.translator,uid = uid, lang = self.lang, characterImgs = self.character_image, characterName = self.character_id, adapt = self.adapt, hide = self.hide, agent = self.agent).start()
        if self.save:
            await save_banner(uid, result.card, "profile")

        return result
    
    async def create_cards(self, uid, style=1):
        check = check_UID_and_template(uid, style)
        tasks = []
        
        if check is not True:
            raise TypeError(check)
        else:
            if isinstance(self.character_image, dict):
                self.character_image = await get_character_art(self.character_image)
            
            if isinstance(self.color, dict):
                self.color = await get_color_user(self.color)
            
            async with EnkaNetworkAPI(user_agent = self.agent, lang=self.lang) as client:
                info = await client.fetch_user(uid)
            
            if style == 1:
                for charters in info.characters:                    
                    if self.color:
                        color = self.color.get(str(charters.id))
                    else:
                        color = None
                          
                    if self.character_image:
                        character_image = self.character_image.get(str(charters.id))
                    else:
                        character_image = None
                        
                    if self.character_id:
                        if not str(charters.id) in self.character_id:
                            continue
                    tasks.append(style_one.Creat(info = charters, name = info.player.nickname, translator = self.translator, adapt = self.adapt, hide = self.hide, color = color, art = character_image, uid = uid).start())
                
            result = await asyncio.gather(*tasks)

            if self.save:
                await asyncio.gather(*[save_banner(uid, key["card"], key["name"]) for key in result])

            data = {
                "uid": uid,
                "name": info.player.nickname,
                "lang": self.lang,
                "card": result
            }
                    
            return ENCardResult.EnkaNetworkCard(**data)
    
    async def update_assets(self, path = None):
        client = EnkaNetworkAPI()
        async with client:
            await client.update_assets()
