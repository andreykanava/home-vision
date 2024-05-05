def center_vertical(stdscr, string, row=0):
    h, w = stdscr.getmaxyx()

    x = w//2 - len(string)//2
    y = h//2 + row

    return y, x

def left_vertical_scedule(stdscr, string, row=0):
    h, w = stdscr.getmaxyx()

    x = w//30# - len(string)//2
    y = h//10 + row

    return y, x

def left_vertical(stdscr, string, row=0):
    h, w = stdscr.getmaxyx()

    x = w//30# - len(string)//2
    y = h//2 + row

    return y, x