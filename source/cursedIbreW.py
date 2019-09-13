import sys
import time
import logo
import curses
import re
from curses.textpad import Textbox
from person import Person
from drink import Drink
version= "v0.5"

PEOPLE_FILE = "dbs/people.db"
DRINKS_FILE = "dbs/drinks.db"

people = []
drinks = []

stdscr =""
currentChoice = 0
menuChoices = [
        "Manage/View People",
        "Manage/View Drinks",
        "View all tables",
        "Save all tables",
        "Settings",
        "Exit"] # Ensure this element comes last
peopleChoices = [
    "Add person",
    "Remove Person",
    "Sort table alphabetically",
    "Reverse table",
    "Assign favorite drink to person",
    "Assign pick-me-up drink to person",
    "View People Table",
    "Go back"] # Ensure this element comes last
drinkChoices = [
    "Add drink",
    "Remove drink",
    "Sort table alphabetically",
    "Reverse table",
    "Assign drink to person",
    "View Drinks Table",
    "Go back"] # Ensure this element comes last

def filterTable(dataList,regex):
    regex = re.compile(regex, re.IGNORECASE)
    newDataList = []
    for data in dataList:
        if regex.match(data.displayName) != None:
            newDataList.append(data)
    return newDataList

def calcTableWidth(title,dataList):
        width = len(title)
        for data in dataList:
            if (width<len(data.displayName)):
                width=len(data.displayName)
        return width

def printTable(title,dataList, Indexed=False, filterBy="" , selected=None):
    global stdscr
    clearScreen()
    tableWidth = calcTableWidth(title,dataList)
    if(tableWidth<16):
        tableWidth=16
    titleMargins=0
    if Indexed:
        tableWidth+=5
        titleMargins+=5
    tableMargins = 6
    tableSeparator = "+"
    for i in range(tableWidth+tableMargins+titleMargins):
        tableSeparator+="-"
    tableSeparator += "+\n"
    stdscr.addstr(tableSeparator)
    stdscr.addstr("|{title:^{width}}|\n".format(title=title, width=tableWidth+tableMargins+titleMargins),curses.A_BOLD)
    stdscr.addstr(tableSeparator)
    stdscr.addstr("|")
    stdscr.addstr("Filter:",curses.A_BOLD)
    stdscr.addstr("{filtertext:15}".format(filtertext = filterBy))
    stdscr.addstr("|\n")
    stdscr.addstr(tableSeparator)
    for index,entry in enumerate(dataList):
        if Indexed:
            if selected == index:
                stdscr.addstr("|")
                stdscr.addstr("[{index:<2}] {entry:^{width}}".format(index = index, entry=entry.displayName, width=tableWidth+tableMargins), curses.A_REVERSE)
                stdscr.addstr("|\n")
            else:
                stdscr.addstr("|")
                stdscr.addstr("[{index:<2}] {entry:^{width}}".format(index = index, entry=entry.displayName, width=tableWidth+tableMargins))
                stdscr.addstr("|\n")
        else:
            if selected == index:
                stdscr.addstr("|")
                stdscr.addstr("{entry:^{width}}".format(entry=entry.displayName, width=tableWidth+tableMargins), curses.A_REVERSE)
                stdscr.addstr("|\n")
            else:
                stdscr.addstr("|")
                stdscr.addstr("{entry:^{width}}".format(entry=entry.displayName, width=tableWidth+tableMargins))
                stdscr.addstr("|\n")
    stdscr.addstr(tableSeparator+"\n")
    stdscr.refresh()

def handleItemRows(choice,table):
    global stdscr
    keyIn = stdscr.getkey()
    selected = False
    if keyIn == "KEY_DOWN" and choice < len(table):
        choice += 1
    elif keyIn == "KEY_UP":
        choice -= 1
    elif keyIn == "\n" or keyIn ==" " :
        selected = True
    elif keyIn == "q":
        choice = -1
    return choice, selected

def handleTables(title,dataList,filterRegex, choice=0):
    global stdscr
    itemSelected = False
    selectedItemIDs = []
    while True:
        clearScreen()
        filteredTable = filterTable(dataList, filterRegex)
        if(choice == 0): # Filter row
            printTable(title,filteredTable, False, filterRegex)
            keyIn = stdscr.getkey()
            if(len(filterRegex) < 15): # max char limit for filter
                if (keyIn == "KEY_BACKSPACE"):
                    filterRegex = filterRegex[:-1]
                elif (keyIn == "KEY_DELETE"):
                    filterRegex = ""
                elif keyIn == "KEY_DOWN":
                    if(choice<len(filteredTable)):
                        choice += 1
                elif keyIn == "KEY_ESC":
                    break
                elif keyIn != "KEY_LEFT" and keyIn != "KEY_RIGHT" and keyIn != "KEY_UP":
                    filterRegex += keyIn
            else: # if at max chat limit
                if (keyIn == "KEY_BACKSPACE"):
                    filterRegex = filterRegex[:-1]
                elif keyIn == "KEY_DOWN":
                    choice += 1
                elif keyIn == "KEY_ESC":
                    break
        elif( choice > 0 and choice <= len(filteredTable) ): # Item rows
            printTable(title,filteredTable, False, filterRegex, choice-1)
            choice, itemSelected = handleItemRows(choice,filteredTable)
            if(itemSelected):
                selectedItemIDs.append(choice-1)
                itemSelected = False
            elif(choice == -1):
                break
        
            

