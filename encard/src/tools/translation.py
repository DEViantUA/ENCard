# Copyright 2022 DEViantUa <t.me/deviant_ua>
# All rights reserved.
supportLang= {"en":"en", 
        "ru":"ru",
        "vi": "vi", 
        "th":"th",
        "pt":"pt",
        "kr":"ko",
        "jp":"ja",
        "zh":"zh-cn",
        "id":"id",
        "fr":"fr",
        "es":"es",
        "de":"de",
        "chs":"zh-cn",
        "cht":"zh-tw"
    }

translationLang = {"en":{"lvl": "LVL", "AR":"AR", "WL":"WL", "AC": "Achievements", "AB": "Abyss", "MP": "Main page", "NC": "Name cards", "CS": "Character stand"}, 
        "ru": {"lvl": "Уровень", "AR":"РП", "WL":"УМ", "AC": "Достижения", "AB": "Бездна", "MP": "Главная страница", "NC": "Именные карточки", "CS": "Витрина персонажей"},
        "vi": {'lvl': 'Cấp độ ', 'AR': 'AR', 'WL': 'WL', 'AC': 'Thành tích ', 'AB': 'Vực thẳm', "MP": "Trang chính", "NC": "danh thiếp", "CS": "Character stand"},
        "th": {'lvl': 'ระดับ ', 'AR': 'AR', 'WL': 'WL', 'AC': ' ความสำเร็จ ', 'AB': 'Abyss', "MP": "หน้าหลัก", "NC": "นามบัตร", "CS": "Character stand"},
        "pt": {'lvl': 'Nível ', 'AR': 'AR', 'WL': 'WL', 'AC': ' Conquistas ', 'AB': 'Abismo', "MP": "Página principal", "NC": "cartões de nome", "CS": "Character stand"},
        "kr": {'lvl': '레벨 ', 'AR': 'AR', 'WL': 'WL', 'AC': '업적', 'AB': '어비스', "MP": "메인 페이지", "NC": "명함", "CS": "Character stand"},
        "jp": {'lvl': 'レベル ', 'AR': 'AR', 'WL': 'WL', 'AC': 'アチーブメント', 'AB': 'アビス', "MP": "メインページ", "NC": "ネームカード", "CS": "Character stand"},
        "zh": {'lvl': '等级', 'AR': 'AR', 'WL': 'WL', 'AC': '成就总数', 'AB': '深境螺旋', "MP": "主頁", "NC": "名片", "CS": "Character stand"},
        "id": {'lvl': 'Level ', 'AR': 'AR', 'WL': 'WL', 'AC': ' Prestasi ', 'AB': ' Abyss', "MP": "Halaman Utama", "NC": "Kartu nama", "CS": "Character stand"},
        "fr": {'lvl': 'Niveau ', 'AR': 'AR', 'WL': 'WL', 'AC': ' Réalisations ', 'AB': ' Abîme', "MP": "Page d'accueil", "NC": "Cartes de visite", "CS": "Character stand"},
        "es": {'lvl': 'Nivel ', 'AR': 'AR', 'WL': 'WL', 'AC': ' Logros ', 'AB': ' Abismo', "MP": "Pagina principal", "NC": "Tarjetas de nombre", "CS": "Character stand"},
        "de": {'lvl': 'Level ', 'AR': 'AR', 'WL': 'WL', 'AC': ' Erfolge ', 'AB': ' Abyss', "MP": "Hauptseite", "NC": "Namenskarten", "CS": "Character stand"},
        "chs": {'lvl': '等级', 'AR': 'AR', 'WL': 'WL', 'AC': '成就总数', 'AB': '深境螺旋', "MP": "主頁", "NC": "名片", "CS": "Character stand"},
        "cht": {'lvl': '等級', 'AR': 'AR', 'WL': 'WL', 'AC': '成就總數', 'AB': '深境螺旋', "MP": "主頁", "NC": "名片", "CS": "Character stand"},
    }



class Translator:
    def __init__(self,lang) -> None:
        self.lang = str(lang)
        
    def __getattr__(self,name):
        if self.lang  in translationLang:
            return translationLang[self.lang].get(name)
        else:
            raise AttributeError(f"'{type(self)}' object has no attribute '{self.lang}'")