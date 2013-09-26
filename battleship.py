import sys
from scanner import *
import poll
from random import *
import time
move1 = 1
ships = {"C":0, "B":0, "D":0, "S":0, "P":0}
attacks = []
opponent = {"location":(0, 0), "location1":(0, 0),  "N":(0, 0), "S":(0, 0), "E":(0, 0), "W":(0, 0), "Parallel": ""}
sunked = {"C":0, "B":0, "D":0, "S":0, "P":0}
emptyhits = 0
sanity = 0
numships = 0
sunked = 0

def main():
    if len(sys.argv) != 2:
        print("Incorrect number of arguments. Type --help for more instructions.")
        sys.exit(1)
	
    player = sys.argv[1]

    if player == "a" or player == "A":
        player = "A"
        enemy = "B"
    elif player == "b" or player == "B":
        player = "B"
        enemy = "A"
    elif player == "--help":
        print ("This is a battleshipbot.")
        print ("To begin, give me an argument of A or B.")
        print ("Another battlebot must be used to battle this bot.")
        sys.exit(1)
    else:
        print ("Invalid Argument, please give the argument --help for more help.")
        sys.exit(1)

 
    board1 = createboard()
    board5 = createboard()


    fileplayerattack = player + ".salvo"
    me = open(fileplayerattack, "w")
    me.close() 
    fileplayerresponse = player + ".response"
    me2  = open(fileplayerresponse, "w")
    me2.close()

    fileopponentattack = enemy + ".salvo"
    fileopponentresponse = enemy + ".response"
	
    carrier = createship(board1, "C")

    while carrier == 0:
        carrier = createship(board1, "C")

    battleship = createship(board1, "B")

    while battleship == 0:
        battleship = createship(board1, "B")

    destroyer = createship(board1, "D")

    while destroyer == 0:
        destroyer = createship(board1, "D")

    submarine = createship(board1, "S")

    while submarine == 0:
        submarine = createship(board1, "S")

    patrol = createship(board1, "P")

    while patrol == 0:
        patrol = createship(board1, "P")


    defeat = 0	
    global sanity
    global move1
    global emptyhits
    global opponent
    global sunked

	
	
    if player == "B":
        time.sleep(5)

        poll.waitUntilChanged(fileopponentattack, 0)
        poll.waitUntilChanged(fileopponentresponse, 0)

        poll.waitUntilChanged(fileopponentattack, 0)
        location = oplocation(fileopponentattack)
        theirattack = incoming(board1, location)
        ourresponse = response(theirattack, fileplayerresponse)

    elif player == "A":
        time.sleep(5)
        poll.waitUntilChanged(fileopponentattack, 0)
        poll.waitUntilChanged(fileopponentresponse, 0)
        time.sleep(5)

    while defeat == 0:
        if emptyhits < 2:
            opponent["Parallel"] = "No"
        if emptyhits == 1:
            sanity = 1
        if sanity == 0:
            eptyhits = 0
            attacking = myattack(board5)
            ourattack = attack(attacking[0], attacking[1], fileplayerattack)
            move(board5)
            move(board1)
            poll.waitUntilChanged(fileopponentresponse, 2)
            s = Scanner(fileopponentresponse)
            z = s.readtoken()
            if z == "HIT":
                board5[attacking[0]][attacking[1]] = "X"
                sanity = 1
                opponent["location"] = (attacking[0], attacking[1])
            elif z == "MISS":
                board5[attacking[0]][attacking[1]] = "O"
            elif z == "SUNK":
                board5[attacking[0]][attacking[1]] = "X"
            elif z == "DEFEATED":
                board5[attacking[0]][attacking[1]] = "X"
                defeat = 1
                print ("Player " + player + " Wins")
                sys.exit()
            s.close()
            poll.waitUntilChanged(fileopponentattack, 2)
            location1 = oplocation(fileopponentattack)
            theirattack1 = incoming(board1, location1)
            ourresponse1 = response(theirattack1, fileplayerresponse)
            move1 += 2

        elif sanity > 0:
            if sanity > 4:
                if emptyhits <= 0:
                    sanity = 0
                    attacking = myattack(board5)
                elif emptyhits > 0: 
                    attacking = sink(board5)
                    while attacking == 0:
                        if attacking == "None":
                            myattack(board5)
                        attacking = sink(board5)
                ourattack = attack(attacking[0], attacking[1], fileplayerattack)
                move(board5)
                move(board1)
                poll.waitUntilChanged(fileopponentresponse, 2)
                s = Scanner(fileopponentresponse)
                z = s.readtoken()
                if z == "HIT":
                    board5[attacking[0]][attacking[1]] = "X"
                    sanity += 1 
                elif z == "MISS":
                    emptyhits -= 1
                    board5[attacking[0]][attacking[1]] = "O"
                    if opponent["N"] != (0, 0) and opponent["N"] != attacking:
                        opponent["location"] = opponent["N"]
                        sanity = 1
                    elif opponent["S"] != (0, 0) and opponent["S"] != attacking:
                        opponent["location"] = opponent["S"]
                        sanity = 1
                    elif opponent["E"] != (0, 0) and opponent["E"] != attacking:
                        opponent["location"] = opponent["E"]
                        sanity = 1
                    elif opponent["W"] != (0, 0) and opponent["W"] != attacking:
                        opponent["location"] = opponent["W"]
                        sanity = 1
                    elif emptyhits == 0:
                        sanity = 0 
                    elif emptyhits > 0:
                        sanity = 5
                elif z == "SUNK":
                    board5[attacking[0]][attacking[1]] = "X"
                    if emptyhits < 1 or opponent["Parallel"] == "Yes":
                        sanity = 0
                        emptyhits = 0
                    else:
                        if opponent["N"] != (0, 0) and opponent["N"] != attacking:
                            opponent["location"] = opponent["N"]
                        elif opponent["S"] != (0, 0) and opponent["S"] != attacking:
                            opponent["location"] = opponent["S"]
                        elif opponent["E"] != (0, 0) and opponent["E"] != attacking:
                            opponent["location"] = opponent["E"]
                        elif opponent["W"] != (0, 0) and opponent["W"] != attacking:
                            opponent["location"] = opponent["W"] 
                        sanity = 1
                elif z == "DEFEATED":
                    board5[attacking[0]][attacking[1]] = "X"
                    defeat = 1
                    print ("Player " + player + " Wins")
                    sys.exit()
                s.close()
                poll.waitUntilChanged(fileopponentattack, 2)
                location1 = oplocation(fileopponentattack)
                theirattack1 = incoming(board1, location1)
                ourresponse1 = response(theirattack1, fileplayerresponse)
                move1 += 2
            elif sanity > 0 and sanity < 5:
                attacking = sink(board5)
                while attacking == 0:
                    if attacking == "None":
                        myattack(board5)
                    attacking = sink(board5)
                ourattack = attack(attacking[0], attacking[1], fileplayerattack)
                move(board5)
                move(board1)
                poll.waitUntilChanged(fileopponentresponse, 2)
                s = Scanner(fileopponentresponse)
                z = s.readtoken()
                if z == "HIT":
                    if sanity > 0 and sanity < 5:
                        board5[attacking[0]][attacking[1]] = "X"
                        if sanity == 1:
                            opponent["N"] = (attacking[0], attacking[1])
                        elif sanity == 2:
                            opponent["S"] = (attacking[0], attacking[1])
                        elif sanity == 3:
                            opponent["W"] = (attacking[0], attacking[1])
                        elif sanity == 4:
                            opponent["E"] = (attacking[0], attacking[1])
                        sanity += 1
                        emptyhits += 1
                    else:
                        board5[attacking[0]][attacking[1]] = "X"
                        sanity = 1
                elif z == "MISS":
                    board5[attacking[0]][attacking[1]] = "O"
                    if sanity == 1:
                        opponent["N"] = (0, 0)
                    elif sanity == 2:
                        opponent["S"] = (0, 0)
                    elif sanity == 3:
                        opponent["W"] = (0, 0)
                    elif sanity == 4:
                        opponent["E"] = (0, 0)
                    sanity += 1
                elif z == "SUNK":
                    board5[attacking[0]][attacking[1]] = "X"
                    sanity = 0
                    if emptyhits > 1 and opponent["Parallel"] != "Yes":
                        if opponent["N"] != (0, 0):
                            opponent["location"] = opponent["N"]
                        elif opponent["S"] != (0, 0):
                            opponent["location"] = opponent["S"]
                        elif opponent["E"] != (0, 0): 
                            opponent["location"] = opponent["E"]
                        elif opponent["W"] != (0, 0):
                            opponent["location"] = opponent["W"]
                        sanity = 1
                    else:
                        emptyhits = 0

                    opponent["N"] = (0, 0)
                    opponent["S"] = (0, 0)
                    opponent["W"] = (0, 0)
                    opponent["E"] = (0, 0)
                    sanity = 0
                elif z == "DEFEATED":
                    board5[attacking[0]][attacking[1]] = "X"
                    defeat = 1
                    print ("Player " + player + " Wins")
                    sys.exit()
                s.close()
                poll.waitUntilChanged(fileopponentattack, 2)
                location1 = oplocation(fileopponentattack)
                theirattack1 = incoming(board1, location1)
                ourresponse1 = response(theirattack1, fileplayerresponse)
                move1 += 2
        else:
            "Unknown Error"
            sys.exit()
	
	
