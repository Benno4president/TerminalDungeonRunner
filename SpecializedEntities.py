import time

from EntityClass import Entity
from Enums import Direction, EntType, Kind
from Misc import ANSI_WHITE, to_list, ANSI_RED, ANSI_YELLOW, ANSI_GREEN, ANSI_CYAN, ANSI_RAINBOW, ANSI_BLUE, ANSI_PURPLE


class Bullet(Entity):
    def __init__(self, dir: Direction, position, symbol='*', kind=Kind.ENEMY, skip=0):
        super(Bullet, self).__init__(symbol, EntType.BULLET)
        _dir = dir
        if _dir == Direction.NONE:
            _dir = Direction.UP
        self.kind_of: Kind = kind
        self.direction = _dir
        self.skip = skip

        self.set_pos(position)

        self.update()

    def update(self):
        for i in range(self.skip + 1):
            self.move(self.direction)


class DamagingFloor(Entity):
    def __init__(self, position, delay=3, symbol='N', kind=Kind.FRIENDLY):
        super(DamagingFloor, self).__init__(symbol, EntType.FLOOR)
        self.frames_before_removal = delay
        self.kind_of: Kind = kind
        self.set_pos(position)

    def update(self):
        self.frames_before_removal -= 1
        if self.frames_before_removal <= 0:
            return True


class Coin(Entity):
    def __init__(self, position, amount=1, symbol=ANSI_GREEN('$')):
        super(Coin, self).__init__(symbol, EntType.COIN)
        self.set_pos(position)
        self.amount = amount

    def add_coin_to_player(self, player):
        player.coin += self.amount


""" healing heart kinds works like the coin so yeah"""


class HealingHeart(Coin):
    def __init__(self, position, amount=1):
        super(HealingHeart, self).__init__(position, amount, symbol=ANSI_BLUE('♥'))

    def add_coin_to_player(self, player):
        player.heal(self.amount)


class Trigger(Entity):
    def __init__(self, position, x_len=3, y_len=3, symbol=ANSI_BLUE('8')):
        super(Trigger, self).__init__(symbol, EntType.TRIGGER)
        cpos = position
        new_pos = []

        for x in range(x_len):
            for y in range(y_len):
                new_pos.append([x + cpos[0], y + cpos[1]])
        self.set_pos(new_pos)


class BuyTile(Entity):
    def __init__(self, position, content, price=0, symbol=ANSI_RAINBOW('$')):
        super(BuyTile, self).__init__(symbol, EntType.SHOP)
        self.set_pos(position)
        self.shop_content: object = content
        self.price = price
        self.destroy_this = False

    def update(self, player):
        if not self.collides(player):
            return
        if player.coin < self.price:
            return
        player.coin -= self.price
        if issubclass(type(self.shop_content), Item):
            player.add_item(self.shop_content)
            self.destroy_this = True
        else:
            return self.shop_content
        return


class TextBox(Entity):
    def __init__(self, position, char: str):
        super(TextBox, self).__init__(char, EntType.OBJECT)
        self.set_pos(position)

    @classmethod
    def add_word(cls, position, text: str):
        text_box_list = []
        i = 0
        for char in text:
            text_box_list.append(TextBox([position[0], position[1] + i], char))
            i += 1
        return text_box_list


class Wall(Entity):
    def __init__(self, top_left_corner_pos, x_len, y_len):
        super(Wall, self).__init__('#', EntType.WALL)
        cpos = top_left_corner_pos
        new_pos = []

        for x in range(x_len):
            for y in range(y_len):
                new_pos.append([x + cpos[0], y + cpos[1]])
        self.set_pos(new_pos)


