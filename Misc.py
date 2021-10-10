# https://stackoverflow.com/a/48136131/404271
import os
import sys

if sys.platform == 'win32':
    import msvcrt

    getch = msvcrt.getch
    getche = msvcrt.getche
else:
    import sys
    from select import select
    import termios, atexit


    def __gen_ch_getter(echo):
        def __fun():
            fd = sys.stdin.fileno()
            oldattr = termios.tcgetattr(fd)
            newattr = oldattr[:]
            try:
                if echo:
                    # disable ctrl character printing, otherwise, backspace will be printed as "^?"
                    lflag = ~(termios.ICANON | termios.ECHOCTL)
                else:
                    lflag = ~(termios.ICANON | termios.ECHO)
                newattr[3] &= lflag
                termios.tcsetattr(fd, termios.TCSADRAIN, newattr)
                ch = sys.stdin.read(1)
                if echo and ord(ch) == 127:  # backspace
                    # emulate backspace erasing
                    # https://stackoverflow.com/a/47962872/404271
                    sys.stdout.write('\b \b')
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, oldattr)
            return ch

        return __fun


    getch = __gen_ch_getter(False)
    getche = __gen_ch_getter(True)

""" clear terminal"""


def moveCursor(x=0, y=0):
    print("\033[%d;%dH" % (x, y))


def clearConsole():
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')


class KBHit:

    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''

        if os.name == 'nt':
            pass

        else:

            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)

    def set_normal_term(self):
        """ Resets to normal terminal.  On Windows this is a no-op.
        """

        if os.name == 'nt':
            pass

        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def getch(self):
        """ Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        """

        s = ''

        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')

        else:
            return sys.stdin.read(1)

    def getarrow(self):
        """ Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        """

        if os.name == 'nt':
            msvcrt.getch()  # skip 0xE0
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]

        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]

        return vals.index(ord(c.decode('utf-8')))

    def kbhit(self):
        """ Returns True if keyboard character was hit, False otherwise.
        """
        if os.name == 'nt':
            return msvcrt.kbhit()

        else:
            dr, dw, de = select([sys.stdin], [], [], 0)
            return dr != []


def read_text_file(filename):
    lines = []
    with open(filename, encoding='utf8') as f:
        lines = f.readlines()
    return lines


def write_text_file(lines, filename):
    with open(filename, 'w') as f:
        f.writelines(lines)


def to_list(_input):
    if _input is None:
        return []
    if type(_input) != type([]):
        return [_input]
    return _input


def ANSI_RESET(text):
    return f"\u001B[0m{text}\u001B[0m"


def ANSI_BLACK(text):
    return f"\u001B[30m{text}\u001B[0m"


def ANSI_RED(text):
    return f"\u001B[31m{text}\u001B[0m"


def ANSI_GREEN(text):
    return f"\u001B[32m{text}\u001B[0m"


def ANSI_YELLOW(text):
    return f"\u001B[33m{text}\u001B[0m"


def ANSI_BLUE(text):
    return f"\u001B[34m{text}\u001B[0m"


def ANSI_PURPLE(text):
    return f"\u001B[35m{text}\u001B[0m"


def ANSI_CYAN(text):
    return f"\u001B[36m{text}\u001B[0m"


def ANSI_WHITE(text):
    return f"\u001B[37m{text}\u001B[0m"


ansi_rainbow_global_variable: int = 0


def ANSI_RAINBOW(text, reset_on=10):
    global ansi_rainbow_global_variable
    if reset_on == 0 or ansi_rainbow_global_variable % reset_on == 0:
        ansi_rainbow_global_variable = 0
    rainbow_str: str = ''
    for char in text:
        if char == ' ':
            rainbow_str += ' '
        elif ansi_rainbow_global_variable == 0:
            rainbow_str += ANSI_RED(char)
            ansi_rainbow_global_variable += 1
        elif ansi_rainbow_global_variable == 1:
            rainbow_str += ANSI_YELLOW(char)
            ansi_rainbow_global_variable += 1
        elif ansi_rainbow_global_variable == 2:
            rainbow_str += ANSI_GREEN(char)
            ansi_rainbow_global_variable += 1
        elif ansi_rainbow_global_variable == 3:
            rainbow_str += ANSI_BLUE(char)
            ansi_rainbow_global_variable += 1
        else:
            rainbow_str += ANSI_PURPLE(char)
            ansi_rainbow_global_variable = 0
    return rainbow_str
