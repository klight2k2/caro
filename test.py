import pygame
import button
import math

pygame.init()

HUMAN = 'X'
AI = 'O'
pygame.display.set_caption("Tic Tac Toe")  # the caption\
WIDTH = 800
HEIGHT = 800
ximg = pygame.image.load("images/X.png")
oimg = pygame.image.load("images/O.png")
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # screen setup
LINE_COLOR = (228, 231, 236)
clock = pygame.time.Clock()  # the Clock object for framerate
BACKGROUND = (254, 254, 254)
attackScore = [0, 3, 24, 192, 1536, 12288, 98304]
defenseScore = [0, 1, 9, 81, 729, 6561, 59049]

RULE=5
class Board:
    def __init__(self, SIZE):
        self.SIZE = SIZE
        self.CEIL = 80
        self.board = self.make_empty_board(SIZE, SIZE)
        self.curTurn = HUMAN
        self.historyMoves = []

    def checkVertical(self,row, col,prevTurn,curTurn):
        head = False
        tail = False
        cnt = 1
        # print('turn ', curTurn, prevTurn)
        for k in range(1, RULE + 1):
            if (row - k < 0): break
            if (self.board[row - k][col] == prevTurn):
                cnt += 1
            elif (self.board[row - k][col] == curTurn):
                head = True
                break
            else:
                break
        for k in range(1, RULE + 1):
            if (row + k >= self.SIZE): break
            if (self.board[row + k][col] == prevTurn):
                cnt += 1
            elif (self.board[row + k][col] == curTurn):
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

    def checkHorizontal(self,row, col,prevTurn,curTurn):
        head = False
        tail = False
        cnt = 1
        for k in range(1, RULE + 1):
            if (col - k < 0): break
            if (self.board[row][col - k] == prevTurn):
                cnt += 1
            elif (self.board[row][col - k] == curTurn):
                head = True
                break
            else:
                break
        for k in range(1, RULE + 1):
            if (col + k >= self.SIZE): break
            if (self.board[row][col + k] == prevTurn):
                cnt += 1
            elif (self.board[row][col + k] == curTurn):
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

    def checkMajorDiagonal(self,row, col,prevTurn,curTurn):
        head = False
        tail = False
        cnt = 1
        for k in range(1, RULE + 1):
            if (row - k < 0 or col - k < 0): break
            if (self.board[row - k][col - k] == prevTurn):
                cnt += 1
            elif (self.board[row - k][col - k] == curTurn):
                head = True
                break
            else:
                break
        for k in range(1, RULE + 1):
            if (row + k >= self.SIZE or col + k >= self.SIZE): break
            if (self.board[row + k][col + k] == prevTurn):
                cnt += 1
            elif (self.board[row + k][col + k] == curTurn):
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

    def checkMinorDiagonal(self,row, col,prevTurn,curTurn):
        head = False
        tail = False
        cnt = 1
        for k in range(1, RULE + 1):
            if (row - k < 0 or col + k >= self.SIZE): break
            if (self.board[row - k][col + k] == prevTurn):
                cnt += 1
            elif (self.board[row - k][col + k] == curTurn):
                head = True
                break
            else:
                break
        for k in range(1, RULE + 1):
            if (row + k >= self.SIZE or col - k < 0): break
            if (self.board[row + k][col - k] == prevTurn):
                cnt += 1
            elif (self.board[row + k][col - k] == curTurn):
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
    def make_empty_board(self, row, col):
        board = [[' '] * row for _ in range(col)]
        return board

    def is_empty(board):
        return board == [[' '] * len(board)] * len(board)

    def get_position(
            self):  # to render the image at the clicked position update value of curTurn as in whose turn it is
        x,y = pygame.mouse.get_pos()
        x = math.floor(x / self.CEIL)
        y = math.floor(y / self.CEIL)
        print(y,x)
        return (y, x)

    def draw_img(self, x, y,curnTurn):
        posx = x * self.CEIL
        posy = y * self.CEIL
        if (curnTurn == HUMAN):
            screen.blit(ximg, (posy,posx))
        else:
            screen.blit(oimg, ( posy,posx))
        pygame.display.update()

    def draw_grid(self):
        screen.fill(BACKGROUND)
        x = 0
        y = 0
        for l in range(self.SIZE):
            x += self.CEIL
            y += self.CEIL
            pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, WIDTH), 6)
            pygame.draw.line(screen, LINE_COLOR, (0, y), (HEIGHT, y), 6)



    def attack_score_vertical(self, row, col, curTurn):
        # Duyet doc 
        global attackScore,defenseScore
        armyCount = 0
        enermyCount = 0
        for i in range(1, 6):
            if (i + row >= self.SIZE): break
            if (self.board[row + i][col] == curTurn):
                armyCount += 1
            elif (self.board[row + i][col] != ' '):
                enermyCount += 1
                break
            else: break
        for i in range(1, 6):
            if (row - i < 0): break
            if (self.board[row - i][col] == curTurn):
                armyCount += 1
            elif (self.board[row - i][col] != ' '):
                enermyCount += 1
                break
            else: break

        if (enermyCount == 2): return 0
        score = attackScore[armyCount] - defenseScore[enermyCount + 1]
        return score

    def attack_score_horizontal(self, row, col, curTurn):
        # Duyet doc 
        global attackScore,defenseScore
        armyCount = 0
        enermyCount = 0
        for i in range(1, 6):
            if (i + col >= self.SIZE): break
            if (self.board[row][col + i] == curTurn):
                armyCount += 1
            elif (self.board[row][col + i] != ' '):
                enermyCount += 1
                break
            else: break

        for i in range(1, 6):
            if (col - i < 0): break
            if (self.board[row][col - i] == curTurn):
                armyCount += 1
            elif (self.board[row][col - i] != ' '):
                enermyCount += 1
                break
            else: break

        if (enermyCount == 2): return 0
        score = attackScore[armyCount] - defenseScore[enermyCount + 1]
        return score

    def attack_score_major(self, row, col, curTurn):
        
        global attackScore,defenseScore
        # Duyet doc
        armyCount = 0
        enermyCount = 0
        for i in range(1, 6):
            if (i + row >= self.SIZE or col+i>=self.SIZE ): break
            if (self.board[row + i][col+i] == curTurn):
                armyCount += 1
            elif (self.board[row + i][col+i] != ' '):
                enermyCount += 1
                break
            else: break

        for i in range(1, 6):
            if (row - i<0   or col - i <0): break
            if (self.board[row - i][col-i] == curTurn):
                armyCount += 1
            elif (self.board[row - i][col-i] != ' '):
                enermyCount += 1
                break
            else: break

        if (enermyCount == 2): return 0
        score = attackScore[armyCount] - defenseScore[enermyCount + 1]
        return score
    def attack_score_minor(self, row, col, curTurn):
        
        global attackScore,defenseScore
        # Duyet doc
        armyCount = 0
        enermyCount = 0
        for i in range(1, 6):
            if (i + row >= self.SIZE or col-i < 0 ): break
            if (self.board[row + i][col-i] == curTurn):
                armyCount += 1
            elif (self.board[row + i][col-i] != ' '):
                enermyCount += 1
                break
            else: break

        for i in range(1, 6):
            if (row - i <0   or col + i >=self.SIZE): break
            if (self.board[row - i][col+i] == curTurn):
                armyCount += 1
            elif (self.board[row - i][col+i] != ' '):
                enermyCount += 1
                break
            else: break

        if (enermyCount == 2): return 0
        score=attackScore[armyCount] - defenseScore[enermyCount+1]
        return score
    def defense_score_vertical(self, row, col, curTurn):
        # Duyet doc 
        global defenseScore
        armyCount = 0
        enermyCount = 0
        for i in range(1, 6):
            if (i + row >= self.SIZE): break
            if (self.board[row + i][col] == curTurn):
                armyCount += 1
                break
            elif (self.board[row + i][col] != ' '):
                enermyCount += 1
            else: break

        for i in range(1, 6):
            if (row - i < 0): break
            if (self.board[row - i][col] == curTurn):
                armyCount += 1
                break
            elif (self.board[row - i][col] != ' '):
                enermyCount += 1
            else: break

        if (armyCount == 2): return 0
        score = defenseScore[enermyCount]
        # print("defense vertical",score)
        return score

    def defense_score_horizontal(self, row, col, curTurn):
        # Duyet doc global defenseScore
        global defenseScore
        armyCount = 0
        enermyCount = 0
        for i in range(1, 6):
            if (i + col >= self.SIZE): break
            if (self.board[row][col + i] == curTurn):
                armyCount += 1
                break
            elif (self.board[row][col + i] != ' '):
                enermyCount += 1
            else: break

        for i in range(1, 6):
            if (col - i < 0): break
            if (self.board[row][col - i] == curTurn):
                armyCount += 1
                break
            elif (self.board[row][col - i] != ' '):
                enermyCount += 1
            else: break

        if (armyCount == 2): return 0
        score = defenseScore[enermyCount]
        # print("horizontal defense score",score)
        return score

    def defense_score_major(self, row, col, curTurn):
        global defenseScore
        # Duyet doc
        armyCount = 0
        enermyCount = 0
        for i in range(1, 6):
            if (i + row >= self.SIZE or col+i>=self.SIZE ): break
            if (self.board[row + i][col+i] == curTurn):
                armyCount += 1
                break
            elif (self.board[row + i][col+i] != ' '):
                enermyCount += 1
            else: break

        for i in range(1, 6):
            if (row - i<0   or col - i <0): break
            if (self.board[row - i][col-i] == curTurn):
                armyCount += 1
                break

            elif (self.board[row - i][col-i] != ' '):
                enermyCount += 1
            else: break

        if (armyCount == 2): return 0
        score = defenseScore[enermyCount]
        # print("defense score", score)
        return score
    def defense_score_minor(self, row, col, curTurn):
        global defenseScore
        # Duyet doc
        armyCount = 0
        enermyCount = 0
        for i in range(1, 6):
            if (i + row >= self.SIZE or col-i < 0 ): break
            if (self.board[row + i][col-i] == curTurn):
                armyCount += 1
                break
            elif (self.board[row + i][col-i] != ' '):
                enermyCount += 1
        for i in range(1, 6):
            if (row - i <0   or col + i >=self.SIZE): break
            if (self.board[row - i][col+i] == curTurn):
                armyCount += 1
                break
            elif (self.board[row - i][col+i] != ' '):
                enermyCount += 1


        if (armyCount == 2): return 0
        score = defenseScore[enermyCount]
        # print("minor defense score", score)
        return score

    def find_move(self,curTurn):
        scoreMax = -1000
        move=(-1,-1)
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if (self.board[i][j] == ' '):
                    scoreAttack =self.attack_score_vertical(i,j,curTurn)+self.attack_score_horizontal(i,j,curTurn)+self.attack_score_major(i,j,curTurn) + self.attack_score_minor(i,j,curTurn)

                    scoreDefense =self.defense_score_vertical(i,j,curTurn)+self.defense_score_horizontal(i,j,curTurn)+self.defense_score_major(i,j,curTurn) + self.defense_score_minor(i,j,curTurn)
                    tempScore=scoreAttack
                    # print(i,j,scoreAttack,scoreDefense,self.defense_score_minor(i,j,curTurn))
                    if(tempScore < scoreDefense): tempScore= scoreDefense
                    if(tempScore > scoreMax):
                        scoreMax=tempScore
                        move=(i,j)
                        # print("best score",scoreMax,scoreDefense,self.defense_score_minor(i,j,curTurn))
        return move
    def play_chess(self,move,curTurn):
        self.historyMove=move
        x,y=move
        self.board[x][y]=curTurn
        self.draw_img(x,y,curTurn)

    def check_win(self,prevMove,prevTurn,curTurn):
        row,col= prevMove
        if(self.checkVertical(row,col,prevTurn,curTurn) or self.checkHorizontal(row,col,prevTurn,curTurn) or self.checkMajorDiagonal(row,col,prevTurn,curTurn) or self.checkMinorDiagonal(row,col,prevTurn,curTurn)):
            return prevTurn
        else:
            for i in range(self.SIZE):
                for j in range(self.SIZE):
                    if (self.board[i][j] == ' '): return 'continue'
        return 'draw'
    def heuristic(self):
        move = self.find_move(AI)
        self.play_chess(move,AI)

    def min_value(self, prevMove,curTurn, depth):
        #     if success
        prevTurn = AI

        winnner = self.check_win(prevMove, prevTurn, curTurn)
        print("winner",winnner)
        pprint(self.board)
        if (winnner != 'continue'):
            if (winnner == AI):
                return prevMove, 100000
            else:
                return  prevMove,0
        if (depth >= 2):
            return self.find_move(curTurn), -100000
        bestScore = float('-inf')
        bestMove = (-1, -1)

        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if (self.board[i][j] == ' '):
                    self.board[i][j] = curTurn
                    move, score = self.max_value((i,j),AI, depth+1)
                    if (score > bestScore):
                        bestScore = score
                        bestMove = move
                    self.board[i][j]=' '

        print("best min",bestMove,bestScore)
        return bestMove, -bestScore
    def max_value(self,prevMove,curTurn,depth):
        #if success
        # if(self.check_win()):
        prevTurn = HUMAN

        winnner= self.check_win(prevMove, prevTurn, curTurn)
        print("winner",winnner)

        if (winnner !='continue'):
            if(winnner==HUMAN):
                return prevMove,-100000
            else:
                return  prevMove,0
        if(depth >=2):
            return self.find_move(curTurn),100000

        bestScore=float('-inf')
        bestMove=(-1,-1)
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if (self.board[i][j] == ' '):
                    self.board[i][j]=curTurn
                    move,score= self.min_value( (i,j),HUMAN,depth+1)
                    if(score>bestScore):
                        bestScore=score
                        bestMove=move
                    self.board[i][j]=' '
        print("best max",bestMove,bestScore)
        return bestMove,bestScore


    def minimax(self):
        print("history move",self.historyMove)
        bestMove,bestScore=self.max_value(self.historyMove,AI,1)
        print("minimax",bestMove)
        return bestMove



board = Board(10)
from pprint import pprint
board.draw_grid()
curTurn=HUMAN
run = True
global playing
playing = False
drawGridCkeck = False
while run:  # the game loop
    for event in pygame.event.get():
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if(curTurn==HUMAN):
                board.play_chess(board.get_position(),HUMAN)
                curTurn=AI
                print("human")
                pprint(board.board)
            else:
                bestMove =board.minimax()
                board.play_chess(bestMove, AI)
                curTurn=HUMAN
            pprint(board.board)

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()
    clock.tick(30)  # refresh rate
