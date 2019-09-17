import curses
import os
import re
import sys
import time
import pickle

from curses import wrapper
from curses.textpad import Textbox

import logo
from drink import Drink
from person import Person

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

def loadObjects(file):
    global stdscr
    data = None
    try:
        pickle_in = open(file,"rb")
        data = pickle.load(pickle_in)
    except:
        stdscr.addstr(f"Cant load data from {file}\n")
        stdscr.getch()
        return -1
    finally:
        pickle_in.close()
    return data


def saveObjects(file, data):
    global stdscr
    try:
        pickleOut = open(file,"wb")
        pickle.dump(data,pickleOut)
    except:
        stdscr.addstr(f"Cant save data to {file}\n")
        stdscr.refresh()
        return -1
    finally:
        pickleOut.close()

def getPeople():
    global people
    return people

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

def printTable(title,dataList, start=0, end=0, filterBy="" , selected=[], current = -1, normaltextFormatting = curses.A_NORMAL, selectedtextFormat = curses.A_REVERSE, currentTextFormat = curses.A_REVERSE):
    global stdscr
    clearScreen()
    decorationLines = 9
    minlines = decorationLines + 1
    tableWidth = calcTableWidth(title,dataList)
    if(tableWidth<16):
        tableWidth=16
    titleMargins=0
    tableMargins = 6
    if end == 0 or end > minlines-decorationLines:
        if curses.LINES>=minlines:
            end = curses.LINES-decorationLines+2
        else:
            stdscr.addstr("Resize terminal to atleast {minlines} Lines and {width} columns\n".format(minlines = minlines, width = tableWidth+tableMargins+3))
            isGoodSize = False
            while not isGoodSize:
                keyIn = stdscr.getch()
                if(keyIn == curses.KEY_RESIZE):
                    curses.update_lines_cols()
                    if curses.LINES >= minlines and curses.COLS >= tableWidth+tableMargins:
                        stdscr.resize(curses.LINES,curses.COLS)
                        isGoodSize = True
                        end = curses.LINES -decorationLines
                        clearScreen()

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
    if current >= end:
        end = current + 1
        start = end - (curses.LINES - decorationLines)
    elif current < start and current > 0:
        start -= 1
        end -= 1 
    for index,entry in enumerate(dataList):
        if index >= start and index < end:
            if index == current:
                stdscr.addstr("|")
                stdscr.addstr("{entry:^{width}}".format(entry=entry.displayName, width=tableWidth+tableMargins), currentTextFormat)
                stdscr.addstr("|\n")
            elif index in selected:
                stdscr.addstr("|")
                stdscr.addstr("{entry:^{width}}".format(entry=entry.displayName, width=tableWidth+tableMargins), selectedtextFormat)
                stdscr.addstr("|\n")
            else:
                stdscr.addstr("|")
                stdscr.addstr("{entry:^{width}}".format(entry=entry.displayName, width=tableWidth+tableMargins), normaltextFormatting)
                stdscr.addstr("|\n")
    stdscr.addstr(tableSeparator)
    stdscr.refresh()

def handleItemRows(choice,table):
    global stdscr
    keyIn = stdscr.getch()
    selected = False
    if keyIn == curses.KEY_DOWN and choice < len(table):
        choice += 1
    elif keyIn == curses.KEY_UP:
        choice -= 1
    elif keyIn == curses.KEY_ENTER or curses.ascii.isspace(keyIn) :
        selected = True
    elif curses.ascii.ctrl(keyIn) == 23 and curses.ascii.isctrl(keyIn): # CTRL + W (EXIT)
        choice = -1
    return choice, selected

def handleSingleSelectTable(title,dataList,filterRegex, choice=0, caption=""):
    global stdscr
    itemSelected = False
    while True:
        clearScreen()
        filteredTable = filterTable(dataList, filterRegex)
        if(choice == 0): # Filter row
            printTable(title,filteredTable,0,curses.LINES, filterRegex)
            stdscr.addstr(caption)
            keyIn = stdscr.getch()
            if(len(filterRegex) < 15): # max char limit for filter
                if (keyIn == curses.KEY_BACKSPACE):
                    filterRegex = filterRegex[:-1]
                elif (keyIn == curses.KEY_DC):
                    filterRegex = ""
                elif keyIn == curses.KEY_DOWN:
                    if(choice<len(filteredTable)):
                        choice += 1
                elif curses.ascii.ctrl(keyIn) == 23 and curses.ascii.isctrl(keyIn):
                    break
                elif keyIn == curses.KEY_ENTER or keyIn == 10 or keyIn == 13:
                    if len(filteredTable)>0:
                        choice = 1
                elif curses.ascii.isascii(keyIn):
                    filterRegex += chr(keyIn)
            else: # if at max chat limit
                if (keyIn == curses.KEY_BACKSPACE):
                    filterRegex = filterRegex[:-1]
                elif keyIn == curses.KEY_DOWN:
                    choice += 1
                elif curses.ascii.ctrl(keyIn) == 23 and curses.ascii.isctrl(keyIn):
                    break
        elif( choice > 0 and choice <= len(filteredTable) ): # Item rows
            printTable(title,filteredTable,0,0, filterRegex, [choice-1], choice-1)
            stdscr.addstr(caption)
            choice, itemSelected = handleItemRows(choice,filteredTable)
            if(itemSelected):
                return filteredTable[choice-1]
    return None

