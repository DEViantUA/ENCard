import asyncio
from PIL import ImageDraw,Image

from enkanetwork.enum import EquipmentsType, DigitType
from enkanetwork.model.stats import Stats
from ..tools import git, namecard_map, pill,EnkanetworkApi
from ..modal import ENCardResult


_gitFile = git.openFile()

IconAddTrue = ["FIGHT_PROP_PHYSICAL_ADD_HURT","FIGHT_PROP_HEAL_ADD","FIGHT_PROP_GRASS_ADD_HURT","FIGHT_PROP_FIRE_ADD_HURT","FIGHT_PROP_MAX_HP","FIGHT_PROP_CUR_ATTACK","FIGHT_PROP_CUR_DEFENSE","FIGHT_PROP_ELEMENT_MASTERY","FIGHT_PROP_CRITICAL","FIGHT_PROP_CRITICAL_HURT","FIGHT_PROP_CHARGE_EFFICIENCY","FIGHT_PROP_ELEC_ADD_HURT","FIGHT_PROP_ROCK_ADD_HURT","FIGHT_PROP_ICE_ADD_HURT","FIGHT_PROP_WIND_ADD_HURT","FIGHT_PROP_WATER_ADD_HURT"]
dopStatAtribute = {"FIGHT_PROP_MAX_HP": "BASE_HP", "FIGHT_PROP_CUR_ATTACK":"FIGHT_PROP_BASE_ATTACK","FIGHT_PROP_CUR_DEFENSE":"FIGHT_PROP_BASE_DEFENSE"}

async def get_color(element):
    if element == "Fire":
        return (255,45,37,255) 
    elif element== "Grass":
        return (0,255,93,255) 
    elif element == "Electric":
        return (156,38,255,255) 
    elif element == "Water":
        return (0,184,255,255) 
    elif element == "Wind":
        return (0,255,196,255) 
    elif element== "Rock":
        return (255,139,23,255) 
    else:
        return (0,255,251,255) 

async def get_background(element):
    if element == "Fire":
        background_one = await _gitFile.background_one_pyro
    elif element== "Grass":
        background_one  = await _gitFile.background_one_dendro
    elif element == "Electric":
        background_one  = await _gitFile.background_one_electro
    elif element == "Water":
        background_one = await _gitFile.background_one_gydro
    elif element == "Wind":
        background_one  =  await _gitFile.background_one_anemo
    elif element== "Rock":
        background_one = await _gitFile.background_one_geo
    else:
        background_one = await _gitFile.background_one_cryo

    return background_one.copy()


async def get_stars_icon(rating):
    if rating == 5:
        return await _gitFile.stars5
    elif rating == 4:
        return await _gitFile.stars4
    elif rating == 3:
        return await _gitFile.stars3
    elif rating == 2:
        return await _gitFile.stars2
    else:
        return await _gitFile.stars1


