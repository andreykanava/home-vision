import curses
#from screens.test_text import text_screen
from screens.start_menu import main_screen

curses.wrapper(main_screen)