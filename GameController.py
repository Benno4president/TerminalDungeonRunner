from EntityClass import Entity
from Enums import EntType, Direction, Kind
from GridController import Grid
from LevelController import LevelHandler
from Misc import to_list
from SpecializedEntities import Player, Coin


class Game:
    def __init__(self, height: int = 20, width: int = 60):
        self.player = Player(6)
        self.grid = Grid(height, width)
        self.lvlh = LevelHandler(self.grid.height, self.grid.width)
        self.entities: list[Entity] = []
        self.current_key = ''

    def update(self, key_input: Direction, shoot_bullet: bool):
        """ update everything """
        if player_objects := to_list(self.player.update(key_input, shoot_bullet, self.entities)):
            self.entities.extend(player_objects)

        for ent in self.entities:
            if ent.type == EntType.BULLET:
                ent.update()
                if self.player.collides(ent) and ent.kind_of == Kind.ENEMY:
                    self.player.damage()
            elif ent.type == EntType.ENEMY:
                if enemy_actions := to_list(ent.update(self.player)):  # used for drops/bombs/bullets etc.
                    self.entities.extend(enemy_actions)
                if self.player.collides(ent):
                    self.player.damage()
            elif ent.type == EntType.COIN and self.player.collides(ent):
                ent.add_pickup_to_player(self.player)
                self.entities.remove(ent)
            elif ent.type == EntType.SHOP:
                if shop_drop := to_list(ent.update(self.player)):
                    self.entities.extend(shop_drop)
                    self.entities.remove(ent)
                elif ent.destroy_this:
                    self.entities.remove(ent)
            elif ent.type == EntType.TRIGGER and self.player.collides(ent):
                self.lvlh.trigger_hit()
            elif ent.type == EntType.FLOOR:
                if ent.update():
                    self.entities.remove(ent)

        for ent in self.entities:
            if not (ent.type == EntType.BULLET or ent.type == EntType.FLOOR):
                continue
            if not ent.kind_of == Kind.FRIENDLY:
                continue
            for s_ent in self.entities:
                if not s_ent.type == EntType.ENEMY:
                    continue
                if ent.collides(s_ent):
                    if s_ent.damage_and_is_dead():
                        if ddrop := s_ent.death_drops():
                            self.entities.extend(ddrop)  # ent could return drop
                        self.entities.remove(s_ent)
                    if ent in self.entities:
                        self.entities.remove(ent)

        for ent in self.entities:
            if self.grid.is_point_wall(ent, self.entities):
                if ent.type == EntType.BULLET:
                    self.entities.remove(ent)
                else:
                    ent.illegal_move()

        self.lvlh.update(self.player, self.entities)

        self.grid.update_grid(self.player, self.entities)
        self.grid.print_grid(self.player)
        if not key_input == '':
            self.current_key = key_input
