from src.menu import *
from src.connectRPC import *
from src.connectToMaster import *
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
        else:
            print("Invalid option. Please try again.")

    # Now connect to the actual worker node/lobby with lobby_info

    connectWorkerNode(lobby_info, USER_ID)
    while True:
        printGameMenu()
        option = input("Enter an option: ")
        if option == "1":
            # Send message etc.
            print("Remove this")
        elif option == "2":
            disconnectServer() # Exit application.
            print("\nGoodbye!")
            break
        else:
            print("Invalid option. Please try again.")
    
    return 0

main()