async def getIconAdd(x, size = None, stats = False):
    if stats:
        if not x in IconAddTrue:
            return None
    if x == "FIGHT_PROP_MAX_HP" or x == "FIGHT_PROP_HP":
        icons = await _gitFile.FIGHT_PROP_MAX_HP
    elif x == "FIGHT_PROP_CUR_ATTACK" or x =="FIGHT_PROP_ATTACK":
        icons = await _gitFile.FIGHT_PROP_CUR_ATTACK
    elif x == "FIGHT_PROP_CUR_DEFENSE" or x == "FIGHT_PROP_DEFENSE":
        icons = await _gitFile.FIGHT_PROP_CUR_DEFENSE
    elif x == "FIGHT_PROP_ELEMENT_MASTERY":
        icons = await _gitFile.FIGHT_PROP_ELEMENT_MASTERY
    elif x == "FIGHT_PROP_CRITICAL":
        icons = await _gitFile.FIGHT_PROP_CRITICAL
    elif x == "FIGHT_PROP_CRITICAL_HURT":
        icons = await _gitFile.FIGHT_PROP_CRITICAL_HURT
    elif x == "FIGHT_PROP_CHARGE_EFFICIENCY":
        icons = await _gitFile.FIGHT_PROP_CHARGE_EFFICIENCY
    elif x == "FIGHT_PROP_ELEC_ADD_HURT":
        icons =  await _gitFile.FIGHT_PROP_ELEC_ADD_HURT
    elif x == "FIGHT_PROP_DEFENSE_PERCENT":
        icons = await _gitFile.FIGHT_PROP_DEFENSE_PERCENT
    elif x == "FIGHT_PROP_ATTACK_PERCENT":
        icons = await _gitFile.FIGHT_PROP_ATTACK_PERCENT
    elif x == "FIGHT_PROP_HP_PERCENT":
        icons = await _gitFile.FIGHT_PROP_HP_PERCENT
    elif x == "FIGHT_PROP_WATER_ADD_HURT":
        icons = await _gitFile.FIGHT_PROP_WATER_ADD_HURT
    elif x == "FIGHT_PROP_WIND_ADD_HURT":
        icons = await _gitFile.FIGHT_PROP_WIND_ADD_HURT
    elif x == "FIGHT_PROP_ICE_ADD_HURT":
        icons = await _gitFile.FIGHT_PROP_ICE_ADD_HURT
    elif x == "FIGHT_PROP_ROCK_ADD_HURT":
        icons = await _gitFile.FIGHT_PROP_ROCK_ADD_HURT
    elif x == "FIGHT_PROP_FIRE_ADD_HURT":
        icons = await _gitFile.FIGHT_PROP_FIRE_ADD_HURT
    elif x == "FIGHT_PROP_GRASS_ADD_HURT":
        icons = await _gitFile.FIGHT_PROP_GRASS_ADD_HURT
    elif x == "FIGHT_PROP_HEAL_ADD":
        icons = await _gitFile.FIGHT_PROP_HEAL_ADD
    elif x == "FIGHT_PROP_HEAL":
        icons = await _gitFile.FIGHT_PROP_HEAL
    elif x == "FIGHT_PROP_PHYSICAL_ADD_HURT":
        icons = await _gitFile.FIGHT_PROP_PHYSICAL_ADD_HURT
    else:
        return False
    if size:
        icons.thumbnail(size)
        return icons.convert("RGBA").copy()
    else:
        return icons.convert("RGBA").copy()


async def get_constellations_background(element):
    if element == "Fire":
        open_constellations, clos_constellations = await _gitFile.OPEN_CONSTANT_PYRO, await _gitFile.CLOSED_CONSTANT_PYRO
    elif element== "Grass":
        open_constellations, clos_constellations  = await _gitFile.OPEN_CONSTANT_DENDRO, await _gitFile.CLOSED_CONSTANT_DENDRO
    elif element == "Electric":
        open_constellations, clos_constellations  = await _gitFile.OPEN_CONSTANT_ELECTRO, await _gitFile.CLOSED_CONSTANT_ELECTRO
    elif element == "Water":
        open_constellations, clos_constellations = await _gitFile.OPEN_CONSTANT_GYDRO, await _gitFile.CLOSED_CONSTANT_GYDRO
    elif element == "Wind":
        open_constellations, clos_constellations  =  await _gitFile.OPEN_CONSTANT_ANEMO, await _gitFile.CLOSED_CONSTANT_ANEMO
    elif element== "Rock":
        open_constellations, clos_constellations = await _gitFile.OPEN_CONSTANT_GEO, await _gitFile.CLOSED_CONSTANT_GEO
    else:
        open_constellations, clos_constellations = await _gitFile.OPEN_CONSTANT_CRYO, await _gitFile.CLOSED_CONSTANT_CRYO
    
    return open_constellations, clos_constellations, await _gitFile.CLOSED_CONSTANT

