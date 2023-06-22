
import random
import time
import pygame
from pprint import pprint
import math

pygame.init()
HUMAN = 'b'
AI = 'w'
pygame.display.set_caption("Tic Tac Toe")  # the caption\
WIDTH = 400
HEIGHT = 400
CEIL=40
ximg = pygame.image.load("images/X.png")
ximg=pygame.transform.scale(ximg,(40,40))
oimg = pygame.image.load("images/O.png")
oimg=pygame.transform.scale(oimg,(40,40))

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # screen setup
LINE_COLOR = (228, 231, 236)
clock = pygame.time.Clock()  # the Clock object for framerate
BACKGROUND = (254, 254, 254)

move_history = []
win = False
caseAI = ['ww00w0', '0ww00w', 'w0w0w0', '0w00ww', '0w0w0w', 'w00ww0', '000ww0', '00w0w0', '00ww00', '000ww00', '00w0w00', '0ww000', '0www00', '0ww0w0', '0w0ww0', '00ww0w', '00w0ww', '000www', 'www000', 'ww0w00', 'w0ww00', '0ww0w0', '0w0ww0', '00www0', '00www0', '0www00', '00www00', '00ww0w0', '00w0ww0', '000www0', '0w0w0w0w', '0w0ww00w', '0w00ww0w', '0www000', '0ww0w00', '0w0ww00', '00www00', 'w0w0w0w0', 'w0ww00w0', 'w00ww0w0', '00wwww', '0w0www', '0ww0ww', '0www0w', '0www0w', '0wwww0', '0wwww0', 'w0www0', 'ww0ww0', 'www0w0', 'www0w0', 'wwww00', '0wwwww', 'wwwww0']
caseUser =['bb00b0', '0bb00b', 'b0b0b0', '0b00bb', '0b0b0b', 'b00bb0', '000bb0', '00b0b0', '00bb00', '000bb00', '00b0b00', '0bb000', '0bbb00', '0bb0b0', '0b0bb0', '00bb0b', '00b0bb', '000bbb', 'bbb000', 'bb0b00', 'b0bb00', '0bb0b0', '0b0bb0', '00bbb0', '00bbb0', '0bbb00', '00bbb00', '00bb0b0', '00b0bb0', '000bbb0', '0b0b0b0b', '0b0bb00b', '0b00bb0b', '0bbb000', '0bb0b00', '0b0bb00', '00bbb00', 'b0b0b0b0', 'b0bb00b0', 'b00bb0b0', '00bbbb', '0b0bbb', '0bb0bb', '0bbb0b', '0bbb0b', '0bbbb0', '0bbbb0', 'b0bbb0', 'bb0bb0', 'bbb0b0', 'bbb0b0', 'bbbb00', '0bbbbb', 'bbbbb0']
SIZE=10
point = [
    	4, 4, 4,4, 4, 4,
    	8, 8, 8,
    	8, 8, 8, 8, 8, 8, 
    	8,
    	8, 8, 8,
    	8, 8, 8, 8, 8, 8, 
    	8,
    	500, 500, 500, 500, 500, 500, 500,
    	500, 500, 500, 500, 500, 500, 500,
    	1000, 1000, 1000, 1000, 1000, 1000,
    	1000, 1000, 1000, 1000, 1000, 1000,
    	100000,
    	100000];
attackScore = {0, 3, 24, 192, 1536, 12288}; 


def evaluateState(board):
    splitSymbol=';'
    rem=''
    for i in range(SIZE):
        for j in range(SIZE):
            rem+=board[i][j]
        rem+=splitSymbol
        for j in range(SIZE):
            rem+=board[j][i]
        rem+=splitSymbol 
        
    for i in range(SIZE-4):
        for j in range(SIZE-i):
            rem+=board[j][i+j]
        rem+=splitSymbol  
    for i in range(SIZE-5):
        for j in range(SIZE-i):
            rem+=board[i+j][j]
        rem+=splitSymbol      
    # check nửa trên đường chéo trái ( / )
    for i in range(4, SIZE):
        for j in range(i + 1):
            rem += board[i - j][j]
        rem += ";"

    # check nửa dưới đường chéo trái ( / )
    for i in range(SIZE - 5, 0, -1):
        for j in range(SIZE - 1, i - 1, -1):
            rem += board[j][i + SIZE - j - 1]
        rem += ";\n"
    
    
    find1 = ""
    find2 = ""
    diem = 0

    # Tính điểm của trạng thái
    for i in range(len(caseUser)):
        find1 = caseAI[i]  # duyệt những đường chiến lược của AI
        find2 = caseUser[i]  # duyệt những đường chiến lược của User
        diem += point[i] * rem.count(find1)  # cộng vào điểm lượng giá của AI
        diem -= point[i] * rem.count(find2)  # trừ đi điểm lượng giá của User

    return diem

     
           
