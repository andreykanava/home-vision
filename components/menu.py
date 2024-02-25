from curses import color_pair, init_pair

class menu_ui():
    def menu(stdscr, align, list, color, background, selected=0):
        init_pair(1, color, background)
        for row, string in enumerate(list):
            coords = align(stdscr, string, row)
            if row == selected:
                stdscr.attron(color_pair(1))
                stdscr.addstr(coords[0], coords[1], string)
                stdscr.attroff(color_pair(1))
            else:
                stdscr.addstr(coords[0], coords[1], string)