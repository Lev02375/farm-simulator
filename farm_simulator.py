import tkinter as tk
from tkinter import messagebox
import time
import random

# ===================== КЛАССЫ =====================

class Crop:
    def __init__(self, name, seed_cost, sell_price, grow_time_min, color, unlock_level=1):
        self.name = name
        self.seed_cost = seed_cost
        self.sell_price = sell_price
        self.grow_time = grow_time_min * 60  # в секундах
        self.color = color
        self.unlock_level = unlock_level

class FarmCell:
    def __init__(self):
        self.crop = None
        self.plant_time = None
        self.watered = False
        self.stage = 'empty'  # empty, seed, sprout, growing, ready, withered
        self.progress = 0.0

class Weather:
    def __init__(self):
        self.current = 'sunny'  # sunny, rain, storm, snow, cloudy
        self.last_change = time.time()
        self.change_interval = 120  # смена погоды каждые 2 мин
        self.names = {
            'sunny': 'SUNNY',
            'rain': 'RAIN',
            'storm': 'STORM',
            'snow': 'SNOW',
            'cloudy': 'CLOUDY'
        }
        self.colors = {
            'sunny': '#F39C12',
            'rain': '#3498DB',
            'storm': '#8E44AD',
            'snow': '#BDC3C7',
            'cloudy': '#7F8C8D'
        }

class FarmGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Farm Simulator - Realistic Edition")
        self.root.geometry("1200x850")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)

        # --- Ресурсы ---
        self.money = 200
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        self.water = 50
        self.max_water = 50
        self.grid_size = 3

        # --- Инструменты ---
        self.has_watering_can = False
        self.watering_can_level = 0
        self.auto_water = False
        self.growth_speed = 1.0
        self.auto_harvest = False
        self.price_bonus = 1.0
        self.greenhouse = False
        self.rain_collector = False

        # --- Погода ---
        self.weather = Weather()

        # --- 18 растений (время в МИНУТАХ) ---
        self.crops = {
            'wheat':      Crop('Wheat',       15,  40,   1, '#F4D03F', 1),
            'carrot':     Crop('Carrot',      30,  80,   2, '#E67E22', 1),
            'potato':     Crop('Potato',      50,  140,  3, '#D4AC0D', 1),
            'tomato':     Crop('Tomato',      90,  220,  4, '#E74C3C', 2),
            'corn':       Crop('Corn',        140, 400,  5, '#F39C12', 2),
            'strawberry': Crop('Strawberry',  120, 320,  4, '#FF6B6B', 2),
            'onion':      Crop('Onion',       70,  180,  3, '#DDA0DD', 3),
            'garlic':     Crop('Garlic',      85,  220,  4, '#F5F5DC', 3),
            'rice':       Crop('Rice',        100, 280,  5, '#FFFFF0', 3),
            'pepper':     Crop('Pepper',      180, 500,  6, '#2ECC71', 4),
            'cabbage':    Crop('Cabbage',     150, 380,  5, '#82E0AA', 4),
            'broccoli':   Crop('Broccoli',    200, 550,  7, '#27AE60', 4),
            'eggplant':   Crop('Eggplant',    280, 750,  8, '#8E44AD', 5),
            'watermelon': Crop('Watermelon',  250, 650,  8, '#2ECC71', 5),
            'pumpkin':    Crop('Pumpkin',     320, 900,  10, '#E67E22', 5),
            'sunflower':  Crop('Sunflower',   300, 800,  9, '#F1C40F', 6),
            'pineapple':  Crop('Pineapple',   400, 1100, 10, '#F39C12', 6),
            'grape':      Crop('Grape',       500, 1400, 12, '#9B59B6', 7),
        }

        self.selected_crop = 'wheat'
        self.farm = [[FarmCell() for _ in range(6)] for _ in range(6)]
        self.cell_canvases = [[None for _ in range(6)] for _ in range(6)]
        self.cell_frames = [[None for _ in range(6)] for _ in range(6)]

        self.setup_ui()
        self.game_loop()

    # ===================== UI =====================

    def setup_ui(self):
        # --- Верхняя панель ---
        top = tk.Frame(self.root, bg='#16213e', height=70)
        top.pack(fill=tk.X, padx=8, pady=4)
        top.pack_propagate(False)

        self.money_lbl = tk.Label(top, text='Money: $200', font=('Arial', 13, 'bold'), fg='#2ECC71', bg='#16213e')
        self.money_lbl.pack(side=tk.LEFT, padx=12, pady=12)

        self.level_lbl = tk.Label(top, text='Level: 1', font=('Arial', 13, 'bold'), fg='#F39C12', bg='#16213e')
        self.level_lbl.pack(side=tk.LEFT, padx=12, pady=12)

        self.xp_lbl = tk.Label(top, text='XP: 0/100', font=('Arial', 12), fg='#3498DB', bg='#16213e')
        self.xp_lbl.pack(side=tk.LEFT, padx=12, pady=12)

        self.water_lbl = tk.Label(top, text='Water: 50/50', font=('Arial', 12), fg='#5DADE2', bg='#16213e')
        self.water_lbl.pack(side=tk.LEFT, padx=12, pady=12)

        self.weather_lbl = tk.Label(top, text='Weather: SUNNY', font=('Arial', 12, 'bold'), fg='#F39C12', bg='#16213e')
        self.weather_lbl.pack(side=tk.LEFT, padx=12, pady=12)

        # --- Основная область ---
        main = tk.Frame(self.root, bg='#1a1a2e')
        main.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # --- Левая часть: Поле ---
        left = tk.Frame(main, bg='#5D4037', bd=3, relief=tk.RIDGE)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

        tk.Label(left, text='YOUR FARM', font=('Arial', 16, 'bold'), bg='#5D4037', fg='white').pack(pady=6)

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

        for name, label in [('crops', 'CROPS'), ('shop', 'SHOP'), ('help', 'HELP')]:
            btn = tk.Button(tabs, text=label, font=('Arial', 10, 'bold'), bg='#3498DB', fg='white', width=10,
                           command=lambda n=name: self.switch_tab(n))
            btn.pack(side=tk.LEFT, padx=2)
            self.tab_buttons[name] = btn
            frame = tk.Frame(right, bg='#0f3460')
            self.tab_frames[name] = frame

        self.current_tab = 'crops'
        self.tab_frames['crops'].pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.tab_buttons['crops'].config(bg='#27AE60')

        # --- Вкладка CROPS ---
        crops_f = self.tab_frames['crops']
        canvas = tk.Canvas(crops_f, bg='#0f3460', highlightthickness=0)
        sb = tk.Scrollbar(crops_f, orient=tk.VERTICAL, command=canvas.yview)
        inner = tk.Frame(canvas, bg='#0f3460')
        inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=inner, anchor='nw')
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.crop_var = tk.StringVar(value='wheat')
        self.crop_buttons = {}

        for crop_id, crop in self.crops.items():
            f = tk.Frame(inner, bg='#1a1a2e', bd=2, relief=tk.GROOVE)
            f.pack(fill=tk.X, padx=4, pady=2)

            locked = self.level < crop.unlock_level
            state = tk.DISABLED if locked else tk.NORMAL
            fg_color = '#7F8C8D' if locked else 'white'

            mins = crop.grow_time // 60
            rb = tk.Radiobutton(f, text=crop.name, variable=self.crop_var, value=crop_id,
                               font=('Arial', 10, 'bold'), bg='#1a1a2e', fg=fg_color, selectcolor='#0f3460', state=state,
                               command=lambda: self.select_crop())
            rb.pack(anchor=tk.W, padx=4, pady=1)

            info = 'Seed: $' + str(crop.seed_cost) + ' | Sell: $' + str(crop.sell_price) + ' | Grow: ' + str(mins) + ' min'
            if locked:
                info = info + ' | LOCK Lv.' + str(crop.unlock_level)
            tk.Label(f, text=info, font=('Arial', 8), bg='#1a1a2e', fg='#95A5A6').pack(anchor=tk.W, padx=4, pady=(0,2))
            self.crop_buttons[crop_id] = (rb, f)

        # --- Вкладка SHOP ---
        shop_f = self.tab_frames['shop']
        shop_canvas = tk.Canvas(shop_f, bg='#0f3460', highlightthickness=0)
        shop_sb = tk.Scrollbar(shop_f, orient=tk.VERTICAL, command=shop_canvas.yview)
        shop_inner = tk.Frame(shop_canvas, bg='#0f3460')
        shop_inner.bind('<Configure>', lambda e: shop_canvas.configure(scrollregion=shop_canvas.bbox('all')))
        shop_canvas.create_window((0, 0), window=shop_inner, anchor='nw')
        shop_canvas.configure(yscrollcommand=shop_sb.set)
        shop_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        shop_sb.pack(side=tk.RIGHT, fill=tk.Y)

        shop_items = [
            ('watering_can', 'Watering Can', 'Enable watering. Lv1: 1 cell. Lv2: 3x3.', 80, self.buy_watering_can),
            ('auto_water', 'Auto-Water', 'Plants never dry out.', 1200, self.buy_auto_water),
            ('growth_boost', 'Growth Boost', 'Plants grow 50% faster.', 1500, self.buy_growth_boost),
            ('expand', 'Expand Field', 'Increase farm size.', 500, self.expand_farm),
            ('greenhouse', 'Greenhouse', 'Plants never wither.', 2000, self.buy_greenhouse),
            ('auto_harvest', 'Auto-Harvest', 'Auto collect ready crops.', 3000, self.buy_auto_harvest),
            ('pest', 'Pest Control', 'Protects from pests.', 800, self.buy_pest_control),
            ('marketing', 'Marketing', '+25% sell price.', 1000, self.buy_marketing),
            ('water_tank', 'Water Tank', '+25 max water.', 300, self.buy_water_tank),
            ('rain', 'Rain Collector', 'Auto-refills water.', 1500, self.buy_rain_collector),
        ]

        self.shop_buttons = {}
        for key, name, desc, cost, cmd in shop_items:
            f = tk.Frame(shop_inner, bg='#1a1a2e', bd=2, relief=tk.GROOVE)
            f.pack(fill=tk.X, padx=4, pady=2)
            btn = tk.Button(f, text=name + ' ($' + str(cost) + ')', font=('Arial', 9, 'bold'), bg='#3498DB', fg='white', command=cmd)
            btn.pack(fill=tk.X, padx=4, pady=(4,0))
            tk.Label(f, text=desc, font=('Arial', 8), bg='#1a1a2e', fg='#95A5A6', justify=tk.LEFT).pack(anchor=tk.W, padx=4, pady=(0,3))
            self.shop_buttons[key] = btn

        # --- Вкладка HELP ---
        help_f = self.tab_frames['help']
        help_text = "HOW TO PLAY" + chr(10) + chr(10)
        help_text += "Left Click = Plant / Harvest" + chr(10)
        help_text += "Right Click = Water (need Watering Can!)" + chr(10) + chr(10)
        help_text += "WEATHER SYSTEM:" + chr(10)
        help_text += "- SUNNY: Normal growth" + chr(10)
        help_text += "- RAIN: Auto-waters all plants" + chr(10)
        help_text += "- STORM: Risk of destroying plants!" + chr(10)
        help_text += "- SNOW: Plants stop growing" + chr(10)
        help_text += "- CLOUDY: Slower growth" + chr(10) + chr(10)
        help_text += "WATER SYSTEM:" + chr(10)
        help_text += "- Buy Watering Can first!" + chr(10)
        help_text += "- Each water costs 5 units" + chr(10)
        help_text += "- Water refills over time" + chr(10) + chr(10)
        help_text += "18 CROPS (1-12 min grow time)" + chr(10)
        help_text += "- Unlock by leveling up" + chr(10)
        help_text += "- Higher level = more profit" + chr(10) + chr(10)
        help_text += "CHEAT CODES:" + chr(10)
        help_text += "- money [amount]" + chr(10)
        help_text += "- level [amount]" + chr(10)
        help_text += "- water [amount]" + chr(10)
        help_text += "- weather [sunny/rain/storm/snow]" + chr(10)
        help_text += "- speed [multiplier]" + chr(10)
        help_text += "- unlockall" + chr(10)
        tk.Label(help_f, text=help_text, font=('Arial', 9), bg='#0f3460', fg='white', justify=tk.LEFT, wraplength=280).pack(padx=8, pady=8)

        # --- Лог ---
        self.log_text = tk.Text(right, height=6, width=38, font=('Courier', 9), state=tk.DISABLED, bg='#1a1a2e', fg='#2ECC71', wrap=tk.WORD)
        self.log_text.pack(fill=tk.X, padx=4, pady=4)

        # --- Консоль читов ---
        cheat_frame = tk.Frame(self.root, bg='#16213e', height=40)
        cheat_frame.pack(fill=tk.X, padx=8, pady=(0, 4))
        cheat_frame.pack_propagate(False)

        tk.Label(cheat_frame, text='CHEAT:', font=('Courier', 10, 'bold'), fg='#E74C3C', bg='#16213e').pack(side=tk.LEFT, padx=8, pady=8)
        self.cheat_entry = tk.Entry(cheat_frame, font=('Courier', 10), bg='#1a1a2e', fg='#2ECC71', insertbackground='#2ECC71')
        self.cheat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4, pady=6)
        self.cheat_entry.bind('<Return>', lambda e: self.execute_cheat())
        tk.Button(cheat_frame, text='EXECUTE', font=('Arial', 9, 'bold'), bg='#E74C3C', fg='white',
                 command=self.execute_cheat).pack(side=tk.RIGHT, padx=8, pady=6)

        self.log('Welcome to Farm Simulator - Realistic Edition!')
        self.log('Plants now take MINUTES to grow!')
        self.log('Buy a Watering Can to start!')

    # ===================== РЕАЛИСТИЧНЫЕ ГРЯДКИ (CANVAS) =====================

    def create_grid(self):
        for i in range(6):
            for j in range(6):
                frame = tk.Frame(self.grid_frame, width=110, height=110, bg='#3E2723', bd=2, relief=tk.SUNKEN)
                frame.grid(row=i, column=j, padx=3, pady=3)
                frame.grid_propagate(False)

                cv = tk.Canvas(frame, width=106, height=106, bg='#5D4037', highlightthickness=0)
                cv.pack(fill=tk.BOTH, expand=True)

                # Земля
                cv.create_rectangle(0, 0, 106, 106, fill='#6D4C41', outline='#4E342E', width=2)

                # Текстура земли (точки)
                for _ in range(8):
                    x, y = random.randint(10, 96), random.randint(10, 96)
                    cv.create_oval(x, y, x+3, y+3, fill='#5D4037', outline='')

                # Растение (центр)
                plant = cv.create_oval(40, 40, 66, 66, fill='', outline='')

                # Стебель
                stem = cv.create_line(53, 66, 53, 85, fill='', width=3)

                # Листья
                leaf1 = cv.create_polygon(53, 75, 40, 70, 45, 80, fill='', outline='')
                leaf2 = cv.create_polygon(53, 75, 66, 70, 61, 80, fill='', outline='')

                # Статус текст
                status = cv.create_text(53, 95, text='', font=('Arial', 8, 'bold'), fill='white')

                # Прогресс-бар фон
                cv.create_rectangle(8, 8, 98, 16, fill='#3E2723', outline='#5D4037', width=1)
                # Прогресс-бар
                progress_bar = cv.create_rectangle(8, 8, 8, 16, fill='#2ECC71', outline='')

                cv.bind('<Button-1>', lambda e, r=i, c=j: self.cell_click(r, c))
                cv.bind('<Button-3>', lambda e, r=i, c=j: self.cell_water(r, c))

                self.cell_canvases[i][j] = {
                    'canvas': cv,
                    'plant': plant,
                    'stem': stem,
                    'leaf1': leaf1,
                    'leaf2': leaf2,
                    'status': status,
                    'progress': progress_bar,
                    'frame': frame
                }
                self.cell_frames[i][j] = frame

                if i >= self.grid_size or j >= self.grid_size:
                    frame.grid_remove()

    def update_cell_visual(self, row, col):
        cell = self.farm[row][col]
        vis = self.cell_canvases[row][col]
        cv = vis['canvas']

        if row >= self.grid_size or col >= self.grid_size:
            vis['frame'].grid_remove()
            return
        else:
            vis['frame'].grid()

        if cell.stage == 'empty':
            cv.itemconfig(vis['plant'], fill='', outline='')
            cv.itemconfig(vis['stem'], fill='')
            cv.itemconfig(vis['leaf1'], fill='', outline='')
            cv.itemconfig(vis['leaf2'], fill='', outline='')
            cv.itemconfig(vis['status'], text='')
            cv.coords(vis['progress'], 8, 8, 8, 16)
            # Земля сухая/влажная
            soil = '#5D4037' if not cell.watered else '#3E2723'
            cv.create_rectangle(0, 0, 106, 106, fill=soil, outline='#4E342E', width=2)

        elif cell.stage == 'growing':
            crop = self.crops[cell.crop]
            progress = min(1.0, cell.progress)
            bar_width = int(90 * progress)

            # Стадии визуального роста
            if progress < 0.2:
                # Семя
                cv.itemconfig(vis['plant'], fill='#8D6E63', outline='#5D4037')
                cv.coords(vis['plant'], 50, 55, 56, 61)
                cv.itemconfig(vis['stem'], fill='')
                cv.itemconfig(vis['leaf1'], fill='', outline='')
                cv.itemconfig(vis['leaf2'], fill='', outline='')
            elif progress < 0.4:
                # Росток
                cv.itemconfig(vis['plant'], fill='#81C784', outline='#4CAF50')
                cv.coords(vis['plant'], 48, 45, 58, 55)
                cv.itemconfig(vis['stem'], fill='#66BB6A')
                cv.coords(vis['stem'], 53, 55, 53, 70)
                cv.itemconfig(vis['leaf1'], fill='#66BB6A', outline='#4CAF50')
                cv.coords(vis['leaf1'], 53, 65, 42, 60, 47, 72)
                cv.itemconfig(vis['leaf2'], fill='', outline='')
            elif progress < 0.7:
                # Куст
                cv.itemconfig(vis['plant'], fill='#4CAF50', outline='#388E3C')
                cv.coords(vis['plant'], 38, 35, 68, 60)
                cv.itemconfig(vis['stem'], fill='#388E3C')
                cv.coords(vis['stem'], 53, 60, 53, 78)
                cv.itemconfig(vis['leaf1'], fill='#66BB6A', outline='#4CAF50')
                cv.coords(vis['leaf1'], 53, 72, 38, 65, 45, 80)
                cv.itemconfig(vis['leaf2'], fill='#66BB6A', outline='#4CAF50')
                cv.coords(vis['leaf2'], 53, 72, 68, 65, 61, 80)
            else:
                # Цветение/плодообразование
                cv.itemconfig(vis['plant'], fill=crop.color, outline='#388E3C')
                cv.coords(vis['plant'], 40, 30, 66, 56)
                cv.itemconfig(vis['stem'], fill='#388E3C')
                cv.coords(vis['stem'], 53, 56, 53, 80)
                cv.itemconfig(vis['leaf1'], fill='#4CAF50', outline='#388E3C')
                cv.coords(vis['leaf1'], 53, 75, 35, 68, 42, 85)
                cv.itemconfig(vis['leaf2'], fill='#4CAF50', outline='#388E3C')
                cv.coords(vis['leaf2'], 53, 75, 71, 68, 64, 85)

            # Прогресс-бар
            cv.coords(vis['progress'], 8, 8, 8 + bar_width, 16)

            if cell.watered:
                cv.itemconfig(vis['progress'], fill='#2ECC71')
                mins_left = int((crop.grow_time - progress * crop.grow_time) / 60)
                if mins_left < 1:
                    cv.itemconfig(vis['status'], text='<1 min', fill='#2ECC71')
                else:
                    cv.itemconfig(vis['status'], text=str(mins_left) + ' min', fill='#2ECC71')
            else:
                cv.itemconfig(vis['progress'], fill='#E74C3C')
                cv.itemconfig(vis['status'], text='DRY!', fill='#E74C3C')

        elif cell.stage == 'ready':
            crop = self.crops[cell.crop]
            cv.itemconfig(vis['plant'], fill=crop.color, outline='#F1C40F')
            cv.coords(vis['plant'], 38, 28, 68, 58)
            cv.itemconfig(vis['stem'], fill='#388E3C')
            cv.coords(vis['stem'], 53, 58, 53, 82)
            cv.itemconfig(vis['leaf1'], fill='#4CAF50', outline='#388E3C')
            cv.coords(vis['leaf1'], 53, 78, 35, 70, 42, 88)
            cv.itemconfig(vis['leaf2'], fill='#4CAF50', outline='#388E3C')
            cv.coords(vis['leaf2'], 53, 78, 71, 70, 64, 88)
            cv.itemconfig(vis['status'], text='READY!', fill='#F1C40F')
            cv.coords(vis['progress'], 8, 8, 98, 16)
            cv.itemconfig(vis['progress'], fill='#F1C40F')

        elif cell.stage == 'withered':
            cv.itemconfig(vis['plant'], fill='#5D6D7E', outline='#34495E')
            cv.coords(vis['plant'], 40, 40, 66, 66)
            cv.itemconfig(vis['stem'], fill='#5D6D7E')
            cv.coords(vis['stem'], 53, 66, 53, 85)
            cv.itemconfig(vis['leaf1'], fill='', outline='')
            cv.itemconfig(vis['leaf2'], fill='', outline='')
            cv.itemconfig(vis['status'], text='DEAD', fill='#7F8C8D')
            cv.coords(vis['progress'], 8, 8, 98, 16)
            cv.itemconfig(vis['progress'], fill='#5D6D7E')

    # ===================== ПОГОДА =====================

    def update_weather(self):
        current_time = time.time()
        if current_time - self.weather.last_change > self.weather.change_interval:
            self.weather.last_change = current_time
            weather_types = ['sunny', 'rain', 'cloudy', 'storm', 'snow']
            weights = [40, 25, 20, 10, 5]
            self.weather.current = random.choices(weather_types, weights=weights)[0]

            w = self.weather.current
            self.weather_lbl.config(text='Weather: ' + self.weather.names[w], fg=self.weather.colors[w])

            if w == 'rain':
                self.log('It started raining! Plants are being watered!')
            elif w == 'storm':
                self.log('STORM! Some plants may be destroyed!')
            elif w == 'snow':
                self.log('Snowing! Plants stopped growing!')
            elif w == 'sunny':
                self.log('The sun is shining! Perfect for growing!')
            elif w == 'cloudy':
                self.log('Cloudy weather. Growth is slower.')

    def get_weather_growth_multiplier(self):
        w = self.weather.current
        if w == 'sunny':
            return 1.0
        elif w == 'rain':
            return 0.8
        elif w == 'cloudy':
            return 0.6
        elif w == 'snow':
            return 0.0
        elif w == 'storm':
            return 0.3
        return 1.0

    # ===================== ЧИТ-КОДЫ =====================

    def execute_cheat(self):
        cmd = self.cheat_entry.get().strip().lower()
        self.cheat_entry.delete(0, tk.END)

        if not cmd:
            return

        parts = cmd.split()
        action = parts[0]

        try:
            if action == 'money' and len(parts) > 1:
                self.money = int(parts[1])
                self.log('CHEAT: Money set to $' + str(self.money))
            elif action == 'level' and len(parts) > 1:
                self.level = int(parts[1])
                self.log('CHEAT: Level set to ' + str(self.level))
            elif action == 'water' and len(parts) > 1:
                self.water = int(parts[1])
                self.log('CHEAT: Water set to ' + str(self.water))
            elif action == 'speed' and len(parts) > 1:
                self.growth_speed = float(parts[1])
                self.log('CHEAT: Growth speed x' + str(self.growth_speed))
            elif action == 'weather' and len(parts) > 1:
                w = parts[1]
                if w in self.weather.names:
                    self.weather.current = w
                    self.weather_lbl.config(text='Weather: ' + self.weather.names[w], fg=self.weather.colors[w])
                    self.log('CHEAT: Weather set to ' + self.weather.names[w])
            elif action == 'unlockall':
                self.level = 99
                self.log('CHEAT: All crops unlocked!')
            elif action == 'maxwater':
                self.max_water = 999
                self.water = 999
                self.log('CHEAT: Max water set to 999')
            elif action == 'godmode':
                self.auto_water = True
                self.greenhouse = True
                self.auto_harvest = True
                self.growth_speed = 10.0
                self.log('CHEAT: GOD MODE ACTIVATED!')
            else:
                self.log('Unknown cheat: ' + cmd)
        except:
            self.log('Invalid cheat syntax: ' + cmd)

        self.update_stats()

    # ===================== ВКЛАДКИ =====================

    def switch_tab(self, name):
        self.tab_frames[self.current_tab].pack_forget()
        self.tab_buttons[self.current_tab].config(bg='#3498DB')
        self.current_tab = name
        self.tab_frames[name].pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.tab_buttons[name].config(bg='#27AE60')

    def select_crop(self):
        self.selected_crop = self.crop_var.get()

    # ===================== ИГРОВАЯ ЛОГИКА =====================

    def cell_click(self, row, col):
        cell = self.farm[row][col]

        if cell.stage == 'empty':
            crop = self.crops[self.selected_crop]
            if self.level < crop.unlock_level:
                messagebox.showwarning('Locked', 'Reach level ' + str(crop.unlock_level) + '!')
                return
            if self.money >= crop.seed_cost:
                self.money -= crop.seed_cost
                cell.crop = self.selected_crop
                cell.plant_time = time.time()
                cell.watered = True
                cell.stage = 'growing'
                cell.progress = 0.0
                self.log('Planted ' + crop.name + ' (-$' + str(crop.seed_cost) + ')')
                self.update_stats()
            else:
                messagebox.showwarning('No Money', 'Need $' + str(crop.seed_cost))

        elif cell.stage == 'ready':
            crop = self.crops[cell.crop]
            sell_price = int(crop.sell_price * self.price_bonus)
            self.money += sell_price
            xp_gain = int(sell_price / 5)
            self.xp += xp_gain

            self.log('Harvested ' + crop.name + ' (+$' + str(sell_price) + ', +' + str(xp_gain) + ' XP)')

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
            self.log('Cleared dead plant')

        self.update_cell_visual(row, col)

    def cell_water(self, row, col):
        if not self.has_watering_can:
            messagebox.showinfo('No Tool', 'Buy Watering Can in Shop!')
            return

        if self.watering_can_level >= 2:
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    ni, nj = row + di, col + dj
                    if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size:
                        self._water_single(ni, nj)
            self.log('Watered 3x3 at [' + str(row) + ',' + str(col) + ']')
        else:
            self._water_single(row, col)

    def _water_single(self, row, col):
        cell = self.farm[row][col]
        if cell.stage == 'growing' and self.water >= 5:
            self.water -= 5
            cell.watered = True
            self.update_cell_visual(row, col)
            self.update_stats()

    def game_loop(self):
        current_time = time.time()

        # Обновление погоды
        self.update_weather()

        weather_mult = self.get_weather_growth_multiplier()

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.farm[i][j]

                if cell.stage == 'growing':
                    crop = self.crops[cell.crop]

                    # Дождь автоматически поливает
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
                        # Засыхание
                        elapsed = current_time - cell.plant_time
                        if elapsed > 15 and cell.progress < 1.0:
                            cell.stage = 'withered'

                # Шторм уничтожает растения
                if self.weather.current == 'storm' and cell.stage in ['growing', 'ready']:
                    if random.random() < 0.001:  # 0.1% шанс в тик
                        cell.stage = 'withered'
                        self.log('STORM destroyed a ' + self.crops[cell.crop].name + '!')

                self.update_cell_visual(i, j)

        # Восстановление воды
        if not hasattr(self, 'last_refill'):
            self.last_refill = current_time

        interval = 3 if self.rain_collector else 8
        amount = 3 if self.rain_collector else 1

        # Дождь даёт больше воды
        if self.weather.current == 'rain':
            interval = 2
            amount = 5

        if current_time - self.last_refill > interval:
            self.last_refill = current_time
            self.water = min(self.max_water, self.water + amount)
            self.update_stats()

        self.root.after(500, self.game_loop)

    # ===================== СТАТЫ =====================

    def update_stats(self):
        self.money_lbl.config(text='Money: $' + str(self.money))
        self.level_lbl.config(text='Level: ' + str(self.level))
        self.xp_lbl.config(text='XP: ' + str(self.xp) + '/' + str(self.xp_to_next))
        self.water_lbl.config(text='Water: ' + str(self.water) + '/' + str(self.max_water))

        if not self.has_watering_can:
            self._set_shop('watering_can', 'Watering Can ($80)', False)
        elif self.watering_can_level == 1:
            self._set_shop('watering_can', 'Watering Can UPGRADE ($200)', False)
        else:
            self._set_shop('watering_can', 'Watering Can [MAX]', True)

        self._set_shop('auto_water', 'Auto-Water [ON]', self.auto_water, 'Auto-Water ($1200)')
        self._set_shop('growth_boost', 'Growth x' + str(self.growth_speed) + ' [MAX]' if self.growth_speed >= 2.5 else 'Growth Boost ($1500)', self.growth_speed >= 2.5)

        if self.grid_size >= 6:
            self._set_shop('expand', 'Field [MAX]', True)
        else:
            self._set_shop('expand', 'Expand Field ($' + str(500*self.grid_size) + ')', False)

        self._set_shop('greenhouse', 'Greenhouse [ON]', self.greenhouse, 'Greenhouse ($2000)')
        self._set_shop('auto_harvest', 'Auto-Harvest [ON]', self.auto_harvest, 'Auto-Harvest ($3000)')
        self._set_shop('pest', 'Pest Control [ON]', False, 'Pest Control ($800)')
        self._set_shop('marketing', 'Marketing +' + str(int((self.price_bonus-1)*100)) + '% [MAX]' if self.price_bonus >= 1.5 else 'Marketing ($1000)', self.price_bonus >= 1.5)
        self._set_shop('water_tank', 'Water Tank (+25) ($300)', False)
        self._set_shop('rain', 'Rain Collector [ON]', self.rain_collector, 'Rain Collector ($1500)')

        for crop_id, (rb, f) in self.crop_buttons.items():
            crop = self.crops[crop_id]
            if self.level >= crop.unlock_level:
                rb.config(state=tk.NORMAL, fg='white')

    def _set_shop(self, key, active_text, active, default_text=None):
        btn = self.shop_buttons.get(key)
        if not btn:
            return
        if active:
            btn.config(text=active_text, state=tk.DISABLED, bg='#27AE60')
        else:
            btn.config(text=default_text or active_text, state=tk.NORMAL, bg='#3498DB')

    # ===================== ПОКУПКИ =====================

    def buy_watering_can(self):
        if not self.has_watering_can:
            if self.money >= 80:
                self.money -= 80
                self.has_watering_can = True
                self.watering_can_level = 1
                self.log('Bought Watering Can! RMB to water.')
                self.update_stats()
            else:
                messagebox.showwarning('No Money', 'Need $80')
        elif self.watering_can_level == 1:
            if self.money >= 200:
                self.money -= 200
                self.watering_can_level = 2
                self.log('Advanced Watering Can! 3x3 area!')
                self.update_stats()
            else:
                messagebox.showwarning('No Money', 'Need $200')

    def buy_auto_water(self):
        if not self.auto_water and self.money >= 1200:
            self.money -= 1200
            self.auto_water = True
            self.log('Auto-Water ON!')
            self.update_stats()

    def buy_growth_boost(self):
        if self.growth_speed < 2.5 and self.money >= 1500:
            self.money -= 1500
            self.growth_speed += 0.5
            self.log('Growth x' + str(self.growth_speed) + '!')
            self.update_stats()

    def expand_farm(self):
        if self.grid_size < 6:
            cost = 500 * self.grid_size
            if self.money >= cost:
                self.money -= cost
                self.grid_size += 1
                self.log('Farm ' + str(self.grid_size) + 'x' + str(self.grid_size) + '!')
                self.update_stats()
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    self.cell_frames[i][j].grid()
                    self.update_cell_visual(i, j)

    def buy_greenhouse(self):
        if not self.greenhouse and self.money >= 2000:
            self.money -= 2000
            self.greenhouse = True
            self.log('Greenhouse ON!')
            self.update_stats()

    def buy_auto_harvest(self):
        if not self.auto_harvest and self.money >= 3000:
            self.money -= 3000
            self.auto_harvest = True
            self.log('Auto-Harvest ON!')
            self.update_stats()

    def buy_pest_control(self):
        if self.money >= 800:
            self.money -= 800
            self.log('Pest Control ON!')
            self.update_stats()

    def buy_marketing(self):
        if self.price_bonus < 1.5 and self.money >= 1000:
            self.money -= 1000
            self.price_bonus += 0.25
            self.log('Price bonus +' + str(int((self.price_bonus-1)*100)) + '%!')
            self.update_stats()

    def buy_water_tank(self):
        if self.money >= 300:
            self.money -= 300
            self.max_water += 25
            self.water = min(self.max_water, self.water + 25)
            self.log('Water max: ' + str(self.max_water))
            self.update_stats()

    def buy_rain_collector(self):
        if not self.rain_collector and self.money >= 1500:
            self.money -= 1500
            self.rain_collector = True
            self.log('Rain Collector ON!')
            self.update_stats()

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next
        self.xp_to_next = int(self.xp_to_next * 1.4)
        bonus = 50 * self.level
        self.money += bonus
        self.water = self.max_water
        self.log('LEVEL ' + str(self.level) + '! Bonus +$' + str(bonus) + '!')
        msg = 'Level ' + str(self.level) + '!' + chr(10) + 'Bonus: +$' + str(bonus) + chr(10) + 'New crops!'
        messagebox.showinfo('Level Up!', msg)

    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + chr(10))
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    game = FarmGame(root)
    root.mainloop()
