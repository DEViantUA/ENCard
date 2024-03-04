from .src.teamplate import generating_template_one
from .src.teamplate  import generation_profile_one
from .src.tools import translation
import asyncio,os,datetime

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


def check_ENCard_params(parameters):

    """
    ENCard parameter check.
    lang - must be a string and it must match the following data ["ru", "en"]
    characterImgs - must be a dictionary {"Name": Link_to_image, Path to file, or PILL.Image, "Name": Link_to_image, Path to file, or PILL.Image, ...}
    characterName - comma separated names line
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
    if not isinstance(parameters.characterImgs, dict):
        raise InvalidValueError("The characterImgs parameter must be a dictionary.")
    for key, value in parameters.characterImgs.items():
        if not isinstance(key, str):
            raise InvalidValueError("The keys in the characterImgs parameter must be strings.")
        if not isinstance(value, (str, str)):
           raise InvalidValueError(f"Invalid value for the key '{key}' in the characterImgs parameter")
    if not isinstance(parameters.characterName, str):
       raise InvalidValueError("The characterName parameter must be a string.")
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
    def __init__(self, lang="ru", characterImgs=None, characterName=None, adapt=False,
                 hide=False, save=False, agent="Library: 0.0.1_Beta"):
        """
        :param lang: str, What language to receive information supported:  en, ru, vi, th, pt, kr, jp, zh, id, fr, es, de, chs, cht.
        :param characterImgs: dict, Dictionary: {"Name_charter_1": "image link","Name_charter_2": "image link",...}.
        :param characterName: str, If we want to get certain characters: "Name_charter_1,Name_charter_1,Name_charter_1" Character names must be in the same language as in the lang parameter.
        :param adapt: bool, Adapt colors to custom image.
        :param hide: bool, Display UID.
        :param save: bool, Save images or not.
        :param agent: str, USER-AGENT to send requests.

        """

        self.lang = lang
        self.translator = translation.Translator(lang)
        self.characterImgs = characterImgs or {}
        self.characterName = characterName or ''
        self.adapt = adapt
        self.hide = hide
        self.save = save
        self.agent = agent
        check = check_ENCard_params(self)
        if check is True:
            pass
        else:
            return check

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass
    
    async def create_profile(self, uid, template=1):
        check = check_UID_and_template(uid, template)

        if check is not True:
            return check
        else:
            if template == 1:
                result = await generation_profile_one.ProfileOne(translation = self.translator,uid = uid, lang = self.lang, characterImgs = self.characterImgs, characterName = self.characterName, adapt = self.adapt, hide = self.hide, agent = self.agent).start()
        if self.save:
            await save_banner(uid, result.card, "profile")

        return result
    
    async def create_cards(self, uid, template=1):
        check = check_UID_and_template(uid, template)

        if check is not True:
            return check
        else:
            if isinstance(self.characterImgs, dict):
                chImg = {}
                for key in self.characterImgs:
                    if not key in chImg:
                        chImg[key.lower()] = self.characterImgs[key]
                self.characterImgs = chImg
            if template == 1:
                result = await generating_template_one.TeampleOne(translation = self.translator.lvl,uid = uid, lang = self.lang, characterImgs = self.characterImgs, characterName = self.characterName, adapt = self.adapt, hide = self.hide, agent = self.agent).start()
        if self.save:
            await asyncio.gather(*[save_banner(uid, key.card, key.name) for key in result.card])

                
        return result