def opresponse(filename):
    s = Scanner(filename)
    x = s.readtoken()
    response = (x)
    s.close()
    return response

def oplocation(filename):
    s = Scanner(filename) 
    x = int(s.readtoken())
    y = int(s.readtoken())
    location = (x, y)
    s.close()
    return location

def response(str, fileout):
    file = open(fileout, "w") 
    if str == "HIT":
        file.write("HIT")
    elif str == "MISS":
        file.write("MISS")
    elif str == "SUNK":
        file.write("SUNK")
    elif str == "DEFEATED":
        file.write("DEFEATED")
        print ("I Lose")
        sys.exit()
    else:
        print ("There was a problem in the bot response file. Now Quitting...")
        sys.exit(1)
    file.close()
	

def attack(x, y, fileout):
    file = open(fileout, "w")
    z = "                     " + str(x) + "\n " + "    " + "    " + "    " + "\n " + "    " + "    " + "                             " + str(y) 
    file.write(z)
    file.close()

def createboard():
    name = []
    for i in range(10):
        x = ["-" ,"-" ,"-" ,"-" ,"-" ,"-" ,"-" ,"-" ,"-" ,"-"]
        name.append(x)
    return name

def placement(board, row, column, size, orientation):
    unavailable = []
    ship = []
    x = 0
    a = 0

    for i in range(10):
        for b in range(10):
            if board[i][b] != '-':
                unavailable.append((i, b))
        

    while x <= size:
        if orientation == "N":
            if a == 0:
                row = row
                a = a + 1
            else:
                row = row - 1
            if row >= 0 and column >= 0:
                if row <= 9 and column <= 9:
                    if (row, column) not in unavailable:
                        ship.append((row, column))
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        elif orientation == "S":
            if a == 0:
                row = row
                a = a + 1
            else:
                row = row + 1
            if row >= 0 and column >= 0:
                if row <= 9 and column <= 9:
                    if (row, column) not in unavailable:
                        ship.append((row, column))
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        elif orientation == "E":
            if a == 0:
                column = column
                a = a + 1
            else:
                column = column + 1
            if row >= 0 and column >= 0:
                if row <= 9 and column <= 9:
                    if (row, column) not in unavailable:
                        ship.append((row, column))
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        elif orientation == "W":
            if a == 0:
                column = column
                a = a + 1
            else:
                column = column - 1
            if row >= 0 and column >= 0:
                if row <= 9 and column <= 9:
                    if (row, column) not in unavailable:
                        ship.append((row, column))
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        x += 1
    return ship

