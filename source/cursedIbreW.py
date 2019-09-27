import curses
import curses.ascii
import os
import re
import sys
import time

from curses import wrapper

# TODO import logo (convert to cursed)
from source.state import State
import source.menuHandler as menuHandler
import source.menuOptions as menuOptions
import source.ui as UI

def initializeScreen():
    screen = curses.initscr()
    return screen

def deinitializeScreen(screen):
    screen.endwin()


def exitApp(state, screen):
    UI.clearScreen(screen)
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    state.saveObjectsToDB()
    exit()

def main(screen):
    curses.curs_set(False)
    state = State()
    state.loadObjectsFromDB()
    currentChoice = 0
    while currentChoice != -1:
        currentChoice = menuHandler.handleMainMenu(state,
            screen,
            menuOptions.getMainMenuOptions(),
            currentChoice)
    exitApp(state, screen)

screen = initializeScreen()

if __name__ == "__main__":
    wrapper(main)
else:
    state = State()
    state.loadObjectsFromDB()