def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append(["0"] * sz)
    return board


def is_empty(board):
    return board == [['0'] * len(board)] * len(board)


def is_in(board, y, x):
    return 0 <= y < len(board) and 0 <= x < len(board)


def is_win(board):
    black = score_of_col(board, 'b')
    white = score_of_col(board, 'w')

    sum_sumcol_values(black)
    sum_sumcol_values(white)

    if 5 in black and black[5] == 1:
        return 'Black won'
    elif 5 in white and white[5] == 1:
        return 'White won'

    if sum(black.values()) == black[-1] and sum(white.values()) == white[-1] or possible_moves(board) == []:
        return 'Draw'

    return 'Continue playing'


##AI Engine

def march(board, y, x, dy, dx, length):
    '''
    tìm vị trí xa nhất trong dy,dx trong khoảng length

    '''
    yf = y + length * dy
    xf = x + length * dx
    # chừng nào yf,xf không có trong board
    while not is_in(board, yf, xf):
        yf -= dy
        xf -= dx

    return yf, xf


def score_ready(scorecol):
    '''
    Khởi tạo hệ thống điểm

    '''
    sumcol = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    for key in scorecol:
        for score in scorecol[key]:
            if key in sumcol[score]:
                sumcol[score][key] += 1
            else:
                sumcol[score][key] = 1

    return sumcol


def sum_sumcol_values(sumcol):
    '''
    hợp nhất điểm của mỗi hướng
    '''

    for key in sumcol:
        if key == 5:
            sumcol[5] = int(1 in sumcol[5].values())
        else:
            sumcol[key] = sum(sumcol[key].values())


def score_of_list(lis, col):
    blank = lis.count('0')
    filled = lis.count(col)

    if blank + filled < 5:
        return -1
    elif blank == 5:
        return 0
    else:
        return filled


def row_to_list(board, y, x, dy, dx, yf, xf):
    '''
    trả về list của y,x từ yf,xf

    '''
    row = []
    while y != yf + dy or x != xf + dx:
        row.append(board[y][x])
        y += dy
        x += dx
    return row


def score_of_row(board, cordi, dy, dx, cordf, col):
    '''
    trả về một list với mỗi phần tử đại diện cho số điểm của 5 khối

    '''
    colscores = []
    y, x = cordi
    yf, xf = cordf
    row = row_to_list(board, y, x, dy, dx, yf, xf)
    # print("score", row)

    for start in range(len(row) - 4):
        score = score_of_list(row[start:start + 5], col)
        colscores.append(score)

    return colscores


def score_of_col(board, col):
    '''
    tính toán điểm số mỗi hướng của column dùng cho is_win;
    '''

    f = len(board)
    # scores của 4 hướng đi
    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}
    for start in range(len(board)):
        scores[(0, 1)].extend(score_of_row(board, (start, 0), 0, 1, (start, f - 1), col))
        scores[(1, 0)].extend(score_of_row(board, (0, start), 1, 0, (f - 1, start), col))
        scores[(1, 1)].extend(score_of_row(board, (start, 0), 1, 1, (f - 1, f - 1 - start), col))
        scores[(-1, 1)].extend(score_of_row(board, (start, 0), -1, 1, (0, start), col))

        if start + 1 < len(board):
            scores[(1, 1)].extend(score_of_row(board, (0, start + 1), 1, 1, (f - 2 - start, f - 1), col))
            scores[(-1, 1)].extend(score_of_row(board, (f - 1, start + 1), -1, 1, (start + 1, f - 1), col))

    return score_ready(scores)


