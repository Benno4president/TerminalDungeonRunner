import random
import time

from EntityClass import Entity
from Enums import EntType, Direction
from Misc import ANSI_RED, ANSI_YELLOW, ANSI_GREEN, ANSI_CYAN, ANSI_RAINBOW, ANSI_BLUE, ANSI_PURPLE
from SpecializedEntities import Bullet, Coin


class Enemy(Entity):
    def __init__(self, position, symbol=ANSI_YELLOW('%')):
        super(Enemy, self).__init__(symbol, EntType.ENEMY)
        self.hp = 1
        self.set_pos(position)

    def update(self, player):
        num = random.randint(1, 2)
        if num == 1:
            self.move_random_dir()
        else:
            self.move_towards(player)

    def damage_and_is_dead(self):
        self.hp -= 1
        if self.hp <= 0:
            return True
        return False

    def death_drops(self):
        if random.randint(1, 3) == 1:
            return [Coin(self.pos[0])]


class SprayerEnemy(Enemy):
    def __init__(self, position):
        super(SprayerEnemy, self).__init__(position, symbol=ANSI_PURPLE('+'))
        self.shot_timeout: time = time.time()
        self.last_dir = 0

    def update(self, player):
        num = random.randint(1, 4)
        if num == 1:
            self.move_random_dir()
        elif num == 2:
            self.move_towards(player)

        if time.time() - self.shot_timeout > 0.5:
            _dir = Direction((self.last_dir % 4) + 1)
            self.last_dir += 1
            self.shot_timeout = time.time()
            return Bullet(_dir, self.pos, symbol=ANSI_CYAN('*'))


class BruteEnemy(Enemy):
    def __init__(self, position):
        new_pos = [position, [position[0] + 1, position[1]], [position[0], position[1] + 1],
                   [position[0] + 1, position[1] + 1]]
        super(BruteEnemy, self).__init__(new_pos, symbol=ANSI_YELLOW('Z'))
        self.hp = 3
        self.shot_timeout: time = time.time()

    def update(self, player):
        num = random.randint(1, 2)
        if num == 1:
            self.move_random_dir()
        else:
            self.move_towards(player)

        if time.time() - self.shot_timeout > 2:
            _dir = self.dir_of(player)
            self.shot_timeout = time.time()
            return Bullet(_dir, self.pos, symbol=ANSI_CYAN('*'))


class FloaterEnemy(Enemy):
    def __init__(self, position):
        _p = position
        new_pos = [[_p[0] - 1, _p[1] - 1], [_p[0] - 1, _p[1]], [_p[0] - 1, _p[1] + 1],
                   [_p[0], _p[1] - 1], [_p[0], _p[1]], [_p[0], _p[1] + 1],
                   [_p[0] + 1, _p[1] - 1], [_p[0] + 1,
                                            _p[1]], [_p[0] + 1, _p[1] + 1]
                   ]

        super(FloaterEnemy, self).__init__(new_pos, symbol=ANSI_YELLOW('€'))
        self.hp = 3
        self.shot_timeout: time = time.time()

    def update(self, player):
        num = random.randint(1, 5)
        if num == 1:
            self.move_towards(player)
        else:
            self.move_random_dir()

        if time.time() - self.shot_timeout > 4:
            self.shot_timeout = time.time()
            bullet_list = []
            bullet_list.append(
                Bullet(Direction.UP, self.pos, symbol=ANSI_CYAN('*')))
            bullet_list.append(
                Bullet(Direction.DOWN, self.pos, symbol=ANSI_CYAN('*')))
            bullet_list.append(
                Bullet(Direction.RIGHT, self.pos, symbol=ANSI_CYAN('*')))
            bullet_list.append(
                Bullet(Direction.LEFT, self.pos, symbol=ANSI_CYAN('*')))
            return bullet_list


""" worm, standard"""


class WormEnemy(Enemy):
    def __init__(self, position, symbol=ANSI_GREEN('&'), length: int = 7):
        p = position[:]
        new_pos = []
        for i in range(length):
            new_pos.append([p[0], p[1] + i])

        super(WormEnemy, self).__init__(new_pos, symbol)
        self.hp = 3

    def update(self, player):
        num = random.randint(1, 3)
        if num == 1:
            self.move_random_dir()
        else:
            self.move_towards(player)

    def move(self, dir: Direction):
        try:
            new_pos = self.pos[:]
            new_pos.remove(new_pos[0])
            _p = new_pos[len(new_pos) - 1]
            if dir == Direction.UP:
                new_pos.append([_p[0] - 1, _p[1]])
            elif dir == Direction.DOWN:
                new_pos.append([_p[0] + 1, _p[1]])
            elif dir == Direction.LEFT:
                new_pos.append([_p[0], _p[1] - 1])
            elif dir == Direction.RIGHT:
                new_pos.append([_p[0], _p[1] + 1])
            self.set_pos(new_pos)
        except IndexError as e:
            print(e)


""" worm, the world fucker (worm with more than 1 char as symbol, maybe rainbow?)"""


class WormWorldFucker(WormEnemy):
    def __init__(self, position, length=12):
        super(WormWorldFucker, self).__init__(position, symbol=ANSI_RAINBOW('{}'), length=length)
        self.hp = 10


""" trailer, enemy which drops toxic trail """


class BulletBlaster(Enemy):
    def __init__(self, position, symbol=ANSI_RED(':D')):
        super(Enemy, self).__init__(symbol, EntType.ENEMY)
        self.hp = 4
        self.set_pos(position)
        self.shot_timeout: time = time.time()

    def update(self, player):
        num = random.randint(1, 5)
        if num == 1:
            self.move_towards(player)
        else:
            self.move_random_dir()
            
        if time.time() - self.shot_timeout > 0.5:
            self.shot_timeout = time.time()
            bullet_list = []
            bullet_list.append(
                Bullet(Direction.UP, self.pos, symbol=ANSI_RAINBOW('*')))
            bullet_list.append(
                Bullet(Direction.DOWN, self.pos, symbol=ANSI_RAINBOW('*')))
            bullet_list.append(
                Bullet(Direction.RIGHT, self.pos, symbol=ANSI_RAINBOW('*')))
            bullet_list.append(
                Bullet(Direction.LEFT, self.pos, symbol=ANSI_RAINBOW('*')))
            return bullet_list

