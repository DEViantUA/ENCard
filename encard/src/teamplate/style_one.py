import asyncio
from PIL import ImageDraw,Image
from enkanetwork.enum import EquipmentsType, DigitType
from enkanetwork.model.stats import Stats

from ..tools import pill, namecard_map, git



_gitFile = git.openFile()
IconAddTrue = ["FIGHT_PROP_PHYSICAL_ADD_HURT","FIGHT_PROP_HEAL_ADD","FIGHT_PROP_GRASS_ADD_HURT","FIGHT_PROP_FIRE_ADD_HURT","FIGHT_PROP_MAX_HP","FIGHT_PROP_CUR_ATTACK","FIGHT_PROP_CUR_DEFENSE","FIGHT_PROP_ELEMENT_MASTERY","FIGHT_PROP_CRITICAL","FIGHT_PROP_CRITICAL_HURT","FIGHT_PROP_CHARGE_EFFICIENCY","FIGHT_PROP_ELEC_ADD_HURT","FIGHT_PROP_ROCK_ADD_HURT","FIGHT_PROP_ICE_ADD_HURT","FIGHT_PROP_WIND_ADD_HURT","FIGHT_PROP_WATER_ADD_HURT"]
dopStatAtribute = {"FIGHT_PROP_MAX_HP": "BASE_HP", "FIGHT_PROP_CUR_ATTACK":"FIGHT_PROP_BASE_ATTACK","FIGHT_PROP_CUR_DEFENSE":"FIGHT_PROP_BASE_DEFENSE"}






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


async def get_constellations_background(color):
    maska_open = await _gitFile.OPEN_ADAPT_MASK_CONSTANT
    maska_closed = await _gitFile.CLOSED_ADAPT_MASK_CONSTANT
    maska_bg = await _gitFile.maska_constant
    bg = Image.new("RGBA", (944,968), (0,0,0,0))
    bg_color = Image.new("RGBA", (944,968), (48,48,48,255))
    bg.paste(bg_color,(0,0),maska_bg.convert("L"))
    
    colors = Image.new("RGBA", (944,968), color)
    opens = await _gitFile.const_adapt
    opens = await pill.recolor_image(opens, color)

    closed = bg.copy()
    closed.paste(colors,(0,0),maska_closed.convert("L"))
    
    return opens, closed, await _gitFile.CLOSED_CONSTANT
    
    
    



