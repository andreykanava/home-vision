from curses import color_pair, init_pair

class menu_ui():
    def menu(stdscr, align, list, color, background, row=0, selected=0):
        init_pair(1, color, background)
        for list_row, string in enumerate(list):
            coords = align(stdscr, string, list_row+row)
            if list_row == selected:
                stdscr.attron(color_pair(1))
                stdscr.addstr(coords[0], coords[1], string)
                stdscr.attroff(color_pair(1))
            else:
                stdscr.addstr(coords[0], coords[1], string)
    
    def scroll_menu(stdscr, align, list, limit, color, background, selected = 0):
        init_pair(1, color, background)
        start_index = max(0, selected - limit // 2)
        end_index = min(start_index + limit, len(list))
        start_index = max(0, end_index - limit)
        for i in range(start_index, end_index):
            row = i - start_index
            string = list[i]
            coords = align(stdscr, string, row)
            if i == selected:
                stdscr.attron(color_pair(1))
                stdscr.addstr(coords[0], coords[1], string)
                stdscr.attroff(color_pair(1))
            else:
                stdscr.addstr(coords[0], coords[1], string)