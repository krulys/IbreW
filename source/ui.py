import curses

class UI:
    def clearScreen():
        global stdscr
        stdscr.clear()
    
    def printMenu(menu, selected = 0, start = 0 , end = None):
        global stdscr
        clearScreen()
        contentLines = curses.LINES - 1
        end = contentLines
        if contentLines >= len(menu)*2: #Stylish option| no pagination
            for index, choice in enumerate(menu):
                if(index == selected):
                    stdscr.addstr("\n\t")
                    stdscr.addstr("[{index}] {choice}\n".format(index=index+1, choice=choice), curses.A_STANDOUT)
                else:
                    stdscr.addstr("\n\t[{index}] {choice}\n".format(index=index+1, choice=choice))
        else: # Short version for smaller terminals | possible pagination
            # Paginate
            if selected >= end: # Scroll Down
                end = selected + 1
                start = end - contentLines
            for index, choice in enumerate(menu):
                if index>=start and index < end:
                    if(index == selected):
                        stdscr.addstr("\n\t")
                        stdscr.addstr("[{index}] {choice}".format(index=index, choice=choice), curses.A_STANDOUT)
                    else:
                        stdscr.addstr("\n\t[{index}] {choice}".format(index=index, choice=choice))
        stdscr.refresh()

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

    def calcTableWidth(title,dataList):
        width = len(title)
        for data in dataList:
            if (width<len(data.displayName)):
                width=len(data.displayName)
        return width


    