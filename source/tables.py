import curses
import curses.ascii
import re
from ui import UI as UI

class Tables:

    FILTER_CHAR_LIMIT = 15

    def handleFilterField(screen,filterRegex,choice,filteredTable):
        keyIn = screen.getch()
        if(len(filterRegex) < Tables.FILTER_CHAR_LIMIT): # max char limit for filter
            if (keyIn == curses.KEY_BACKSPACE):
                filterRegex = filterRegex[:-1]
            elif (keyIn == curses.KEY_DC):
                filterRegex = ""
            elif keyIn == curses.KEY_DOWN:
                if(choice<len(filteredTable)):
                    choice += 1
            elif curses.ascii.ctrl(keyIn) == 23 and curses.ascii.isctrl(keyIn):
                return -1, filterRegex
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
                return -1, filterRegex

        return choice,filterRegex

    def handleSingleSelectTable(screen, title,dataList,filterRegex, choice=0, caption=""):
        itemSelected = False
        while True:
            UI.clearScreen(screen)

            filteredTable = Tables.filterTable(dataList, filterRegex)

            if(choice == 0): # Filter row
                UI.printTable(screen,title,filteredTable,0,curses.LINES, filterRegex)
                screen.addstr(caption)
                choice, filterRegex = Tables.handleFilterField(screen,filterRegex,choice,filteredTable)

            elif( choice > 0 and choice <= len(filteredTable) ): # Item rows
                UI.printTable(screen, title,filteredTable,0,0, filterRegex, [choice-1], choice-1)
                screen.addstr(caption)
                choice, itemSelected = Tables.handleItemRows(screen,choice,filteredTable)
                if(itemSelected):
                    return filteredTable[choice-1]

            if choice == -1 :
                break

        return None

    def handleMultiSelectTable(screen, title,dataList,filterRegex, choice=0):
        itemSelected = False
        selectedItems = []
        while True:
            UI.clearScreen(screen)
            selectedItemIDs = []
            filteredTable = Tables.filterTable(dataList, filterRegex)
            for index, item in enumerate(filteredTable):
                if item in selectedItems:
                    selectedItemIDs.append(index)
            if(choice == 0): # Filter row
                UI.printTable(screen,title,filteredTable, 0, curses.LINES,
                              filterRegex, selectedItemIDs, choice -1 , curses.A_DIM ,
                              curses.A_NORMAL)
                choice, filterRegex = Tables.handleFilterField(screen,filterRegex,choice,filteredTable)

            elif( choice > 0 and choice <= len(filteredTable) ): # Item rows
                UI.printTable(screen,title,filteredTable, 0,
                              curses.LINES, filterRegex, selectedItemIDs,choice -1 ,
                              curses.A_DIM , curses.A_NORMAL, curses.A_REVERSE)
                choice, itemSelected = Tables.handleItemRows(screen, choice,filteredTable)

                if(itemSelected):
                    if(filteredTable[choice - 1] in selectedItems):
                        selectedItems.remove(filteredTable[choice-1])
                        selectedItemIDs.remove(choice-1)
                    else:
                        selectedItems.append(filteredTable[choice-1])
                        selectedItemIDs.append(choice-1)
                    itemSelected = False
                    
            if (choice == -1):
                break
        return selectedItems

    def handleItemRows(screen,choice,table):
        keyIn = screen.getch()
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


    def filterTable(dataList,regex):
        regex = re.compile(regex, re.IGNORECASE)
        newDataList = []
        for data in dataList:
            if regex.match(data.displayName) != None:
                newDataList.append(data)
        return newDataList
    
    def findPeopleByTeam(team,people):
        tempPeople = []
        for person in people:
            if person.team == team:
                tempPeople.append(person)
        return tempPeople