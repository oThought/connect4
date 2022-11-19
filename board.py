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
        if move == "s":
          downMove(board)
        if move == "d":
          rightMove(board)
        if move == "a":
          leftMove(board)
        if move == "w":
          upMove(board)
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

# digits move up
def upMove(board):
    for x in [1, 2]:
        for num in range(len(board))[::-1]:
            if board[num] != "-" and num >= 4:
                if board[num - 4] == board[num] != "-":
                    board[num - 4] = int(board[num]) * 2
                    board[num] = "-"
                elif board[num] != board[num-4] != "-":
                    pass
                else:
                    board[num - 4] = board[num]
                    board[num] = "-"

# digits move right
def rightMove(board):
    for x in [1, 2]:
        for i in range(len(board)):
            if board[i] != "-" and i not in [15, 11, 7, 3]:
                if board[i] == board[i+1] != "-":
                    board[i+1] = int(board[i]) * 2
                    board[i] = "-"         
                elif board[i] != board[i+1] != "-":
                    pass
                else:
                    board[i+1] = board[i]
                    board[i] = "-"        
            
# digits move down
def downMove(board):
    for x in [1, 2]:
        for num in range(len(board)):
            if board[num] != "-" and num <= 11:
                if board[num + 4] == board[num] != "-":
                    board[num + 4] = int(board[num]) * 2
                    board[num] = "-"
                elif board[num] != board[num+4] != "-":
                    pass
                else:
                    board[num + 4] = board[num]
                    board[num] = "-"

# digits move left
def leftMove(board):
    for x in [1, 2]:
        for i in [15,11,7,3,14,10,6,2,13,9,5,1]:
            if board[i] != "-" and i not in [0, 4, 8, 12]:
                if board[i] == board[i-1] != "-":
                    board[i-1] = int(board[i]) * 2
                    board[i] = "-"  
                elif board[i] != board[i-1] != "-":
                    pass
                else:
                    board[i-1] = board[i]
                    board[i] = "-"
        
# creates a board for easier reading
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


# links with |alternateBoard| to respond to displacements
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