class Player(Entity):
    def __init__(self, hp):
        super(Player, self).__init__(ANSI_BLUE('@'), EntType.PLAYER)
        self.hp = hp
        self.coin = 0
        self.item_list = []
        self.set_pos([6, 30])

    def update(self, key: Direction, shoot_bullet: bool, entities_on_map):
        _key = key

        self.move(_key)

        for itm in self.item_list:
            if res := to_list(itm.update(self.pos, self, shoot_bullet, _key)):
                entities_on_map.extend(res)

        if shoot_bullet:
            return Bullet(_key, self.pos,
                          kind=Kind.FRIENDLY)  # true false could be called from dict to see if power up is activated
        return None

    def damage(self):
        self.hp -= 1
        if self.hp <= 0:
            self.hp = int(input('Game over, type new hp to continue..'))  # some real code to die

    def heal(self, amount=1):
        self.hp += amount

    def add_item(self, item):
        for im in self.item_list:
            if type(im) == type(item):
                im.upgrade()
                return
        self.item_list.append(item)


class Item:

    def update(self, position, player, shoot_bullet: bool, dir: Direction = Direction.UP):
        pass

    def upgrade(self):
        pass


class NeonCat(Item):
    def __init__(self):
        self.trail_length = 4

    def update(self, position, player, shoot_bullet, dir=Direction.UP):
        return DamagingFloor(position, self.trail_length, symbol=ANSI_RAINBOW('x'))

    def upgrade(self):
        self.trail_length += 3


class MultiShot(Item):
    def __init__(self):
        self.shots = 2

    def update(self, position, player, shoot_bullet, dir=Direction.UP):
        if not shoot_bullet:
            return
        bullet_placement = 1
        bullet_list = []
        for i in range(1, self.shots + 1):
            if dir == Direction.UP or dir == Direction.DOWN:
                bullet_list.append(Bullet(dir, [position[0][0], position[0][1] + bullet_placement], kind=Kind.FRIENDLY))
            elif dir == Direction.LEFT or dir == Direction.RIGHT:
                bullet_list.append(Bullet(dir, [position[0][0] + bullet_placement, position[0][1]], kind=Kind.FRIENDLY))
            if (i % 2) == 0:
                if bullet_placement > 0:
                    bullet_placement += 1
                else:
                    bullet_placement -= 1
            bullet_placement = -bullet_placement

        return bullet_list

    def upgrade(self):
        self.shots += 2


class RailShot(Item):
    def __init__(self):
        self.length = 2
        self.time_out: time = time.time()

    def update(self, position, player, shoot_bullet, dir=Direction.UP):
        if not shoot_bullet:
            return
        if time.time() - self.time_out < 3:
            return
        self.time_out = time.time()
        bullet_list = []
        for i in range(1, self.length + 1):
            if dir == Direction.UP:
                bullet_list.append(
                    Bullet(dir, [position[0][0] - i + self.length * 2, position[0][1]], kind=Kind.FRIENDLY,
                           skip=self.length))
            elif dir == Direction.DOWN:
                bullet_list.append(
                    Bullet(dir, [position[0][0] + i - self.length * 2, position[0][1]], kind=Kind.FRIENDLY,
                           skip=self.length))
            elif dir == Direction.LEFT:
                bullet_list.append(
                    Bullet(dir, [position[0][0], position[0][1] - i + self.length * 2], kind=Kind.FRIENDLY,
                           skip=self.length))
            elif dir == Direction.RIGHT:
                bullet_list.append(
                    Bullet(dir, [position[0][0], position[0][1] + i - self.length * 2], kind=Kind.FRIENDLY,
                           skip=self.length))

        return bullet_list

    def upgrade(self):
        self.length += 1

class Bomb(Entity):
    def __init__(self, position, delay=15, symbol='O', kind=Kind.FRIENDLY):
        super(Bomb, self).__init__(symbol, EntType.SHOP)
        self.frames_before_removal = delay
        self.kind_of: Kind = kind
        self.set_pos(position)
        self.destroy_this = False
        self.delay = delay
    def update(self, player):
        self.frames_before_removal -= 1
        if self.frames_before_removal <= 0:
            return DamagingFloor(self.pos, symbol='O', delay=self.delay, kind=Kind.ENEMY)
        
        if self.frames_before_removal % 2 == 0:
            self.symbol = ANSI_RED('O')
        else:
            self.symbol = ANSI_WHITE('O')