def createship(board, ship):
    ships = {"C": 5, "B": 4, "D": 3, "S": 3, "P": 2}
    a = ships[ship]
    b = ship
    position = ""
    rand1 = randrange(0, 9)
    rand2 = randrange(0, 9)
    rand3 = randrange(0, 3)
    c = []

    if rand3 == 0:
        position = "N"
    elif rand3 == 1:
        position = "S"
    elif rand3 == 2:
        position = "E"
    elif rand3 == 3:
        position = "W"

    if placement(board, rand1, rand2, a, position) != 0:
        for i in range(a):
            if position == "N":
                rand1 -= 1
                if rand1 >= 0 and rand1 <= 9:
                    board[rand1][rand2] = b
                else:
                    return 0
            elif position == "S":
                rand1 += 1
                if rand1 >= 0 and rand1 <= 9:
                    board[rand1][rand2] = b
                else:
                    return 0
            elif position == "E":
                rand2 += 1
                if rand2 >= 0 and rand2 <= 9:
                    board[rand1][rand2] = b
                else:
                    return 0
            elif position == "W":
                rand2 -= 1
                if rand2 >= 0 and rand2 <= 9:
                    board[rand1][rand2] = b
                else:
                    return 0
        return board
    else:
        return 0

def move(board):
    global move1
    print ("move number is " + str(move1))
    for i in range(10):
        a = [0,1,2,3,4,5,6,7,8,9]
        print (board[i][a[0]]+" "+board[i][a[1]]+" "+board[i][a[2]]+" "+board[i][a[3]]+" "+board[i][a[4]]+" "+board[i][a[5]]+" "+board[i][a[6]]+" "+board[i][a[7]]+" "+board[i][a[8]]+" "+board[i][a[9]])

