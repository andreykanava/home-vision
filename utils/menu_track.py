from curses import KEY_UP, KEY_DOWN, KEY_ENTER

def menu_select(stdscr, menu, selected = 0):
    key = stdscr.getch()

    if key == KEY_UP and selected > 0:
        return selected - 1
    elif key == KEY_UP and selected == 0:
        return len(menu)-1
    elif key == KEY_DOWN and selected < len(menu)-1:
        return selected + 1
    elif key == KEY_DOWN and selected == len(menu) -1:
        return 0
    elif key == KEY_ENTER or key in [10, 13]:
        return "Enter"
    else:
        return selected