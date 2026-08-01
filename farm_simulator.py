import tkinter as tk
from tkinter import messagebox
import time

class Crop:
    def __init__(self, name, seed_cost, sell_price, grow_time, color, icon, unlock_level=1):
        self.name = name
        self.seed_cost = seed_cost
        self.sell_price = sell_price
        self.grow_time = grow_time
        self.color = color
        self.icon = icon
        self.unlock_level = unlock_level

class FarmCell:
    def __init__(self):
        self.crop = None
        self.plant_time = None
        self.watered = False
        self.stage = 'empty'
        self.progress = 0.0
        self.fertilized = False

class FarmGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Farm Simulator Deluxe")
        self.root.geometry("1050x750")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)
        self.money = 150
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
        self.crops = {
            'wheat': Crop('Wheat', 10, 25, 5, '#F4D03F', '[W]', 1),
            'carrot': Crop('Carrot', 20, 50, 8, '#E67E22', '[C]', 1),
            'potato': Crop('Potato', 35, 90, 12, '#D4AC0D', '[P]', 1),
            'tomato': Crop('Tomato', 60, 150, 18, '#E74C3C', '[T]', 2),
            'corn': Crop('Corn', 100, 280, 25, '#F39C12', '[N]', 2),
            'strawberry': Crop('Strawberry', 80, 200, 15, '#FF6B6B', '[S]', 2),
            'onion': Crop('Onion', 40, 110, 10, '#DDA0DD', '[O]', 3),
            'garlic': Crop('Garlic', 55, 140, 14, '#F5F5DC', '[G]', 3),
            'rice': Crop('Rice', 70, 180, 16, '#FFFFF0', '[R]', 3),
            'pepper': Crop('Pepper', 120, 320, 20, '#2ECC71', '[E]', 4),
            'cabbage': Crop('Cabbage', 90, 240, 22, '#82E0AA', '[B]', 4),
            'broccoli': Crop('Broccoli', 130, 350, 28, '#27AE60', '[L]', 4),
            'eggplant': Crop('Eggplant', 180, 480, 30, '#8E44AD', '[A]', 5),
            'watermelon': Crop('Watermelon', 150, 400, 35, '#2ECC71', '[M]', 5),
            'pumpkin': Crop('Pumpkin', 200, 550, 45, '#E67E22', '[K]', 5),
            'sunflower': Crop('Sunflower', 170, 450, 40, '#F1C40F', '[F]', 6),
            'pineapple': Crop('Pineapple', 250, 700, 50, '#F39C12', '[I]', 6),
            'grape': Crop('Grape', 300, 800, 60, '#9B59B6', '[V]', 7),
        }
        self.selected_crop = 'wheat'
        self.farm = [[FarmCell() for _ in range(6)] for _ in range(6)]
        self.cell_buttons = [[None for _ in range(6)] for _ in range(6)]
        self.setup_ui()
        self.game_loop()

    def setup_ui(self):
        top = tk.Frame(self.root, bg='#16213e', height=60)
        top.pack(fill=tk.X, padx=8, pady=4)
        top.pack_propagate(False)
        self.money_lbl = tk.Label(top, text='Money: 150', font=('Arial', 13, 'bold'), fg='#2ECC71', bg='#16213e')
        self.money_lbl.pack(side=tk.LEFT, padx=15, pady=12)
        self.level_lbl = tk.Label(top, text='Level: 1', font=('Arial', 13, 'bold'), fg='#F39C12', bg='#16213e')
        self.level_lbl.pack(side=tk.LEFT, padx=15, pady=12)
        self.xp_lbl = tk.Label(top, text='XP: 0/100', font=('Arial', 12), fg='#3498DB', bg='#16213e')
        self.xp_lbl.pack(side=tk.LEFT, padx=15, pady=12)
        self.water_lbl = tk.Label(top, text='Water: 50/50', font=('Arial', 12), fg='#5DADE2', bg='#16213e')
        self.water_lbl.pack(side=tk.LEFT, padx=15, pady=12)
        main = tk.Frame(self.root, bg='#1a1a2e')
        main.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        left = tk.Frame(main, bg='#5D4037', bd=3, relief=tk.RIDGE)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
        tk.Label(left, text='YOUR FARM', font=('Arial', 16, 'bold'), bg='#5D4037', fg='white').pack(pady=6)
        self.grid_frame = tk.Frame(left, bg='#5D4037')
        self.grid_frame.pack(padx=8, pady=8)
        self.create_grid()
        right = tk.Frame(main, width=320, bg='#0f3460')
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=4)
        right.pack_propagate(False)
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
            rb = tk.Radiobutton(f, text=crop.icon + ' ' + crop.name, variable=self.crop_var, value=crop_id,
                               font=('Arial', 10, 'bold'), bg='#1a1a2e', fg=fg_color, selectcolor='#0f3460', state=state,
                               command=lambda: self.select_crop())
            rb.pack(anchor=tk.W, padx=4, pady=1)
            info = 'Seed: $' + str(crop.seed_cost) + ' | Sell: $' + str(crop.sell_price) + ' | Time: ' + str(crop.grow_time) + 's'
            if locked:
                info = info + ' | LOCK Lv.' + str(crop.unlock_level)
            tk.Label(f, text=info, font=('Arial', 8), bg='#1a1a2e', fg='#95A5A6').pack(anchor=tk.W, padx=4, pady=(0,2))
            self.crop_buttons[crop_id] = (rb, f)
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
            ('watering_can', 'Watering Can', 'Buy to enable watering. Lv1: 1 cell. Lv2: 3x3 area.', 80, self.buy_watering_can),
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
        help_f = self.tab_frames['help']
        help_text = "HOW TO PLAY" + chr(10) + chr(10)
        help_text += "Left Click = Plant / Harvest" + chr(10)
        help_text += "Right Click = Water (need Watering Can!)" + chr(10) + chr(10)
        help_text += "WATER SYSTEM:" + chr(10)
        help_text += "- Buy Watering Can first!" + chr(10)
        help_text += "- Each water costs 5 units" + chr(10)
        help_text += "- Water refills over time" + chr(10)
        help_text += "- Buy upgrades for more water" + chr(10) + chr(10)
        help_text += "18 CROPS:" + chr(10)
        help_text += "- Unlock by leveling up" + chr(10)
        help_text += "- Higher level = more profit" + chr(10) + chr(10)
        help_text += "TIPS:" + chr(10)
        help_text += "- Plants dry out in 10s" + chr(10)
        help_text += "- Withered = no profit" + chr(10)
        help_text += "- Use upgrades wisely!" + chr(10) + chr(10)
        help_text += "Good luck, farmer!"
        tk.Label(help_f, text=help_text, font=('Arial', 10), bg='#0f3460', fg='white', justify=tk.LEFT, wraplength=280).pack(padx=8, pady=8)
        self.log_text = tk.Text(right, height=7, width=38, font=('Courier', 9), state=tk.DISABLED, bg='#1a1a2e', fg='#2ECC71', wrap=tk.WORD)
        self.log_text.pack(fill=tk.X, padx=4, pady=4)
        self.log('Welcome to Farm Simulator Deluxe!')
        self.log('Buy a Watering Can to start watering!')

    def switch_tab(self, name):
        self.tab_frames[self.current_tab].pack_forget()
        self.tab_buttons[self.current_tab].config(bg='#3498DB')
        self.current_tab = name
        self.tab_frames[name].pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.tab_buttons[name].config(bg='#27AE60')

    def create_grid(self):
        for i in range(6):
            for j in range(6):
                btn = tk.Button(self.grid_frame, width=10, height=5, font=('Arial', 9, 'bold'), bg='#6D4C41', fg='white',
                               relief=tk.RIDGE, bd=2, command=lambda r=i, c=j: self.cell_click(r, c))
                btn.bind('<Button-3>', lambda e, r=i, c=j: self.cell_water(r, c))
                btn.grid(row=i, column=j, padx=2, pady=2)
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
            btn.config(text='[EMPTY]', bg='#6D4C41', fg='white')
        elif cell.stage == 'growing':
            crop = self.crops[cell.crop]
            progress = min(100, int(cell.progress * 100))
            if progress < 30:
                icon = '(seed)'
            elif progress < 60:
                icon = '(grow)'
            else:
                icon = crop.icon
            if cell.watered:
                btn.config(text=icon + chr(10) + str(progress) + '%', bg='#27AE60', fg='white')
            else:
                btn.config(text=icon + chr(10) + 'DRY! ' + str(progress) + '%', bg='#D35400', fg='white')
        elif cell.stage == 'ready':
            crop = self.crops[cell.crop]
            btn.config(text=crop.icon + chr(10) + 'HARVEST!', bg=crop.color, fg='black')
        elif cell.stage == 'withered':
            btn.config(text='[DEAD]' + chr(10) + 'Clear', bg='#5D6D7E', fg='white')

    def select_crop(self):
        self.selected_crop = self.crop_var.get()

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
            cell.fertilized = False
            self.update_stats()
        elif cell.stage == 'withered':
            cell.stage = 'empty'
            cell.crop = None
            cell.watered = False
            cell.progress = 0
            self.log('Cleared dead plant')
        self.update_cell(row, col)

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
            self.update_cell(row, col)
            self.update_stats()

    def game_loop(self):
        current_time = time.time()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.farm[i][j]
                if cell.stage == 'growing':
                    crop = self.crops[cell.crop]
                    if self.auto_water or self.greenhouse:
                        cell.watered = True
                    if cell.watered:
                        elapsed = current_time - cell.plant_time
                        speed = self.growth_speed * (1.5 if cell.fertilized else 1.0)
                        cell.progress = min(1.0, elapsed / (crop.grow_time / speed))
                        if cell.progress >= 1.0:
                            cell.stage = 'ready'
                            if self.auto_harvest:
                                self.cell_click(i, j)
                    else:
                        elapsed = current_time - cell.plant_time
                        if elapsed > 10 and cell.progress < 1.0:
                            cell.stage = 'withered'
                self.update_cell(i, j)
        if not hasattr(self, 'last_refill'):
            self.last_refill = current_time
        interval = 3 if self.rain_collector else 5
        amount = 2 if self.rain_collector else 1
        if current_time - self.last_refill > interval:
            self.last_refill = current_time
            self.water = min(self.max_water, self.water + amount)
            self.update_stats()
        self.root.after(400, self.game_loop)

    def update_stats(self):
        self.money_lbl.config(text='Money: ' + str(self.money))
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
                    self.cell_buttons[i][j].grid()
                    self.update_cell(i, j)

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