def handleMultiSelectTable(title,dataList,filterRegex, choice=0):
    global stdscr
    itemSelected = False
    selectedItems = []
    while True:
        clearScreen()
        selectedItemIDs = []
        filteredTable = filterTable(dataList, filterRegex)
        for index, item in enumerate(filteredTable):
            if item in selectedItems:
                selectedItemIDs.append(index)
        if(choice == 0): # Filter row
            printTable(title,filteredTable, 0, curses.LINES, filterRegex, selectedItemIDs, choice -1 , curses.A_DIM , curses.A_NORMAL)
            keyIn = stdscr.getch()
            if(len(filterRegex) < 15): # max char limit for filter
                if (keyIn == curses.KEY_BACKSPACE):
                    filterRegex = filterRegex[:-1]
                elif (keyIn == curses.KEY_DC):
                    filterRegex = ""
                elif keyIn == curses.KEY_DOWN:
                    if(choice<len(filteredTable)):
                        choice += 1
                elif curses.ascii.ctrl(keyIn) == 23 and curses.ascii.isctrl(keyIn):
                    break
                elif curses.ascii.isascii(keyIn):
                    filterRegex += chr(keyIn)
            else: # if at max chat limit
                if (keyIn == curses.KEY_BACKSPACE):
                    filterRegex = filterRegex[:-1]
                elif keyIn == curses.KEY_DOWN:
                    choice += 1
                elif curses.ascii.ctrl(keyIn) == 23 and curses.ascii.isctrl(keyIn): # CTRL+w (EXIT)
                    break
        elif( choice > 0 and choice <= len(filteredTable) ): # Item rows
            printTable(title,filteredTable, 0, curses.LINES, filterRegex, selectedItemIDs,choice -1 , curses.A_DIM , curses.A_NORMAL, curses.A_REVERSE)
            choice, itemSelected = handleItemRows(choice,filteredTable)
            if(itemSelected):
                if(filteredTable[choice - 1] in selectedItems):
                    selectedItems.remove(filteredTable[choice-1])
                    selectedItemIDs.remove(choice-1)
                else:
                    selectedItems.append(filteredTable[choice-1])
                    selectedItemIDs.append(choice-1)
                itemSelected = False
            elif (choice == -1):
                break
    return selectedItems
                
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

def addNewPerson(name="",team="",favDrink=None,PMUDrink="N/A"):
    global stdscr
    clearScreen()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    if not name:
        name = cursedInput("Enter name of person: ")
    if not team:
        team = cursedInput("Enter name of team person is in: ")
    if not favDrink:
        favDrink = handleSingleSelectTable("Drinks", drinks,"",0,"Select this persons favorite drink")
    people.append(Person(name,team,favDrink,PMUDrink))

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
    global currentChoice, start, end, people, drinks
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
            saveObjects(PEOPLE_FILE,people)
            saveObjects(DRINKS_FILE,drinks)
            stdscr.addstr(0,0,"Saved!")
            stdscr.getch()
        elif(currentChoice == 4): # View Settings
            pass
        elif(currentChoice == 5): # Exit application
            clearScreen()
            saveObjects(PEOPLE_FILE,people)
            saveObjects(DRINKS_FILE,drinks)
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()

            exit()

def handlePeopleMenu():
    global currentChoice, start, end
    stdscr.clear()
    while True:
        if(curses.LINES > len(peopleChoices)+1): # No pagination
            printMenu(peopleChoices,currentChoice)
        else:#Paginate
            if(end == len(peopleChoices)): # Initial menu list length based on terminal size
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
                removableItems = handleMultiSelectTable("People",people,"",0)
                for item in removableItems:
                    people.remove(item)
            elif(currentChoice == 2): # SORT table
                people.sort(key= lambda person: person.name)
                stdscr.addstr(3,37,"...Sorted!")
                stdscr.getch()
            elif(currentChoice == 3): # Reverse Table
                people.reverse()
                stdscr.addstr(4,25,"...Reversed!")
                stdscr.getch()
            elif(currentChoice == 4): # ASSIGN drink
                person = handleSingleSelectTable("People", people, "", 0,"Select a person to assign drink to")
                drink = handleSingleSelectTable("Drinks", drinks, "", 0 , f"Select drink to assign to {person.displayName}")
                person.favDrink = drink
            elif(currentChoice == 5): # ASSIGN PMU
                person = handleSingleSelectTable("People", people, "", 0,"Select a person to assign drink to")
                drink = handleSingleSelectTable("Drinks", drinks, "", 0 , f"Select drink to assign to {person.displayName}")
                person.PMUDrink = drink
            elif(currentChoice == 6): # View Table
                handleSingleSelectTable("People",people,"",0)
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
start = 0
end = len(menuChoices)

def main(stdscr):
    global people, drinks

    people = loadObjects(PEOPLE_FILE)
    drinks = loadObjects(DRINKS_FILE)

    while True:
        handleMainMenu()

if __name__ == "__main__":
    wrapper(main)
else:
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    people = loadObjects(PEOPLE_FILE)
    drinks = loadObjects(DRINKS_FILE)

