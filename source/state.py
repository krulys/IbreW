import pickle

class State:
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
