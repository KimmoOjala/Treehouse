import sys
from entry import Entry
from search import Search

from collections import OrderedDict


def menu_loop():
    """Show the menu"""
    while(True):
        Entry().clear_screen()
        print('''\n\nWORK LOG\nWhat would you like to do?''')
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input("\nAction: ")
        if choice in menu:
            menu[choice]()
        else:
            choice = input('Please enter {}, {}, {} or {}: '.format(
                           menu.keys()[0],
                           menu.keys()[1],
                           menu.keys()[2])
                           ).lower().strip()


def quit_program():
    '''Quit program'''
    print("Bye")
    sys.exit()


menu = OrderedDict([
    ('a', Entry().add_entry),
    ('b', Search().choose_search),
    ('c', quit_program)
])

if __name__ == '__main__':
    Entry().initialize()
    menu_loop()
