from curses import KEY_UP, KEY_DOWN, KEY_ENTER
import RPi.GPIO as GPIO

def menu_select(stdscr, menu, selected = 0):
    L1 = 5
    L2 = 6
    L3 = 13
    L4 = 19

    C1 = 12
    C2 = 16
    C3 = 20
    C4 = 21

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(L1, GPIO.OUT)
    GPIO.setup(L2, GPIO.OUT)
    GPIO.setup(L3, GPIO.OUT)
    GPIO.setup(L4, GPIO.OUT)

    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    #            ^` ^l      ^o  ^e ^`           ^o  ^a   ^a ^b   ^o     ^o             
    key_states = {
        '1': False, '2': False, '3': False, 'A': False,
        '4': False, '5': False, '6': False, 'B': False,
        '7': False, '8': False, '9': False, 'C': False,
        '*': False, '0': False, '#': False, 'D': False
    }
    def readLine(line, characters):
        pressed_key = None
        GPIO.output(line, GPIO.HIGH)
        for i, char in enumerate(characters):
            if GPIO.input([C1, C2, C3, C4][i]) == 1:
                if not key_states[char]:
                    print(char)
                    pressed_key = char
                    key_states[char] = True
            else:
                key_states[char] = False
        GPIO.output(line, GPIO.LOW)
        return pressed_key
    
    pressed_key = None
    pressed_key = readLine(L1, ["1", "2", "3", "A"]) or pressed_key
    pressed_key = readLine(L2, ["4", "5", "6", "B"]) or pressed_key
    pressed_key = readLine(L3, ["7", "8", "9", "C"]) or pressed_key
    pressed_key = readLine(L4, ["*", "0", "#", "D"]) or pressed_key
    if pressed_key is not None:
        if pressed_key == "2":
            key = KEY_UP
        elif pressed_key == "5":
            key = KEY_ENTER
        elif pressed_key == "8":
            key = KEY_DOWN
        else:
            key = stdscr.getch()
    else:
        key = stdscr.getch()

    if key == KEY_UP and selected > 0:
        GPIO.cleanup()
        return selected - 1
    elif key == KEY_UP and selected == 0:
        GPIO.cleanup()
        return len(menu)-1
    elif key == KEY_DOWN and selected < len(menu)-1:
        GPIO.cleanup()
        return selected + 1
    elif key == KEY_DOWN and selected == len(menu) -1:
        GPIO.cleanup()
        return 0
    elif key == KEY_ENTER or key in [10, 13]:
        GPIO.cleanup()
        return "Enter"
    else:
        GPIO.cleanup()
        return selected