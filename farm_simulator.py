import tkinter as tk
from tkinter import messagebox
import time

class Crop:
    def __init__(self, name, seed_cost, sell_price, grow_time, color):
        self.name = name
        self.seed_cost = seed_cost
        self.sell_price = sell_price
        self.grow_time = grow_time
        self.color = color

class FarmCell:
    def __init__(self):
        self.crop = None
        self.plant_time = None
        self.watered = False
        self.stage = 'empty'
        self.progress = 0

class FarmGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Farm Simulator")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        self.money = 100
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        self.grid_size = 3
        self.auto_water = False
        self.growth_speed = 1.0

        self.crops = {
            'wheat': Crop('Wheat', 10, 25, 5, '#F4D03F'),
            'carrot': Crop('Carrot', 25, 60, 10, '#E67E22'),
            'potato': Crop('Potato', 50, 120, 15, '#D4AC0D'),
            'tomato': Crop('Tomato', 100, 250, 20, '#E74C3C')
        }

        self.selected_crop = 'wheat'
        self.farm = [[FarmCell() for _ in range(5)] for _ in range(5)]
        self.cell_buttons = [[None for _ in range(5)] for _ in range(5)]

        self.setup_ui()
        self.game_loop()

    def setup_ui(self):
        stats_frame = tk.Frame(self.root, bg='#2C3E50', height=60)
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        stats_frame.pack_propagate(False)

        self.money_label = tk.Label(stats_frame, text=f'Money: {self.money}', 
                                   font=('Arial', 14, 'bold'), fg='#2ECC71', bg='#2C3E50')
        self.money_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.level_label = tk.Label(stats_frame, text=f'Level: {self.level}', 
                                   font=('Arial', 14, 'bold'), fg='#F39C12', bg='#2C3E50')
        self.level_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.xp_label = tk.Label(stats_frame, text=f'XP: {self.xp}/{self.xp_to_next}', 
                                font=('Arial', 12), fg='#3498DB', bg='#2C3E50')
        self.xp_label.pack(side=tk.LEFT, padx=20, pady=10)

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        farm_frame = tk.Frame(main_frame, bg='#8B4513', bd=3, relief=tk.RIDGE)
        farm_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(farm_frame, text='Your Farm', font=('Arial', 16, 'bold'), 
                bg='#8B4513', fg='white').pack(pady=5)

        self.grid_frame = tk.Frame(farm_frame, bg='#8B4513')
        self.grid_frame.pack(padx=10, pady=10)

        self.update_grid()

        right_frame = tk.Frame(main_frame, width=280, bg='#ECF0F1')
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        right_frame.pack_propagate(False)

        crop_frame = tk.LabelFrame(right_frame, text='Select Crop', 
                                  font=('Arial', 12, 'bold'), bg='#ECF0F1')
        crop_frame.pack(fill=tk.X, padx=5, pady=5)

        self.crop_var = tk.StringVar(value='wheat')
        for crop_id, crop in self.crops.items():
            rb = tk.Radiobutton(crop_frame, text=f'{crop.name} (${crop.seed_cost})', 
                               variable=self.crop_var, value=crop_id,
                               font=('Arial', 10), bg='#ECF0F1',
                               command=lambda: self.select_crop())
            rb.pack(anchor=tk.W, padx=5, pady=2)

        shop_frame = tk.LabelFrame(right_frame, text='Shop', 
                                  font=('Arial', 12, 'bold'), bg='#ECF0F1')
        shop_frame.pack(fill=tk.X, padx=5, pady=5)

        self.upgrade_buttons = []

        btn_expand = tk.Button(shop_frame, text='Expand Field ($500)', 
                              font=('Arial', 10), command=self.expand_farm,
                              bg='#3498DB', fg='white')
        btn_expand.pack(fill=tk.X, padx=5, pady=3)
        self.upgrade_buttons.append(('expand', btn_expand))

        btn_water = tk.Button(shop_frame, text='Auto-Water ($1000)', 
                             font=('Arial', 10), command=self.buy_auto_water,
                             bg='#3498DB', fg='white')
        btn_water.pack(fill=tk.X, padx=5, pady=3)
        self.upgrade_buttons.append(('water', btn_water))

        btn_speed = tk.Button(shop_frame, text='Growth Speed ($1500)', 
                             font=('Arial', 10), command=self.buy_speed,
                             bg='#3498DB', fg='white')
        btn_speed.pack(fill=tk.X, padx=5, pady=3)
        self.upgrade_buttons.append(('speed', btn_speed))

        info_frame = tk.LabelFrame(right_frame, text='How to Play', 
                                  font=('Arial', 12, 'bold'), bg='#ECF0F1')
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        info_text = """Controls:

LMB - Plant / Harvest
RMB - Water plant

Watch the water!
Plants without water
wither in 10 sec.

Sell crops to earn
money and XP."""

        self.info_label = tk.Label(info_frame, text=info_text, 
                                  font=('Arial', 10), bg='#ECF0F1', 
                                  justify=tk.LEFT, wraplength=250)
        self.info_label.pack(padx=5, pady=5)

        self.log_text = tk.Text(right_frame, height=6, width=30, 
                               font=('Arial', 9), state=tk.DISABLED,
                               bg='#2C3E50', fg='#2ECC71')
        self.log_text.pack(fill=tk.X, padx=5, pady=5)

    def select_crop(self):
        self.selected_crop = self.crop_var.get()

    def update_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.farm[i][j]
                btn = tk.Button(self.grid_frame, width=8, height=4,
                               font=('Arial', 10, 'bold'),
                               command=lambda r=i, c=j: self.cell_click(r, c))
                btn.bind('<Button-3>', lambda e, r=i, c=j: self.water_cell(r, c))

                self.update_cell_button(btn, cell)
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.cell_buttons[i][j] = btn

    def update_cell_button(self, btn, cell):
        if cell.stage == 'empty':
            btn.config(text='[EMPTY]', bg='#D4A373', state=tk.NORMAL)
        elif cell.stage == 'growing':
            progress = min(100, int(cell.progress * 100))
            if cell.watered:
                btn.config(text=f'GROW\n{progress}%', bg='#82E0AA')
            else:
                btn.config(text=f'GROW\n{progress}%', bg='#F5B041')
        elif cell.stage == 'ready':
            btn.config(text='HARVEST!\nClick', bg=self.crops[cell.crop].color)
        elif cell.stage == 'withered':
            btn.config(text='WITHERED\nClear', bg='#5D6D7E')

    def cell_click(self, row, col):
        cell = self.farm[row][col]

        if cell.stage == 'empty':
            crop = self.crops[self.selected_crop]
            if self.money >= crop.seed_cost:
                self.money -= crop.seed_cost
                cell.crop = self.selected_crop
                cell.plant_time = time.time()
                cell.watered = True
                cell.stage = 'growing'
                cell.progress = 0
                self.log(f'Planted: {crop.name} (-${crop.seed_cost})')
                self.update_stats()
            else:
                messagebox.showwarning('Not enough money', 
                                     f'Need ${crop.seed_cost} for {crop.name}')

        elif cell.stage == 'ready':
            crop = self.crops[cell.crop]
            self.money += crop.sell_price
            xp_gain = int(crop.sell_price / 5)
            self.xp += xp_gain

            self.log(f'Harvested: {crop.name} (+${crop.sell_price}, +{xp_gain} XP)')

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
            self.log('Withered plant removed')

        self.update_grid()

    def water_cell(self, row, col):
        cell = self.farm[row][col]
        if cell.stage == 'growing':
            cell.watered = True
            self.log(f'Watered: [{row},{col}]')
            self.update_grid()

    def game_loop(self):
        current_time = time.time()

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.farm[i][j]

                if cell.stage == 'growing':
                    crop = self.crops[cell.crop]

                    if self.auto_water:
                        cell.watered = True

                    if cell.watered:
                        elapsed = current_time - cell.plant_time
                        cell.progress = min(1.0, elapsed / (crop.grow_time / self.growth_speed))

                        if cell.progress >= 1.0:
                            cell.stage = 'ready'
                    else:
                        elapsed = current_time - cell.plant_time
                        if elapsed > 10 and cell.progress < 1.0:
                            cell.stage = 'withered'

        self.update_grid()
        self.root.after(500, self.game_loop)

    def update_stats(self):
        self.money_label.config(text=f'Money: {self.money}')
        self.level_label.config(text=f'Level: {self.level}')
        self.xp_label.config(text=f'XP: {self.xp}/{self.xp_to_next}')

        for upgrade_type, btn in self.upgrade_buttons:
            if upgrade_type == 'expand':
                if self.grid_size >= 5:
                    btn.config(text='Max Size', state=tk.DISABLED, bg='#7F8C8D')
                else:
                    btn.config(text=f'Expand Field (${500 * self.grid_size})')
                    if self.money < 500 * self.grid_size:
                        btn.config(state=tk.DISABLED)
                    else:
                        btn.config(state=tk.NORMAL)

            elif upgrade_type == 'water':
                if self.auto_water:
                    btn.config(text='Auto-Water [BOUGHT]', state=tk.DISABLED, bg='#27AE60')
                else:
                    btn.config(text='Auto-Water ($1000)')
                    if self.money < 1000:
                        btn.config(state=tk.DISABLED)
                    else:
                        btn.config(state=tk.NORMAL)

            elif upgrade_type == 'speed':
                if self.growth_speed >= 2.0:
                    btn.config(text='Max Speed [BOUGHT]', state=tk.DISABLED, bg='#27AE60')
                else:
                    cost = int(1500 * self.growth_speed)
                    btn.config(text=f'Growth Speed (${cost})')
                    if self.money < cost:
                        btn.config(state=tk.DISABLED)
                    else:
                        btn.config(state=tk.NORMAL)

    def expand_farm(self):
        cost = 500 * self.grid_size
        if self.money >= cost and self.grid_size < 5:
            self.money -= cost
            self.grid_size += 1
            self.log(f'Field expanded to {self.grid_size}x{self.grid_size}!')
            self.update_stats()
            self.update_grid()

    def buy_auto_water(self):
        if self.money >= 1000 and not self.auto_water:
            self.money -= 1000
            self.auto_water = True
            self.log('Auto-Water bought!')
            self.update_stats()

    def buy_speed(self):
        cost = int(1500 * self.growth_speed)
        if self.money >= cost and self.growth_speed < 2.0:
            self.money -= cost
            self.growth_speed += 0.5
            self.log(f'Growth speed x{self.growth_speed}!')
            self.update_stats()

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next
        self.xp_to_next = int(self.xp_to_next * 1.5)
        self.money += 50 * self.level
        self.log(f'Level {self.level}! Bonus: +${50 * self.level}')
        messagebox.showinfo('Level Up!', 
                          f'You reached level {self.level}!\nBonus: +${50 * self.level}')

    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    game = FarmGame(root)
    root.mainloop()
