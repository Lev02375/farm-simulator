import tkinter as tk
from tkinter import messagebox
import time
import random

# ===================== ЛОКАЛИЗАЦИЯ =====================

TEXTS = {
    'en': {
        'title': "Farm Simulator",
        'money': "Money",
        'level': "Level",
        'xp': "XP",
        'water': "Water",
        'weather': "Weather",
        'farm_title': "YOUR FARM",
        'crops_tab': "CROPS",
        'shop_tab': "SHOP",
        'settings_tab': "SETTINGS",
        'help_tab': "HELP",
        'cheats_tab': "CHEATS",
        'empty': "[SOIL]",
        'ready': "READY",
        'dead': "[DEAD]",
        'dry': "DRY",
        'min': "min",
        'locked': "LOCK Lv.",
        'seed': "Seed",
        'sell': "Sell",
        'grow': "Grow",
        'buy': "Buy",
        'bought': "[BOUGHT]",
        'max': "[MAX]",
        'no_money': "Not enough money!",
        'need': "Need",
        'locked_title': "Locked",
        'reach_level': "Reach level",
        'no_tool': "No Tool",
        'buy_can_first': "Buy Watering Can first!",
        'water_mode_on': "WATER MODE ON",
        'water_mode_off': "WATER MODE",
        'watered': "Watered",
        'planted': "Planted",
        'harvested': "Harvested",
        'cleared': "Cleared dead plant",
        'level_up': "Level Up",
        'bonus': "Bonus",
        'new_crops': "New crops unlocked!",
        'weather_sunny': "Sunny! Normal growth.",
        'weather_rain': "Raining! Auto-watering active.",
        'weather_storm': "STORM! Plants at risk!",
        'weather_snow': "Snowing! Growth stopped.",
        'weather_cloudy': "Cloudy. Slower growth.",
        'storm_destroy': "STORM destroyed a",
        'language': "Language",
        'watering_can': "Watering Can",
        'watering_can_desc': "Enables watering. Lv1: 1 cell. Lv2: 3x3 area.",
        'auto_water': "Auto-Water",
        'auto_water_desc': "Plants never dry out.",
        'growth_boost': "Growth Boost",
        'growth_boost_desc': "Plants grow 50% faster.",
        'expand_field': "Expand Field",
        'expand_field_desc': "Increase farm size.",
        'greenhouse': "Greenhouse",
        'greenhouse_desc': "Plants never wither.",
        'auto_harvest': "Auto-Harvest",
        'auto_harvest_desc': "Auto collect ready crops.",
        'pest_control': "Pest Control",
        'pest_control_desc': "Protects from pests.",
        'marketing': "Marketing",
        'marketing_desc': "+25% sell price.",
        'water_tank': "Water Tank",
        'water_tank_desc': "+25 max water capacity.",
        'rain_collector': "Rain Collector",
        'rain_collector_desc': "Auto-refills water faster.",
        'help_text': "HOW TO PLAY\n\nLeft Click = Plant / Harvest\nClick WATER MODE then Left Click = Water\n\nWATER SYSTEM:\n- Buy Watering Can first!\n- Click WATER MODE to enable watering\n- Each water costs 5 units\n- Water refills over time\n\n25 CROPS (1-18 min grow time)\n- Unlock by leveling up\n- Higher level = more profit\n\nTIPS:\n- Plants dry out in 15s without water\n- Withered = no profit\n- Buy upgrades wisely!",
        'cheat_codes': "CHEAT CODES",
        'enter_cheat': "Enter cheat code:",
        'execute': "EXECUTE",
        'cheat_money': "money [amount] - set money",
        'cheat_level': "level [amount] - set level",
        'cheat_water': "water [amount] - set water",
        'cheat_speed': "speed [mult] - growth speed",
        'cheat_weather': "weather [sunny/rain/storm/snow/cloudy]",
        'cheat_unlock': "unlockall - unlock all crops",
        'cheat_god': "godmode - activate god mode",
        'cheat_maxwater': "maxwater - infinite water",
        'secret_unlocked': "SECRET CROP UNLOCKED!",
        'money_tree': "Money Tree",
    },
    'ru': {
        'title': "Фермерский Симулятор",
        'money': "Деньги",
        'level': "Уровень",
        'xp': "Опыт",
        'water': "Вода",
        'weather': "Погода",
        'farm_title': "ВАША ФЕРМА",
        'crops_tab': "РАСТЕНИЯ",
        'shop_tab': "МАГАЗИН",
        'settings_tab': "НАСТРОЙКИ",
        'help_tab': "ПОМОЩЬ",
        'cheats_tab': "ЧИТЫ",
        'empty': "[ЗЕМЛЯ]",
        'ready': "ГОТОВО",
        'dead': "[ЗАСОХЛО]",
        'dry': "СУХО",
        'min': "мин",
        'locked': "ЗАМОК Ур.",
        'seed': "Семена",
        'sell': "Продажа",
        'grow': "Рост",
        'buy': "Купить",
        'bought': "[КУПЛЕНО]",
        'max': "[МАКС]",
        'no_money': "Недостаточно денег!",
        'need': "Нужно",
        'locked_title': "Закрыто",
        'reach_level': "Достигните уровня",
        'no_tool': "Нет инструмента",
        'buy_can_first': "Сначала купите лейку!",
        'water_mode_on': "РЕЖИМ ПОЛИВА ВКЛ",
        'water_mode_off': "РЕЖИМ ПОЛИВА",
        'watered': "Полито",
        'planted': "Посажено",
        'harvested': "Собрано",
        'cleared': "Убрано засохшее растение",
        'level_up': "Новый уровень",
        'bonus': "Бонус",
        'new_crops': "Новые растения открыты!",
        'weather_sunny': "Солнечно! Нормальный рост.",
        'weather_rain': "Идет дождь! Авто-полив активен.",
        'weather_storm': "ГРОЗА! Растения в опасности!",
        'weather_snow': "Идет снег! Рост остановлен.",
        'weather_cloudy': "Облачно. Медленный рост.",
        'storm_destroy': "ГРОЗА уничтожила",
        'language': "Язык",
        'watering_can': "Лейка",
        'watering_can_desc': "Включает полив. Ур.1: 1 клетка. Ур.2: 3x3.",
        'auto_water': "Авто-полив",
        'auto_water_desc': "Растения не сохнут.",
        'growth_boost': "Ускорение роста",
        'growth_boost_desc': "Растения растут на 50% быстрее.",
        'expand_field': "Расширить поле",
        'expand_field_desc': "Увеличить размер фермы.",
        'greenhouse': "Теплица",
        'greenhouse_desc': "Растения не засыхают.",
        'auto_harvest': "Авто-сбор",
        'auto_harvest_desc': "Автоматически собирает урожай.",
        'pest_control': "Защита от вредителей",
        'pest_control_desc': "Защищает от вредителей.",
        'marketing': "Маркетинг",
        'marketing_desc': "+25% к цене продажи.",
        'water_tank': "Бак для воды",
        'water_tank_desc': "+25 макс. воды.",
        'rain_collector': "Дождесборник",
        'rain_collector_desc': "Быстрее восполняет воду.",
        'help_text': "КАК ИГРАТЬ\n\nЛКМ = Посадить / Собрать\nНажми РЕЖИМ ПОЛИВА, затем ЛКМ = Полить\n\nСИСТЕМА ВОДЫ:\n- Сначала купи лейку!\n- Нажми РЕЖИМ ПОЛИВА для полива\n- Каждый полив стоит 5 воды\n- Вода восстанавливается со временем\n\n25 РАСТЕНИЙ (1-18 мин рост)\n- Открываются по уровням\n- Выше уровень = больше прибыли\n\nСОВЕТЫ:\n- Растения сохнут за 15 сек без воды\n- Засохшие = нет прибыли\n- Покупай улучшения с умом!",
        'cheat_codes': "ЧИТ-КОДЫ",
        'enter_cheat': "Введите чит-код:",
        'execute': "ВЫПОЛНИТЬ",
        'cheat_money': "money [сумма] - установить деньги",
        'cheat_level': "level [уровень] - установить уровень",
        'cheat_water': "water [кол-во] - установить воду",
        'cheat_speed': "speed [множитель] - скорость роста",
        'cheat_weather': "weather [sunny/rain/storm/snow/cloudy]",
        'cheat_unlock': "unlockall - открыть все растения",
        'cheat_god': "godmode - режим бога",
        'cheat_maxwater': "maxwater - бесконечная вода",
        'secret_unlocked': "СЕКРЕТНОЕ РАСТЕНИЕ ОТКРЫТО!",
        'money_tree': "Денежное Дерево",
    }
}

