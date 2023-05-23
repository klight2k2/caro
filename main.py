#                                              TIC TAC TOE


import pygame
import button
import math

pygame.init()

human = 'X'
ai = 'O'
curTurn = human  # the initialised variable that stores whose turn it is
prevTurn = ai

ROW = 3
COL = 3
RULE=3
board=[[None] * ROW for _ in range(ROW)]
winner = None  # to store the winner used in checkwin
draw = None  # to see if it is a draw a boolean
def init_game():
    global board,winner ,draw
    board=[[None] * ROW for _ in range(ROW)]
    winner = None  # to store the winner used in checkwin

    draw = None  # to see if it is a draw a boolean
clock = pygame.time.Clock()  # the Clock object for framerate
WIDTH = 240
HEIGHT = 240
SIZE = HEIGHT // ROW
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # screen setup

pygame.display.set_caption("Tic Tac Toe")  # the caption\

ximg = pygame.image.load("images/X.png")
oimg = pygame.image.load("images/O.png")  # loaded images from the folder

humanImg = pygame.transform.scale(ximg, (SIZE, SIZE))
aiImg = pygame.transform.scale(oimg, (SIZE, SIZE))  # scaled both the images according to the size of one block available

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
    message = ''
    if winner:
        message = winner + " won!"
    if draw:
        message = "Game Draw!"

    font = pygame.font.SysFont('Georgia', 70)
    text = font.render(message, 1, '#22b491')
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
    screen.blit(text, text_rect)
    pygame.display.update()


def checkVertical(row, col):
    global prevTurn, board
    head = False
    tail = False
    cnt = 1
    # print('turn ', curTurn, prevTurn)
    for k in range(1, RULE+1):
        if (row - k < 0): break
        if (board[row - k][col] == prevTurn):
            cnt += 1
        elif (board[row - k][col] is not None and board[row - k][col] != prevTurn):
            head = True
            break
        else:
            break
    for k in range(1, RULE+1):
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
    elif (cnt == RULE):
        return True
    else:
        return False


def checkHorizontal(row, col):
    global prevTurn, board, curTurn
    head = False
    tail = False
    cnt = 1
    for k in range(1, RULE+1):
        if (col - k < 0): break
        if (board[row][col - k] == prevTurn):
            cnt += 1
        elif (board[row][col - k] == curTurn):
            head = True
            break
        else:
            break
    for k in range(1, RULE+1):
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
    elif (cnt == RULE):
        return True
    else:
        return False


def checkMajorDiagonal(row, col):
    head = False
    tail = False
    cnt = 1
    for k in range(1, RULE+1):
        if (row - k < 0 or col - k < 0): break
        if (board[row - k][col - k] == prevTurn):
            cnt += 1
        elif (board[row - k][col - k] == curTurn):
            head = True
            break
        else:
            break
    for k in range(1, RULE+1):
        if (row + k >= ROW or col + k >= COL): break
        if (board[row + k][col + k] == prevTurn):
            cnt += 1
        elif (board[row + k][col + k] == curTurn):
            tail = True
            break
        else:
            break
    if (tail and head):
        return False
    elif (cnt == RULE):
        return True
    else:
        return False


def checkMinorDiagonal(row, col):
    head = False
    tail = False
    cnt = 1
    for k in range(1, RULE+1):
        if (row - k < 0 or col + k >= COL): break
        if (board[row - k][col + k] == prevTurn):
            cnt += 1
        elif (board[row - k][col + k] == curTurn):
            head = True
            break
        else:
            break
    for k in range(1, RULE+1):
        if (row + k >= ROW or col - k < 0): break
        if (board[row + k][col - k] == prevTurn):
            cnt += 1
        elif (board[row + k][col - k] == curTurn):
            tail = True
            break
        else:
            break
    if (tail and head):
        return False
    elif (cnt == RULE):
        return True
    else:
        return False


def wincases(row, col):  # check the winner and draw a line across how the win was
    global winner
    if (checkVertical(row, col) or checkHorizontal(row, col) or checkMajorDiagonal(row, col) or checkMinorDiagonal(row,
                                                                                                                   col)):
        winner = prevTurn
        return  True
    else:
        for i in range(ROW):
            for j in range(COL):
                if(board[i][j] is None): return False
    winner='draw'
    return True

