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

def main():
    print("\n###################################################################")
    print("Welcome to Guess a word! A world class videogame made just for you!")
    print("###################################################################")
    
    # Ask for the username
    USER_ID = input("\nEnter your username: ")
    
    # Ask user if connecting to existing lobby or creating a new one.
    while True:
        printInitMenu()
        option = input("Enter an option: ")
        if option == "1":
            lobby_info = connectMasterNode(1, USER_ID) # Connect to an existing lobby
            break
        elif option == "2":
            lobby_info = connectMasterNode(2, USER_ID) # Create a new lobby
            break
        elif option == "3":                            # Quit
            break
        elif option == "1000":
            lobby_info = ["localhost", 0]
            break
        else:
            print("Invalid option. Please try again.")

    # Now connect to the actual worker node/lobby with lobby_info

    role = connectWorkerNode(lobby_info, USER_ID)
    while True:
        printGameMenu()
        option = input("Enter an option: ")
        if option == "1":
            if role == 0:
                print("Not working yet.")
                # startGameAsAdmin()
            else:
                startGame(USER_ID, lobby_info[1])
        elif option == "2":
            disconnectServer() # Exit application.
            print("\nGoodbye!")
            break
        elif option == "1000":
            getStatus()
        else:
            print("Invalid option. Please try again.")
    
    return 0

main()