# ===================== КЛАССЫ =====================

class Crop:
    def __init__(self, name_en, name_ru, seed_cost, sell_price, grow_time_min, color, unlock_level=1):
        self.name_en = name_en
        self.name_ru = name_ru
        self.seed_cost = seed_cost
        self.sell_price = sell_price
        self.grow_time = grow_time_min * 60
        self.color = color
        self.unlock_level = unlock_level

class FarmCell:
    def __init__(self):
        self.crop = None
        self.plant_time = None
        self.watered = False
        self.stage = 'empty'
        self.progress = 0.0

class Weather:
    def __init__(self):
        self.current = 'sunny'
        self.last_change = time.time()
        self.change_interval = 120
        self.names = {'sunny': 'SUNNY', 'rain': 'RAIN', 'storm': 'STORM', 'snow': 'SNOW', 'cloudy': 'CLOUDY'}
        self.colors = {'sunny': '#F39C12', 'rain': '#3498DB', 'storm': '#8E44AD', 'snow': '#BDC3C7', 'cloudy': '#7F8C8D'}

# ASCII-арт растений
_s = chr(92)
SEED_ART = '  .  ' + chr(10) + ' /|' + _s + ' ' + chr(10) + '/ | ' + _s
SPROUT_ART = '  |  ' + chr(10) + ' /|' + _s + ' ' + chr(10) + '/ | ' + _s
GROW_ART = '  Y  ' + chr(10) + ' /|' + _s + ' ' + chr(10) + '/ | ' + _s
BUSH_ART = '  *  ' + chr(10) + ' /|' + _s + ' ' + chr(10) + '/ | ' + _s
READY_ART = ' [O] ' + chr(10) + ' /|' + _s + ' ' + chr(10) + '/ | ' + _s
DEAD_ART = '  x  ' + chr(10) + ' /|' + _s + ' ' + chr(10) + '/ | ' + _s
MONEY_TREE_ART = '  $  ' + chr(10) + ' /|' + _s + ' ' + chr(10) + '/ | ' + _s