def getimg(row, col):  # to render the image at the clicked position update value of curTurn as in whose turn it is
    global board, curTurn, prevTurn,prevCol,prevRow
    prevCol = col
    prevRow = row
    posx = col * SIZE
    posy = row * SIZE

    # assigning the block on board its value
    board[row][col] = curTurn
    # print(curTurn)
    if (curTurn == human):

        # if its X's turn put ximg and change it to O
        screen.blit(ximg, (posx, posy))
        curTurn = ai
        prevTurn = human

    else:  # and vice versa
        screen.blit(oimg, (posx, posy))
        curTurn = human
        prevTurn = ai
    pygame.display.update()

prevCol=-1
prevRow=-1
def input_to_block():  # to get the position of the coordinate clicked so that you use the above function draw to get the respective sign at the clicked position
    # basically to find out which block is clicked on board
    # get coordinates of mouse click
    global  prevRow,prevCol
    x, y = pygame.mouse.get_pos()

    col = math.floor(x / SIZE)
    row = math.floor(y / SIZE)

    prevCol=col
    prevRow=row
    if (row + 1 and col + 1 and board[row][col] is None):
        global curTurn
        # print(y, x)
        getimg(row, col)  # put in the row and column determined
        wincases(row, col)  # and check if the game is won by any player yet


scores={
    'X':-10,
    'O':10,
    'draw':0
}

def min_value(row,col,deep):
    global winner,prevTurn,curTurn

    if wincases(row,col):
        print('min winner',winner)
        a=winner
        winner=None
        return dict(
            pos=(row, col),
            score=scores[a],
            d = deep
        )
    bestScore=dict(
        score=float('inf')
    )
    bestDeep = float('-inf')
    for i in range(ROW):
        for j in range(COL):
            if board[i][j] is None:
                board[i][j]=human
                prevTurn=human
                curTurn=ai
                # print(board)
                v= max_value(i,j,deep+1)

                d=v['d']
                # print('v',v)
                if bestScore['score'] > v['score']:
                    bestScore = v
                    bestScore['pos']=(i,j)
                    bestDeep = d
                elif bestScore['score'] == v['score'] and d > bestDeep:
                    bestScore = v
                    bestDeep = d
                    bestScore['pos']=(i,j)
                board[i][j]=None
                prevTurn = ai
                curTurn = human
    print('min',bestScore)
    return  bestScore

def max_value(row,col,deep):
    global winner,prevTurn,curTurn
    if wincases(row,col):
        print('max winner',winner)

        a = winner
        winner = None
        return dict(
            pos=(row, col),
            score=scores[a],
            d=deep
        )
    bestScore=dict(
        score=float('-inf')
    )
    bestDeep=float('inf')

    for i in range(ROW):
        for j in range(COL):
            if board[i][j] is None:
                board[i][j]=ai
                print(board)
                prevTurn = ai
                curTurn = human
                v= min_value(i,j,deep+1)
                d=v['d']
                # print('v', v)
                if bestScore['score'] < v['score']:
                    bestScore=v
                    bestDeep=d
                    bestScore['pos']=(i,j)

                elif bestScore['score'] == v['score'] and d <bestDeep:
                    bestScore = v
                    bestDeep = d
                    bestScore['pos']=(i,j)

                board[i][j]=None
                prevTurn = human
                curTurn = ai
    print('max',bestScore)

    return  bestScore


def minimax(row,col):
    v=max_value(row,col,0)
    getimg(v['pos'][0],v['pos'][1])
    print('minimax',v)
    return v

drawgrid()  # calling the function in the main part
font = pygame.font.SysFont('Georgia', 15)
again = button.button(HEIGHT /2, WIDTH /2, font, 'Play Again?')

play = button.button(WIDTH /2, HEIGHT /2 - 50, font, 'Play')

playWithAi = button.button(WIDTH /2, HEIGHT /2 , font, 'Play vs computer')

bg = pygame.image.load("images/bg.jpg")

run = True
global playing
playing= False
drawGridCkeck=False
while run:  # the game loop
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if (not playing):
            screen.blit(bg, (0, 0))
            if play.draw_button(screen):
                playing = True
                print('play')
                drawGridCkeck=True
            if playWithAi.draw_button(screen):
                print('play with computer')
        else:
            if drawGridCkeck:
                drawGridCkeck=False
                drawgrid()
            if  winner is None:
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    if curTurn != ai:
                        input_to_block()
                    else:
                        minimax(prevRow, prevCol)
                    wincases(prevRow,prevCol)
            else:
                print("test",winner)
                if again.draw_button(screen):
                    print('Again')
                    screen.blit(bg, (0, 0))
                    playing = False
                    winner = None
                    init_game()

    pygame.display.update()
    clock.tick(30)  # refresh rate
