import random
import time

# Color constants
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RESET = '\033[0m'
BOLD =	'\033[1m'
BLUE =	'\033[34m'
print(RED + "This is in red" + RESET)
print(f"This is {GREEN}in green{RESET} but this is default.")
print(f"{YELLOW}Warning: Something is happening!{RESET}")

# a class to represent the game, the board, and the control code
class snakesAndLadders():
    ladderNum = 10
    snakeNum = 10


    def __init__(self, players):
        self.players = players
        self.snakeEnd = []
        self.ladderEnd = []
    
    #generates snakes and ladders while making sure no snake or ladder occupy the same start or end cells. Stores the ladders and snakes in custom classes in the board list
    def generateBoard(self):
        self.board = []
        self.snakeEnd = []
        self.ladderEnd = []
        
        for i in range(10**2):
            self.board.append(0)

        starts = [None]
        ends = [None]

        # generate ladders
        for num in range(self.ladderNum):
            start,end = starts[0],ends[0]
            while start in starts or end in ends or end in starts or start in ends:
                try:
                    start,end = self.__calcLadder()
                except ValueError:
                    pass
            starts.append(start)
            ends.append(end)
            self.ladderEnd.append(end)
            self.board[start-1] = boardElement(start, end, "Ladder",self)

        # generate snakes
        for num in range(self.snakeNum):
            start,end = starts[0],ends[0]
            while start in starts or end in starts or start in ends:
                try:    
                    start,end = self.__calcSnake()
                except ValueError:
                    pass

            starts.append(start)
            ends.append(end)
            self.snakeEnd.append(end)
            self.board[start-1] = boardElement(start, end, "Snake",self)


    #controls the game for a single round. Includes alternating turns, moving players, and seeing if a ladder or snake was landed on 
    def playRound(self):
        self.generateBoard()
        
        while(True):
            snakesAndLadders.clearScreen()
            print(self)
            for player in self.players:
                roll = player.rollDice()

                if player.position + roll > 100:
                    roll = 0
                    print(f"{player.name} rolled too high and will not move.")
                    time.sleep(1)

                else:
                    
                    #move player the number of cells they rolled
                    print(self)
                    time.sleep(1)
                    for i in range(roll):
                        player.position += 1
                        print(self)
                        time.sleep(0.5)
                    

                    if self.board[player.position - 1] != 0:
                        self.board[player.position - 1].grabPlayer(player)
                        print(self)

                    #check if someone has won and change wins/losses if so 
                    elif player.position == 100:
                        print(f"Congrats! {player.name} has won the game!")
                        player.wins += 1
                        for oplayer in self.players:
                            if oplayer != player:
                                oplayer.losses += 1
                        
                        print("\nGame Over\n")

                        #print player stats
                        print("Stats Thus Far:")
                        for nplayer in self.players:
                            print(nplayer)
                        return ""
                    print(self)
    
    #controls the central game play for mutliple rounds. 
    def play(self):
        print("Starting the Game! Get Ready...")
        time.sleep(1)
        while (True):
            for player in self.players:
                player.position = 1
            print(self.playRound())
            b = 1
            while(b):
                answer = input(f"Do you want to play again?: (Y/N)\n")
                if answer == "N" or answer =="n" or answer == "no" or answer == "NO":
                    print("Thanks for playing my game. :)")
                    return 0
                elif answer == "Y" or answer == "y" or answer == "YES" or answer == "yes":
                    b = 0
                    
                else:
                    print("Not supported!")
    
    # long method to print the game board. Uses __Str__ methods of other classes to simplify. Prints into a color coded grid with proper alignment.

    def __str__(self):
        string = ""
        invert = 1
        playerSpace = 2

        # determine the max possible cell length. Either all players in same cell or biggest player next to ladder/snake
        # equalizer so each cell has the same length of ascii chars

        largestPlayerName = len(self.players[0].name)
        for player in self.players:
            playerSpace += len(player.name) + 1
            if len(player.name) > largestPlayerName:
                largestPlayerName = len(player.name)
        extraSpaceOG = max(playerSpace+1,7 + largestPlayerName)

        #generate the power divider. 
        lineBreak = "\n|" 
        for i in range(10*(5+extraSpaceOG) - 1):
            lineBreak+="_"
        lineBreak+="|\n"

        #loop through the rows, top to bottom
        for i in range(10,0,-1):
            line = "|"

            #if ordering is inverted, change column indexing
            if invert == 1:
                start,end,step = 10,0,-1
            else:
                start, end, step = 1,10 + 1,1

            for j in range(start,end,step):

                index = 10*i - (10 - j)
                element = self.board[index-1]

                line += f" {BOLD}{BLUE}{index}{RESET} "

                extraSpace = extraSpaceOG

                # check to see if something important should be printed and print it if so 
                if index in self.snakeEnd:
                    line += f"{RED}U{RESET}"
                    extraSpace -= 1
                elif index in self.ladderEnd:
                    line += f"{GREEN}U{RESET}"
                    extraSpace -= 1
                if element != 0:
                    line += str(element)
                    extraSpace -= 6
                    if element.end < 10:
                        extraSpace += 1
                for player in self.players:
                    if player.position == index:
                        line +=f" {BOLD}{YELLOW}{player.name}{RESET} "
                        extraSpace -= 2 + len(player.name)
                if index < 10:
                    extraSpace += 1
                elif index == 100:
                    extraSpace -= 1

                #add extra space to cell
                for ele in range(extraSpace):
                    line += " "
                line += "|"     
            invert *= -1 
            string += lineBreak + line 
        return string + lineBreak

    def clearScreen():
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")       

    #calculates a possible ladder that could exist
    def __calcLadder(self):
        startPos = random.randint(2,90)
        endPos = random.randint(10*(startPos // 10 + 1) + 1, 99)
        return startPos,endPos
    
    #calculates a possible snake that could exist
    def __calcSnake(self):
        startPos = random.randint(11,99)
        endPos = random.randint(1,10*(startPos // 10 - 1) - 1)
        return startPos,endPos

# an object representing either a snake or a ladder. Includes code for a player stepping on this object
class boardElement():

    def __init__(self, start, end, type, game):
        self.start = start
        self.end = end
        self.type = type
        self.game = game
    
    #moves a player to the end point of this object
    def grabPlayer(self,player):
        print(f"{player.name} landed on a {self.type}!\n Moving to {self.end}")
        time.sleep(2)
        delta = self.end - player.position
        
        if self.type == "Ladder":
            player.ladders += 1
        else:
            player.snakes += 1

        player.distance += abs(delta)
        for i in range(abs(delta)):
            player.position += int((delta/abs(delta)))
            time.sleep(2/abs(delta))
            print(self.game)

    def __str__(self):
        if self.type == "Ladder":
            return f"{GREEN}L-^{self.end}{RESET} "
        else:
            return f"{RED}S-v{self.end}{RESET} "
            
# a class for the player. Holds statistics and allows for rolling dice
class player():

    def __init__(self, num, startingLocation = 1):
        self.name = input(f"Name for player {num}?\n")
        self.position = startingLocation
        self.wins = 0
        self.losses = 0
        self.rolls = 0
        self.distance = 0
        self.rolledDistance = 0
        self.ladders = 0
        self.snakes = 0
    
    def moveTo(self, position):
        self.position = position
    
    #roll dice in a more interactive way
    def rollDice(self):
        b = 1
        while(b):
            answer = input(f"{self.name} do you want to roll dice: (Y/N)\n")
            if answer == "Y" or answer == "y" or answer == "yes" or answer == "YES":
                b = 0
            else:
                print("Not supported!")
        print(f"{random.randint(1,6)} ... ", end="",flush=True)
        time.sleep(0.25)        
        print(f"{random.randint(1,6)} ... ", end="",flush=True)
        time.sleep(0.5)        
        print(f"{random.randint(1,6)} ... ", end="",flush=True)
        time.sleep(0.75)        
        print(f"{random.randint(1,6)} ... ", end="",flush=True)
        time.sleep(1)
        roll = random.randint(1,6)
        print(roll)
        time.sleep(2)
        self.rolls += 1
        self.distance += roll
        self.rolledDistance += roll
        return roll
    
    def __str__(self):
        return f"Player {self.name}:\nWins: {self.wins}\nLosses: {self.losses}\nTotal Distance: {self.distance}\nNumber of Rolls: {self.rolls}\nTotal Snakes: {self.snakes}\nTotal Ladders: {self.ladders}\n"

# main function to run the program.
def main():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nWelcome to Snakes and Ladders by Matthew Randa")
    time.sleep(1)
    b = 1
    while(b):
        numPlayers = input("Number of players? (int only)\n")
        if numPlayers.isdigit():
            b = 0
        else:
            print("Not supported!")

    players = []
    for i in range(int(numPlayers)):
        players.append(player(i+1))
        snakesAndLadders.clearScreen()
    
    game = snakesAndLadders(players)
    
    input("\nARE YOU READY FOR..... penn state footba----- SNAKES AND LADDERS?\n")
    time.sleep(1)
    print("\n I dont care what you said you are READY!")
    time.sleep(1)

    snakesAndLadders.clearScreen()

    game.play()


main()
    