def score_of_col_one(board, col, y, x):
    '''
    trả lại điểm số của column trong y,x theo 4 hướng,
    key: điểm số khối đơn vị đó -> chỉ ktra 5 khối thay vì toàn bộ
    '''

    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}

    scores[(0, 1)].extend(score_of_row(board, march(board, y, x, 0, -1, 4), 0, 1, march(board, y, x, 0, 1, 4), col))

    scores[(1, 0)].extend(score_of_row(board, march(board, y, x, -1, 0, 4), 1, 0, march(board, y, x, 1, 0, 4), col))

    scores[(1, 1)].extend(score_of_row(board, march(board, y, x, -1, -1, 4), 1, 1, march(board, y, x, 1, 1, 4), col))

    scores[(-1, 1)].extend(score_of_row(board, march(board, y, x, -1, 1, 4), 1, -1, march(board, y, x, 1, -1, 4), col))

    return score_ready(scores)


def possible_moves(board):
    '''
    khởi tạo danh sách tọa độ có thể có tại danh giới các nơi đã đánh phạm vi 3 đơn vị
    '''
    # mảng taken lưu giá trị của người chơi và của máy trên bàn cờ
    taken = []
    # mảng directions lưu hướng đi (8 hướng)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    # cord: lưu các vị trí không đi 
    cord = {}

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != '0':
                taken.append((i, j))
    ''' duyệt trong hướng đi và mảng giá trị trên bàn cờ của người chơi và máy, kiểm tra nước không thể đi(trùng với 
    nước đã có trên bàn cờ)
    '''
    for direction in directions:
        dy, dx = direction
        for coord in taken:
            y, x = coord
            for length in [1, 2, 3, 4]:
                move = march(board, y, x, dy, dx, length)
                if move not in taken and move not in cord:
                    cord[move] = False
    return cord


def TF34score(score3, score4):
    '''
    trả lại trường hợp chắc chắn có thể thắng(4 ô liên tiếp)
    '''
    for key4 in score4:
        if score4[key4] >= 1:
            for key3 in score3:
                if key3 != key4 and score3[key3] >= 2:
                    return True
    return False


def stupid_score(board, col, anticol, y, x):
    '''
    cố gắng di chuyển y,x
    trả về điểm số tượng trưng lợi thế 
    '''

    M = 1000
    res, adv, dis = 0, 0, 0

    # tấn công
    board[y][x] = col
    # draw_stone(x,y,colors[col])
    sumcol = score_of_col_one(board, col, y, x)
    # print(sumcol)
    a = winning_situation(sumcol)
    adv += a * M
    sum_sumcol_values(sumcol)
    # {0: 0, 1: 15, 2: 0, 3: 0, 4: 0, 5: 0, -1: 0}
    adv += sumcol[-1] + sumcol[1] + 4 * sumcol[2] + 8 * sumcol[3] + 16 * sumcol[4]

    # phòng thủ
    board[y][x] = anticol
    sumanticol = score_of_col_one(board, anticol, y, x)
    d = winning_situation(sumanticol)
    dis += d * (M - 100)
    sum_sumcol_values(sumanticol)
    dis += sumanticol[-1] + sumanticol[1] + 4 * sumanticol[2] + 8 * sumanticol[3] + 16 * sumanticol[4]

    res = adv + dis

    board[y][x] = '0'
    return res


