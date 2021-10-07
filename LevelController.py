import random

from Enemies import BulletBlaster, Enemy, BruteEnemy, SprayerEnemy, FloaterEnemy, WormEnemy, WormWorldFucker
from Enums import EntType
from Misc import clearConsole
from SpecializedEntities import Trigger, Wall, BuyTile, NeonCat, MultiShot, TextBox, RailShot


class LevelHandler:
    def __init__(self, grid_h, grid_w, challenge: int = 1, current_floor=0):
        self.tp_point_spawned: bool = False
        self.trigger: bool = False
        self.grid_height = grid_h
        self.grid_width = grid_w
        self.challenge = challenge
        self.current_floor = current_floor
        self.sr_factory = SpecialRoomFactory()

    def left_rand(self):
        return random.randint(2, 14)

    def right_rand(self):
        return random.randint(2, 3)

    def random_pos(self, x_mod=0, y_mod=0):
        rnd_pos = [self.right_rand() + x_mod, self.left_rand() + y_mod]
        return rnd_pos

    def update(self, player, entities_on_map):
        for ent in entities_on_map:
            if ent.type == EntType.ENEMY:
                return
        if not self.tp_point_spawned:
            entities_on_map.append(Trigger(self.random_pos(4, 40)))  # tp plate
            self.tp_point_spawned = True
        if not self.trigger:
            return

        self.tp_point_spawned = False
        self.trigger = False
        self.current_floor += 1
        if self.current_floor % 2 == 0:
            self.generate_walls(entities_on_map, awesomify=True)
            self.add_floor_enemies_to(entities_on_map)
        else:
            self.generate_walls(entities_on_map)
            self.sr_factory.get_next_room(player, entities_on_map)
            player.teleport([7, 29])

        for ent in entities_on_map:
            if ent.type == EntType.WALL and player.collides(ent):
                entities_on_map.remove(ent)

    def add_floor_enemies_to(self, entities_on_map):
        enemy_selection = {'1': Enemy(self.random_pos()),
                           '2': BruteEnemy(self.random_pos()),
                           '3': SprayerEnemy(self.random_pos()),
                           '4': FloaterEnemy(self.random_pos()),
                           '5': WormEnemy(self.random_pos()),
                           '6': WormWorldFucker(self.random_pos()),
                           '7': BulletBlaster(self.random_pos())
                           }
        for i in range(self.current_floor):
            enemy = enemy_selection[str(random.randint(1, len(enemy_selection)))]
            entities_on_map.append(enemy)

    def generate_walls(self, entities_on_map, awesomify=False, scale_only_neg=0):
        """ removes everything and places walls """
        clearConsole()
        entities_on_map.clear()

        entities_on_map.append(Wall([0, 0], self.grid_height - 1 + scale_only_neg, 1))  # left
        entities_on_map.append(Wall([0, 0], 1, self.grid_width - 1 + scale_only_neg))  # top
        entities_on_map.append(
            Wall([0, self.grid_width - 1 + scale_only_neg], self.grid_height + scale_only_neg, 1))  # right
        entities_on_map.append(
            Wall([self.grid_height - 1 + scale_only_neg, 0], 1, self.grid_width - 1 + scale_only_neg))  # bottom

        if awesomify:
            seed = 0
            for i in range(random.randint(5, 10)):
                if random.randint(1, 2) % 2 == 0:
                    seed += i
                xx = random.randint(1, self.grid_height - 2)
                yy = random.randint(1, self.grid_width - 2)
                new_wall = Wall([xx, yy], 3, 3)
                sub_wall = Wall([xx - 1, yy + 3], random.randint(1, 4), random.randint(1, 4))
                entities_on_map.append(new_wall)
                entities_on_map.append(sub_wall)

    def trigger_hit(self):
        self.trigger = True


class SpecialRoomFactory:
    def __init__(self):
        self.room_count = 0

    def get_next_room(self, player, entities_on_map):
        self.room_count += 1
        if self.room_count == 1:
            self.start_room(player, entities_on_map)
        else:
            self.shop_room(player, entities_on_map)

    def start_room(self, player, entities_on_map):
        entities_on_map.append(WormEnemy([10, 10]))
        entities_on_map.append(WormWorldFucker([10, 10]))
        entities_on_map.append(Wall([1, 1], 18, 11))
        entities_on_map.extend(TextBox.add_word([1, 28], 'Yee ol\' Shop'))
        entities_on_map.extend(TextBox.add_word([2, 13], 'SHOT UP'))
        entities_on_map.append(BuyTile([3, 14], MultiShot(), price=0))
        entities_on_map.append(BuyTile([3, 16], MultiShot(), price=0))
        entities_on_map.append(BuyTile([3, 18], MultiShot(), price=0))
        entities_on_map.append(BuyTile([3, 20], MultiShot(), price=0))
        entities_on_map.extend(TextBox.add_word([5, 13], 'NEON CAT'))
        entities_on_map.append(BuyTile([6, 14], NeonCat(), price=0))
        entities_on_map.append(BuyTile([6, 16], NeonCat(), price=0))
        entities_on_map.append(BuyTile([6, 18], NeonCat(), price=0))
        entities_on_map.append(BuyTile([6, 20], NeonCat(), price=0))
        entities_on_map.extend(TextBox.add_word([8, 13], 'RAIL SHOT'))
        entities_on_map.append(BuyTile([9, 14], RailShot(), price=0))
        entities_on_map.append(BuyTile([9, 16], RailShot(), price=0))
        entities_on_map.append(BuyTile([9, 18], RailShot(), price=0))
        entities_on_map.append(BuyTile([9, 20], RailShot(), price=0))

    def shop_room(self, player, entities_on_map):
        entities_on_map.append(BuyTile([6, 20], MultiShot(), price=1))
        entities_on_map.append(BuyTile([8, 20], NeonCat(), price=1))
        entities_on_map.append(BuyTile([10, 20], NeonCat(), price=1))
        entities_on_map.append(BuyTile([12, 20], NeonCat(), price=1))