class Creat:
    def __init__(self, **items) -> None:
        self.info = items.get("info")
        self.name = items.get("name")
        self.translator = items.get("translator")
        self.adapt = items.get("adapt")
        self.hide = items.get("hide")
        self.color = items.get("color")
        self.user_art = items.get("art")
        self.uid = items.get("uid")
        self.element_color = pill.get_element_color(self.info.element)
        self.light = True

    async def config_self(self):  
        
                  
        if not self.user_art is None:
            self.art = await pill.get_dowload_img(self.user_art)
        else:
            self.art = await pill.get_dowload_img(self.info.image.banner.url, size = (1503,751))
                
        if self.adapt:
            if not self.user_art is None and self.color is None:
                self.element_color = await pill.get_colors(self.art, 15, common=True, radius=5, quality=800)
                
        
        if self.color:
            self.element_color = self.color
            self.light = False
                 
    async def get_background(self):
        name_card = await namecard_map.Get(self.info.id).image
        name_card = await pill.get_dowload_img(name_card, size = (1342,639))
        
        font = await pill.get_font(21)
        
        cart_right_mask,cart_left_mask,cart_center_background,cart_center_mask = await asyncio.gather(_gitFile.cart_right_mask, _gitFile.cart_left_mask,
                                                                                                        _gitFile.cart_center,_gitFile.cart_center_mask)
        shadow = await _gitFile.cart_shadow
        self.background = await _gitFile.background_adapt
        self.background = self.background.convert("RGBA").copy()
        self.background.alpha_composite(shadow)
        
        frame = await _gitFile.background_adatpt_frame
        frame = await pill.recolor_image(frame.copy(), self.element_color, light = self.light)
        self.background.alpha_composite(frame)

        _CENTR = Image.new("RGBA", (347,564), (255,255,255,0))
        cart_center_background = cart_center_background.copy()
        self.art = await pill.get_centr_size((347,564), self.art)
        cart_center_background.alpha_composite(self.art,(0,0))
        _CENTR_BACKGROUND = Image.composite(_CENTR, cart_center_background, cart_center_mask.convert("L"))
        
        _RIGHT = Image.new("RGBA", (477,631), (255,255,255,0))
        _RIGHT_BACKGROUND = _RIGHT.copy()
        _RIGHT.alpha_composite(name_card, (-668,0))
        _RIGHT_BACKGROUND = Image.composite(_RIGHT_BACKGROUND, _RIGHT, cart_right_mask.convert("L"))

        _LEFT = Image.new("RGBA", (452,599), (255,255,255,0))
        _LEFT_BACKGROUND = _LEFT.copy()
        _LEFT.alpha_composite(name_card, (-47,-38))
        _LEFT_BACKGROUND = Image.composite(_LEFT_BACKGROUND, _LEFT, cart_left_mask.convert("L"))        
        
        self.background.alpha_composite(_RIGHT_BACKGROUND, (497,16))
        self.background.alpha_composite(_LEFT_BACKGROUND, (363,58))
        self.background.alpha_composite(_CENTR_BACKGROUND, (483,92))
        
        
        size = int(font.getlength(self.name))
        name = Image.new("RGBA", (size+2,22), (255,255,255,0))
        draw = ImageDraw.Draw(name)
        draw.text((0,0), self.name, font= font, fill=(255,255,255,70))

        text = ImageDraw.Draw(self.background)
        text.text((16,18), self.info.name, font= font, fill=(255,255,255,255))
        text.text((16,52), f"{self.translator.lvl}: {self.info.level}/90", font= font, fill=(255,255,255,255))
        text.text((47,86), str(self.info.friendship_level), font= font, fill=(255,255,255,255))
        text.text((16,175), f'UID: {self.uid}', font= await pill.get_font(15), fill=(255,255,255,100))

        size = int(font.getlength(self.info.name))
        self.background.alpha_composite(await _gitFile.nickname_icon, (size+16+5,21))
        self.background.alpha_composite(name, (size+16+25,17))
        
    async def creat_weapon(self):
        weapon = self.info.equipments[-1]
        self.background_weapon = Image.new("RGBA", (347,130), (255,255,255,0))
        weapon_icon = await pill.get_dowload_img(weapon.detail.icon.url, size = (109,114))
        self.background_weapon.alpha_composite(weapon_icon, (3,2))
        stars_icon = await get_stars_icon(weapon.detail.rarity)
        self.background_weapon.alpha_composite(stars_icon, (0,101))
        refinement = f"R{weapon.refinement}"
        level = f"{self.translator.lvl}: {weapon.level}/90"
        substate_value = "0"
        weapon_value = f"{weapon.detail.mainstats.value}{'%' if weapon.detail.mainstats.type == DigitType.PERCENT else ''}"
        if weapon.detail.substats != []:
            for substate in weapon.detail.substats:
                substate_icon = await getIconAdd(substate.prop_id, size= (24,24))
                substate_value = f"{substate.value}{'%' if substate.type == DigitType.PERCENT else ''}"
            
            self.background_weapon.alpha_composite(substate_icon, (227,27))

        draw = ImageDraw.Draw(self.background_weapon)
        font = await pill.get_font(20)

        draw.text((257,25), substate_value, font= font, fill=(255,255,255,255))
        draw.text((144,25), weapon_value, font= font, fill=self.element_color)


        size = int(font.getlength(level))
        draw.text((113,64), level, font= font, fill=(255,255,255,255))
        draw.text((113+size+10,64), refinement, font= font, fill=self.element_color)

        self.weapon_name = await pill.create_image_with_text(weapon.detail.name,20) 
  
    async def creat_stats(self):
        stats = self.info.stats
        dopval = {}
        elementUp = True
        self.background_main  = Image.new("RGBA", (170,172), (255,255,255,0))
        draw_main = ImageDraw.Draw(self.background_main)
        
        self.background_dop_stats = Image.new("RGBA", (168,240), (255,255,255,0))
        draw_dop = ImageDraw.Draw(self.background_dop_stats)
        font_main,font_main_mini = await asyncio.gather(pill.get_font(21),pill.get_font(14))
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
                    stats_value = key[1].to_rounded() if isinstance(key[1], Stats) else key[1].to_percentage_symbol()

                    dopStatVal = int(dopval[dopStatAtribute[key[0]]])
                    dopStatValArtifact = f'+{int(stats_value - dopval[dopStatAtribute[key[0]]])}'
                    
                    x = int(font_main.getlength(str(stats_value)))
                    draw_main.text((169-x,position_main[i][0]), str(stats_value), font= font_main, fill=(255,255,255,255))

                    xx = int(font_main_mini.getlength(dopStatValArtifact))
                    draw_main.text((169-xx,position_main[i][1]), dopStatValArtifact, font= font_main_mini, fill=self.element_color)

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
                    self.background_dop_stats.alpha_composite(icon_stats,(16,position_dop[ix][0]))

                    stats_dop_value = f"{key[1].to_rounded() if isinstance(key[1], Stats) else key[1].to_percentage_symbol()}"
                    x = int(font_main.getlength(stats_dop_value))
                    draw_dop.text((167-x-2,position_dop[ix][1]), str(stats_dop_value), font= font_main, fill=(255,255,255,255))
                    ix += 1    
    
    async def creat_constellations(self):
        constellations = self.info.constellations
        self.constellations_background = Image.new("RGBA", (157,615), (255,255,255,0))
        constellation_open, constellation_close, icon_closed  = await get_constellations_background(self.element_color)
        icon_closed = icon_closed.resize((65,64))
        constellation_positions = [(20,0),(8,102),(0,204 ),(0,306),(20,408),(58,513)]
        constellation_positions_icon = [(39,21),(27,125),(19,226),(19,329),(39,427),(76,536)]
        constellation_positions_icon_closed = [(37,20),(25,122),(17,224),(17,326),(37,428),(74,533)]
        for i, key in enumerate(constellations):
            constellations_icon = await pill.get_dowload_img(key.icon.url, size=(60, 60))
            if not key.unlocked:
                closedConstBg = constellation_close.copy().resize((99, 102))
                self.constellations_background.alpha_composite(closedConstBg, constellation_positions[i])
                self.constellations_background.alpha_composite(constellations_icon, constellation_positions_icon[i])
                self.constellations_background.alpha_composite(icon_closed, constellation_positions_icon_closed[i])
            else:
                openConstBg = constellation_open.copy().resize((99, 102))
                self.constellations_background.alpha_composite(openConstBg, constellation_positions[i])
                self.constellations_background.alpha_composite(constellations_icon, constellation_positions_icon[i]) 
        
    async def creat_skills(self):
        
        background, font, = await asyncio.gather(_gitFile.SKILLS,pill.get_font(21))
        self.background_skills = background.copy()
        i = 0
        position_skills_icon = [17,138,259]
        position_skills_level = [52,173,294]

        d = ImageDraw.Draw(self.background_skills)

        for i, key in enumerate(self.info.skills):
            talants_icon = await pill.get_dowload_img(key.icon.url, size=(74, 74))
            self.background_skills.alpha_composite(talants_icon, (position_skills_icon[i], -5))

            fill_color = self.element_color if key.level >= 10 else (255, 255, 255, 255)
            d.text((int(position_skills_level[i] - font.getlength(str(key.level)) / 2), 68),
                str(key.level), font=font, fill=fill_color)
                
    async def creat_artifact(self):
        self.TOTAL_CV = 0
        self.artifact_image= []
        self.artifact_set = {}

        position_substate = [
            (25,193),(138,193),(25,230),(138,230)
        ]

        position_substate_value = [
            (57,192),(170,192),(57,229),(170,229)
        ]

        for artifact in filter(lambda x: x.type == EquipmentsType.ARTIFACT, self.info.equipments):
            CRIT_DMG,CRIT_RATE,CRIT_DMGT,CRIT_RATET = 0,0,0,0

            if not artifact.detail.artifact_name_set in self.artifact_set:
                self.artifact_set[artifact.detail.artifact_name_set] = 1
            else:
                self.artifact_set[artifact.detail.artifact_name_set] += 1
            
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
            self.TOTAL_CV += tcvR

            draw.text((134,136), TCV, font= font, fill=(255,255,255,255))

            self.artifact_image.append(background)

        self.TOTAL_CV = float('{:.2f}'.format(self.TOTAL_CV))
            
            
    async def append_artifact_sets_tcv(self):
        if self.artifact_set != {}:
            max_val = max(self.artifact_set.values())
            max_keys = [k for k, v in self.artifact_set.items() if v == max_val]
            if max_val == 4:
                result = max_keys[0]
            else:
                unique_vals = list(set(self.artifact_set.values()))
                if unique_vals.count(2) == 2:
                    result = [k for k, v in self.artifact_set.items() if v == 2]
                elif 2 in unique_vals and 3 in unique_vals:
                    result = [k for k, v in self.artifact_set.items() if v in [2, 3]]
                else:
                    result = max_keys[:2]
            if len(result) == 2 and type(result) == list:
                pass
            else:
                if type(result) == str:
                    result = [result]
            position_sets_name = [204,319]
            position_sets_count = [204,297]
            font = await pill.get_font(20)

            for i, key in enumerate(result):
                sets_image = await pill.create_image_with_text(key,20,272)
                if i == 1:
                    self.background.alpha_composite(sets_image,(964,position_sets_name[i]-sets_image.size[1]))
                else:
                    self.background.alpha_composite(sets_image,(964,position_sets_name[i]))
                dc = ImageDraw.Draw(self.background)
                dc.text((1263,position_sets_count[i]), str(self.artifact_set[key]), font= font, fill=(255,255,255,255))
            dc.text((53,128), f"{self.TOTAL_CV}TCV", font= font, fill= self.element_color)
    
    async def append_atrtifact(self):
        position_artifact = [
            (17, 694), (274, 694), (531, 694), (788, 694), (1045, 694)
        ]
        for i, key in enumerate(self.artifact_image):
            self.background.alpha_composite(key,position_artifact[i])
            
    async def build(self):
        self.background.alpha_composite(self.background_weapon,(943, 401))
        self.background.alpha_composite(self.weapon_name,(949, 400 - self.weapon_name.size[1]))
        self.background.alpha_composite(self.background_main, (16, 210))
        self.background.alpha_composite(self.background_dop_stats, (16, 403))
        self.background.alpha_composite(self.constellations_background, (231, 63))
        self.background.alpha_composite(self.background_skills,(945, 566))
        
    async def start(self):
        await self.config_self()
        
        await asyncio.gather(self.get_background(), self.creat_weapon(),self.creat_stats(), self.creat_constellations(), self.creat_skills(), self.creat_artifact())

        await asyncio.gather(self.append_artifact_sets_tcv(), self.append_atrtifact())
        
        await self.build()
        
        return {"id": self.info.id, "element": self.info.element, "name": self.info.name, "icon": self.info.image.icon.url, "card": self.background, "color": self.element_color}
        