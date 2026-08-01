import tkinter as tk
from tkinter import messagebox, ttk
import time
import math

# ===================== КЛАССЫ =====================

class Crop:
    def __init__(self, name, seed_cost, sell_price, grow_time, color, emoji, unlock_level=1):
        self.name = name
        self.seed_cost = seed_cost
        self.sell_price = sell_price
        self.grow_time = grow_time
        self.color = color
        self.emoji = emoji
        self.unlock_level = unlock_level

class FarmCell:
    def __init__(self):
        self.crop = None
        self.plant_time = None
        self.watered = False
        self.stage = 'empty'  # empty, growing, ready, withered
        self.progress = 0.0
        self.fertilized = False
        self.pest_protected = False

class Upgrade:
    def __init__(self, name, description, cost, max_level, apply_func):
        self.name = name
        self.description = description
        self.cost = cost
        self.max_level = max_level
        self.level = 0
        self.apply_func = apply_func

# ===================== ИГРА =====================

class FarmGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Farm Simulator Deluxe")
        self.root.geometry("1100x800")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)

        # --- Ресурсы ---
        self.money = 150
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        self.water = 50
        self.max_water = 50
        self.grid_size = 3

        # --- Инструменты ---
        self.has_watering_can = False
        self.watering_can_level = 0  # 0=нет, 1=обычная, 2=улучшенная
        self.auto_water = False
        self.growth_speed = 1.0
        self.auto_harvest = False
        self.price_bonus = 1.0
        self.greenhouse = False
        self.pest_chance = 0.05

        # --- Растения (18 штук) ---
        self.crops = {
            'wheat':     Crop('Wheat',      10,  25,   5,  '#F4D03F', '🌾', 1),
            'carrot':    Crop('Carrot',     20,  50,   8,  '#E67E22', '🥕', 1),
            'potato':    Crop('Potato',     35,  90,   12, '#D4AC0D', '🥔', 1),
            'tomato':    Crop('Tomato',     60,  150,  18, '#E74C3C', '🍅', 2),
            'corn':      Crop('Corn',       100, 280,  25, '#F39C12', '🌽', 2),
            'strawberry':Crop('Strawberry', 80,  200,  15, '#FF6B6B', '🍓', 2),
            'onion':     Crop('Onion',      40,  110,  10, '#DDA0DD', '🧅', 3),
            'garlic':    Crop('Garlic',     55,  140,  14, '#F5F5DC', '🧄', 3),
            'rice':      Crop('Rice',       70,  180,  16, '#FFFFF0', '🍚', 3),
            'pepper':    Crop('Pepper',     120, 320,  20, '#2ECC71', '🫑', 4),
            'cabbage':   Crop('Cabbage',    90,  240,  22, '#82E0AA', '🥬', 4),
            'broccoli':  Crop('Broccoli',   130, 350,  28, '#27AE60', '🥦', 4),
            'eggplant':  Crop('Eggplant',   180, 480,  30, '#8E44AD', '🍆', 5),
            'watermelon':Crop('Watermelon', 150, 400,  35, '#2ECC71', '🍉', 5),
            'pumpkin':   Crop('Pumpkin',    200, 550,  45, '#E67E22', '🎃', 5),
            'sunflower': Crop('Sunflower',  170, 450,  40, '#F1C40F', '🌻', 6),
            'pineapple': Crop('Pineapple',  250, 700,  50, '#F39C12', '🍍', 6),
            'grape':     Crop('Grape',      300, 800,  60, '#9B59B6', '🍇', 7),
        }

        self.selected_crop = 'wheat'
        self.farm = [[FarmCell() for _ in range(6)] for _ in range(6)]
        self.cell_canvases = [[None for _ in range(6)] for _ in range(6)]
        self.cell_frames = [[None for _ in range(6)] for _ in range(6)]

        self.setup_ui()
        self.game_loop()

    # ===================== UI =====================

    def setup_ui(self):
        # --- Верхняя панель статов ---
        top_frame = tk.Frame(self.root, bg='#16213e', height=70)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        top_frame.pack_propagate(False)

        stats = [
            ('💰', 'money', f'Money: {self.money}', '#2ECC71'),
            ('⭐', 'level', f'Level: {self.level}', '#F39C12'),
            ('📈', 'xp', f'XP: {self.xp}/{self.xp_to_next}', '#3498DB'),
            ('💧', 'water', f'Water: {self.water}/{self.max_water}', '#5DADE2'),
        ]

        self.stat_labels = {}
        for emoji, key, text, color in stats:
            lbl = tk.Label(top_frame, text=f'{emoji} {text}', font=('Arial', 13, 'bold'),
                          fg=color, bg='#16213e')
            lbl.pack(side=tk.LEFT, padx=20, pady=15)
            self.stat_labels[key] = lbl

        # --- Основная область ---
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # --- Левая часть: Поле ---
        left_frame = tk.Frame(main_frame, bg='#5D4037', bd=4, relief=tk.RIDGE)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(left_frame, text='🚜 YOUR FARM', font=('Arial', 18, 'bold'),
                bg='#5D4037', fg='white').pack(pady=8)

        self.grid_container = tk.Frame(left_frame, bg='#5D4037')
        self.grid_container.pack(padx=10, pady=10)

        self.create_grid()

        # --- Правая часть: Панели ---
        right_frame = tk.Frame(main_frame, width=340, bg='#0f3460')
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        right_frame.pack_propagate(False)

        # Вкладки
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Стиль вкладок
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#0f3460', tabmargins=[2, 5, 2, 0])
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[10, 5])

        # --- Вкладка: Растения ---
        crops_tab = tk.Frame(self.notebook, bg='#0f3460')
        self.notebook.add(crops_tab, text='🌱 Crops')

        canvas = tk.Canvas(crops_tab, bg='#0f3460', highlightthickness=0)
        scrollbar = ttk.Scrollbar(crops_tab, orient=tk.VERTICAL, command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg='#0f3460')

        scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.crop_var = tk.StringVar(value='wheat')
        self.crop_buttons = {}

        for crop_id, crop in self.crops.items():
            frame = tk.Frame(scroll_frame, bg='#1a1a2e', bd=2, relief=tk.GROOVE)
            frame.pack(fill=tk.X, padx=5, pady=3)

            locked = self.level < crop.unlock_level
            state = tk.DISABLED if locked else tk.NORMAL

            btn = tk.Radiobutton(frame, text=f"{crop.emoji} {crop.name}",
                                variable=self.crop_var, value=crop_id,
                                font=('Arial', 11, 'bold'), bg='#1a1a2e',
                                fg='#7F8C8D' if locked else 'white',
                                selectcolor='#0f3460', state=state,
                                command=lambda: self.select_crop())
            btn.pack(anchor=tk.W, padx=5, pady=2)

            info = f"Cost: ${crop.seed_cost} | Sell: ${crop.sell_price} | Time: {crop.grow_time}s"
            if locked:
                info += f" | 🔒 Lv.{crop.unlock_level}"

            tk.Label(frame, text=info, font=('Arial', 9),
                    bg='#1a1a2e', fg='#95A5A6').pack(anchor=tk.W, padx=5, pady=(0,3))
            self.crop_buttons[crop_id] = (btn, frame)

        # --- Вкладка: Магазин ---
        shop_tab = tk.Frame(self.notebook, bg='#0f3460')
        self.notebook.add(shop_tab, text='🏪 Shop')

        shop_items = [
            ('💧 Watering Can', 'Buy to enable watering\nLevel 1: 1 cell | Level 2: 3x3 area',
             80, self.buy_watering_can),
            ('🚿 Auto-Water', 'Plants never dry out', 1200, self.buy_auto_water),
            ('⚡ Growth Boost', 'Plants grow 50% faster', 1500, self.buy_growth_boost),
            ('📐 Expand Field', f'Increase farm size\nCurrent: {self.grid_size}x{self.grid_size}',
             500, self.expand_farm),
            ('🏠 Greenhouse', 'Plants never wither', 2000, self.buy_greenhouse),
            ('🤖 Auto-Harvest', 'Automatically harvest ready crops', 3000, self.buy_auto_harvest),
            ('🛡️ Pest Control', 'Protects from pests', 800, self.buy_pest_control),
            ('📢 Marketing', '+25% sell price', 1000, self.buy_marketing),
            ('🚰 Water Tank', '+25 max water capacity', 300, self.buy_water_tank),
            ('🌧️ Rain Collector', 'Auto-refills water over time', 1500, self.buy_rain_collector),
        ]

        self.shop_buttons = {}
        for emoji_name, desc, cost, cmd in shop_items:
            frame = tk.Frame(shop_tab, bg='#1a1a2e', bd=2, relief=tk.GROOVE)
            frame.pack(fill=tk.X, padx=5, pady=3)

            name = emoji_name.split(' ', 1)[1] if ' ' in emoji_name else emoji_name
            btn = tk.Button(frame, text=f'{emoji_name} (${cost})',
                           font=('Arial', 10, 'bold'), bg='#3498DB', fg='white',
                           command=cmd)
            btn.pack(fill=tk.X, padx=5, pady=(5,0))

            tk.Label(frame, text=desc, font=('Arial', 9),
                    bg='#1a1a2e', fg='#95A5A6', justify=tk.LEFT).pack(anchor=tk.W, padx=5, pady=(0,5))

            self.shop_buttons[name.lower().replace(' ', '_')] = btn

        # --- Вкладка: Инфо ---
        info_tab = tk.Frame(self.notebook, bg='#0f3460')
        self.notebook.add(info_tab, text='ℹ️ Help')

        help_text = """🎮 HOW TO PLAY

🖱️ Left Click — Plant seeds / Harvest
🖱️ Right Click — Water plant (need Watering Can!)

💧 Water System:
• Buy Watering Can first!
• Each water costs 5 water units
• Water refills over time
• Buy upgrades to get more water

🌱 18 Different Crops:
• Unlock new crops by leveling up
• Higher level = better profit

⚠️ Tips:
• Plants dry out in 10s without water
• Withered plants give nothing
• Use upgrades wisely!

Good luck, farmer! 🚜"""

        tk.Label(info_tab, text=help_text, font=('Arial', 11),
                bg='#0f3460', fg='white', justify=tk.LEFT,
                wraplength=300).pack(padx=10, pady=10)

        # --- Лог ---
        self.log_text = tk.Text(right_frame, height=8, width=40,
                               font=('Consolas', 9), state=tk.DISABLED,
                               bg='#1a1a2e', fg='#2ECC71',
                               wrap=tk.WORD)
        self.log_text.pack(fill=tk.X, padx=5, pady=5)

        self.log('🌾 Welcome to Farm Simulator Deluxe!')
        self.log('💡 Buy a Watering Can to start watering!')

    # ===================== СОЗДАНИЕ ПОЛЯ (БЕЗ МЕРЦАНИЯ) =====================

    def create_grid(self):
        """Создаём грядки ОДИН РАЗ — никакого мерцания!"""
        for i in range(6):
            for j in range(6):
                frame = tk.Frame(self.grid_container, width=90, height=90,
                                bg='#3E2723', bd=2, relief=tk.SUNKEN)
                frame.grid(row=i, column=j, padx=2, pady=2)
                frame.grid_propagate(False)

                # Canvas для рисования
                cv = tk.Canvas(frame, width=86, height=86,
                              bg='#5D4037', highlightthickness=0)
                cv.pack(fill=tk.BOTH, expand=True)

                # Земля (фон)
                cv.create_rectangle(2, 2, 84, 84, fill='#6D4C41', outline='#4E342E', width=2)

                # Текст растения
                plant_text = cv.create_text(43, 35, text='', font=('Arial', 24))

                # Прогресс-бар фон
                cv.create_rectangle(8, 68, 78, 78, fill='#3E2723', outline='#5D4037', width=1)
                # Прогресс-бар заполнение
                progress_bar = cv.create_rectangle(8, 68, 8, 78, fill='#2ECC71', outline='')

                # Текст статуса
                status_text = cv.create_text(43, 55, text='', font=('Arial', 8), fill='white')

                # Клики
                cv.bind('<Button-1>', lambda e, r=i, c=j: self.cell_click(r, c))
                cv.bind('<Button-3>', lambda e, r=i, c=j: self.cell_water(r, c))

                self.cell_canvases[i][j] = {
                    'canvas': cv,
                    'plant': plant_text,
                    'progress': progress_bar,
                    'status': status_text,
                    'frame': frame
                }
                self.cell_frames[i][j] = frame

                # Скрываем клетки за пределами grid_size
                if i >= self.grid_size or j >= self.grid_size:
                    frame.grid_remove()

    def update_cell_visual(self, row, col):
        """Обновляем ВИЗУАЛ одной клетки (без пересоздания!)"""
        cell = self.farm[row][col]
        vis = self.cell_canvases[row][col]
        cv = vis['canvas']

        if row >= self.grid_size or col >= self.grid_size:
            vis['frame'].grid_remove()
            return
        else:
            vis['frame'].grid()

        if cell.stage == 'empty':
            cv.itemconfig(vis['plant'], text='')
            cv.itemconfig(vis['status'], text='')
            cv.coords(vis['progress'], 8, 68, 8, 78)
            cv.itemconfig(vis['progress'], fill='#2ECC71')
            # Земля сухая/влажная
            soil_color = '#5D4037' if not cell.watered else '#3E2723'
            cv.create_rectangle(2, 2, 84, 84, fill=soil_color, outline='#4E342E', width=2)

        elif cell.stage == 'growing':
            crop = self.crops[cell.crop]
            progress = min(1.0, cell.progress)
            bar_width = int(70 * progress)

            # Эмодзи меняется по стадиям роста
            if progress < 0.3:
                emoji = '🌱'
            elif progress < 0.6:
                emoji = '🌿'
            elif progress < 0.9:
                emoji = crop.emoji
            else:
                emoji = crop.emoji

            cv.itemconfig(vis['plant'], text=emoji)

            if cell.watered:
                cv.itemconfig(vis['status'], text=f'{int(progress*100)}%', fill='#82E0AA')
                cv.coords(vis['progress'], 8, 68, 8 + bar_width, 78)
                cv.itemconfig(vis['progress'], fill='#2ECC71')
            else:
                cv.itemconfig(vis['status'], text='NEEDS WATER!', fill='#E74C3C')
                cv.coords(vis['progress'], 8, 68, 8 + bar_width, 78)
                cv.itemconfig(vis['progress'], fill='#F39C12')

        elif cell.stage == 'ready':
            crop = self.crops[cell.crop]
            cv.itemconfig(vis['plant'], text=crop.emoji)
            cv.itemconfig(vis['status'], text='HARVEST!', fill='#F1C40F')
            cv.coords(vis['progress'], 8, 68, 78, 78)
            cv.itemconfig(vis['progress'], fill='#F1C40F')

        elif cell.stage == 'withered':
            cv.itemconfig(vis['plant'], text='🥀')
            cv.itemconfig(vis['status'], text='DEAD', fill='#7F8C8D')
            cv.coords(vis['progress'], 8, 68, 78, 78)
            cv.itemconfig(vis['progress'], fill='#5D6D7E')

    # ===================== ИГРОВАЯ ЛОГИКА =====================

    def select_crop(self):
        self.selected_crop = self.crop_var.get()

    def cell_click(self, row, col):
        cell = self.farm[row][col]

        if cell.stage == 'empty':
            crop = self.crops[self.selected_crop]
            if self.level < crop.unlock_level:
                messagebox.showwarning('Locked', f'Reach level {crop.unlock_level} to unlock {crop.name}!')
                return
            if self.money >= crop.seed_cost:
                self.money -= crop.seed_cost
                cell.crop = self.selected_crop
                cell.plant_time = time.time()
                cell.watered = True
                cell.stage = 'growing'
                cell.progress = 0.0
                self.log(f'🌱 Planted {crop.name} (-${crop.seed_cost})')
                self.update_stats()
            else:
                messagebox.showwarning('No Money', f'Need ${crop.seed_cost} for {crop.name}')

        elif cell.stage == 'ready':
            crop = self.crops[cell.crop]
            sell_price = int(crop.sell_price * self.price_bonus)
            self.money += sell_price
            xp_gain = int(sell_price / 5)
            self.xp += xp_gain

            self.log(f'🌾 Harvested {crop.name} (+${sell_price}, +{xp_gain} XP)')

            if self.xp >= self.xp_to_next:
                self.level_up()

            cell.stage = 'empty'
            cell.crop = None
            cell.watered = False
            cell.progress = 0
            cell.fertilized = False
            self.update_stats()

        elif cell.stage == 'withered':
            cell.stage = 'empty'
            cell.crop = None
            cell.watered = False
            cell.progress = 0
            self.log('🥀 Cleared dead plant')

        self.update_cell_visual(row, col)

    def cell_water(self, row, col):
        if not self.has_watering_can:
            messagebox.showinfo('No Tool', 'Buy a Watering Can in the Shop first!')
            return

        cell = self.farm[row][col]

        if self.watering_can_level >= 2:
            # Поливаем 3x3 область
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    ni, nj = row + di, col + dj
                    if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size:
                        self._water_single(ni, nj)
            self.log(f'💧 Watered 3x3 area around [{row},{col}]')
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

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.farm[i][j]

                if cell.stage == 'growing':
                    crop = self.crops[cell.crop]

                    # Автополив
                    if self.auto_water or self.greenhouse:
                        cell.watered = True

                    # Рост
                    if cell.watered:
                        elapsed = current_time - cell.plant_time
                        speed = self.growth_speed * (1.5 if cell.fertilized else 1.0)
                        cell.progress = min(1.0, elapsed / (crop.grow_time / speed))

                        if cell.progress >= 1.0:
                            cell.stage = 'ready'
                            if self.auto_harvest:
                                self.cell_click(i, j)
                    else:
                        # Засыхание
                        elapsed = current_time - cell.plant_time
                        if elapsed > 10 and cell.progress < 1.0:
                            cell.stage = 'withered'

                # Вредители (если нет защиты)
                if cell.stage == 'growing' and not cell.pest_protected:
                    if not hasattr(cell, 'last_pest_check'):
                        cell.last_pest_check = current_time
                    if current_time - cell.last_pest_check > 5:
                        cell.last_pest_check = current_time
                        # Вредители замедляют рост
                        pass

                self.update_cell_visual(i, j)

        # Восстановление воды
        if hasattr(self, 'rain_collector') and self.rain_collector:
            if not hasattr(self, 'last_water_refill'):
                self.last_water_refill = current_time
            if current_time - self.last_water_refill > 3:
                self.last_water_refill = current_time
                self.water = min(self.max_water, self.water + 2)
                self.update_stats()
        else:
            if not hasattr(self, 'last_water_refill'):
                self.last_water_refill = current_time
            if current_time - self.last_water_refill > 5:
                self.last_water_refill = current_time
                self.water = min(self.max_water, self.water + 1)
                self.update_stats()

        self.root.after(300, self.game_loop)

    # ===================== СТАТЫ =====================

    def update_stats(self):
        self.stat_labels['money'].config(text=f'💰 Money: {self.money}')
        self.stat_labels['level'].config(text=f'⭐ Level: {self.level}')
        self.stat_labels['xp'].config(text=f'📈 XP: {self.xp}/{self.xp_to_next}')
        self.stat_labels['water'].config(text=f'💧 Water: {self.water}/{self.max_water}')

        # Обновляем кнопки магазина
        self._update_shop_button('watering_can', self.has_watering_can,
                                '💧 Watering Can Lv.2 (${200})' if self.watering_can_level == 1 else
                                '💧 Watering Can (${80})' if not self.has_watering_can else
                                '💧 Watering Can [MAX]')

        self._update_shop_button('auto-water', self.auto_water,
                                '🚿 Auto-Water (${1200})', 'Auto-Water [ACTIVE]')

        self._update_shop_button('growth_boost', self.growth_speed >= 2.5,
                                f'⚡ Growth Boost (${1500})', 'Growth Boost [MAX]')

        self._update_shop_button('expand_field', self.grid_size >= 6,
                                f'📐 Expand Field (${500 * self.grid_size})', 'Max Size Reached')

        self._update_shop_button('greenhouse', self.greenhouse,
                                '🏠 Greenhouse (${2000})', 'Greenhouse [ACTIVE]')

        self._update_shop_button('auto-harvest', self.auto_harvest,
                                '🤖 Auto-Harvest (${3000})', 'Auto-Harvest [ACTIVE]')

        self._update_shop_button('pest_control', self.pest_chance <= 0,
                                '🛡️ Pest Control (${800})', 'Pest Control [ACTIVE]')

        self._update_shop_button('marketing', self.price_bonus >= 1.5,
                                '📢 Marketing (${1000})', 'Marketing [MAX]')

        self._update_shop_button('water_tank', False,
                                f'🚰 Water Tank (+25) (${300})')

        self._update_shop_button('rain_collector', getattr(self, 'rain_collector', False),
                                '🌧️ Rain Collector (${1500})', 'Rain Collector [ACTIVE]')

        # Обновляем кнопки растений (разблокировка)
        for crop_id, (btn, frame) in self.crop_buttons.items():
            crop = self.crops[crop_id]
            if self.level >= crop.unlock_level:
                btn.config(state=tk.NORMAL, fg='white')

    def _update_shop_button(self, key, active_or_max, default_text, active_text=None):
        btn = self.shop_buttons.get(key)
        if not btn:
            return
        if active_or_max:
            btn.config(text=active_text or default_text, state=tk.DISABLED, bg='#27AE60')
        else:
            btn.config(text=default_text, state=tk.NORMAL, bg='#3498DB')

    # ===================== УЛУЧШЕНИЯ =====================

    def buy_watering_can(self):
        if not self.has_watering_can:
            if self.money >= 80:
                self.money -= 80
                self.has_watering_can = True
                self.watering_can_level = 1
                self.log('💧 Bought Watering Can! Right-click to water.')
                self.update_stats()
            else:
                messagebox.showwarning('No Money', 'Need $80 for Watering Can')
        elif self.watering_can_level == 1:
            if self.money >= 200:
                self.money -= 200
                self.watering_can_level = 2
                self.log('💧 Upgraded to Advanced Watering Can! Now waters 3x3 area!')
                self.update_stats()
            else:
                messagebox.showwarning('No Money', 'Need $200 for upgrade')

    def buy_auto_water(self):
        if not self.auto_water and self.money >= 1200:
            self.money -= 1200
            self.auto_water = True
            self.log('🚿 Auto-Water activated!')
            self.update_stats()

    def buy_growth_boost(self):
        if self.growth_speed < 2.5 and self.money >= 1500:
            self.money -= 1500
            self.growth_speed += 0.5
            self.log(f'⚡ Growth speed now x{self.growth_speed}!')
            self.update_stats()

    def expand_farm(self):
        if self.grid_size < 6:
            cost = 500 * self.grid_size
            if self.money >= cost:
                self.money -= cost
                self.grid_size += 1
                self.log(f'📐 Farm expanded to {self.grid_size}x{self.grid_size}!')
                self.update_stats()
                # Показываем новые клетки
                for i in range(self.grid_size):
                    for j in range(self.grid_size):
                        self.cell_frames[i][j].grid()
                        self.update_cell_visual(i, j)

    def buy_greenhouse(self):
        if not self.greenhouse and self.money >= 2000:
            self.money -= 2000
            self.greenhouse = True
            self.log('🏠 Greenhouse built! Plants never wither!')
            self.update_stats()

    def buy_auto_harvest(self):
        if not self.auto_harvest and self.money >= 3000:
            self.money -= 3000
            self.auto_harvest = True
            self.log('🤖 Auto-Harvest activated!')
            self.update_stats()

    def buy_pest_control(self):
        if self.pest_chance > 0 and self.money >= 800:
            self.money -= 800
            self.pest_chance = 0
            self.log('🛡️ Pest Control activated!')
            self.update_stats()

    def buy_marketing(self):
        if self.price_bonus < 1.5 and self.money >= 1000:
            self.money -= 1000
            self.price_bonus += 0.25
            self.log(f'📢 Sell price bonus: +{int((self.price_bonus-1)*100)}%!')
            self.update_stats()

    def buy_water_tank(self):
        if self.money >= 300:
            self.money -= 300
            self.max_water += 25
            self.water = min(self.max_water, self.water + 25)
            self.log(f'🚰 Water tank upgraded! Max: {self.max_water}')
            self.update_stats()

    def buy_rain_collector(self):
        if not getattr(self, 'rain_collector', False) and self.money >= 1500:
            self.money -= 1500
            self.rain_collector = True
            self.log('🌧️ Rain Collector installed! Auto water refill!')
            self.update_stats()

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next
        self.xp_to_next = int(self.xp_to_next * 1.4)
        bonus = 50 * self.level
        self.money += bonus
        self.water = self.max_water
        self.log(f'🎉 LEVEL UP! Now level {self.level}! Bonus: +${bonus}, water refilled!')
        messagebox.showinfo('Level Up!', f'You reached level {self.level}!\nBonus: +${bonus}\nNew crops unlocked!')

    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    game = FarmGame(root)
    root.mainloop()
