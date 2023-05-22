#                                              TIC TAC TOE
# the algorithm
'''
1. make the board draw lines and get images loaded
2. a function to get the result of the game which player won or if it was a draw
3. a function to print these results on game screen
4. drawing the X or O at the position choosen would contain two functions
    a.choosing the point using the mouse
    b. rendering the image at that box

WE HAVE THESE 5 FUNCTIONS THAT WE WOULD PUT TOGETHER TO MAKE THE THE TIC TAC TOE GAME
i. draw board function 
ii. get results printed use font
iii. check winning cases and strike the win line draw module
iv. get coordinates of mouse click use mouse module
v. put the picture at these coordinates
'''

import pygame

import math

pygame.init()
X = 'X'
O = 'O'
curTurn = 'X'  # the initialised variable that stores whose turn it is
prevTurn = 'O'
winner = None  # to store the winner used in checkwin

draw = None  # to see if it is a draw a boolean
ROW = 10
COL = 10
board = [[None] * ROW for _ in range(ROW)]  # the board is a matrix basically of size  R

clock = pygame.time.Clock()  # the Clock object for framerate
WIDTH = 800
HEIGHT = 800
SIZE = HEIGHT // ROW
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # screen setup

pygame.display.set_caption("Tic Tac Toe")  # the caption\

ximg = pygame.image.load("images/X.png")
oimg = pygame.image.load("images/O.png")  # loaded images from the folder

ximg = pygame.transform.scale(ximg, (SIZE, SIZE))
oimg = pygame.transform.scale(oimg, (SIZE, SIZE))  # scaled both the images according to the size of one block available

LINE_COLOR = (228, 231, 236)

BACKGROUND = (254, 254, 254)


def drawgrid():  # drawing the board with lines
    x = 0
    y = 0
    screen.fill(BACKGROUND)
    for l in range(ROW):
        x += SIZE
        y += SIZE
        pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, WIDTH), 6)
        pygame.draw.line(screen, LINE_COLOR, (0, y), (HEIGHT, y), 6)

    # two vertical and two horizontal lines are required to create a 3X3 grid


def result():  # to get results and print them on screen
    global draw, winner
    message = 'hello'
    if winner:
        message = winner + " won!"
    if draw:
        message = "Game Draw!"

    font = pygame.font.SysFont('Georgia', 70)
    text = font.render(message, 1, (24, 154, 180))
    # screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()


def checkVertical(row, col):
    global prevTurn, board
    head = False
    tail = False
    cnt = 1
    print('turn ', curTurn, prevTurn)
    for k in range(1, 6):
        if (row - k < 0): break
        if (board[row - k][col] == prevTurn):
            cnt += 1
        elif (board[row - k][col] is not None and board[row - k][col] != prevTurn):
            head = True
            break
        else:
            break
    for k in range(1, 6):
        if (row + k >= ROW): break
        if (board[row + k][col] == prevTurn):
            cnt += 1
        elif (board[row + k][col] is not None and board[row + k][col] != prevTurn):
            tail = True
            break
        else:
            break

    if (head and tail):
        return False
    elif (cnt == 5):
        return True
    else:
        return False


def checkHorizontal(row, col):
    global prevTurn, board, curTurn
    head = False
    tail = False
    cnt = 1
    for k in range(1, 6):
        if (col - k < 0): break
        if (board[row][col - k] == prevTurn):
            cnt += 1
        elif (board[row][col - k] == curTurn):
            head = True
            break
        else:
            break
    for k in range(1, 6):
        if (col + k >= COL): break
        if (board[row][col + k] == prevTurn):
            cnt += 1
        elif (board[row][col + k] == curTurn):
            tail = True
            break
        else:
            break

    if (head and tail):
        return False
    elif (cnt == 5):
        return True
    else:
        return False


def checkMajorDiagonal(row, col):
    head = False
    tail = False
    cnt = 1
    for k in range(1, 6):
        if (row - k < 0 or col - k < 0): break
        if (board[row - k][col - k] == prevTurn):
            cnt += 1
        elif (board[row - k][col - k] == curTurn):
            head = True
            break
        else:
            break
    for k in range(1, 6):
        if (row + k >= ROW or col + k >= COL): break
        if (board[row + k][col + k] == prevTurn):
            cnt += 1
        elif (board[row + k][col + k] == curTurn):
            tail = True
            break
        else:
            break
    if(tail and head):
        return False
    elif(cnt==5):
        return True
    else:
        return False

def checkMinorDiagonal(row, col):
    head = False
    tail = False
    cnt = 1
    for k in range(1, 6):
        if (row - k < 0 or col + k >= COL): break
        if (board[row - k][col + k] == prevTurn):
            cnt += 1
        elif (board[row - k][col + k] == curTurn):
            head = True
            break
        else:
            break
    for k in range(1, 6):
        if (row + k >= ROW or col - k < 0 ): break
        if (board[row + k][col - k] == prevTurn):
            cnt += 1
        elif (board[row + k][col - k] == curTurn):
            tail = True
            break
        else:
            break
    if(tail and head):
        return False
    elif(cnt==5):
        return True
    else:
        return False


def wincases(row, col):  # check the winner and draw a line across how the win was
    global winner
    if (checkVertical(row, col) or checkHorizontal(row, col) or checkMajorDiagonal(row,col) or checkMinorDiagonal(row,col)):
        winner = prevTurn
        result()


def getimg(row, col):  # to render the image at the clicked position update value of curTurn as in whose turn it is
    global board, curTurn, prevTurn

    posx = col * SIZE
    posy = row * SIZE

    # assigning the block on board its value
    board[row][col] = curTurn
    print(curTurn)
    if (curTurn == X):

        # if its X's turn put ximg and change it to O
        screen.blit(ximg, (posx, posy))
        curTurn = O
        prevTurn = X

    else:  # and vice versa
        screen.blit(oimg, (posx, posy))
        curTurn = X
        prevTurn = O
    pygame.display.update()


def input_to_block():  # to get the position of the coordinate clicked so that you use the above function draw to get the respective sign at the clicked position
    # basically to find out which block is clicked on board
    # get coordinates of mouse click
    x, y = pygame.mouse.get_pos()

    col = math.floor(x / SIZE)
    row = math.floor(y / SIZE)

    print(row, col)
    if (row + 1 and col + 1 and board[row][col] is None):
        global curTurn
        print(y, x)
        getimg(row, col)  # put in the row and column determined
        wincases(row, col)  # and check if the game is won by any player yet


drawgrid()  # calling the function in the main part

run=True
while run:  # the game loop
    if game_pause==True:
        screen.fill(BACKGROUND)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if(not winner):
                input_to_block()

    pygame.display.update()
    clock.tick(30)  # refresh rate