def cursedInput(Query):
    global stdscr
    clearScreen()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    stdscr.addstr(Query)
    temp = stdscr.getstr().decode("utf-8")
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return temp

def addNewPerson():
    global stdscr
    clearScreen()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    name = cursedInput("Enter name of person: ")
    team = cursedInput("Enter name of team person is in: ")

def clearScreen():
    global stdscr
    stdscr.clear()

def printMenu(menu, selected = 0, start = 0 , end = None):
    global stdscr
    if end == None:
        end = len(menu)
    stdscr.clear()
    if curses.LINES-1 >= len(menu)*2:
        for index, choice in enumerate(menu):
            if(index == selected):
                stdscr.addstr("\n\t")
                stdscr.addstr("[{index}] {choice}\n".format(index=index+1, choice=choice), curses.A_STANDOUT)
            else:
                stdscr.addstr("\n\t[{index}] {choice}\n".format(index=index+1, choice=choice))
    else: # Short version for smaller terminals
        selected -= start
        for index, choice in enumerate(menu[start:end]):
            if(index == selected):
                stdscr.addstr("\n\t")
                stdscr.addstr("[{index}] {choice}".format(index=index+1+start, choice=choice), curses.A_STANDOUT)
            else:
                stdscr.addstr("\n\t[{index}] {choice}".format(index=index+1+start, choice=choice))
    stdscr.refresh()

def handleMainMenu():
    global currentChoice, start, end
    stdscr.clear()
    
    if(curses.LINES-1 > len(menuChoices)): # No pagination
        printMenu(menuChoices,currentChoice)
    else:#Paginate
        if(end == len(menuChoices)): # Initial menu list lenght based on terminal size
            end = curses.LINES-2
        printMenu(menuChoices,currentChoice,start,end+1)
    input = stdscr.getkey()
    if(input.isdigit() and int(input) > 0 and int(input) <=len(menuChoices)):
        currentChoice = int(input) -1
        input = " "
    if(input == "KEY_DOWN" and currentChoice < len(menuChoices)-1):
        currentChoice+=1
        if(curses.LINES-1 < len(menuChoices) and end < len(menuChoices)-1 and currentChoice == end): # Go down a page
            start += 1
            end += 1
    elif(input == "KEY_UP" and currentChoice > 0):
        currentChoice-=1
        if(curses.LINES-1 < len(menuChoices) and start > 0 and currentChoice==start): # Go up a page
            start -= 1
            end -= 1
    elif(input == "\n" or input ==" "): # ENTER key or SPACE key
        if(currentChoice == 0):
            currentChoice = 0
            start = 0
            end = curses.LINES-2
            handlePeopleMenu()
        elif(currentChoice == 1):
            #handle drinks
            pass
        elif(currentChoice == 2): # View all tables
            pass
        elif(currentChoice == 3): # Save all tables
            pass
        elif(currentChoice == 4): # View Settings
            pass
        elif(currentChoice == 5): # Exit application
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            exit()

def handlePeopleMenu():
    global currentChoice, start, end
    stdscr.clear()
    while True:
        if(curses.LINES-1 > len(peopleChoices)): # No pagination
            printMenu(peopleChoices,currentChoice)
        else:#Paginate
            if(end == len(peopleChoices)): # Initial menu list lenght based on terminal size
                end = curses.LINES-2
            printMenu(peopleChoices,currentChoice,start,end+1)
        input = stdscr.getkey()
        if(input.isdigit() and int(input) > 0 and int(input) <=len(peopleChoices)):
            currentChoice = int(input) -1
            input = " "
        if(input == "KEY_DOWN" and currentChoice < len(peopleChoices)-1):
            currentChoice+=1
            if(curses.LINES-1 < len(peopleChoices) and end < len(peopleChoices)-1 and currentChoice == end): # Go down a page
                start += 1
                end += 1
        elif(input == "KEY_UP" and currentChoice > 0):
            currentChoice-=1
            if(curses.LINES-1 < len(peopleChoices) and start > 0 and currentChoice==start): # Go up a page
                start -= 1
                end -= 1
        elif(input == "\n" or input ==" "): # ENTER key or SPACE key
            if(currentChoice == 0): # ADD person
                addNewPerson()
            elif(currentChoice == 1): # REMOVE person
                pass
            elif(currentChoice == 2): # SORT table
                pass
            elif(currentChoice == 3): # Reverse Table
                pass
            elif(currentChoice == 4): # ASSIGN drink
                pass
            elif(currentChoice == 5): # ASSIGN PMU
                pass
            elif(currentChoice == 6): # View Table
                handleTables("People",people,"",0)
                pass
            elif(currentChoice == 7): # Go back
                currentChoice = 0
                start = 0
                end = curses.LINES-2
                break
#----SETUP
stdscr = curses.initscr()
curses.start_color()
curses.curs_set(False)
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
#----START
start = 0
end = len(menuChoices)
people.append(Person("David","david", "Academy", None))
people.append(Person("Henry","henry", "Academy", None))
people.append(Person("Dave","dave", "Academy", None))
while True:
    handleMainMenu()
    
