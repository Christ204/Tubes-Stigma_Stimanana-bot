#Kristof Tsunami Ginting (123140117)
#Mulya Delani (123140019)
#Mega Zayyani (123140180)
from typing import Optional
import random
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class StimananaLogic(BaseLogic):
    def __init__(self):
        
        self.goal: Optional[Position] = None  
        
    def distance(self, A: Position, B: Position):
        return abs(A.x - B.x) + abs(A.y - B.y)

    # Fungsi untuk mencari semua objek bertipe teleporter di board
    # Berguna jika nanti ingin menggunakan teleportasi untuk efisiensi jarak
    def get_teleporters(self, board: Board):
        return [obj for obj in board.game_objects if obj.type == "TeleportGameObject"]
    

    # Fungsi untuk menghitung jarak antara dua titik dengan mempertimbangkan teleport
    def distance_with_teleporter(self, start: Position, end: Position, board: Board):
        teleporters = self.get_teleporters(board)
        if len(teleporters) < 2:
            return self.distance(start, end)
        entry, exit = teleporters
        via_tp = self.distance(start, entry.position) + self.distance(exit.position, end)
        return min(self.distance(start, end), via_tp)

    def get_best_teleport_or_base(self, pos, base, board):
        teleporters = self.get_teleporters(board)
        if len(teleporters) >= 2:
            entry, exit = teleporters
        dist_normal = self.distance(pos, base)
        dist_tp = self.distance(pos, entry.position) + self.distance(exit.position, base)
        if dist_tp < dist_normal:
            return entry.position
        return base
    
    # Fungsi untuk menghitung arah langkah menuju base bot
    def return_to_base(self, bot: GameObject):
        base = bot.properties.base
        dx = 1 if base.x > bot.position.x else -1 if base.x < bot.position.x else 0
        dy = 1 if base.y > bot.position.y else -1 if base.y < bot.position.y else 0
        return dx, dy

    # Fungsi untuk mencari diamond terdekat dari bot
    def get_closest_diamond(self, bot: GameObject, board: Board, red_only=False):
        diamonds = []
        max_capacity = 5
        current = bot.properties.diamonds
        for d in board.diamonds:
            if red_only and d.properties.points == 2:
                if current + 2 <= max_capacity:
                    diamonds.append(d)
            elif not red_only and d.properties.points == 1:
                if current + 1 <= max_capacity:
                    diamonds.append(d)
        if not diamonds:
            return None
        closest = diamonds[0]
        min_dist = self.distance(bot.position, closest.position)
        for d in diamonds[1:]:
            dist = self.distance(bot.position, d.position)
            if dist < min_dist:
                closest = d
                min_dist = dist
        return closest

    # Fungsi untuk mencari musuh terdekat dalam radius tackle (jarak 1)
    # Digunakan dalam strategi Greedy by Tackle
    def find_enemy_to_tackle(self, bot: GameObject, board: Board):
        for enemy in board.bots:
            if enemy.id != bot.id and self.distance(bot.position, enemy.position) == 2:
                return enemy.position
        return None

    # Fungsi untuk menemukan red button (diamond button) di board
    # Digunakan untuk strategi Greedy by Red Button
    def get_red_button(self, board: Board):
        for obj in board.game_objects:
            if obj.type == "DiamondButtonGameObject":
                return obj
        return None

    # Fungsi untuk menentukan bot menekan red button saat diamonds kurang dari 10
    def should_press_red_button(self, bot: GameObject, board: Board):
        if len(board.diamonds) < 10:
            red_button = self.get_red_button(board)
            nearest_diamond = self.get_closest_diamond(bot, board, red_only=True) or \
                               self.get_closest_diamond(bot, board, red_only=False)
            if red_button and nearest_diamond:
                dist_button = self.distance(bot.position, red_button.position)
                dist_diamond = self.distance(bot.position, nearest_diamond.position)
                if dist_button < dist_diamond:
                    return red_button.position
        return None



    # Fungsi utama bot untuk menentukan langkah selanjutnya
    def next_move(self, bot: GameObject, board: Board):
        props = bot.properties
        pos = bot.position
        base = props.base
        time_left = getattr(board, "time_left", 999)  
        steps_to_base = self.distance(pos, base)

        # Greedy by Escape: Jika dekat bot lawan (jarak <=2) dan bawa >=3 diamond, langsung lari ke base
        if props.diamonds >= 3:
            for enemy in board.bots:
                if enemy.id != bot.id and self.distance(pos, enemy.position) <= 2:
                    self.goal = base
                    direction = get_direction(pos.x, pos.y, self.goal.x, self.goal.y)
                    return direction

        # Greedy by Return: Pulang jika waktu tersisa kurang dari atau sama dengan jarak ke base (pakai teleporter jika lebih cepat)
        dist_normal = self.distance(pos, base)
        dist_tp = self.distance_with_teleporter(pos, base, board)
        min_dist = min(dist_normal, dist_tp)
        if time_left <= min_dist:
            self.goal = self.get_best_teleport_or_base(pos, base, board)
            direction = get_direction(pos.x, pos.y, self.goal.x, self.goal.y)
            return direction

        # Pulang jika waktu tersisa sama atau kurang dari langkah ke base
        if time_left <= steps_to_base:
            self.goal = base
            direction = get_direction(pos.x, pos.y, self.goal.x, self.goal.y)
            return direction

        # Greedy by Tackle: Serang musuh yang bawa ≥2 diamond dan jarak 2
        target_enemy = None
        for enemy in board.bots:
            if enemy.id != bot.id and getattr(enemy.properties, "diamonds", 0) >= 2:
                if self.distance(pos, enemy.position) == 1:
                    target_enemy = enemy.position
                    break
        if target_enemy:
            self.goal = target_enemy
        
        #Greedy by Red Button: Tekan red button 
        red_button_pos = self.should_press_red_button(bot, board)
        if red_button_pos:
            self.goal = red_button_pos

         # Greedy by Distance: Jika inventory penuh (≥5 diamond), langsung pulang
        elif props.diamonds >= 5 or time_left <= steps_to_base + 1:
            # langsung pulang (pakai teleporter jika efisien)
           self.goal = self.get_best_teleport_or_base(pos, base, board)

        # Greedy by Red Diamond: Jika sudah bawa ≥3 diamond, pulang atau ambil red diamond jika dekat
        elif props.diamonds >= 3:
            red = self.get_closest_diamond(bot, board, red_only=True)
            if red and self.distance(pos, red.position) <= 3:
                self.goal = red.position
            else:
                # Greedy by Teleporter: Gunakan teleporter jika efisien untuk pulang
                self.goal = self.get_best_teleport_or_base(pos, base, board)

        # Greedy by Diamond: Cari red diamond, jika tidak ada baru cari blue diamond
        else:
            red = self.get_closest_diamond(bot, board, red_only=True)
            blue = self.get_closest_diamond(bot, board, red_only=False)
            # Jika ada red diamond dan blue diamond, cek jarak
            if red and blue:
                dist_red = self.distance(pos, red.position)
                dist_blue = self.distance(pos, blue.position)
                # Jika blue diamond lebih dekat, ambil blue diamond dulu
                if dist_blue < dist_red:
                    self.goal = blue.position
                # Jika red diamond lebih dekat, cek apakah muat di inventory
                elif props.diamonds + 2 <= 5:
                    self.goal = red.position
                else:
                    # Jika Tidak muat ambil red diamond, langsung ke base
                    self.goal = base
            elif red:
                # Hanya ada red diamond, cek apakah muat di inventory
                if props.diamonds + 2 <= 5:
                    self.goal = red.position
                else:
                    self.goal = base
            elif blue:
                self.goal = blue.position
            else:
                self.goal = base

        # Greedy by Return: Mampir ke base saat dilewati dan bawa diamond
        if self.goal != base and self.distance(pos, base) == 1 and props.diamonds > 0:
            self.goal = base

        # Hitung arah gerakan menggunakan get_direction
        direction = get_direction(pos.x, pos.y, self.goal.x, self.goal.y)
        
        return direction
