from time import time

from Enums import Direction
from GameController import Game
from Misc import getch, KBHit, clearConsole, read_text_file, write_text_file


def print_banner(file_path: str):
    art = read_text_file(file_path)
    for line in art:
        print(line, sep='', end='')


def exit_art():
    clearConsole()
    print_banner('ascii_end_art.txt')
    exit()


def run_game_instance():
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
            if score := game.update(pressed_key, shoot_bullet):
                return score
            shoot_bullet = False


def open_game_options():
    clearConsole()
    print('This is left as an exercise for the next developer.')
    getch()


def menu():
    done = False
    new_score = 0
    high_score = int(read_text_file('score.txt')[0])

    while not done:
        clearConsole()
        print_banner('ascii_menu_art.txt')
        print('\nHIGH SCORE: ', high_score)
        print('LAST SCORE: ', new_score)
        print('Begin game? [almost any key]   Exit? l   options? o')
        menu_input = ''
        try:
            menu_input = getch()
        except UnicodeDecodeError as e:
            print(e)
            print('maybe try a different key...')
        if menu_input == 'l':
            exit_art()
        elif menu_input == 'o':
            open_game_options()

        new_score = run_game_instance()
        if new_score > high_score:
            high_score = new_score
            write_text_file([str(high_score)], 'score.txt')
        print('u dead boi..\n\nFinal score:', new_score)
        input('[enter]')



if __name__ == '__main__':
    menu()
