import random

from Enemies import BulletBlaster, Enemy, BruteEnemy, SprayerEnemy, FloaterEnemy, WormEnemy, WormWorldFucker
from Enums import EntType
from Misc import clearConsole
from SpecializedEntities import Trigger, Wall, BuyTile, NeonCat, MultiShot, TextBox, RailShot, HealingHeart


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
        self.rooms = {
            1: self.shop_room,
            2: self.fire_place_room,
            3: self.item_for_worms_room
        }
        """ shop dict: id: list[ Shop name, instance, price ] """
        self.shop_item_selection = {
            1: ['Rail Shot:', RailShot(), 10],
            2: ['Broad Shot:', MultiShot(), 12],
            3: ['Neon Cat:', NeonCat(), 8]
        }

    def get_random_shop_item(self, rand_price: bool = True):
        item_num = random.randint(1, len(self.shop_item_selection))
        item = self.shop_item_selection[item_num][:]
        if rand_price:
            item[2] += random.randint(-5, 5)
        return item

    def get_next_room(self, player, entities_on_map):
        self.room_count += 1
        if self.room_count == 1:
            self.start_room(player, entities_on_map)
            # self.shop_room(player, entities_on_map) # tester
        else:
            room_num = random.randint(1, len(self.rooms))
            room_func = self.rooms[room_num]
            room_func(player, entities_on_map)

    def start_room(self, player, entities_on_map):
        entities_on_map.extend(TextBox.add_word([1, 10], 'Hello there,'))
        entities_on_map.extend(TextBox.add_word([2, 10], 'welcome to a generic terminal dungeon runner'))
        entities_on_map.extend(TextBox.add_word([3, 10], 'May you journey be filled with horrible'))
        entities_on_map.extend(TextBox.add_word([4, 10], 'bugs and bullsh*t spawn deaths'))
        entities_on_map.extend(TextBox.add_word([6, 10], 'Good fucking luck.'))
        entities_on_map.extend(TextBox.add_word([10, 10], 'Move: wasd'))
        entities_on_map.extend(TextBox.add_word([12, 10], 'Shoot: m'))
        entities_on_map.extend(TextBox.add_word([14, 10], 'Leave this cursed game: l'))
        entities_on_map.append(BuyTile([1, 7], RailShot()))
        entities_on_map.append(BuyTile([1, 5], RailShot()))

    def shop_room(self, player, entities_on_map):

        entities_on_map.append(Wall([1, 1], 18, 11))
        entities_on_map.extend(TextBox.add_word([1, 28], 'Yee ol\' Shop'))
        entities_on_map.extend(TextBox.add_word([12, 30], '> Welcome UwU,'))
        entities_on_map.extend(TextBox.add_word([13, 30], '  puiz buy my stuff<3<3'))
        entities_on_map.extend(TextBox.add_word([14, 30], '  i need herOwOin'))
        entities_on_map.extend(TextBox.add_word([16, 30], '  ,---/V\\'))
        entities_on_map.extend(TextBox.add_word([17, 30], ' ~|__(o.o)'))
        entities_on_map.extend(TextBox.add_word([18, 30], '  UU  UU'))

        tile_num = 3
        for i in range(random.randint(1, 5)):
            item = self.get_random_shop_item()
            entities_on_map.extend(TextBox.add_word([tile_num, 13], item[0] + str(item[2]) + '$'))
            tile_num += 1
            entities_on_map.append(BuyTile([tile_num, 14], item[1], price=item[2]))
            tile_num += 2

    def fire_place_room(self, player, entities):
        entities.extend(TextBox.add_word([1, 20], '..a fireplace'))
        entities.extend(TextBox.add_word([5, 13], '> zzz *UwUaua*,'))
        entities.extend(TextBox.add_word([6, 13], '  Something to'))
        entities.extend(TextBox.add_word([7, 13], '  sleep on? zzz'))
        entities.extend(TextBox.add_word([8, 13], '  ,---/V\\'))
        entities.extend(TextBox.add_word([9, 13], ' ~|__(o.o)'))

        entities.extend(TextBox.add_word([9, 24], '   )'))
        entities.extend(TextBox.add_word([10, 24], '  ) \\'))
        entities.extend(TextBox.add_word([11, 24], ' \\(_)/'))

        entities.append(HealingHeart([10, 20]))

    def item_for_worms_room(self, player, entities):
        entities.extend(TextBox.add_word([4, 18], '..at least it\'s free'))
        entities.append(BuyTile([5, 20], [WormWorldFucker([15, 3], 20), WormWorldFucker([15, 3], 20), WormWorldFucker([15, 3], 20), WormWorldFucker([15, 3], 20), WormWorldFucker([15, 3], 20)]))
        entities.append(BuyTile([5, 20], self.get_random_shop_item()[1]))





