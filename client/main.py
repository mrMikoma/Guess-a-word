from time import sleep
from src.menu import *
from src.connectRPC import *
from src.connectToMaster import *
from src.connectToWorker import *
from src.chatChannel import *

###
# References:
# 
#
###

COLOR_GREEN = "\033[92m"  
COLOR_YELLOW = "\033[93m"  
COLOR_RED = "\033[91m"  
COLOR_BLUE = '\033[34m'
COLOR_RESET = "\033[0m"  # Reset color to default

def main():
    print(COLOR_BLUE + "\n###################################################################" + COLOR_RESET)
    print(COLOR_BLUE + "Welcome to Guess a word! A world class videogame made just for you!" + COLOR_RESET)
    print(COLOR_BLUE + "###################################################################" + COLOR_RESET)
    
    # Ask for the username
    USER_ID = input(COLOR_YELLOW + "\nEnter your username: " + COLOR_RESET)
    
    # Ask user if connecting to existing lobby or creating a new one.
    while True:
        printInitMenu()
        option = input(COLOR_YELLOW + "Enter an option: " + COLOR_RESET)
        if option == "1":
            lobby_info = connectMasterNode(1, USER_ID) # Connect to an existing lobby
            break
        elif option == "2":
            lobby_info = connectMasterNode(2, USER_ID) # Create a new lobby
            break
        elif option == "3":                            # Quit
            break
        else:
            print(COLOR_RED + "Invalid option. Please try again." + COLOR_RESET)

    # Now connect to the actual worker node/lobby with lobby_info
    
    role = connectWorkerNode(lobby_info, USER_ID)
    while True:
        printGameMenu()
        option = input(COLOR_YELLOW + "Enter an option: " + COLOR_RESET)
        if option == "1":
            if role == 0:
                startGameAsAdmin(USER_ID, lobby_info[1])
            else:
                print(COLOR_BLUE + "Starting game:" + COLOR_RESET)
                startGame(USER_ID, lobby_info[1])
        elif option == "2":
            disconnectServer() # Exit application.
            print(COLOR_BLUE + "\nGoodbye!" + COLOR_RESET)
            break
        elif option == "1000":
            getStatus()
        else:
            print(COLOR_RED + "Invalid option. Please try again." + COLOR_RESET)
    
    return 0

main()
