from curses import init_pair, color_pair
import curses


class text_ui():
    def add_text(stdscr, align, string, row=0, color=None, background=None):
        coords = align(stdscr, string, row)
        if color and background:
            if color == curses.COLOR_BLACK and background == curses.COLOR_WHITE:
                init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
                stdscr.attron(color_pair(1))
                stdscr.addstr(coords[0], coords[1], string)
                stdscr.attroff(color_pair(1))
            elif color == curses.COLOR_WHITE and background == curses.COLOR_GREEN:
                init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
                stdscr.attron(color_pair(2))
                stdscr.addstr(coords[0], coords[1], string)
                stdscr.attroff(color_pair(2))
            elif color == curses.COLOR_WHITE and background == curses.COLOR_RED:
                init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
                stdscr.attron(color_pair(3))
                stdscr.addstr(coords[0], coords[1], string)
                stdscr.attroff(color_pair(3))
            else:
                init_pair(4, color, background)
                stdscr.attron(color_pair(1))
                stdscr.addstr(coords[0], coords[1], string)
                stdscr.attroff(color_pair(1))
        else:
            stdscr.addstr(coords[0], coords[1], string)