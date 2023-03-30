import aiohttp
from io import BytesIO
from PIL import Image
import weakref


_mapping = {
    'background_one_anemo': 'template_one/background/ANEMO.png',
    'background_one_electro': 'template_one/background/ELECTRO.png',
    'background_one_gydro': 'template_one/background/GYDRO.png',
    'background_one_cryo': 'template_one/background/CRYO.png',
    'background_one_geo': 'template_one/background/GEO.png',
    'background_one_pyro': 'template_one/background/PYRO.png',
    'background_one_dendro': 'template_one/background/DENDRO.png',

    'background_adapt': 'template_one/background/ADAPT.png',
    'background_adapt_mask': 'template_one/background/FRAME_MASKA_ADAPT.png',

    'cart_center': 'template_one/background_character/CENTER.png',
    'cart_left': 'template_one/background_character/LEFT.png',
    'cart_right': 'template_one/background_character/RIGHT.png',

    'cart_center_mask': 'template_one/background_character/MASK_CENTER.png',
    'cart_left_mask': 'template_one/background_character/MASK_LEFT.png',
    'cart_right_mask': 'template_one/background_character/MASK_RIGHT.png',

    'nickname_icon': 'icon/NICK.png',

    'stars5': 'stars/Star5.png',
    'stars4': 'stars/Star4.png',
    'stars3': 'stars/Star3.png',
    'stars2': 'stars/Star2.png',
    'stars1': 'stars/Star1.png',

    'FIGHT_PROP_MAX_HP': 'icon/HP.png',
    'FIGHT_PROP_CUR_ATTACK': 'icon/ATTACK.png',

    'FIGHT_PROP_CUR_DEFENSE': 'icon/DEFENSE.png',
    'FIGHT_PROP_ELEMENT_MASTERY': 'icon/MASTERY.png',
    'FIGHT_PROP_CRITICAL': 'icon/CRITICAL_HURT.png',


    'FIGHT_PROP_CRITICAL_HURT': 'icon/CRITICAL.png',
    'FIGHT_PROP_CHARGE_EFFICIENCY': 'icon/CHARGE_EFFICIENCY.png',

    'FIGHT_PROP_ELEC_ADD_HURT': 'icon/ELECTRO.png',
    'FIGHT_PROP_DEFENSE_PERCENT': 'icon/DEFENSE_PERCENT.png',
    'FIGHT_PROP_ATTACK_PERCENT': 'icon/ATTACK_PERCENT.png',



    'FIGHT_PROP_HP_PERCENT': 'icon/HP_PERCENT.png',
    'FIGHT_PROP_WATER_ADD_HURT': 'icon/HYDRO.png',

    'FIGHT_PROP_WIND_ADD_HURT': 'icon/ANEMO.png',
    'FIGHT_PROP_ICE_ADD_HURT': 'icon/CRYO.png',
    'FIGHT_PROP_ROCK_ADD_HURT': 'icon/GEO.png',



    'FIGHT_PROP_FIRE_ADD_HURT': 'icon/PYRO.png',
    'FIGHT_PROP_GRASS_ADD_HURT': 'icon/DENDRO.png',

    'FIGHT_PROP_HEAL_ADD': 'icon/HEALED_ADD.png',
    'FIGHT_PROP_HEAL': 'icon/HEAL.png',
    'FIGHT_PROP_PHYSICAL_ADD_HURT': 'icon/PHYSICAL_ADD_HURT.png',


    'OPEN_CONSTANT_ANEMO': 'template_one/constant/open/OPEN_CONST_ANEMO.png',
    'OPEN_CONSTANT_CRYO': 'template_one/constant/open/OPEN_CONST_CRYO.png',
    'OPEN_CONSTANT_DENDRO': 'template_one/constant/open/OPEN_CONST_DENDRO.png',
    'OPEN_CONSTANT_ELECTRO': 'template_one/constant/open/OPEN_CONST_ELECTRO.png',
    'OPEN_CONSTANT_GEO': 'template_one/constant/open/OPEN_CONST_GEO.png',
    'OPEN_CONSTANT_GYDRO': 'template_one/constant/open/OPEN_CONST_GYDRO.png',
    'OPEN_CONSTANT_PYRO': 'template_one/constant/open/OPEN_CONST_PYRO.png',
    'OPEN_ADAPT_MASK_CONSTANT': 'template_one/constant/open/ADAPT.png',

    'CLOSED_CONSTANT_ANEMO': 'template_one/constant/closed/CLOSE_CONST_ANEMO.png',
    'CLOSED_CONSTANT_CRYO': 'template_one/constant/closed/CLOSE_CONST_CRYO.png',
    'CLOSED_CONSTANT_DENDRO': 'template_one/constant/closed/CLOSE_CONST_DENDRO.png',
    'CLOSED_CONSTANT_ELECTRO': 'template_one/constant/closed/CLOSE_CONST_ELECTRO.png',
    'CLOSED_CONSTANT_GEO': 'template_one/constant/closed/CLOSE_CONST_GEO.png',
    'CLOSED_CONSTANT_GYDRO': 'template_one/constant/closed/CLOSE_CONST_GYDRO.png',
    'CLOSED_CONSTANT_PYRO': 'template_one/constant/closed/CLOSE_CONST_PYRO.png',
    'CLOSED_CONSTANT': 'template_one/constant/closed/CLOSED.png',
    'CLOSED_ADAPT_MASK_CONSTANT': 'template_one/constant/closed/ADAPT.png',


    'SKILLS': 'template_one/talants/bg.png',

    }


# Define the base URL where files are stored on Github and a dictionary of file names
# Define a cache to store images that have already been downloaded
_BASE_URL = 'https://raw.githubusercontent.com/DEViantUA/ENCard/main/src/assets/'
_cache = weakref.WeakValueDictionary()


class openFile:
    # Method to download the image from the given URL and return its content in bytes
    @classmethod
    async def download_image(cls, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.content.read()
                return BytesIO(data)

    # Method to load the image from the given name and return it as a PIL Image object
    @classmethod
    async def _load_image(cls, name):
        url = _BASE_URL + name
        # Check if the image has already been downloaded and is in the cache
        if url in _cache:
            return _cache[url]
        else:
            image_data = await cls.download_image(url)
            image = Image.open(image_data)
            _cache[url] = image
            return image


    # Method to get the value of an attribute with the given name
    async def __getattr__(self, name):
        # Check if the attribute name is in the file name mapping
        if name in _mapping:
            return await self._load_image(_mapping[name])
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


