from time import time

from Enums import Direction
from GameController import Game
from Misc import getch, KBHit, clearConsole, read_text_file


def exit_art():
    clearConsole()
    art = read_text_file('ascii_end_art.txt')
    for line in art:
        print(line, sep='', end='')
    exit()


def run():
    delay_in_seconds: float = 0.2
    time_since_update: time = time()
    pressed_key: Direction = Direction.NONE
    shoot_bullet = False
    kb = KBHit()
    game = Game()
    clearConsole()
    while True:
        is_pressed = ''
        try:
            if kb.kbhit():
                is_pressed = getch()
        except UnicodeDecodeError as e:
            _ = input('Key not allowed... bug?\ncontinue?  ')
            if _ != 'yes':
                break
        if is_pressed == 'w':
            pressed_key = Direction.UP
        elif is_pressed == 'a':
            pressed_key = Direction.LEFT
        elif is_pressed == 's':
            pressed_key = Direction.DOWN
        elif is_pressed == 'd':
            pressed_key = Direction.RIGHT
        elif is_pressed == 'm':
            shoot_bullet = True
        elif is_pressed == 'l':
            exit_art()
        if time() - time_since_update >= delay_in_seconds:
            time_since_update = time()
            game.update(pressed_key, shoot_bullet)
            print('[', is_pressed, ']', pressed_key, shoot_bullet)
            shoot_bullet = False

    print("Game exited.")
    return 0


if __name__ == '__main__':
    run()