def incoming(board, location):
        global ships
        if location[0] < 0 or location[0] > 9 or location[1] < 0 or location[1] > 9:
            return "MISS"
            print ("WARNING: LAST SALVO WAS OUT OF RANGE") 
        elif board[location[0]][location[1]] == '-':
            board[location[0]][location[1]] = "O"
            return "MISS"
        elif board[location[0]][location[1]] == "O":
            return "MISS"
        elif board[location[0]][location[1]] == "X":
            return "HIT"
        elif board[location[0]][location[1]] == "C":
            if ships["C"] == 4 and ships["B"] == 4 and ships["D"] == 3 and ships["S"] == 3 and ships["P"] == 2:
                ships["C"] += 1
                board[location[0]][location[1]] = "X"
                return "DEFEATED"
            elif ships["C"] == 4:
                ships["C"] += 1
                board[location[0]][location[1]] = "X"
                return "SUNK"
            else:
                ships["C"] += 1
                board[location[0]][location[1]] = "X"
                return "HIT"
        elif board[location[0]][location[1]] == "B":
            if ships["B"] == 3 and ships["C"] == 5 and ships["D"] == 3 and ships["S"] == 3 and ships["P"] == 2:
                ships["B"] += 1
                board[location[0]][location[1]] = "X"
                return "DEFEATED"
            elif ships["B"] == 3:
                ships["B"] += 1
                board[location[0]][location[1]] = "X"
                return "SUNK"
            else:
                ships["B"] += 1
                board[location[0]][location[1]] = "X"
                return "HIT"
        elif board[location[0]][location[1]] == "D":
            if ships["D"] == 2 and ships["B"] == 4 and ships["C"] == 5 and ships["S"] == 3 and ships["P"] == 2:
                ships["D"] += 1
                board[location[0]][location[1]] = "X"
                return "DEFEATED"
            elif ships["D"] == 2:
                ships["D"] += 1
                board[location[0]][location[1]] = "X"
                return "SUNK"
            else:
                ships["D"] += 1
                board[location[0]][location[1]] = "X"
                return "HIT"
        elif board[location[0]][location[1]] == "S":
            if ships["S"] == 2 and ships["B"] == 4 and ships["D"] == 3 and ships["C"] == 5 and ships["P"] == 2:
                ships["S"] += 1
                board[location[0]][location[1]] = "X"
                return "DEFEATED"
            elif ships["S"] == 2:
                ships["S"] += 1
                board[location[0]][location[1]] = "X"
                return "SUNK"
            else:
                ships["S"] += 1
                board[location[0]][location[1]] = "X"
                return "HIT"
        elif board[location[0]][location[1]] == "P":
            if ships["P"] == 1 and ships["B"] == 4 and ships["D"] == 3 and ships["C"] == 5 and ships["S"] == 3:
                board[location[0]][location[1]] = "X"
                ships["P"] += 1
                return "DEFEATED"
            elif ships["P"] == 1:
                ships["P"] += 1
                board[location[0]][location[1]] = "X"
                return "SUNK"
            else:
                ships["P"] += 1
                board[location[0]][location[1]] = "X"
                return "HIT"
        else:
            return 0

