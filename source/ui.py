import curses

TABLE_DECORATION_LINES = 9
TABLE_MINIMUM_LINES = TABLE_DECORATION_LINES + 1

def promptResize(screen, lines,columns):
    screen.addstr("Resize terminal to atleast {height} Lines and {width} columns\n".format(
        height = lines, width = columns))
    isGoodSize = False

    while not isGoodSize:
        keyIn = screen.getch()
        if keyIn == curses.KEY_RESIZE:
            curses.update_lines_cols()
            if curses.LINES >= lines and curses.COLS >= columns:
                screen.resize(curses.LINES,curses.COLS)
                isGoodSize = True
                clearScreen(screen)

def clearScreen(screen):
    screen.clear()
    
def scrollDownMenu(selected, end, contentLines):
    end = selected + 1
    start = end - contentLines
    return start, end

def printDoubleSpacedMenu(screen, menu, selected):
    for index, choice in enumerate(menu):
        if index == selected:
            screen.addstr("\n\t")
            screen.addstr("[{index}] {choice}\n".format(index=index+1, choice=choice), curses.A_STANDOUT)
        else:
            screen.addstr("\n\t[{index}] {choice}\n".format(index=index+1, choice=choice))

def printSingleSpacedMenu(screen, menu, selected, start, end):
    for index, choice in enumerate(menu):
        if index >= start and index < end:
            if(index == selected):
                screen.addstr("\n\t")
                screen.addstr("[{index}] {choice}".format(index=index, choice=choice), curses.A_STANDOUT)
            else:
                screen.addstr("\n\t[{index}] {choice}".format(index=index, choice=choice))

def printMenu(screen, menu, selected = 0, start = 0, end = None):
    clearScreen(screen)
    contentLines = curses.LINES - 1
    end = contentLines
    if contentLines >= len(menu)*2: #Stylish option (no pagination, spaced options)
        printDoubleSpacedMenu(screen,menu,selected)
    else: # Short version for smaller terminals | possible pagination
        # Paginate
        if selected >= end: # Scroll Down
            start, end = scrollDownMenu(selected, end, contentLines)
        printSingleSpacedMenu(screen, menu, selected, start, end)
    screen.refresh()


def paginateTable(current, end):
    start = 0
    if current >= end:
        end = current + 1
        start = end - (curses.LINES - TABLE_DECORATION_LINES)
    elif current < start and current > 0:
        start -= 1
        end -= 1 
    return start, end
    
def printTableSeparator(screen, width):
    tableSeparator = "+"
    for i in range(width):
        tableSeparator += "-"
    tableSeparator += "+\n"
    screen.addstr(tableSeparator)

def printTableHeader(screen, title, width, filtertext):
    printTableSeparator(screen, width)
    screen.addstr("|{title:^{width}}|\n".format(title=title, width=width), curses.A_BOLD)
    printTableSeparator(screen, width)
    screen.addstr("|")
    screen.addstr("Filter:", curses.A_BOLD)
    screen.addstr("{filtertext:15}".format(filtertext = filtertext))
    screen.addstr("|\n")
    printTableSeparator(screen, width)

def printMultiColumnTableHeader(screen,title,width,filtertext):
    printTableSeparator(screen, width)
    screen.addstr("|{title:^{width}}|\n".format(title=title, width=width), curses.A_BOLD)
    printTableSeparator(screen, width)

def printItem(screen,entry,width,textFormatting,isNewLine=True,isFirstColumn=True):
    if isFirstColumn:
        screen.addstr("|")
    screen.addstr("{entry:^{width}}".format(
        entry=entry.displayName, width=width), textFormatting)
    if isNewLine:
        screen.addstr("|\n")

def printTable(screen, title, dataList, start=0, end=0,
    filterBy="", selected=[], current = -1, normaltextFormat = curses.A_NORMAL,
    selectedtextFormat = curses.A_REVERSE, currentTextFormat = curses.A_REVERSE):
    
    clearScreen(screen)

    tableWidth = calcTableWidth(title, dataList)
    if tableWidth < 16:
        tableWidth = 16
    titleMargins = 0
    tableMargins = 6

    if end == 0 or end > TABLE_MINIMUM_LINES-TABLE_DECORATION_LINES:
        if curses.LINES>=TABLE_MINIMUM_LINES:
            end = curses.LINES-TABLE_DECORATION_LINES+2
        else:
            promptResize(screen,TABLE_MINIMUM_LINES,tableWidth+tableMargins)
            end = curses.LINES - TABLE_DECORATION_LINES

    printTableHeader(screen, title, tableWidth + tableMargins + titleMargins, filterBy)

    start, end = paginateTable(current, end)

    for index, entry in enumerate(dataList):
        if index >= start and index < end:
            if index == current:
                printItem(screen,entry,tableWidth + tableMargins,currentTextFormat)
            elif index in selected:
                printItem(screen,entry,tableWidth + tableMargins,selectedtextFormat)
            else:
                printItem(screen,entry,tableWidth + tableMargins,normaltextFormat)
    
    printTableSeparator(screen, tableWidth + tableMargins + titleMargins)
    screen.refresh()

def printMultiColumnTable(screen, title, dataLists=[], start=0, end=0,
    filterBy="", selected=[], current = -1, normaltextFormat = curses.A_NORMAL,
    selectedtextFormat = curses.A_REVERSE, currentTextFormat = curses.A_REVERSE):
    
    clearScreen(screen)
    titleMargins = 0
    tableMargins = 6
    tableWidth = 0
    for dataList in dataLists:
        tableWidth += (calcTableWidth(title, dataList) + tableMargins + titleMargins)
    if end == 0 or end > TABLE_MINIMUM_LINES-TABLE_DECORATION_LINES:
        if curses.LINES>=TABLE_MINIMUM_LINES:
            end = curses.LINES-TABLE_DECORATION_LINES+2
        else:
            promptResize(screen,TABLE_MINIMUM_LINES,tableWidth+tableMargins)
            end = curses.LINES - TABLE_DECORATION_LINES

    printMultiColumnTableHeader(screen, title, ((tableWidth + tableMargins + titleMargins)*len(dataLists))+len(dataLists)-1, filterBy)

    start, end = paginateTable(current, end)
    for i in range(start,end):
        for index, dataList in enumerate(dataLists):
            if i >= start and i < end:
                if i < len(dataList):
                    if i == current:
                        printItem(screen,dataList[i],
                        tableWidth + tableMargins,currentTextFormat
                        ,index==len(dataLists)-1,index==0)
                    elif i in selected:
                        printItem(screen,dataList[i],tableWidth + tableMargins,selectedtextFormat,index==len(dataLists)-1)
                    else:
                        printItem(screen,dataList[i],tableWidth + tableMargins,normaltextFormat,index==len(dataLists)-1)
    
    printTableSeparator(screen, ((tableWidth + tableMargins + titleMargins)*len(dataLists))+len(dataLists)-1)
    screen.refresh()

def calcTableWidth(title,dataList):
    width = len(title)
    for data in dataList:
        if width < len(data.displayName):
            width = len(data.displayName)
    return width

def cursedInput(screen, query):
    clearScreen(screen)
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    screen.addstr(query)
    temp = screen.getstr().decode("utf-8")
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    return temp
