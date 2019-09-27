import curses
import source.ui as UI
import source.menuOptions as menuOptions
from source.person import Person
from source.state import State as state
from source.tables import Tables as tables
from source.brewRound import BrewRound

def handleMainMenu(state, screen,menuChoices, currentChoice):
    screen.clear()
    UI.printMenu(screen, menuChoices,currentChoice)
    input = screen.getkey()
    if input.isdigit() and int(input) > 0 and int(input) <=len(menuChoices):
        currentChoice = int(input) -1
        input = " "

    if input == "KEY_DOWN" and currentChoice < len(menuChoices)-1:
        currentChoice+=1

    elif input == "KEY_UP" and currentChoice > 0:
        currentChoice-=1

    elif input == "\n" or input ==" ": # ENTER key or SPACE key
        if currentChoice == 0: # Start round
            initiator = tables.handleSingleSelectTable(screen,"People",state._people,"",0,"Choose yourself from this list")
            teamMembers = tables.findPeopleByTeam(initiator.team,state._people)
            teamMembers.remove(initiator)
            participants = tables.handleMultiSelectTable(screen,"Team members",teamMembers,"")
            bRound = BrewRound(-1,initiator,participants)
            state._rounds.append(bRound)
            screen.clear()
            screen.getch()
            screen.addstr(str(state.saveRoundsToDB(screen)))
            screen.getch()
            UI.printMultiColumnTable(screen,"Brew Round",[bRound.getPeople(),bRound.getDrinks()])
            screen.getch()
            #TODO finish this
            pass

        elif currentChoice == 1: # People Submenu
            peopleChoice = 0
            while peopleChoice != -1:
                peopleChoice = handlePeopleMenu(state,
                    screen,
                    menuOptions.getPeopleOptions(),
                    peopleChoice)

        elif currentChoice == 2: # Drinks Submenu
            drinksChoice = 0
            while drinksChoice != -1:
                drinksChoice = handleDrinksMenu(state,
                    screen,
                    menuOptions.getDrinkOptions(),
                    drinksChoice)

        elif currentChoice == 3: # View all tables
            #TODO implement
            pass

        elif currentChoice == 4: # Save all tables
            state.saveObjectsToDB()
            screen.addstr(0,0,"Saved!")
            screen.getch()

        elif currentChoice == 5: # View Settings
            #TODO implement
            pass

        elif currentChoice == 6: # Exit application
            currentChoice = -1
    return currentChoice

def handlePeopleMenu(state,screen,peopleMenuOptions, currentChoice):
    screen.clear()
    UI.printMenu(screen, peopleMenuOptions,currentChoice)
    input = screen.getkey()
    if input.isdigit() and int(input) > 0 and int(input) <=len(peopleMenuOptions): # Go-to option
        currentChoice = int(input) -1
        input = " "
        
    if input == "KEY_DOWN" and currentChoice < len(peopleMenuOptions)-1:
        currentChoice+=1

    elif input == "KEY_UP" and currentChoice > 0:
        currentChoice-=1

    elif input == "\n" or input ==" ": # ENTER key or SPACE key
        if currentChoice == 0: # ADD person
            state.addNewPerson(state, screen)

        elif currentChoice == 1: # REMOVE person
            state.removePeople(state, screen)

        elif currentChoice == 2: # SORT table
            state.sortPeople()
            #TODO fix pagination
            screen.addstr(3,37,"...Sorted!")
            screen.getch()

        elif currentChoice == 3: # Reverse Table
            state.reversePeople()
            #TODO fix pagination
            screen.addstr(4,25,"...Reversed!")
            screen.getch()

        elif currentChoice == 4: # ASSIGN drink
            state.assignFavDrinkPreference(screen)

        elif currentChoice == 5: # View Table
            tables.handleSingleSelectTable(screen,"People",state._people,"",0)
            pass

        elif currentChoice == 6: # Go back
            currentChoice = -1
    return currentChoice

def handleDrinksMenu(state,screen,drinkMenuOptions, currentChoice):
        screen.clear()
        UI.printMenu(screen, drinkMenuOptions,currentChoice)
        input = screen.getkey()
        if input.isdigit() and int(input) > 0 and int(input) <=len(drinkMenuOptions): # Go-to option
            currentChoice = int(input) -1
            input = " "

        if input == "KEY_DOWN" and currentChoice < len(drinkMenuOptions)-1:
            currentChoice+=1

        elif input == "KEY_UP" and currentChoice > 0:
            currentChoice-=1

        elif input == "\n" or input ==" ": # ENTER key or SPACE key
            if currentChoice == 0: # ADD person
                state.addNewDrink(screen)

            elif currentChoice == 1: # REMOVE person
                state.removeDrinks(screen)

            elif currentChoice == 2: # SORT table
                state.sortDrinks()
                #TODO fix pagination
                screen.addstr(3,37,"...Sorted!")
                screen.getch()

            elif currentChoice == 3: # Reverse Table
                state.reverseDrinks()
                #TODO fix pagination
                screen.addstr(4,25,"...Reversed!")
                screen.getch()

            elif currentChoice == 4: # ASSIGN drink
                state.assignFavDrinkPreference(screen)

            elif currentChoice == 5: # View Table
                tables.handleSingleSelectTable(screen,"Drinks",state._drinks,"",0)

            elif currentChoice == 6: # Go back
               currentChoice = -1

        return currentChoice