def winning_situation(sumcol):
    '''
    trả lại tình huống chiến thắng dạng như:
    {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    1-5 lưu điểm có độ nguy hiểm từ thấp đến cao,
    -1 là rơi vào trạng thái tồi, cần phòng thủ
    '''

    if 1 in sumcol[5].values():
        return 5
    elif len(sumcol[4]) >= 2 or (len(sumcol[4]) >= 1 and max(sumcol[4].values()) >= 2):
        return 4
    elif TF34score(sumcol[3], sumcol[4]):
        return 4
    else:
        score3 = sorted(sumcol[3].values(), reverse=True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
            return 3
    return 0


def best_move(board, col):
    '''
    trả lại điểm số của mảng trong lợi thế của từng màu
    '''
    if col == 'w':
        anticol = 'b'
    else:
        anticol = 'w'

    movecol = (0, 0)
    curScore=0
    maxscorecol = ''
    # kiểm tra nếu bàn cờ rỗng thì cho vị trí random nếu không thì đưa ra giá trị trên bàn cờ nên đi 
    if is_empty(board):
        movecol = (int((len(board)) * random.random()), int((len(board[0])) * random.random()))
    else:
        moves = possible_moves(board)

        for move in moves:
            y, x = move
            if maxscorecol == '':
                scorecol = stupid_score(board, col, anticol, y, x)
                maxscorecol = scorecol
                movecol = move
                curScore+=scorecol
            else:
                scorecol = stupid_score(board, col, anticol, y, x)
                curScore+=scorecol
                if scorecol > maxscorecol:
                    maxscorecol = scorecol
                    movecol = move
    return scorecol

##Graphics Engine
def draw_img( y, x,curnTurn):
    posx = x * 40
    posy = y * 40
    if (curnTurn == HUMAN):
        screen.blit(ximg, (posy,posx))
    else:
        screen.blit(oimg, ( posy,posx))
    pygame.display.update()
def get_position():  # to render the image at the clicked position update value of curTurn as in whose turn it is
        x,y = pygame.mouse.get_pos()
        x = math.floor(x / 80)
        y = math.floor(y / 80)
        # print(y,x)
        return (x,y)
board = make_empty_board(10)
def click(x,y):
    global board
    if x == -1 and y == -1 and len(move_history) != 0:
        x, y = move_history[-1]

        del (move_history[-1])
        board[y][x] = "0"
        x, y = move_history[-1]

        del (move_history[-1])
        board[y][x] = "0"
        return

    if not is_in(board, y, x):
        return

    if board[y][x] == '0':
        draw_img(x, y, HUMAN)
        board[y][x] = 'b'


        move_history.append((x, y))

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            win = True
            return

        ay, ax = minimax(board,(y,x))
        print(ay, ax)
        draw_img(ax,ay, AI)
        board[ay][ax] = 'w'
        print("board",board)
        pprint(board)

        move_history.append((ax, ay))

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            win = True
            return
def draw_grid():
        screen.fill(BACKGROUND)
        x = 0
        y = 0
        for l in range(10):
            x += 40
            y += 40
            pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, WIDTH), 2)
            pygame.draw.line(screen, LINE_COLOR, (0, y), (HEIGHT, y), 2)
def min_value(board,curTurn, depth):
    #     if success
    prevTurn = AI
    curTurn=HUMAN
    winnner = is_win(board)
    print("winner min",winnner)

    if (depth >= 3):
        state=evaluateState(board)
        print("state",state)
        return state
    bestScore = float('inf')

    moves = possible_moves(board)
    if is_empty(board):
        bestMove = (int((len(board)) * random.random()), int((len(board[0])) * random.random()))
    else:
        for move in moves:
            y,x = move
            board[y][x] =curTurn
            tempScore =  max_value(board,AI,depth+1)
            if tempScore < bestScore:
                bestScore = tempScore
            board[y][x] ='0'
            
   
    # print("best min",bestMove,bestScore)
    return bestScore
def max_value(board,curTurn,depth):
    prevTurn = HUMAN

    winnner = is_win(board)
    print("winner min",winnner)

    if (depth >= 3):
        state=evaluateState(board)
        print("state",state)
        return state
    bestScore = float('-inf')

    moves = possible_moves(board)
    pprint(moves)
    if is_empty(board):
        bestMove = (int((len(board)) * random.random()), int((len(board[0])) * random.random()))
    else:
        for move in moves:
            y,x = move
            board[y][x] =curTurn
            tempScore = min_value(board,HUMAN, depth+1)
            if tempScore > bestScore:
                bestScore = tempScore
            board[y][x] ='0'
            
    return bestScore


def minimax(board,prevMove):
    curTurn=AI
    winnner = is_win(board)
    print("winner min",winnner)

    bestScore = float('-inf')
    bestMove=(-1,-1)
    moves = possible_moves(board)
    pprint(moves)
    if is_empty(board):
        bestMove = (int((len(board)) * random.random()), int((len(board[0])) * random.random()))
    else:
        for move in moves:
            y,x = move
            board[y][x] =curTurn
            tempScore = min_value(board,HUMAN, 2)
            if tempScore > bestScore:
                bestScore = tempScore
                bestMove=move
            board[y][x] ='0'
    return bestMove

       
draw_grid()
run = True
global playing
playing = False
drawGridCkeck = False
while run:  # the game loop
    for event in pygame.event.get():
        if (event.type == pygame.MOUSEBUTTONDOWN):
           x,y=get_position()
           click(x,y)
           print("click",x,y)

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()
    clock.tick(30)  # refresh rate

