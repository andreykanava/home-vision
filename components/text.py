from curses import init_pair, color_pair

class text_ui():
    def add_text(stdscr, align, string, row=0, color=None, background=None):
        coords = align(stdscr, string, row)
        if color and background:
            init_pair(1, color, background)
            stdscr.attron(color_pair(1))
            stdscr.addstr(coords[0], coords[1], string)
            stdscr.attroff(color_pair(1))
        else:
            stdscr.addstr(coords[0], coords[1], string)