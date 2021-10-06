import random

from Enums import EntType, Direction


class Entity:
    def __init__(self, symbol, ent_type):
        self.pos: list[list[int]] = [[5, 5]]
        self.symbol: str = symbol
        self.type: EntType = ent_type
        self.old_pos = [[5, 5]]

    def set_pos(self, position):
        self.old_pos = self.pos[:]
        if type(position[0]) != type([]):
            self.pos = [position]
        else:
            self.pos = position

    def illegal_move(self):
        self.set_pos(self.old_pos)

    def collides(self, ent: 'Entity'):
        for xy in self.pos:
            for ent_xy in ent.pos:
                if xy[0] == ent_xy[0] and xy[1] == ent_xy[1]:
                    return True
        return False

    def move(self, dir: Direction):
        new_pos = []
        if dir == Direction.NONE:
            return
        for xy in self.pos:
            if dir == Direction.UP:
                new_pos.append([xy[0] - 1, xy[1]])
            elif dir == Direction.DOWN:
                new_pos.append([xy[0] + 1, xy[1]])
            elif dir == Direction.LEFT:
                new_pos.append([xy[0], xy[1] - 1])
            elif dir == Direction.RIGHT:
                new_pos.append([xy[0], xy[1] + 1])
        self.set_pos(new_pos)

    """ return neg if ent xy is closer to  0,0"""

    def x_from_entity(self, ent: 'Entity'):
        return ent.pos[0][0] - self.pos[0][0]

    def y_from_entity(self, ent: 'Entity'):
        return ent.pos[0][1] - self.pos[0][1]

    def move_towards(self, ent: 'Entity', xy_change_up=True):
        num = 1
        if xy_change_up:
            num = random.randint(1, 2)
        if num == 1 or self.x_from_entity(ent) == 0 and self.y_from_entity(ent) != 0:
            if self.x_from_entity(ent) >= 0:
                self.move(Direction.DOWN)
                return Direction.DOWN
            elif self.x_from_entity(ent) <= 0:
                self.move(Direction.UP)
                return Direction.UP
        else:
            if self.y_from_entity(ent) >= 0:
                self.move(Direction.RIGHT)
                return Direction.RIGHT
            elif self.y_from_entity(ent) <= 0:
                self.move(Direction.LEFT)
                return Direction.LEFT

    def move_random_dir(self):
        num = random.randint(1, 4)
        if num == 1:
            self.move(Direction.DOWN)
            return Direction.DOWN
        elif num == 1:
            self.move(Direction.UP)
            return Direction.UP
        elif num == 1:
            self.move(Direction.RIGHT)
            return Direction.RIGHT
        elif num == 1:
            self.move(Direction.LEFT)
            return Direction.LEFT

    def dir_of(self, ent: 'Entity', xy_change_up=True) -> Direction:
        num = 1
        if xy_change_up:
            num = random.randint(1, 4)
        if num == 1 or num == 2 or self.x_from_entity(ent) == 0 and self.y_from_entity(ent) != 0:
            if self.x_from_entity(ent) >= 0:
                return Direction.DOWN
            elif self.x_from_entity(ent) <= 0:
                return Direction.UP
        else:
            if self.y_from_entity(ent) >= 0:
                return Direction.RIGHT
            elif self.y_from_entity(ent) <= 0:
                return Direction.LEFT

    def teleport(self, pos):
        ent = Entity(' ', EntType.OBJECT)
        ent.set_pos(pos)
        while not self.collides(ent):
            self.move_towards(ent)

