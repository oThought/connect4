from random import randint 

# game function
def main():
    number = 0
    board = ["-"]*16
    board[randint(0, 8)] = "2"
    board[randint(8, 15)] = "2"
    printBoard(board, alternateBoard(board), number)
    gameLoop(board, number)

# repeating game system
def gameLoop(board, number):    
    while True:
        move = input("Move (wasd) to move numbers: ")
        remadeMove(board, move)
        generation(board)
        number += 1
        printBoard(board, alternateBoard(board), number)        
    

# checks for win
def winCheck(board):
    for i in board():
        if int(i.strip()) == 2048:
            print("YOU WIN!")
            
# generating new digits
def generation(board):
    empty = []
    for i in range(len(board)):
        if board[i] == "-":
            empty.append(i)
    board[empty[randint(0, len(empty)-1)]] = "2"

# changing boardsize to accomodate for displacements
def alternateBoard(board):
    for num in board:
        if len(str(num)) > 1:
            return len(str(num)) - 1
    return 0

# direction move
def remadeMove(board, direction):
    dict1 = {"w":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], "d":[1,5,9,13,2,6,10,14,3,7,11,15], "s":[15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0], "a":                        [15,11,7,3,14,10,6,2,13,9,5,1]}   
    for x in range(2):
        for num in dict1[direction]:
            dict2 = {"w":num >= 4, "d":num not in [15, 11, 7, 3], "s":num <= 11, "a":num not in [0, 4, 8, 12]}
            dict3 = {"w":num - 4, "d": num + 1, "s":num + 4, "a":num - 1}
            #print(type(board[num]))
            if ("-" not in str(board[num])) and dict2[direction]:
                    if board[dict3[direction]] == board[num] and "-" not in board[num]:
                        board[dict3[direction]] = str(int(board[num]) * 2)
                        board[num] = "-"
                    elif board[num] != board[dict3[direction]] and "-" not in board[dict3[direction]]:
                        pass
                    else:
                        board[dict3[direction]] = board[num]
                        board[num] = "-"

# prints board
def printBoard(board, x, number):
    print("-----------------" + 4 * x * "-")
    print(f"| {spaces(board, x, 0)} | {spaces(board, x, 1)} | {spaces(board, x, 2)} | {spaces(board, x, 3)} |")
    print("-----------------" + 4 * x * "-")
    print(f"| {spaces(board, x, 4)} | {spaces(board, x, 5)} | {spaces(board, x, 6)} | {spaces(board, x, 7)} |")
    print("-----------------" + 4 * x * "-")
    print(f"| {spaces(board, x, 8)} | {spaces(board, x, 9)} | {spaces(board, x, 10)} | {spaces(board, x, 11)} |")
    print("-----------------" + 4 * x * "-")
    print(f"| {spaces(board, x, 12)} | {spaces(board, x, 13)} | {spaces(board, x, 14)} | {spaces(board, x, 15)} |")
    print("-----------------" + 4 * x * "-")
    print(f"Number of Moves: {number}")
    print()

def spaces(board, x, num):
    if "-" in str(board[num]):
        return str(board[num]) + "-" * x
    if len(str(board[num])) - 1 == x:
        return str(board[num])
    if len(str(board[num])) - 1 != x:
        updatedX = x - len(str(board[num])) + 1
        return str(board[num]) + " " * updatedX

# runs game
main()