def myattack(board):
        global attacks
        a = 0
        b = 4
        c = 8
        d = 2
        e = 6
        f = 1
        g = 3
        h = 5
        j = 7
        k = 9

        for i in range(10):
            if board[i][a] == "O":
                a += 1
            elif board[i][a] == "X":
                a += 1
            else:
                board[i][a] = "-"
                attacks.append((i, a))
                return (i, a)
        a = 0


        for i in range(6):
            if board[i][b] == "O":
                b += 1
            elif board[i][b] == "X":
                b += 1
            else:
                board[i][b] = "-"
                attacks.append((i, b))
                return (i, b)
        b = 4

        for i in range(4, 10):
            if board[i][a] == "O":
                a += 1
            elif board[i][a] == "X":
                a += 1
            else:
                board[i][a] = "-"
                attacks.append((i, a))
                return (i, a)
        a = 0

        for i in range(2):
            if board[i][c] == "O":
                c += 1
            elif board[i][c] == "X":
                c += 1
            else:
                board[i][c] = "-"
                attacks.append((i, c))
                return (i, c)
        c = 8


        for i in range(8, 10):
            if board[i][a] == "O":
                a += 1
            elif board[i][a] == "X":
                a += 1
            else:
                board[i][a] = "-"
                attacks.append((i, a))
                return (i, a)
        a = 0

        for i in range(8):
            if board[i][d] == "O":
                d += 1
            elif board[i][d] == "X":
                d += 1
            else:
                board[i][d] = "-"
                attacks.append((i, d))
                return (i, d)
        d = 2

        for i in range(2, 10):
            if board[i][a] == "O":
                a += 1
            elif board[i][a] == "X":
                a += 1
            else:
                board[i][a] = "-"
                attacks.append((i, a))
                return (i, a)
        a = 0

        for i in range(6, 10):
            if board[i][a] == "O":
                a += 1
            elif board[i][a] == "X":
                a += 1
            else:
                board[i][a] = "-"
                attacks.append((i, a))
                return (i, a)
        a = 0


        for i in range(4):
            if board[i][e] == "O":
                e += 1
            elif board[i][e] == "X":
                e += 1
            else:
                board[i][e] = "-"
                attacks.append((i, e))
                return (i, e)
        e = 6
	
        for i in range(9):
            if board[i][f] == "O":
                f += 1
            elif board[i][f] == "X":
                f += 1
            else:
                board[i][f] = "-"
                attacks.append((i, f))
                return (i, f)

        f = 1

        for i in range(1, 10):
            if board[i][a] == "O":
                a += 1
            elif board[i][a] == "X":
                a += 1
            else:
                board[i][a] = "-"
                attacks.append((i, a))
                return (i, a)
        a = 0

        for i in range(3, 7):
            if board[i][a] == "O":
                a += 1
            elif board[i][a] == "X":
                a += 1
            else:
                board[i][a] = "-"
                attacks.append((i, a))
                return (i, a)
        a = 0

        for i in range(7):
            if board[i][g] == "O":
                g += 1
            elif board[i][g] == "X":
                g += 1
            else:
                board[i][g] = "-"
                attacks.append((i, g))
                return (i, g)
        g = 3

        for i in range(5, 10):
            if board[i][a] == "O":
                a += 1
            elif board[i][a] == "X":
                a += 1
            else:
                board[i][a] = "-"
                attacks.append((i, a))
                return (i, a)
        a = 0

        for i in range(5):
            if board[i][h] == "O":
                h += 1
            elif board[i][h] == "X":
                h += 1
            else:
                board[i][h] = "-"
                attacks.append((i, h))
                return (i, h)
        h = 5

        for i in range(7, 10):
            if board[i][a] == "O":
                a += 1
            elif board[i][a] == "X":
                a += 1
            else:
                board[i][a] = "-"
                attacks.append((i, a))
                return (i, a)
        a = 0

        for i in range(3):
            if board[i][j] == "O":
                j += 1
            elif board[i][j] == "X":
                j += 1
            else:
                board[i][j] = "-"
                attacks.append((i, j))
                return (i, j)
        j = 7

        for i in range(9, 10):
            if board[i][a] == "O":
                a += 1
            elif board[i][a] == "X":
                a += 1
            else:
                board[i][a] = "-"
                attacks.append((i, a))
                return (i, a)
        a = 0

        for i in range(1):
            if board[i][k] == "O":
                k += 1
            elif board[i][k] == "X":
                k += 1
            else:
                board[i][k] = "-"
                attacks.append((i, k))
                return (i, k)
        k = 9




