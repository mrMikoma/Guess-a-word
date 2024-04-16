import random

#list of players, should be updated when new players join or leave
PLAYERS = ["Samuel", "Otto", "Miko", "Jeremias"]
SCORE = []
for player in PLAYERS:
    SCORE.append(0)
WORD_TO_GUESS = "ABC" #this will be randomised from the wordlist

#mocks for receiving and sending messages
def private_message(message, player):
    print(message)
def send_message(sender, message):
    msg = sender + ": " + message
    print(msg)
def receive_message():
    messages = [WORD_TO_GUESS, "I dunno", "Potato"]
    return messages[random.randint(0, len(messages) - 1)]
def receive_ID():
    return random.randint(0, len(PLAYERS) - 1)
#end of mocks

for i in range(3):
    msg = "Round " + str(i + 1)
    send_message(PLAYERS[0], msg)
    guessed = []
    for player in PLAYERS:
        guessed.append(0)
    private_message(WORD_TO_GUESS, PLAYERS[0])
    msg = "The word is " + str(len(WORD_TO_GUESS)) + " letters long."
    send_message(PLAYERS[0], msg)
    remaining_players = len(PLAYERS) - 1 
    while remaining_players > 0:
        message = receive_message()
        playerID = receive_ID()

        if playerID == 0:
            send_message(PLAYERS[0], message)

        else:
            if message == WORD_TO_GUESS:
                if guessed[playerID] == 0:
                    send_message(PLAYERS[playerID], "guessed correctly!")
                    SCORE[playerID] += remaining_players
                    remaining_players -= 1
                    guessed[playerID] = 1
                
            else:
                send_message(PLAYERS[playerID], message)

print("Game has ended and the results are here!")
for i in range(1, len(PLAYERS)):
    player = PLAYERS[i]
    points = str(SCORE[i])
    msg = player + ": " + points
    print(msg)