class FarmGame:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x850")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)

        self.lang = 'en'
        self.t = TEXTS[self.lang]

        self.money = 200
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        self.water = 50
        self.max_water = 50
        self.grid_size = 3

        self.has_watering_can = False
        self.watering_can_level = 0
        self.auto_water = False
        self.growth_speed = 1.0
        self.auto_harvest = False
        self.price_bonus = 1.0
        self.greenhouse = False
        self.rain_collector = False
        self.water_mode = False

        self.weather = Weather()

        self.crops = {
            'wheat':      Crop('Wheat',       'Пшеница',      15,  40,   1, '#F4D03F', 1),
            'carrot':     Crop('Carrot',      'Морковь',      30,  80,   2, '#E67E22', 1),
            'potato':     Crop('Potato',      'Картофель',    50,  140,  3, '#D4AC0D', 1),
            'tomato':     Crop('Tomato',      'Помидор',      90,  220,  4, '#E74C3C', 2),
            'corn':       Crop('Corn',        'Кукуруза',     140, 400,  5, '#F39C12', 2),
            'strawberry': Crop('Strawberry',  'Клубника',     120, 320,  4, '#FF6B6B', 2),
            'onion':      Crop('Onion',       'Лук',          70,  180,  3, '#DDA0DD', 3),
            'garlic':     Crop('Garlic',      'Чеснок',       85,  220,  4, '#F5F5DC', 3),
            'rice':       Crop('Rice',        'Рис',          100, 280,  5, '#FFFFF0', 3),
            'pepper':     Crop('Pepper',      'Перец',        180, 500,  6, '#2ECC71', 4),
            'cabbage':    Crop('Cabbage',     'Капуста',      150, 380,  5, '#82E0AA', 4),
            'broccoli':   Crop('Broccoli',    'Брокколи',     200, 550,  7, '#27AE60', 4),
            'eggplant':   Crop('Eggplant',    'Баклажан',     280, 750,  8, '#8E44AD', 5),
            'watermelon': Crop('Watermelon',  'Арбуз',        250, 650,  8, '#2ECC71', 5),
            'pumpkin':    Crop('Pumpkin',     'Тыква',        320, 900,  10, '#E67E22', 5),
            'sunflower':  Crop('Sunflower',   'Подсолнух',    300, 800,  9, '#F1C40F', 6),
            'pineapple':  Crop('Pineapple',   'Ананас',       400, 1100, 10, '#F39C12', 6),
            'grape':      Crop('Grape',       'Виноград',     500, 1400, 12, '#9B59B6', 7),
            'cherry':     Crop('Cherry',      'Вишня',        600, 1600, 12, '#E91E63', 7),
            'olive':      Crop('Olive',       'Олива',        750, 2000, 13, '#9E9D24', 8),
            'peach':      Crop('Peach',       'Персик',       850, 2300, 13, '#FFAB91', 8),
            'mango':      Crop('Mango',       'Манго',        1000, 2800, 14, '#FFD54F', 9),
            'coconut':    Crop('Coconut',     'Кокос',        1200, 3400, 15, '#795548', 9),
            'dragonfruit':Crop('Dragon Fruit','Питахайя',     1500, 4200, 16, '#AB47BC', 10),
            'saffron':    Crop('Saffron',     'Шафран',       2000, 6000, 18, '#FBC02D', 11),
            'money_tree': Crop('Money Tree',  'Денежное Дерево', 0, 0, 1, '#FFD700', 999),
        }

        self.selected_crop = 'wheat'
        self.farm = [[FarmCell() for _ in range(6)] for _ in range(6)]
        self.cell_buttons = [[None for _ in range(6)] for _ in range(6)]

        self.setup_ui()
        self.game_loop()

    def setup_ui(self):
        self.root.title(self.t['title'])

        # --- Верхняя панель ---
        top = tk.Frame(self.root, bg='#16213e', height=70)
        top.pack(fill=tk.X, padx=8, pady=4)
        top.pack_propagate(False)

        self.money_lbl = tk.Label(top, text=self.t['money'] + ': $200', font=('Arial', 13, 'bold'), fg='#2ECC71', bg='#16213e')
        self.money_lbl.pack(side=tk.LEFT, padx=10, pady=12)
        self.level_lbl = tk.Label(top, text=self.t['level'] + ': 1', font=('Arial', 13, 'bold'), fg='#F39C12', bg='#16213e')
        self.level_lbl.pack(side=tk.LEFT, padx=10, pady=12)
        self.xp_lbl = tk.Label(top, text=self.t['xp'] + ': 0/100', font=('Arial', 12), fg='#3498DB', bg='#16213e')
        self.xp_lbl.pack(side=tk.LEFT, padx=10, pady=12)
        self.water_lbl = tk.Label(top, text=self.t['water'] + ': 50/50', font=('Arial', 12), fg='#5DADE2', bg='#16213e')
        self.water_lbl.pack(side=tk.LEFT, padx=10, pady=12)
        self.weather_lbl = tk.Label(top, text=self.t['weather'] + ': ' + self.weather.names['sunny'], font=('Arial', 12, 'bold'), fg='#F39C12', bg='#16213e')
        self.weather_lbl.pack(side=tk.LEFT, padx=10, pady=12)

        # Кнопка режима полива
        self.water_mode_btn = tk.Button(top, text=self.t['water_mode_off'], font=('Arial', 10, 'bold'),
                                        bg='#3498DB', fg='white', command=self.toggle_water_mode)
        self.water_mode_btn.pack(side=tk.RIGHT, padx=10, pady=12)

        # --- Основная область ---
        main = tk.Frame(self.root, bg='#1a1a2e')
        main.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # --- Левая часть: Поле ---
        left = tk.Frame(main, bg='#5D4037', bd=3, relief=tk.RIDGE)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

        self.farm_title = tk.Label(left, text=self.t['farm_title'], font=('Arial', 16, 'bold'), bg='#5D4037', fg='white')
        self.farm_title.pack(pady=6)

        self.grid_frame = tk.Frame(left, bg='#5D4037')
        self.grid_frame.pack(padx=8, pady=8)

        self.create_grid()

        # --- Правая часть ---
        right = tk.Frame(main, width=340, bg='#0f3460')
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=4)
        right.pack_propagate(False)

        # Вкладки
        tabs = tk.Frame(right, bg='#0f3460')
        tabs.pack(fill=tk.X, padx=4, pady=4)

        self.tab_frames = {}
        self.tab_buttons = {}

        tab_names = [('crops', 'crops_tab'), ('shop', 'shop_tab'), ('settings', 'settings_tab'), ('help', 'help_tab'), ('cheats', 'cheats_tab')]
        for name, label_key in tab_names:
            btn = tk.Button(tabs, text=self.t[label_key], font=('Arial', 9, 'bold'), bg='#3498DB', fg='white', width=7,
                           command=lambda n=name: self.switch_tab(n))
            btn.pack(side=tk.LEFT, padx=1)
            self.tab_buttons[name] = btn
            frame = tk.Frame(right, bg='#0f3460')
            self.tab_frames[name] = frame

        self.current_tab = 'crops'
        self.tab_frames['crops'].pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.tab_buttons['crops'].config(bg='#27AE60')

        # --- Вкладка CROPS ---
        self.build_crops_tab()

        # --- Вкладка SHOP ---
        self.build_shop_tab()

        # --- Вкладка SETTINGS ---
        self.build_settings_tab()

        # --- Вкладка HELP ---
        self.build_help_tab()

        # --- Вкладка CHEATS ---
        self.build_cheats_tab()

        # --- Лог ---
        self.log_text = tk.Text(right, height=5, width=38, font=('Courier', 9), state=tk.DISABLED, bg='#1a1a2e', fg='#2ECC71', wrap=tk.WORD)
        self.log_text.pack(fill=tk.X, padx=4, pady=4)

        self.log('Welcome!')
        self.log('Buy Watering Can, then click WATER MODE to water!')

    def _on_mousewheel(self, event, canvas):
        if event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "units")

    def build_crops_tab(self):
        crops_f = self.tab_frames['crops']
        for widget in crops_f.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(crops_f, bg='#0f3460', highlightthickness=0)
        sb = tk.Scrollbar(crops_f, orient=tk.VERTICAL, command=canvas.yview)
        inner = tk.Frame(canvas, bg='#0f3460')

        canvas.create_window((0, 0), window=inner, anchor='nw', width=310)
        canvas.configure(yscrollcommand=sb.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.crops_canvas = canvas
        self.crops_sb = sb

        # Привязка колесика мыши
        def on_mousewheel(event):
            if event.num == 4 or event.delta > 0:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                canvas.yview_scroll(1, "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        canvas.bind_all("<Button-4>", on_mousewheel)
        canvas.bind_all("<Button-5>", on_mousewheel)

        self.crop_var = tk.StringVar(value='wheat')
        self.crop_buttons = {}

        for crop_id, crop in self.crops.items():
            if crop_id == 'money_tree':
                continue
            f = tk.Frame(inner, bg='#1a1a2e', bd=2, relief=tk.GROOVE)
            f.pack(fill=tk.X, padx=4, pady=2)
            locked = self.level < crop.unlock_level
            state = tk.DISABLED if locked else tk.NORMAL
            fg_color = '#7F8C8D' if locked else 'white'
            name = crop.name_ru if self.lang == 'ru' else crop.name_en
            rb = tk.Radiobutton(f, text=name, variable=self.crop_var, value=crop_id,
                               font=('Arial', 10, 'bold'), bg='#1a1a2e', fg=fg_color, selectcolor='#0f3460', state=state,
                               command=lambda: self.select_crop())
            rb.pack(anchor=tk.W, padx=4, pady=1)
            mins = crop.grow_time // 60
            info = self.t['seed'] + ': $' + str(crop.seed_cost) + ' | ' + self.t['sell'] + ': $' + str(crop.sell_price) + ' | ' + self.t['grow'] + ': ' + str(mins) + ' ' + self.t['min']
            if locked: info = info + ' | ' + self.t['locked'] + str(crop.unlock_level)
            tk.Label(f, text=info, font=('Arial', 8), bg='#1a1a2e', fg='#95A5A6').pack(anchor=tk.W, padx=4, pady=(0,2))
            self.crop_buttons[crop_id] = (rb, f)
    def build_shop_tab(self):
        shop_f = self.tab_frames['shop']
        for widget in shop_f.winfo_children():
            widget.destroy()
        shop_canvas = tk.Canvas(shop_f, bg='#0f3460', highlightthickness=0)
        shop_sb = tk.Scrollbar(shop_f, orient=tk.VERTICAL, command=shop_canvas.yview)
        shop_inner = tk.Frame(shop_canvas, bg='#0f3460')

        shop_canvas.create_window((0, 0), window=shop_inner, anchor='nw', width=310)
        shop_canvas.configure(yscrollcommand=shop_sb.set)

        shop_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        shop_sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.shop_canvas = shop_canvas
        self.shop_sb = shop_sb

        shop_items = [
            ('watering_can', self.t['watering_can'], self.t['watering_can_desc'], 80, self.buy_watering_can),
            ('auto_water', self.t['auto_water'], self.t['auto_water_desc'], 1200, self.buy_auto_water),
            ('growth_boost', self.t['growth_boost'], self.t['growth_boost_desc'], 1500, self.buy_growth_boost),
            ('expand', self.t['expand_field'], self.t['expand_field_desc'], 500, self.expand_farm),
            ('greenhouse', self.t['greenhouse'], self.t['greenhouse_desc'], 2000, self.buy_greenhouse),
            ('auto_harvest', self.t['auto_harvest'], self.t['auto_harvest_desc'], 3000, self.buy_auto_harvest),
            ('pest', self.t['pest_control'], self.t['pest_control_desc'], 800, self.buy_pest_control),
            ('marketing', self.t['marketing'], self.t['marketing_desc'], 1000, self.buy_marketing),
            ('water_tank', self.t['water_tank'], self.t['water_tank_desc'], 300, self.buy_water_tank),
            ('rain', self.t['rain_collector'], self.t['rain_collector_desc'], 1500, self.buy_rain_collector),
        ]

        self.shop_buttons = {}
        for key, name, desc, cost, cmd in shop_items:
            f = tk.Frame(shop_inner, bg='#1a1a2e', bd=2, relief=tk.GROOVE)
            f.pack(fill=tk.X, padx=4, pady=2)
            btn = tk.Button(f, text=name + ' ($' + str(cost) + ')', font=('Arial', 9, 'bold'), bg='#3498DB', fg='white', command=cmd)
            btn.pack(fill=tk.X, padx=4, pady=(4,0))
            tk.Label(f, text=desc, font=('Arial', 8), bg='#1a1a2e', fg='#95A5A6', justify=tk.LEFT).pack(anchor=tk.W, padx=4, pady=(0,3))
            self.shop_buttons[key] = btn
    def build_settings_tab(self):
        settings_f = self.tab_frames['settings']
        for widget in settings_f.winfo_children():
            widget.destroy()
        tk.Label(settings_f, text=self.t['language'], font=('Arial', 14, 'bold'), bg='#0f3460', fg='white').pack(pady=20)

        lang_frame = tk.Frame(settings_f, bg='#0f3460')
        lang_frame.pack(pady=10)

        self.lang_var = tk.StringVar(value=self.lang)
        tk.Radiobutton(lang_frame, text='English', variable=self.lang_var, value='en',
                      font=('Arial', 12), bg='#0f3460', fg='white', selectcolor='#0f3460',
                      command=lambda: self.change_language('en')).pack(anchor=tk.W, padx=10, pady=5)
        tk.Radiobutton(lang_frame, text='Русский', variable=self.lang_var, value='ru',
                      font=('Arial', 12), bg='#0f3460', fg='white', selectcolor='#0f3460',
                      command=lambda: self.change_language('ru')).pack(anchor=tk.W, padx=10, pady=5)

        tk.Label(settings_f, text='Farm Simulator v5', font=('Arial', 10), bg='#0f3460', fg='#95A5A6').pack(pady=30)

    def build_help_tab(self):
        help_f = self.tab_frames['help']
        for widget in help_f.winfo_children():
            widget.destroy()
        tk.Label(help_f, text=self.t['help_text'], font=('Arial', 10), bg='#0f3460', fg='white', justify=tk.LEFT, wraplength=300).pack(padx=8, pady=8)

    def build_cheats_tab(self):
        cheats_f = self.tab_frames['cheats']
        for widget in cheats_f.winfo_children():
            widget.destroy()

        tk.Label(cheats_f, text=self.t['cheat_codes'], font=('Arial', 14, 'bold'), bg='#0f3460', fg='#E74C3C').pack(pady=10)

        tk.Label(cheats_f, text=self.t['enter_cheat'], font=('Arial', 10), bg='#0f3460', fg='white').pack(pady=5)

        self.cheat_entry = tk.Entry(cheats_f, font=('Courier', 11), bg='#1a1a2e', fg='#2ECC71', insertbackground='#2ECC71')
        self.cheat_entry.pack(fill=tk.X, padx=10, pady=5)
        self.cheat_entry.bind('<Return>', lambda e: self.execute_cheat())

        tk.Button(cheats_f, text=self.t['execute'], font=('Arial', 10, 'bold'), bg='#E74C3C', fg='white',
                 command=self.execute_cheat).pack(pady=5)

        # Подсказки убраны по запросу

    def change_language(self, lang):
        if self.lang == lang:
            return
        self.lang = lang
        self.t = TEXTS[self.lang]

        # Пересоздаём UI
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_ui()

        # Восстанавливаем состояние грядок
        for i in range(6):
            for j in range(6):
                self.update_cell(i, j)
        self.update_stats()

    def toggle_water_mode(self):
        self.water_mode = not self.water_mode
        if self.water_mode:
            self.water_mode_btn.config(text=self.t['water_mode_on'], bg='#E74C3C')
        else:
            self.water_mode_btn.config(text=self.t['water_mode_off'], bg='#3498DB')

    def switch_tab(self, name):
        self.tab_frames[self.current_tab].pack_forget()
        self.tab_buttons[self.current_tab].config(bg='#3498DB')
        self.current_tab = name
        self.tab_frames[name].pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.tab_buttons[name].config(bg='#27AE60')

        # Обновляем scrollregion, когда вкладка становится видимой
        if name == 'crops' and hasattr(self, 'crops_canvas'):
            self.crops_canvas.after(50, lambda: self.crops_canvas.configure(scrollregion=self.crops_canvas.bbox('all')))
        elif name == 'shop' and hasattr(self, 'shop_canvas'):
            self.shop_canvas.after(50, lambda: self.shop_canvas.configure(scrollregion=self.shop_canvas.bbox('all')))

    def create_grid(self):
        for i in range(6):
            for j in range(6):
                btn = tk.Button(self.grid_frame, width=12, height=6,
                               font=('Courier', 8, 'bold'),
                               bg='#6D4C41', fg='#D7CCC8',
                               activebackground='#5D4037',
                               relief=tk.RIDGE, bd=3,
                               command=lambda r=i, c=j: self.cell_click(r, c))
                btn.grid(row=i, column=j, padx=3, pady=3)
                self.cell_buttons[i][j] = btn
                if i >= self.grid_size or j >= self.grid_size:
                    btn.grid_remove()

    def update_cell(self, row, col):
        cell = self.farm[row][col]
        btn = self.cell_buttons[row][col]
        if row >= self.grid_size or col >= self.grid_size:
            btn.grid_remove()
            return
        else:
            btn.grid()

        if cell.stage == 'empty':
            btn.config(text=self.t['empty'], bg='#6D4C41', fg='#D7CCC8',
                      activebackground='#5D4037', relief=tk.RIDGE, bd=3)
        elif cell.stage == 'growing':
            crop = self.crops[cell.crop]
            progress = min(1.0, cell.progress)
            if cell.crop == 'money_tree':
                art = MONEY_TREE_ART
            elif progress < 0.2:
                art = SEED_ART
            elif progress < 0.4:
                art = SPROUT_ART
            elif progress < 0.7:
                art = GROW_ART
            else:
                art = BUSH_ART
            mins_left = int((crop.grow_time - progress * crop.grow_time) / 60)
            if mins_left < 1:
                time_text = '<1' + self.t['min']
            else:
                time_text = str(mins_left) + self.t['min']
            if cell.watered:
                btn.config(text=art + chr(10) + '---' + chr(10) + time_text,
                          bg='#2E7D32', fg='white',
                          activebackground='#1B5E20', relief=tk.RAISED, bd=4)
            else:
                btn.config(text=art + chr(10) + '---' + chr(10) + self.t['dry'] + '! ' + time_text,
                          bg='#BF360C', fg='white',
                          activebackground='#870000', relief=tk.SUNKEN, bd=2)
        elif cell.stage == 'ready':
            crop = self.crops[cell.crop]
            if cell.crop == 'money_tree':
                art = MONEY_TREE_ART
            else:
                art = READY_ART
            name = crop.name_ru if self.lang == 'ru' else crop.name_en
            btn.config(text=art + chr(10) + '---' + chr(10) + name.upper(),
                      bg=crop.color, fg='black',
                      activebackground='#F1C40F', relief=tk.RAISED, bd=5)
        elif cell.stage == 'withered':
            art = DEAD_ART
            btn.config(text=art + chr(10) + '---' + chr(10) + self.t['dead'],
                      bg='#455A64', fg='#B0BEC5',
                      activebackground='#37474F', relief=tk.SUNKEN, bd=2)

    def update_weather(self):
        current_time = time.time()
        if current_time - self.weather.last_change > self.weather.change_interval:
            self.weather.last_change = current_time
            weather_types = ['sunny', 'rain', 'cloudy', 'storm', 'snow']
            weights = [40, 25, 20, 10, 5]
            self.weather.current = random.choices(weather_types, weights=weights)[0]
            w = self.weather.current
            self.weather_lbl.config(text=self.t['weather'] + ': ' + self.weather.names[w], fg=self.weather.colors[w])
            if w == 'sunny':
                self.log(self.t['weather_sunny'])
            elif w == 'rain':
                self.log(self.t['weather_rain'])
            elif w == 'storm':
                self.log(self.t['weather_storm'])
            elif w == 'snow':
                self.log(self.t['weather_snow'])
            elif w == 'cloudy':
                self.log(self.t['weather_cloudy'])

    def get_weather_growth_multiplier(self):
        w = self.weather.current
        if w == 'sunny': return 1.0
        elif w == 'rain': return 0.8
        elif w == 'cloudy': return 0.6
        elif w == 'snow': return 0.0
        elif w == 'storm': return 0.3
        return 1.0

    def execute_cheat(self):
        cmd = self.cheat_entry.get().strip().lower()
        self.cheat_entry.delete(0, tk.END)
        if not cmd: return
        parts = cmd.split()
        action = parts[0]
        try:
            if action == 'money' and len(parts) > 1:
                self.money = int(parts[1])
                self.log('CHEAT: ' + self.t['money'] + ' = $' + str(self.money))
            elif action == 'level' and len(parts) > 1:
                self.level = int(parts[1])
                self.log('CHEAT: ' + self.t['level'] + ' = ' + str(self.level))
            elif action == 'water' and len(parts) > 1:
                self.water = int(parts[1])
                self.log('CHEAT: ' + self.t['water'] + ' = ' + str(self.water))
            elif action == 'speed' and len(parts) > 1:
                self.growth_speed = float(parts[1])
                self.log('CHEAT: speed x' + str(self.growth_speed))
            elif action == 'weather' and len(parts) > 1:
                w = parts[1]
                if w in self.weather.names:
                    self.weather.current = w
                    self.weather_lbl.config(text=self.t['weather'] + ': ' + self.weather.names[w], fg=self.weather.colors[w])
                    self.log('CHEAT: weather = ' + self.weather.names[w])
            elif action == 'unlockall':
                self.level = 99
                self.log('CHEAT: unlockall')
            elif action == 'maxwater':
                self.max_water = 999
                self.water = 999
                self.log('CHEAT: maxwater')
            elif action == 'godmode':
                self.auto_water = True
                self.greenhouse = True
                self.auto_harvest = True
                self.growth_speed = 10.0
                self.log('CHEAT: GOD MODE!')
            elif action == 'get' and len(parts) >= 3 and parts[1] == 'admin' and parts[2] == 'crop8365':
                # Ищем первую свободную клетку
                planted = False
                for i in range(self.grid_size):
                    for j in range(self.grid_size):
                        if self.farm[i][j].stage == 'empty':
                            cell = self.farm[i][j]
                            cell.crop = 'money_tree'
                            cell.plant_time = time.time()
                            cell.watered = True
                            cell.stage = 'growing'
                            cell.progress = 0.0
                            self.update_cell(i, j)
                            self.log('SECRET: ' + self.t['money_tree'] + ' ' + self.t['planted'] + ' [' + str(i) + ',' + str(j) + ']')
                            planted = True
                            break
                    if planted:
                        break
                if not planted:
                    self.log('SECRET: No empty cell for Money Tree!')
            else:
                self.log('Unknown cheat: ' + cmd)
        except:
            self.log('Invalid cheat: ' + cmd)
        self.update_stats()

    def select_crop(self):
        self.selected_crop = self.crop_var.get()

    def cell_click(self, row, col):
        cell = self.farm[row][col]

        # Режим полива
        if self.water_mode:
            if not self.has_watering_can:
                messagebox.showinfo(self.t['no_tool'], self.t['buy_can_first'])
                self.toggle_water_mode()
                return
            if self.watering_can_level >= 2:
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        ni, nj = row + di, col + dj
                        if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size:
                            self._water_single(ni, nj)
                self.log(self.t['watered'] + ' 3x3 [' + str(row) + ',' + str(col) + ']')
            else:
                self._water_single(row, col)
            return

        # Обычный режим
        if cell.stage == 'empty':
            crop = self.crops[self.selected_crop]
            if self.level < crop.unlock_level:
                messagebox.showwarning(self.t['locked_title'], self.t['reach_level'] + ' ' + str(crop.unlock_level) + '!')
                return
            if self.money >= crop.seed_cost:
                self.money -= crop.seed_cost
                cell.crop = self.selected_crop
                cell.plant_time = time.time()
                cell.watered = True
                cell.stage = 'growing'
                cell.progress = 0.0
                name = crop.name_ru if self.lang == 'ru' else crop.name_en
                self.log(self.t['planted'] + ' ' + name + ' (-$' + str(crop.seed_cost) + ')')
                self.update_stats()
            else:
                messagebox.showwarning(self.t['no_money'], self.t['need'] + ' $' + str(crop.seed_cost))
        elif cell.stage == 'ready':
            crop = self.crops[cell.crop]
            if cell.crop == 'money_tree':
                sell_price = max(1, int(self.money * 0.3))
            else:
                sell_price = int(crop.sell_price * self.price_bonus)
            self.money += sell_price
            xp_gain = int(sell_price / 5)
            self.xp += xp_gain
            name = crop.name_ru if self.lang == 'ru' else crop.name_en
            self.log(self.t['harvested'] + ' ' + name + ' (+$' + str(sell_price) + ', +' + str(xp_gain) + ' XP)')
            if self.xp >= self.xp_to_next:
                self.level_up()
            cell.stage = 'empty'
            cell.crop = None
            cell.watered = False
            cell.progress = 0
            self.update_stats()
        elif cell.stage == 'withered':
            cell.stage = 'empty'
            cell.crop = None
            cell.watered = False
            cell.progress = 0
            self.log(self.t['cleared'])
        self.update_cell(row, col)

    def _water_single(self, row, col):
        cell = self.farm[row][col]
        if cell.stage == 'growing' and self.water >= 5:
            self.water -= 5
            cell.watered = True
            self.update_cell(row, col)
            self.update_stats()

    def game_loop(self):
        current_time = time.time()
        self.update_weather()
        weather_mult = self.get_weather_growth_multiplier()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.farm[i][j]
                if cell.stage == 'growing':
                    crop = self.crops[cell.crop]
                    if self.weather.current == 'rain':
                        cell.watered = True
                    if self.auto_water or self.greenhouse:
                        cell.watered = True
                    if cell.watered and weather_mult > 0:
                        elapsed = current_time - cell.plant_time
                        speed = self.growth_speed * weather_mult
                        cell.progress = min(1.0, elapsed / (crop.grow_time / speed))
                        if cell.progress >= 1.0:
                            cell.stage = 'ready'
                            if self.auto_harvest:
                                self.cell_click(i, j)
                    else:
                        elapsed = current_time - cell.plant_time
                        if elapsed > 15 and cell.progress < 1.0:
                            cell.stage = 'withered'
                if self.weather.current == 'storm' and cell.stage in ['growing', 'ready']:
                    if random.random() < 0.001:
                        cell.stage = 'withered'
                        name = self.crops[cell.crop].name_ru if self.lang == 'ru' else self.crops[cell.crop].name_en
                        self.log(self.t['storm_destroy'] + ' ' + name + '!')
                self.update_cell(i, j)
        if not hasattr(self, 'last_refill'):
            self.last_refill = current_time
        interval = 3 if self.rain_collector else 8
        amount = 3 if self.rain_collector else 1
        if self.weather.current == 'rain':
            interval = 2
            amount = 5
        if current_time - self.last_refill > interval:
            self.last_refill = current_time
            self.water = min(self.max_water, self.water + amount)
            self.update_stats()
        self.root.after(500, self.game_loop)

    def update_stats(self):
        self.money_lbl.config(text=self.t['money'] + ': $' + str(self.money))
        self.level_lbl.config(text=self.t['level'] + ': ' + str(self.level))
        self.xp_lbl.config(text=self.t['xp'] + ': ' + str(self.xp) + '/' + str(self.xp_to_next))
        self.water_lbl.config(text=self.t['water'] + ': ' + str(self.water) + '/' + str(self.max_water))

        if not self.has_watering_can:
            self._set_shop('watering_can', self.t['watering_can'] + ' ($80)', False)
        elif self.watering_can_level == 1:
            self._set_shop('watering_can', self.t['watering_can'] + ' UPGRADE ($200)', False)
        else:
            self._set_shop('watering_can', self.t['watering_can'] + ' ' + self.t['max'], True)

        self._set_shop('auto_water', self.t['auto_water'] + ' ' + self.t['bought'], self.auto_water, self.t['auto_water'] + ' ($1200)')
        self._set_shop('growth_boost', self.t['growth_boost'] + ' x' + str(self.growth_speed) + ' ' + self.t['max'] if self.growth_speed >= 2.5 else self.t['growth_boost'] + ' ($1500)', self.growth_speed >= 2.5)
        if self.grid_size >= 6:
            self._set_shop('expand', self.t['expand_field'] + ' ' + self.t['max'], True)
        else:
            self._set_shop('expand', self.t['expand_field'] + ' ($' + str(500*self.grid_size) + ')', False)
        self._set_shop('greenhouse', self.t['greenhouse'] + ' ' + self.t['bought'], self.greenhouse, self.t['greenhouse'] + ' ($2000)')
        self._set_shop('auto_harvest', self.t['auto_harvest'] + ' ' + self.t['bought'], self.auto_harvest, self.t['auto_harvest'] + ' ($3000)')
        self._set_shop('pest', self.t['pest_control'] + ' ' + self.t['bought'], False, self.t['pest_control'] + ' ($800)')
        self._set_shop('marketing', self.t['marketing'] + ' +' + str(int((self.price_bonus-1)*100)) + '% ' + self.t['max'] if self.price_bonus >= 1.5 else self.t['marketing'] + ' ($1000)', self.price_bonus >= 1.5)
        self._set_shop('water_tank', self.t['water_tank'] + ' (+25) ($300)', False)
        self._set_shop('rain', self.t['rain_collector'] + ' ' + self.t['bought'], self.rain_collector, self.t['rain_collector'] + ' ($1500)')

        for crop_id, (rb, f) in self.crop_buttons.items():
            crop = self.crops[crop_id]
            if self.level >= crop.unlock_level:
                rb.config(state=tk.NORMAL, fg='white')

    def _set_shop(self, key, active_text, active, default_text=None):
        btn = self.shop_buttons.get(key)
        if not btn: return
        if active:
            btn.config(text=active_text, state=tk.DISABLED, bg='#27AE60')
        else:
            btn.config(text=default_text or active_text, state=tk.NORMAL, bg='#3498DB')

    def buy_watering_can(self):
        if not self.has_watering_can:
            if self.money >= 80:
                self.money -= 80; self.has_watering_can = True; self.watering_can_level = 1
                self.log(self.t['watering_can'] + ' ' + self.t['bought'] + '!'); self.update_stats()
            else: messagebox.showwarning(self.t['no_money'], self.t['need'] + ' $80')
        elif self.watering_can_level == 1:
            if self.money >= 200:
                self.money -= 200; self.watering_can_level = 2
                self.log(self.t['watering_can'] + ' UPGRADE!'); self.update_stats()
            else: messagebox.showwarning(self.t['no_money'], self.t['need'] + ' $200')
    def buy_auto_water(self):
        if not self.auto_water and self.money >= 1200:
            self.money -= 1200; self.auto_water = True; self.log(self.t['auto_water'] + ' ON!'); self.update_stats()
    def buy_growth_boost(self):
        if self.growth_speed < 2.5 and self.money >= 1500:
            self.money -= 1500; self.growth_speed += 0.5; self.log('Growth x' + str(self.growth_speed) + '!'); self.update_stats()
    def expand_farm(self):
        if self.grid_size < 6:
            cost = 500 * self.grid_size
            if self.money >= cost:
                self.money -= cost; self.grid_size += 1; self.log(self.t['expand_field'] + '!'); self.update_stats()
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    self.cell_buttons[i][j].grid(); self.update_cell(i, j)
    def buy_greenhouse(self):
        if not self.greenhouse and self.money >= 2000:
            self.money -= 2000; self.greenhouse = True; self.log(self.t['greenhouse'] + ' ON!'); self.update_stats()
    def buy_auto_harvest(self):
        if not self.auto_harvest and self.money >= 3000:
            self.money -= 3000; self.auto_harvest = True; self.log(self.t['auto_harvest'] + ' ON!'); self.update_stats()
    def buy_pest_control(self):
        if self.money >= 800:
            self.money -= 800; self.log(self.t['pest_control'] + ' ON!'); self.update_stats()
    def buy_marketing(self):
        if self.price_bonus < 1.5 and self.money >= 1000:
            self.money -= 1000; self.price_bonus += 0.25; self.log(self.t['marketing'] + ' +' + str(int((self.price_bonus-1)*100)) + '%!'); self.update_stats()
    def buy_water_tank(self):
        if self.money >= 300:
            self.money -= 300; self.max_water += 25; self.water = min(self.max_water, self.water + 25); self.log(self.t['water_tank'] + ' +25!'); self.update_stats()
    def buy_rain_collector(self):
        if not self.rain_collector and self.money >= 1500:
            self.money -= 1500; self.rain_collector = True; self.log(self.t['rain_collector'] + ' ON!'); self.update_stats()
    def level_up(self):
        self.level += 1; self.xp -= self.xp_to_next; self.xp_to_next = int(self.xp_to_next * 1.4)
        bonus = 50 * self.level; self.money += bonus; self.water = self.max_water
        self.log(self.t['level_up'] + ' ' + str(self.level) + '! ' + self.t['bonus'] + ' +$' + str(bonus) + '!')
        msg = self.t['level_up'] + ' ' + str(self.level) + '!' + chr(10) + self.t['bonus'] + ': +$' + str(bonus) + chr(10) + self.t['new_crops']
        messagebox.showinfo(self.t['level_up'], msg)
    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + chr(10))
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    game = FarmGame(root)
    root.mainloop()