def sink(board):
	global attacks
	global opponent
	global sunked
	global emptyhits
	global sanity
	
	if sanity > 0 and sanity < 5:
            if sanity == 1:	
                location = opponent["location"]
                newnorth = location[0] - 1
                if newnorth >= 0 and newnorth <= 9:
                    if (newnorth, location[1]) not in attacks:
                        attacks.append((newnorth, location[1]))
                        return (newnorth, location[1])
                    else:
                        sanity = 2
                        return 0
                else:
                    sanity = 2
                    return 0

            elif sanity == 2:
                location = opponent["location"]
                newsouth = location[0] + 1
                if newsouth >= 0 and newsouth <= 9:
                    if (newsouth, location[1]) not in attacks:
                        attacks.append((newsouth, location[1]))
                        return (newsouth, location[1])
                    else:
                        sanity = 3
                        return 0
                else:
                    sanity = 3
                    return 0

            elif sanity == 3:
                location = opponent["location"]
                newwest = location[1] - 1
                if newwest >= 0 and newwest <= 9:
                    if (location[0], newwest) not in attacks:
                        attacks.append((location[0], newwest))
                        return (location[0], newwest)
                    else:
                        sanity = 4
                        return 0
                else:
                    sanity = 4
                    return 0

            elif sanity == 4:
                location = opponent["location"]
                neweast = location[1] + 1
                if neweast >= 0 and neweast <= 9:
                    if (location[0], neweast) not in attacks:
                        attacks.append((location[0], neweast))
                        return (location[0], neweast)
                    else:
                        sanity = 5
                        return 0
                else:
                    sanity = 5
                    return 0
            else:
                return myattack(board)

	elif sanity > 4:
	    if emptyhits == 0:
                sanity = 0
                return myattack(board)
	    
	    elif emptyhits == 1:
                if opponent["N"] != (0, 0):
                    location = opponent["N"]
                    newnorth = location[0] - 1
                    if newnorth >= 0 and newnorth <= 9:
                        if (newnorth, location[1]) not in attacks:
                            opponent["N"] = (newnorth, location[1])
                            attacks.append((newnorth, location[1]))
                            return (newnorth, location[1])
                        else:
                            opponent["N"] = (0, 0)
                            emptyhits = 0
                            sanity = 0
                            return myattack(board)
                    else:
                        opponent["N"] = (0, 0)
                        emptyhits = 0
                        sanity = 0
                        return myattack(board)

                elif opponent["S"] != (0, 0):
                    location = opponent["S"]
                    newsouth = location[0] + 1
                    if newsouth >= 0 and newsouth <= 9:
                        if (newsouth, location[1]) not in attacks:
                            opponent["S"] = (newsouth, location[1])
                            attacks.append((newsouth, location[1]))
                            return (newsouth, location[1])
                        else:
                            opponent["S"] = (0, 0)
                            emptyhits = 0
                            sanity = 0
                            return myattack(board)
                    else:
                        opponent["S"] = (0, 0)
                        emptyhits = 0
                        sanity = 0
                        return myattack(board)

                elif opponent["E"] != (0, 0):
                    location = opponent["E"]
                    neweast = location[1] + 1
                    if neweast >= 0 and neweast <= 9:
                        if (location[0], neweast) not in attacks:
                            opponent["E"] = (location[0], neweast)
                            attacks.append((location[0], neweast))
                            return (location[0], neweast)
                        else:
                            opponent["E"] = (0, 0)
                            emptyhits = 0
                            sanity = 0
                            return myattack(board)
                    else:
                        opponent["E"] = (0, 0)
                        emptyhits = 0
                        sanity = 0
                        return myattack(board)


                elif opponent["W"] != (0, 0):
                    location = opponent["W"]
                    newwest = location[1] - 1
                    if newwest >= 0 and newwest <= 9:
                        if (location[0], newwest) not in attacks:
                            opponent["W"] = (location[0], newwest)
                            attacks.append((location[0], newwest))
                            return (location[0], newwest)
                        else:
                            sanity = 0
                            emptyhits = 0
                            opponent["W"] = (0, 0)
                            return myattack(board)
                    else:
                        sanity = 0
                        opponent["W"] = (0, 0)
                        emptyhits = 0
                        return myattack(board)

	    elif emptyhits == 2:
                if opponent["N"] != (0, 0) and opponent["S"] != (0, 0):
                    location = opponent["N"]
                    location1 = opponent["S"]
                    newnorth = location[0] - 1
                    newsouth = location1[0] + 1
                    if newsouth >= 0 and newsouth <= 9:
                        newsouth = newsouth
                    else:
                        emptyhits = 1
                        opponent["S"] = (0, 0)
                        return 0 
                    if newnorth >= 0 and newnorth <= 9:
                        if (newnorth, location[1]) not in attacks:
                            opponent["N"] = (newnorth, location[1])
                            attacks.append((newnorth, location[1]))
                            opponent["Parallel"] = "Yes"
                            return (newnorth, location[1])
                        else:
                            emptyhits = 1
                            opponent["N"] = (0, 0)
                            return 0
                    else:
                        opponent["N"] = (0, 0)
                        emptyhits = 1
                        return 0

                elif opponent["S"] != (0, 0) and opponent["E"] != (0, 0):
                    location = opponent["S"]
                    location1 = opponent["E"]
                    newsouth = location[0] + 1
                    neweast = location1[1] + 1
                    if neweast >= 0 and neweast <= 9:
                        neweast = neweast
                    else:
                        emptyhits = 1
                        opponent["E"] = (0, 0)
                        return 0
                    if newsouth >= 0 and newsouth <= 9:
                        if (newsouth, location[1]) not in attacks:
                            opponent["S"] = (newsouth, location[1])
                            attacks.append((newsouth, location[1]))
                            opponent["Parallel"] = "No"
                            return (newsouth, location[1])
                        else:
                            emptyhits = 1
                            opponent["S"] = (0, 0)
                            return 0
                    else:
                        opponent["S"] = (0, 0)
                        emptyhits = 1
                        return 0

                elif opponent["E"] != (0, 0) and opponent["N"] != (0, 0):
                    location = opponent["E"]
                    location1 = opponent["N"]
                    neweast = location[1] + 1
                    newnorth = location[0] - 1
                    if newnorth >= 0 and newnorth <= 9:
                        newnorth = newnorth
                    else:
                        emptyhits = 1
                        opponent["N"] = (0, 0)
                        return 0
                    if neweast >= 0 and neweast <= 9:
                        if (location[0], neweast) not in attacks:
                            opponent["E"] = (location[0], neweast)
                            attacks.append((location[0], neweast))
                            opponent["Parallel"] = "No"
                            return (location[0], neweast)
                        else:
                            emptyhits = 1
                            opponent["E"] = (0, 0)
                            return 0
                    else:
                        opponent["E"] = (0, 0)
                        emptyhits = 1
                        return 0


                elif opponent["W"] != (0, 0) and opponent["N"] != (0, 0):
                    location = opponent["W"]
                    location1 = opponent["N"]
                    newwest = location[1] - 1
                    newnorth = location1[0] - 1
                    if newnorth >= 0 and newnorth <= 9:
                        newnorth = newnorth
                    else:
                        emptyhits = 1
                        opponent["N"] = (0, 0)
                        return 0
                    if newwest >= 0 and newwest <= 9:
                        if (location[0], newwest) not in attacks:
                            opponent["W"] = (location[0], newwest)
                            attacks.append((location[0], newwest))
                            opponent["Parallel"] = "No"
                            return (location[0], newwest)
                        else:
                            emptyhits = 1
                            opponent["W"] = (0, 0)
                            return 0
                    else:
                        opponent["W"] = (0, 0)
                        emptyhits = 1
                        return 0

                elif opponent["W"] != (0, 0) and opponent["S"] != (0, 0):
                    location = opponent["W"]
                    location1 = opponent["S"]
                    newwest = location[1] - 1
                    newsouth = location1[0] + 1
                    if newsouth >= 0 and newsouth <= 9:
                        newsouth = newsouth
                    else:
                        emptyhits = 1
                        opponent["S"] = (0, 0)
                        return 0
                    if newwest >= 0 and newwest <= 9:
                        if (location[0], newwest) not in attacks:
                            opponent["W"] = (location[0], newwest)
                            attacks.append((location[0], newwest))
                            opponent["Parallel"] = "No"
                            return (location[0], newwest)
                        else:
                            emptyhits = 1
                            opponent["W"] = (0, 0)
                            return 0
                    else:
                        opponent["W"] = (0, 0)
                        emptyhits = 1
                        return 0

                elif opponent["W"] != (0, 0) and opponent["E"] != (0, 0):
                    location = opponent["W"]
                    location1 = opponent["E"]
                    newwest = location[1] - 1
                    neweast = location1[1] + 1
                    if neweast >= 0 and neweast <= 9:
                        neweast = neweast
                    else:
                        emptyhits = 1
                        opponent["E"] = (0, 0)
                        return 0
                    if newwest >= 0 and newwest <= 9:
                        if (location[0], newwest) not in attacks:
                            opponent["W"] = (location[0], newwest)
                            attacks.append((location[0], newwest))
                            opponent["Parallel"] = "Yes"
                            return (location[0], newwest)
                        else:
                            emptyhits = 1
                            opponent["W"] = (0, 0)
                            return 0
                    else:
                        opponent["W"] = (0, 0)
                        emptyhits = 1
                        return 0

	    elif emptyhits == 3:
                if opponent["W"] != (0, 0) and opponent["E"] != (0, 0) and opponent["S"] != (0, 0):
                    location = opponent["W"]
                    location1 = opponent["E"]
                    location2 = opponent["S"]
                    newwest = location[1] - 1
                    neweast = location1[1] + 1
                    newsouth = location2[0] + 1
                    if neweast >= 0 and neweast <= 9:
                        neweast = neweast
                    else:
                        emptyhits = 2
                        opponent["E"] = (0, 0)
                        return 0
                    if newsouth >= 0 and newsouth <= 9:
                        newsouth = newsouth
                    else:
                        emptyhits = 2
                        opponent["S"] = (0, 0)
                        return 0
                    if newwest >= 0 and newwest <= 9:
                        if (location[0], newwest) not in attacks:
                            opponent["W"] = (location[0], newwest)
                            attacks.append((location[0], newwest))
                            return (location[0], newwest)
                        else:
                            emptyhits = 2
                            opponent["W"] = (0, 0)
                            return 0
                    else:
                        opponent["W"] = (0, 0)
                        emptyhits = 2
                        return 0

                elif opponent["W"] != (0, 0) and opponent["N"] != (0, 0) and opponent["S"] != (0, 0):
                    location = opponent["W"]
                    location1 = opponent["N"]
                    location2 = opponent["S"]
                    newwest = location[1] - 1
                    newnorth = location1[0] - 1
                    newsouth = location2[0] + 1
                    if newsouth >= 0 and newsouth <= 9:
                        newsouth = newsouth
                    else:
                        emptyhits = 2
                        opponent["S"] = (0, 0)
                        return 0
                    if newnorth >= 0 and newnorth <= 9:
                        newnorth = newnorth
                    else:
                        emptyhits = 2
                        opponent["N"] = (0, 0)
                        return 0

                    if newwest >= 0 and newwest <= 9:
                        if (location[0], newwest) not in attacks:
                            opponent["W"] = (location[0], newwest)
                            attacks.append((location[0], newwest))
                            return (location[0], newwest)
                        else:
                            emptyhits = 2
                            opponent["W"] = (0, 0)
                            return 0
                    else:
                        opponent["W"] = (0, 0)
                        emptyhits = 2
                        return 0

                elif opponent["W"] != (0, 0) and opponent["E"] != (0, 0) and opponent["N"] != (0, 0):
                    location = opponent["W"]
                    location1 = opponent["E"]
                    location2 = opponent["N"]
                    newwest = location[1] - 1
                    neweast = location1[1] + 1
                    newnorth = location2[0] - 1
                    if newnorth >= 0 and newnorth <= 9:
                        newnorth = newnorth
                    else:
                        emptyhits = 2
                        opponent["N"] = (0, 0)
                        return 0
                    if neweast >= 0 and neweast <= 9:
                        neweast = neweast
                    else:
                        emptyhits = 2
                        opponent["E"] = (0, 0)
                        return 0

                    if newwest >= 0 and newwest <= 9:
                        if (location[0], newwest) not in attacks:
                            opponent["W"] = (location[0], newwest)
                            attacks.append((location[0], newwest))
                            return (location[0], newwest)
                        else:
                            emptyhits = 2
                            opponent["W"] = (0, 0)
                            return 0
                    else:
                        opponent["W"] = (0, 0)
                        emptyhits = 2
                        return 0

                elif opponent["N"] != (0, 0) and opponent["E"] != (0, 0) and opponent["S"] != (0, 0):
                    location = opponent["E"]
                    location1 = opponent["S"]
                    location2 = opponent["N"]
                    newwest = location[1] - 1
                    neweast = location1[1] + 1
                    newnorth = location2[0] - 1
                    if neweast >= 0 and neweast <= 9:
                        neweast = neweast
                    else:
                        emptyhits = 2
                        opponent["E"] = (0, 0)
                        return 0
                    if newnorth >= 0 and newnorth <= 9:
                        newnorth = newnorth
                    else:
                        emptyhits = 2
                        opponent["N"] = (0, 0)
                        return 0
                    if newwest >= 0 and newwest <= 9:
                        if (location[0], neweast) not in attacks:
                            opponent["E"] = (location[0], neweast)
                            attacks.append((location[0], neweast))
                            return (location[0], neweast)
                        else:
                            emptyhits = 2
                            opponent["E"] = (0, 0)
                            return 0
                    else:
                        emptyhits = 2
                        opponent["E"] = (0, 0)
                        return 0
                else:
                    emptyhits = 2
                    return 0

	    elif emptyhits == 4:
                if opponent["W"] != (0, 0) and opponent["E"] != (0, 0) and opponent["N"] != (0, 0) and opponent["S"] != (0, 0):
                    location = opponent["W"]
                    location1 = opponent["E"]
                    location2 = opponent["S"]
                    location3 = opponent["N"]
                    newwest = location[1] - 1
                    neweast = location1[1] + 1
                    newsouth = location2[0] + 1
                    newnorth = location3[0] - 1
                    if neweast >= 0 and neweast <= 9:
                        neweast = neweast
                    else:
                        emptyhits = 3
                        opponent["E"] = (0, 0)
                        return 0
                    if newsouth >= 0 and newsouth <= 9:
                        newsouth = newsouth
                    else:
                        emptyhits = 3
                        opponent["S"] = (0, 0)
                        return 0
                    if newnorth >= 0 and newnorth <= 9:
                        newnorth = newnorth
                    else:
                        emptyhits = 3
                        opponent["N"] = (0, 0)
                        return 0
                    if newwest >= 0 and newwest <= 9:
                        if (location[0], newwest) not in attacks:
                            opponent["W"] = (location[0], newwest)
                            attacks.append((location[0], newwest))
                            return (location[0], newwest)
                        else:
                            emptyhits = 3
                            opponent["W"] = (0, 0)
                            return 0
                    else:
                        emptyhits = 3
                        opponent["W"] = (0, 0)
                        return 0
                else:
                    return myattack(board)
	else:
	    return myattack(board) 


main()

