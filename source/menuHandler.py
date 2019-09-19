import curses
from ui import UI as UI
from menuOptions import MenuOptions as menuOptions
from person import Person
from state import State as state
from tables import Tables as tables

class MenuHandler:

    def handleMainMenu(screen,menuChoices, currentChoice, people=[], drinks=[]):
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
                initiator = tables.handleSingleSelectTable(screen,"People",people,"",0,"Choose yourself from this list")
                teamMembers = tables.findPeopleByTeam(initiator.team,people)
                #TODO finish this
                pass

            elif currentChoice == 1: # People Submenu
                peopleChoice = 0
                while peopleChoice != -1:
                    peopleChoice = MenuHandler.handlePeopleMenu(
                        screen,
                        menuOptions.getPeopleOptions(),
                        peopleChoice,
                        people,
                        drinks)

            elif currentChoice == 2: # Drinks Submenu
                drinksChoice = 0
                while drinksChoice != -1:
                    drinksChoice = MenuHandler.handleDrinksMenu(
                        screen,
                        menuOptions.getDrinkOptions(),
                        drinksChoice,
                        people,
                        drinks)

            elif currentChoice == 3: # View all tables
                #TODO implement
                pass

            elif currentChoice == 4: # Save all tables
                state.saveObjects(state.PEOPLE_FILE,people)
                state.saveObjects(state.DRINKS_FILE,drinks)
                screen.addstr(0,0,"Saved!")
                screen.getch()

            elif currentChoice == 5: # View Settings
                #TODO implement
                pass

            elif currentChoice == 6: # Exit application
                currentChoice = -1
        return currentChoice


    def handlePeopleMenu(screen,peopleMenuOptions, currentChoice, people=[], drinks=[]):
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
                state.addNewPerson(screen)

            elif currentChoice == 1: # REMOVE person
                state.removePeople(screen)

            elif currentChoice == 2: # SORT table
                state.sortPeople()
                screen.addstr(3,37,"...Sorted!")
                screen.getch()

            elif currentChoice == 3: # Reverse Table
                state.reversePeople()
                screen.addstr(4,25,"...Reversed!")
                screen.getch()

            elif currentChoice == 4: # ASSIGN drink
                state.assignFavDrinkPreference(screen)

            elif currentChoice == 5: # ASSIGN Pick me up drink
                state.assignPickMeUpDrinkPreference(screen)

            elif currentChoice == 6: # View Table
                tables.handleSingleSelectTable(screen,"People",people,"",0)
                pass

            elif currentChoice == 7: # Go back
               currentChoice = -1
        return currentChoice


    def handleDrinksMenu(screen,drinkMenuOptions, currentChoice, people=[], drinks=[]):
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
                screen.addstr(3,37,"...Sorted!")
                screen.getch()

            elif currentChoice == 3: # Reverse Table
                state.reverseDrinks()
                screen.addstr(4,25,"...Reversed!")
                screen.getch()

            elif currentChoice == 4: # ASSIGN drink
                state.assignFavDrinkPreference(screen)

            elif currentChoice == 5: # ASSIGN Pick me up drink
                state.assignPickMeUpDrinkPreference(screen)

            elif currentChoice == 6: # View Table
                tables.handleSingleSelectTable(screen,"Drinks",drinks,"",0)
                pass

            elif currentChoice == 7: # Go back
               currentChoice = -1

        return currentChoice