class TeampleOne:
    def __init__(self, **items):
        self.lang = items.get('lang', "ru")
        self.characterImgs = items.get('characterImgs')
        self.characterName = items.get('characterName')
        self.adapt = items.get('adapt')
        self.hide = items.get('hide')
        self.agent = items.get('agent')
        self.uid = items.get('uid')
        self.translation = items.get('translation')
    
    async def creat_background(self,charter):
        cart_right_mask,cart_left_mask,cart_center_background,cart_center_mask,font,namecard,splashArt  = await asyncio.gather(_gitFile.cart_right_mask, _gitFile.cart_left_mask,
                                                                                                                       _gitFile.cart_center,_gitFile.cart_center_mask,pill.get_font(21),
                                                                                                                       pill.get_dowload_img(namecard_map.Get(charter.id).image, size = (1342,639)),
                                                                                                                       pill.get_dowload_img(charter.image.banner.url, size = (1503,751)))
        
        
        if charter.name.lower() in self.characterImgs:
            user_image = await pill.get_user_image(self.characterImgs[charter.name.lower()])
            background = await get_background(charter.element)
            cart_center_background = cart_center_background.copy()
            user_image = await pill.get_resize_image(user_image,564,347)
            _CENTR = Image.new("RGBA", (347,564), (255,255,255,0))
            if user_image["type"] == 2:
                cart_center_background.alpha_composite(user_image["img"],(0,0))
            else:
                cart_center_background.alpha_composite(user_image["img"],(int(174 - user_image["img"].size[0]/2),0))
            _CENTR_BACKGROUND = Image.composite(_CENTR, cart_center_background, cart_center_mask.convert("L"))
        else:
            background = await get_background(charter.element)
            cart_center_background = cart_center_background.copy()
            _CENTR = Image.new("RGBA", (347,564), (255,255,255,0))
            cart_center_background.alpha_composite(splashArt,(-577,-75))
            _CENTR_BACKGROUND = Image.composite(_CENTR, cart_center_background, cart_center_mask.convert("L"))

        background = background.convert("RGBA")
        _RIGHT = Image.new("RGBA", (477,631), (255,255,255,0))
        _RIGHT_BACKGROUND = _RIGHT.copy()
        _RIGHT.alpha_composite(namecard, (-668,0))
        _RIGHT_BACKGROUND = Image.composite(_RIGHT_BACKGROUND, _RIGHT, cart_right_mask.convert("L"))

        _LEFT = Image.new("RGBA", (452,599), (255,255,255,0))
        _LEFT_BACKGROUND = _LEFT.copy()
        _LEFT.alpha_composite(namecard, (-47,-38))
        _LEFT_BACKGROUND = Image.composite(_LEFT_BACKGROUND, _LEFT, cart_left_mask.convert("L"))
        

        


        background.alpha_composite(_RIGHT_BACKGROUND, (497,16))
        background.alpha_composite(_LEFT_BACKGROUND, (363,58))
        background.alpha_composite(_CENTR_BACKGROUND, (483,92))

        size = int(font.getlength(self.name_user))
        name = Image.new("RGBA", (size+2,22), (255,255,255,0))
        draw = ImageDraw.Draw(name)
        draw.text((0,0), self.name_user, font= font, fill=(255,255,255,70))

        text = ImageDraw.Draw(background)
        text.text((16,18), charter.name, font= font, fill=(255,255,255,255))
        text.text((16,52), f"{self.translation}: {charter.level}/90", font= font, fill=(255,255,255,255))
        text.text((47,86), str(charter.friendship_level), font= font, fill=(255,255,255,255))

        size = int(font.getlength(charter.name))
        background.alpha_composite(await _gitFile.nickname_icon, (size+16+5,21))
        background.alpha_composite(name, (size+16+25,17))

        return background

    async def creat_weapon(self,weapon, element):
        background = Image.new("RGBA", (347,130), (255,255,255,0))
        color = await get_color(element)
        weapon_icon = await pill.get_dowload_img(weapon.detail.icon.url, size = (109,114))
        background.alpha_composite(weapon_icon, (3,2))
        stars_icon = await get_stars_icon(weapon.detail.rarity)
        background.alpha_composite(stars_icon, (0,101))
        refinement = f"R{weapon.refinement}"
        level = f"{self.translation}: {weapon.level}/90"
        substate_value = "0"
        weapon_value = f"{weapon.detail.mainstats.value}{'%' if weapon.detail.mainstats.type == DigitType.PERCENT else ''}"
        if weapon.detail.substats != []:
            for substate in weapon.detail.substats:
                substate_icon = await getIconAdd(substate.prop_id, size= (24,24))
                substate_value = f"{substate.value}{'%' if substate.type == DigitType.PERCENT else ''}"
            
            background.alpha_composite(substate_icon, (227,27))

        draw = ImageDraw.Draw(background)
        font = await pill.get_font(20)

        draw.text((257,25), substate_value, font= font, fill=(255,255,255,255))
        draw.text((144,25), weapon_value, font= font, fill=color)


        size = int(font.getlength(level))
        draw.text((113,64), level, font= font, fill=(255,255,255,255))
        draw.text((113+size+10,64), refinement, font= font, fill=color)

        weapon_name = await pill.create_image_with_text(weapon.detail.name,20)

        return {"background": background,"name": weapon_name}


    async def creat_artifact(self,artifact_list):
        TOTAL_CV = 0
        artifact_image= []
        artifact_set = {}

        position_substate = [
            (25,193),(138,193),(25,230),(138,230)
        ]

        position_substate_value = [
            (57,192),(170,192),(57,229),(170,229)
        ]

        for artifact in filter(lambda x: x.type == EquipmentsType.ARTIFACT, artifact_list):
            CRIT_DMG,CRIT_RATE,CRIT_DMGT,CRIT_RATET = 0,0,0,0

            if not artifact.detail.artifact_name_set in artifact_set:
                artifact_set[artifact.detail.artifact_name_set] = 1
            else:
                artifact_set[artifact.detail.artifact_name_set] += 1
            
            background = Image.new("RGBA", (250,288), (255,255,255,0))
            
            artiartifact_icon = await pill.get_dowload_img(artifact.detail.icon.url, thumbnail_size = (113,113))
            stars_icon = await get_stars_icon(artifact.detail.rarity)
            
            artiartifact_level = f"+{artifact.level}"

            mainstats_icon = await getIconAdd(artifact.detail.mainstats.prop_id, size= (24,24))
            mainstats_value = f"{artifact.detail.mainstats.value}{'%' if artifact.detail.mainstats.type == DigitType.PERCENT else ''}"

            background.alpha_composite(artiartifact_icon,(68,0))
            background.alpha_composite(stars_icon,(74,259))
            background.alpha_composite(mainstats_icon,(25,123))

            draw = ImageDraw.Draw(background)
            font = await pill.get_font(20)

            draw.text((55,123), mainstats_value, font= font, fill=(255,255,255,255))
            draw.text((24,151), artiartifact_level, font= font, fill=(255,255,255,255))

            if artifact.detail.mainstats.prop_id == "FIGHT_PROP_CRITICAL_HURT":
                CRIT_DMGT += artifact.detail.mainstats.value
            if artifact.detail.mainstats.prop_id == "FIGHT_PROP_CRITICAL":
                CRIT_RATET += artifact.detail.mainstats.value

            if artifact.detail.substats != []:
                i = 0
                for substate in artifact.detail.substats:
                    substate_icon = await getIconAdd(substate.prop_id, size= (24,24))
                    substate_value = f"{substate.value}{'%' if substate.type == DigitType.PERCENT else ''}"
                    background.alpha_composite(substate_icon,position_substate[i])
                    draw.text(position_substate_value[i], substate_value, font= font, fill=(255,255,255,255))
                    i += 1
                    if substate.prop_id == "FIGHT_PROP_CRITICAL_HURT":
                        CRIT_DMG += substate.value
                        CRIT_DMGT += substate.value
                    if substate.prop_id == "FIGHT_PROP_CRITICAL":
                        CRIT_RATE += substate.value
                        CRIT_RATET += substate.value
            tcvR = float('{:.2f}'.format(CRIT_DMG + (CRIT_RATE*2)))
            TCV = f"{tcvR}CV"
            tcvR = float('{:.2f}'.format(CRIT_DMGT + (CRIT_RATET*2)))
            TOTAL_CV += tcvR

            draw.text((134,136), TCV, font= font, fill=(255,255,255,255))

            artifact_image.append(background)

        return {"atrtifact" : artifact_image, "sets": artifact_set, "tcv": float('{:.2f}'.format(TOTAL_CV))}
                    


    async def append_atrtifact(self,background,items, positions):
        for i, key in enumerate(items):
            background.alpha_composite(key,positions[i])
        
        return background
    

    async def append_artifact_sets_tcv(self,background,artifact_set, total_cv, element):
        if artifact_set != {}:
            max_val = max(artifact_set.values())
            max_keys = [k for k, v in artifact_set.items() if v == max_val]
            if max_val == 4:
                result = max_keys[0]
            else:
                unique_vals = list(set(artifact_set.values()))
                if unique_vals.count(2) == 2:
                    result = [k for k, v in artifact_set.items() if v == 2]
                elif 2 in unique_vals and 3 in unique_vals:
                    result = [k for k, v in artifact_set.items() if v in [2, 3]]
                else:
                    result = max_keys[:2]
            if len(result) == 2 and type(result) == list:
                pass
            else:
                if type(result) == str:
                    result = [result]
            position_sets_name = [204,319]
            position_sets_count = [204,297]
            font,color = await asyncio.gather(pill.get_font(20),get_color(element))

            for i, key in enumerate(result):
                sets_image = await pill.create_image_with_text(key,20,272)
                if i == 1:
                    background.alpha_composite(sets_image,(964,position_sets_name[i]-sets_image.size[1]))
                else:
                    background.alpha_composite(sets_image,(964,position_sets_name[i]))
                dc = ImageDraw.Draw(background)
                dc.text((1263,position_sets_count[i]), str(artifact_set[key]), font= font, fill=(255,255,255,255))
            dc.text((53,128), f"{total_cv}TCV", font= font, fill=color)

        return background
    

    async def creat_stats(self,stats,element):
        dopval = {}
        elementUp = True
        background_main  = Image.new("RGBA", (170,172), (255,255,255,0))
        draw_main = ImageDraw.Draw(background_main)
        
        background_dop_stats = Image.new("RGBA", (168,240), (255,255,255,0))
        draw_dop = ImageDraw.Draw(background_dop_stats)
        color,font_main,font_main_mini = await asyncio.gather(get_color(element), pill.get_font(21),pill.get_font(14))
        position_main = [
            (10,34),(64,88),(118,144),
        ]
        position_dop = [
            (14,15),(61,62),(108,109),(155,156),(202,203)
        ]
        i = 0
        ix = 0
        for key in stats:
            if key[1].value <= 0:
                continue
            if key[1].id in [1,4,7]:
                dopval[key[0]] = key[1].value
                continue            
            else:
                if key[1].id in [2000,2001,2002]:
                    stats_value = key[1].to_rounded() if isinstance(key[1], Stats) else key[1].to_percentage_symbol() #key[1].value

                    dopStatVal = int(dopval[dopStatAtribute[key[0]]])
                    dopStatValArtifact = f'+{int(stats_value - dopval[dopStatAtribute[key[0]]])}'
                    
                    x = int(font_main.getlength(str(stats_value)))
                    draw_main.text((169-x,position_main[i][0]), str(stats_value), font= font_main, fill=(255,255,255,255))

                    xx = int(font_main_mini.getlength(dopStatValArtifact))
                    draw_main.text((169-xx,position_main[i][1]), dopStatValArtifact, font= font_main_mini, fill=color)

                    x = int(font_main_mini.getlength(str(dopStatVal)))
                    draw_main.text((169-xx-x-2,position_main[i][1]), str(dopStatVal), font= font_main_mini, fill=(255,255,255,255))
                    i += 1
                else:
                    if key[1].id in [40,41,42,43,44,45,46]:
                        if elementUp:
                            key = max((x for x in stats if 40 <= x[1].id <= 46), key=lambda x: x[1].value)
                            elementUp = False
                        else:
                            continue 
                    icon_stats = await getIconAdd(key[0], size= (26,26),stats = True)
                    if not icon_stats:
                        continue
                    background_dop_stats.alpha_composite(icon_stats,(16,position_dop[ix][0]))

                    stats_dop_value = f"{key[1].to_rounded() if isinstance(key[1], Stats) else key[1].to_percentage_symbol()}"
                    x = int(font_main.getlength(stats_dop_value))
                    draw_dop.text((167-x-2,position_dop[ix][1]), str(stats_dop_value), font= font_main, fill=(255,255,255,255))
                    ix += 1
                    pass

        return {"main":background_main , "dop":background_dop_stats}

    async def creat_constellations(self,constellations, element):
        constellations_background = Image.new("RGBA", (157,615), (255,255,255,0))
        constellation_open, constellation_close, icon_closed  = await get_constellations_background(element)
        icon_closed = icon_closed.resize((63,63))
        constellation_positions = [(20,0),(8,102),(0,204 ),(0,306),(20,408),(58,513)]
        constellation_positions_icon = [(39,21),(27,125),(19,226),(19,329),(39,427),(76,536)]
        for i, key in enumerate(constellations):
            constellations_icon = await pill.get_dowload_img(key.icon.url, size=(60, 60))
            if not key.unlocked:
                closedConstBg = constellation_close.copy().resize((99, 102))
                constellations_background.alpha_composite(closedConstBg, constellation_positions[i])
                constellations_background.alpha_composite(constellations_icon, constellation_positions_icon[i])
                constellations_background.alpha_composite(icon_closed, constellation_positions_icon[i])
            else:
                openConstBg = constellation_open.copy().resize((99, 102))
                constellations_background.alpha_composite(openConstBg, constellation_positions[i])
                constellations_background.alpha_composite(constellations_icon, constellation_positions_icon[i]) 

        return constellations_background
    
    async def creat_skills(self,skills,element):
        background,color,font, = await asyncio.gather(_gitFile.SKILLS,get_color(element),pill.get_font(21))
        background_skills = background.copy()
        i = 0
        position_skills_icon = [17,138,259]
        position_skills_level = [52,173,294]

        d = ImageDraw.Draw(background_skills)

        for i, key in enumerate(skills):
            talants_icon = await pill.get_dowload_img(key.icon.url, size=(74, 74))
            background_skills.alpha_composite(talants_icon, (position_skills_icon[i], -5))

            fill_color = color if key.level >= 10 else (255, 255, 255, 255)
            d.text((int(position_skills_level[i] - font.getlength(str(key.level)) / 2), 68),
                str(key.level), font=font, fill=fill_color)
        return background_skills
    

    async def append_background(self,**items,):
        background = items.get("background")
        position_artifact = [
            (17, 694), (274, 694), (531, 694), (788, 694), (1045, 694)
        ]
        background.alpha_composite(items.get("skills"), (945, 566))
        background.alpha_composite(items.get("const"), (231, 63))
        background.alpha_composite(items.get("weapon")["background"], (943, 401))
        background.alpha_composite(items.get("weapon")["name"], (949, 400 - items.get("weapon")["name"].size[1]))
        background.alpha_composite(items.get("stats")["main"], (16, 210))
        background.alpha_composite(items.get("stats")["dop"], (16, 403))
        background = await self.append_atrtifact(background, items.get("artifact")["atrtifact"], position_artifact)
        background = await self.append_artifact_sets_tcv(background, items.get("artifact")["sets"], items.get("artifact")["tcv"], items.get("element"))

        return background


    async def card(self, charter):
        # Execute all coroutines concurrently using asyncio.gather()
        background, weapon, artifact, stats, const, skills = await asyncio.gather(
            self.creat_background(charter),
            self.creat_weapon(charter.equipments[-1], charter.element),
            self.creat_artifact(charter.equipments),
            self.creat_stats(charter.stats, charter.element),
            self.creat_constellations(charter.constellations, charter.element),
            self.creat_skills(charter.skills, charter.element),
        )

        # Apply the changes to the background image
        background = await self.append_background(background = background, skills = skills, const = const, stats = stats,artifact = artifact, weapon = weapon, element =charter.element)
        return {"id":charter.id,"name": charter.name,"element":charter.element.value ,"card": background}


    async def start(self):

        info = await EnkanetworkApi.get_full_info(self.agent,self.lang,self.uid)
        self.name_user = info.player.nickname

        user_data = {
            "uid": self.uid,
            "name": self.name_user,
            "lang": self.lang,
            "card": [],
        }

        if self.characterName != "":
            tasks = [asyncio.create_task(self.card(charters)) for charters in info.characters if charters.name in self.characterName]
        else:
            tasks = [asyncio.create_task(self.card(charters)) for charters in info.characters]


        user_data["card"] = await asyncio.gather(*tasks)

        return ENCardResult.EnkaNetworkCard(**user_data)
