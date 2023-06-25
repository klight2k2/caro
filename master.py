import pygame
from pprint import pprint
import math

pygame.init()
pygame.display.set_caption("Tic Tac Toe") 

# init constants
HUMAN = 'b'
AI = 'w'
DRAW='draw'
WIDTH = 480
HEIGHT = 480
CEIL=48
SIZE=10
RULE=5

# WIDTH = 240
# HEIGHT = 240
# CEIL=80
# SIZE=3
# RULE=3
win=False
move_history=[]
# Các đường chiến lược để thắng ván cờ
caseAI = ['ww00w0', '0ww00w', 'w0w0w0', '0w00ww', '0w0w0w', 'w00ww0', 
          '000ww0', '00w0w0', '00ww00', 
          '000ww00', '00w0w00', '0ww000', '0www00', '0ww0w0', '0w0ww0', '00ww0w', '00w0ww', '000www', 'www000', 'ww0w00', 'w0ww00', '0ww0w0', '0w0ww0', '00www0', '00www0', '0www00', '00www00', '00ww0w0', '00w0ww0', '000www0', '0w0w0w0w', '0w0ww00w', '0w00ww0w', '0www000', '0ww0w00', '0w0ww00', '00www00', 'w0w0w0w0', 'w0ww00w0', 'w00ww0w0', '00wwww', '0w0www', '0ww0ww', '0www0w', '0www0w', '0wwww0', '0wwww0', 'w0www0', 'ww0ww0', 'www0w0', 'www0w0', 'wwww00', '0wwwww', 'wwwww0']
caseHuman =['bb00b0', '0bb00b', 'b0b0b0', '0b00bb', '0b0b0b', 'b00bb0', '000bb0', '00b0b0', '00bb00', '000bb00', '00b0b00', '0bb000', '0bbb00', '0bb0b0', '0b0bb0', '00bb0b', '00b0bb', '000bbb', 'bbb000', 'bb0b00', 'b0bb00', '0bb0b0', '0b0bb0', '00bbb0', '00bbb0', '0bbb00', '00bbb00', '00bb0b0', '00b0bb0', '000bbb0', '0b0b0b0b', '0b0bb00b', '0b00bb0b', '0bbb000', '0bb0b00', '0b0bb00', '00bbb00', 'b0b0b0b0', 'b0bb00b0', 'b00bb0b0', '00bbbb', '0b0bbb', '0bb0bb', '0bbb0b', '0bbb0b', '0bbbb0', '0bbbb0', 'b0bbb0', 'bb0bb0', 'bbb0b0', 'bbb0b0', 'bbbb00', '0bbbbb', 'bbbbb0']
# Điểm đánh giá của các đường chiến lược
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
# import image 
ximg = pygame.image.load("images/X.png")
ximg=pygame.transform.scale(ximg,(CEIL,CEIL))
oimg = pygame.image.load("images/O.png")
oimg=pygame.transform.scale(oimg,(CEIL,CEIL))

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # screen setup
LINE_COLOR = (228, 231, 236)
clock = pygame.time.Clock()  # the Clock object for framerate
BACKGROUND = (254, 254, 254)

class CheckState():
    def __init__(self,board):
        self.board=board
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
            if (row + k >= SIZE): break
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
            if (col + k >= SIZE): break
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
            if (row + k >= SIZE or col + k >= SIZE): break
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
            if (row - k < 0 or col + k >= SIZE): break
            if (self.board[row - k][col + k] == prevTurn):
                cnt += 1
            elif (self.board[row - k][col + k] == curTurn):
                head = True
                break
            else:
                break
        for k in range(1, RULE + 1):
            if (row + k >= SIZE or col - k < 0): break
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
    def check_win(self,prevMove,prevTurn,curTurn):
        row,col= prevMove
        if(self.checkVertical(row,col,prevTurn,curTurn) or self.checkHorizontal(row,col,prevTurn,curTurn) or self.checkMajorDiagonal(row,col,prevTurn,curTurn) or self.checkMinorDiagonal(row,col,prevTurn,curTurn)):
            return prevTurn
        else:
            for i in range(SIZE):
                for j in range(SIZE):
                    if (self.board[i][j] == '0'): return 'continue'
        return 'draw'


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append(["0"] * sz)
    return board

def is_empty(board):
    '''
    Kiểm tra xem board có rỗng không
    '''
    return board == [['0'] * len(board)] * len(board)


def is_in(board, y, x):
    '''
    Kiểm tra vị trí có tọa độ (x,y) có tồn tại trong board không
    '''
    return 0 <= y < len(board) and 0 <= x < len(board)


def march(board, y, x, dy, dx, length):
    '''
    tìm kiếm vị trí xa nhất trong khoảng length
    '''
    yf = y + length * dy
    xf = x + length * dx
    
    while not is_in(board, yf, xf):
        yf -= dy
        xf -= dx

    return yf, xf

def all_moves(board):
    taken=[]
    for i in range(len(board)):
        for j in range(len(board)):
            if(board[i][j]=="0"): taken.append((i,j))
    return taken
def possible_moves(board):
    '''
    Tìm kiếm các nước đi có thể đi( các nước cách những nước đã đánh trong phạm vi nhất định)
    '''
    # mảng taken lưu giá trị của người chơi và của máy trên bàn cờ
    taken = []
    # mảng directions lưu hướng đi (8 hướng)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    # mảng cord lưu các vị trí có thể đi
    cord = []

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
                    cord.append(move)
    return cord

def count_list_strategic_roads(strategic_roads):
    '''
    Hệ thống các đường chiến lược

    '''
    list_strategic_road = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    for key in strategic_roads:
        for road in strategic_roads[key]:
            if key in list_strategic_road[road]:
                list_strategic_road[road][key] += 1
            else:
                list_strategic_road[road][key] = 1

    return list_strategic_road


def list_road_of_player(sumcol):
    '''
    hợp nhất điểm của mỗi hướng
    '''

    for key in sumcol:
        if key == 5:
            sumcol[5] = int(1 in sumcol[5].values())
        else:
            sumcol[key] = sum(sumcol[key].values())


def score_of_list(lis, player):
    '''
    Trả về các trường hợp chiến lược để chiến thắng
    ví dụ 1: là  001000
    '''
    blank = lis.count('0')
    filled = lis.count(player)

    if blank + filled < 5:
        return -1
    elif blank == 5:
        return 0
    else:
        return filled


def convert_row_to_list(board, y, x, dy, dx, yf, xf):
    '''
    trả về list của y,x từ yf,xf

    '''
    row = []
    while y != yf + dy or x != xf + dx:
        row.append(board[y][x])
        y += dy
        x += dx
    return row


def score_of_row(board, cordi, dy, dx, cordf, player):
    '''
    trả về một list với mỗi phần tử đại diện cho số điểm của 5 khối

    '''
    strategicRoad = []
    y, x = cordi
    yf, xf = cordf
    row = convert_row_to_list(board, y, x, dy, dx, yf, xf)
    # print("score", row)

    for start in range(len(row) - 4):
        road = score_of_list(row[start:start + 5], player)
        strategicRoad.append(road)

    return strategicRoad


def score_of_board(board, player):
    '''
    tính toán điểm số mỗi hướng của player dùng cho is_win;
    '''

    f = len(board)
    # scores của 4 hướng đi
    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}
    for start in range(len(board)):
        scores[(0, 1)].extend(score_of_row(board, (start, 0), 0, 1, (start, f - 1), player))
        scores[(1, 0)].extend(score_of_row(board, (0, start), 1, 0, (f - 1, start), player))
        scores[(1, 1)].extend(score_of_row(board, (start, 0), 1, 1, (f - 1, f - 1 - start), player))
        scores[(-1, 1)].extend(score_of_row(board, (start, 0), -1, 1, (0, start), player))

        if start + 1 < len(board):
            scores[(1, 1)].extend(score_of_row(board, (0, start + 1), 1, 1, (f - 2 - start, f - 1), player))
            scores[(-1, 1)].extend(score_of_row(board, (f - 1, start + 1), -1, 1, (start + 1, f - 1), player))

    return count_list_strategic_roads(scores)


def score_of_ceil(board, player, y, x):
    '''
    trả lại điểm số của playerumn trong y,x theo 4 hướng,
    key: điểm số khối đơn vị đó -> chỉ ktra 5 khối thay vì toàn bộ
    '''

    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}

    scores[(0, 1)].extend(score_of_row(board, march(board, y, x, 0, -1, 4), 0, 1, march(board, y, x, 0, 1, 4), player))

    scores[(1, 0)].extend(score_of_row(board, march(board, y, x, -1, 0, 4), 1, 0, march(board, y, x, 1, 0, 4), player))

    scores[(1, 1)].extend(score_of_row(board, march(board, y, x, -1, -1, 4), 1, 1, march(board, y, x, 1, 1, 4), player))

    scores[(-1, 1)].extend(score_of_row(board, march(board, y, x, -1, 1, 4), 1, -1, march(board, y, x, 1, -1, 4), player))

    return count_list_strategic_roads(scores)
def checkRoad34(road3, road4):
    '''
    trả lại trường hợp chắc chắn có thể thắng(4 ô liên tiếp)
    kiểm tra nước đôi chắc chắn thắng
    '''
    for key4 in road4:
        if road4[key4] >= 1:
            for key3 in road3:
                if key3 != key4 and road3[key3] >= 2:
                    return True
    return False



def calc_score(board, player, rival, y, x):
    '''
    cố gắng di chuyển y,x
    trả về điểm số tượng trưng lợi thế 
    '''

    M = 1000
    res, adv, dis = 0, 0, 0

    # tấn công
    board[y][x] = player
    # draw_stone(x,y,colors[col])
    road_of_player = score_of_ceil(board, player, y, x)
    # print(road_of_player)
    a = winning_situation(road_of_player)
    adv += a * M
    list_road_of_player(road_of_player)
    # {0: 0, 1: 15, 2: 0, 3: 0, 4: 0, 5: 0, -1: 0}
    adv += road_of_player[-1] + road_of_player[1] + 4 * road_of_player[2] + 8 * road_of_player[3] + 16 * road_of_player[4]

    # phòng thủ
    board[y][x] = rival
    road_of_rival = score_of_ceil(board, rival, y, x)
    d = winning_situation(road_of_rival)
    dis += d * (M - 100)
    list_road_of_player(road_of_rival)
    dis += road_of_rival[-1] + road_of_rival[1] + 4 * road_of_rival[2] + 8 * road_of_rival[3] + 16 * road_of_rival[4]

    res = adv + dis

    board[y][x] = '0'
    return res
def winning_situation(road_of_player):
    '''
    trả lại tình huống chiến thắng dạng như:
    {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    1-5 lưu điểm có độ nguy hiểm từ thấp đến cao,
    -1 là rơi vào trạng thái tồi, cần phòng thủ
    '''

    if 1 in road_of_player[5].values():
        return 5
    elif len(road_of_player[4]) >= 2 or (len(road_of_player[4]) >= 1 and max(road_of_player[4].values()) >= 2):
        return 4
    elif checkRoad34(road_of_player[3], road_of_player[4]):
        return 4
    else:
        road3 = sorted(road_of_player[3].values(), reverse=True)
        if len(road3) >= 2 and road3[0] >= road3[1] >= 2:
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
    maxscorecol = float('-inf')
    # kiểm tra nếu bàn cờ rỗng thì cho vị trí random nếu không thì đưa ra giá trị trên bàn cờ nên đi 
    if is_empty(board):
        movecol = (SIZE/2,SIZE/2)
    else:
        moves = possible_moves(board)

        for move in moves:
            y, x = move
            scorecol = calc_score(board, col, anticol, y, x)
            curScore+=scorecol
            if scorecol > maxscorecol:
                maxscorecol = scorecol
                movecol = move
    return movecol

def draw_img( y, x,curnTurn):
    posx = x * CEIL
    posy = y * CEIL
    if (curnTurn == HUMAN):
        screen.blit(ximg, (posy,posx))
    else:
        screen.blit(oimg, ( posy,posx))
    pygame.display.update()
def get_position():
        '''
        lấy vị trí người vừa đánh trên bàn cờ
        return (x,y)
        '''  
        x,y = pygame.mouse.get_pos()
        x = math.floor(x / CEIL)
        y = math.floor(y / CEIL)
        # print(y,x)
        return (x,y)

def draw_grid():
        '''
        vẽ bàn cờ
        '''
        screen.fill(BACKGROUND)
        x = 0
        y = 0
        for l in range(SIZE):
            x += CEIL
            y += CEIL
            pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, WIDTH), 2)
            pygame.draw.line(screen, LINE_COLOR, (0, y), (HEIGHT, y), 2)

# minimax kết hợp sử dụng hàm heuristic 8 hướng, đánh giá trạng thái của bàn
def evaluateState(board):
    splitSymbol=';'
    rem=''
    # check dọc và ngang
    for i in range(SIZE):
        for j in range(SIZE):
            rem+=board[i][j]
        rem+=splitSymbol
        for j in range(SIZE):
            rem+=board[j][i]
        rem+=splitSymbol 
    # check nửa trên đường chéo phải
    for i in range(SIZE-4):
        for j in range(SIZE-i):
            rem+=board[j][i+j]
        rem+=splitSymbol  
    # check nửa dưới đường chéo phải
    for i in range(SIZE-5):
        for j in range(SIZE-i):
            rem+=board[i+j][j]
        rem+=splitSymbol      
    # check nửa trên đường chéo trái 
    for i in range(4, SIZE):
        for j in range(i + 1):
            rem += board[i - j][j]
        rem += splitSymbol

    # check nửa dưới đường chéo trái 
    for i in range(SIZE - 5, 0, -1):
        for j in range(SIZE - 1, i - 1, -1):
            rem += board[j][i + SIZE - j - 1]
        rem += splitSymbol
    
    
    find1 = ""
    find2 = ""
    score = 0

    # Tính điểm của trạng thái
    for i in range(len(caseHuman)):
        find1 = caseAI[i]  # duyệt những đường chiến lược của AI
        find2 = caseHuman[i]  # duyệt những đường chiến lược của User
        score += point[i] * rem.count(find1)  # cộng vào điểm lượng giá của AI
        score -= point[i] * rem.count(find2)  # trừ đi điểm lượng giá của User

    return score
 
def is_win(board):
    human = score_of_board(board, HUMAN)
    ai = score_of_board(board, AI)

    list_road_of_player(human)
    list_road_of_player(ai)

    if 5 in human and human[5] == 1:
        return HUMAN
    elif 5 in ai and ai[5] == 1:
        return AI

    if sum(human.values()) == human[-1] and sum(ai.values()) == ai[-1] or possible_moves(board) == []:
        return DRAW

    return 'Continue playing'

# ----------------------------------------------------------------
# hàm minimax kết hợp tri thức bổ sung
def min_value(board, depth):
    winner = is_win(board)
    # print("winner min",winner)
    if(winner==AI):
        return 100000
    elif(winner==HUMAN):
        return -100000
    elif(winner==DRAW):
        return 0
    if (depth >= 3):
        state=evaluateState(board)
        # print("state",state)
        return state
    bestScore = float('inf')

    moves = possible_moves(board)
    if is_empty(board):
        bestMove = (SIZE/2,SIZE/2)
    else:
        for move in moves:
            y,x = move
            board[y][x] =HUMAN
            tempScore =  max_value(board,depth+1)
            if tempScore < bestScore:
                bestScore = tempScore
            board[y][x] ='0'
    return bestScore
def max_value(board,depth):
    winner = is_win(board)
    if(winner==AI):
        return 100000
    elif(winner==HUMAN):
        return -100000
    elif(winner==DRAW):
        return 0

    if (depth >= 3):
        state=evaluateState(board)
        # print("state",state)
        return state
    bestScore = float('-inf')

    moves = possible_moves(board)
    # pprint(moves)
    if is_empty(board):
        bestMove = (SIZE/2,SIZE/2)
    else:
        for move in moves:
            y,x = move
            board[y][x] =AI
            tempScore = min_value(board, depth+1)
            if tempScore > bestScore:
                bestScore = tempScore
            board[y][x] ='0'
            
    return bestScore

def minimax(board):
    curTurn=AI
    winner = is_win(board)
    # print("winner min",winner)

    bestScore = float('-inf')
    bestMove=(-1,-1)
    moves = possible_moves(board)
    # pprint(moves)
    if is_empty(board):
        bestMove = (SIZE/2,SIZE/2)
    else:
        for move in moves:
            y,x = move
            board[y][x] =curTurn
            tempScore = min_value(board, 2)
            if tempScore > bestScore:
                bestScore = tempScore
                bestMove=move
            board[y][x] ='0'
    return bestMove
def find_minimax(x,y):
    global board,win

    if not is_in(board, y, x) or board[y][x] != '0':
        return

    if board[y][x] == '0':
        draw_img(x, y, HUMAN)
        board[y][x] = HUMAN


        move_history.append((x, y))

        game_res = is_win(board)
        if game_res in [ HUMAN,AI,DRAW]:
            print_game(game_res) 
            return

        ay, ax = minimax(board)
        print(ay, ax)
        draw_img(ax,ay, AI)
        board[ay][ax] = AI
        print("board",board)
        pprint(board)

        move_history.append((ax, ay))

        game_res = is_win(board)
        if game_res in [ HUMAN,AI,DRAW]:
            print_game(game_res) 
            return
# ----------------------------------------------------------------
# hàm minimax kết hợp alpha beta và tri thức bổ sung
def min_value_ab(board, depth,alpha,beta):
    winner = is_win(board)
    # print("winner min",winner)
    if(winner==AI):
        return 100000
    elif(winner==HUMAN):
        return -100000
    elif(winner==DRAW):
        return 0
    if (depth >= 3):
        state=evaluateState(board)
        # print("state",state)
        return state
    bestScore = float('inf')

    moves = possible_moves(board)
    if is_empty(board):
        bestMove = (SIZE/2,SIZE/2)
    else:
        for move in moves:
            y,x = move
            board[y][x] =HUMAN
            tempScore =  max_value_ab(board,depth+1,alpha,beta)
            if tempScore < bestScore:
                bestScore = tempScore
            board[y][x] ='0'
            beta=min(beta,bestScore)
            if(beta<=alpha): break
    return bestScore
def max_value_ab(board,depth,alpha,beta):
    winner = is_win(board)
    if(winner==AI):
        return 100000
    elif(winner==HUMAN):
        return -100000
    elif(winner==DRAW):
        return 0

    if (depth >= 3):
        state=evaluateState(board)
        # print("state",state)
        return state
    bestScore = float('-inf')

    moves = possible_moves(board)
    # pprint(moves)
    if is_empty(board):
        bestMove = (SIZE/2,SIZE/2)
    else:
        for move in moves:
            y,x = move
            board[y][x] =AI
            tempScore = min_value_ab(board, depth+1,alpha,beta)
            if tempScore > bestScore:
                bestScore = tempScore
            board[y][x] ='0'
            alpha=max(alpha,bestScore)
            if(beta<=alpha): break
            
    return bestScore


def minimax_ab(board):
    alpha=float('-inf')
    beta=float('inf')
    curTurn=AI
    winner = is_win(board)
    # print("winner min",winner)

    bestScore = float('-inf')
    bestMove=(-1,-1)
    moves = possible_moves(board)
    # pprint(moves)
    if is_empty(board):
        bestMove = (SIZE/2,SIZE/2)
    else:
        for move in moves:
            y,x = move
            board[y][x] =curTurn
            tempScore = min_value_ab(board, 2,alpha,beta)
            if tempScore > bestScore:
                bestScore = tempScore
                bestMove=move
            board[y][x] ='0'
            alpha=max(alpha,bestScore)
            if(beta<=alpha): break
    return bestMove
# Tìm kiếm với tri thức bổ sung kết hợp minimax  
def find_minimax_ab(x,y):
    global board,win

    if not is_in(board, y, x) or board[y][x] != '0':
        return

    if board[y][x] == '0':
        draw_img(x, y, HUMAN)
        board[y][x] = HUMAN


        move_history.append((x, y))

        game_res = is_win(board)
        if game_res in [ HUMAN,AI,DRAW]:
            print_game(game_res) 
            return

        ay, ax = minimax_ab(board)
        print(ay, ax)
        draw_img(ax,ay, AI)
        board[ay][ax] = AI
        print("board",board)
        pprint(board)

        move_history.append((ax, ay))

        game_res = is_win(board)
        if game_res in [ HUMAN,AI,DRAW]:
            print_game(game_res) 
            return
#  Tìm kiếm với tri thức bổ sung
def heuristic(x,y):
    global board
    if not is_in(board, y, x) or board[y][x] != '0':
        return

    if board[y][x] == '0':
        draw_img(x, y, HUMAN)
        board[y][x] = 'b'


        move_history.append((x, y))

        game_res = is_win(board)
        if game_res in [ HUMAN,AI,DRAW]:
            print_game(game_res) 
            return

        ay, ax = best_move(board,AI)
        print(ay, ax)
        draw_img(ax,ay, AI)
        board[ay][ax] = 'w'
        print("board",board)
        pprint(board)

        move_history.append((ax, ay))

        game_res = is_win(board)
        if game_res in [ HUMAN,AI,DRAW]:
            print_game(game_res) 
            return
# def minimax_not_heuristic():
def min_value_not_heuristic(board,move, depth):
    winner = CheckState(board).check_win(move,AI,HUMAN)
    print("winner min",winner)
    if(winner==AI):
        return 100000
    elif(winner==HUMAN):
        return -100000
    elif(winner==DRAW):
        return 0
    # if (depth >= 3):
    #     state=evaluateState(board)
    #     print("state",state)
    #     return state
    bestScore = float('inf')

    moves = all_moves(board)
    if is_empty(board):
        bestMove = (SIZE/2,SIZE/2)
    else:
        for move in moves:
            y,x = move
            board[y][x] =HUMAN
            tempScore =  max_value_not_heuristic(board,move,depth+1)
            if tempScore < bestScore:
                bestScore = tempScore
            board[y][x] ='0'
    return bestScore
def max_value_not_heuristic(board,move,depth):
    winner = CheckState(board).check_win(move,HUMAN,AI)
    if(winner==AI):
        return 100000
    elif(winner==HUMAN):
        return -100000
    elif(winner==DRAW):
        return 0

    # if (depth >= 3):
    #     state=evaluateState(board)
    #     print("state",state)
    #     return state
    bestScore = float('-inf')

    moves = all_moves(board)
    # pprint(moves)
    if is_empty(board):
        bestMove = (SIZE/2,SIZE/2)
    else:
        for move in moves:
            y,x = move
            board[y][x] =AI
            tempScore = min_value_not_heuristic(board,move, depth+1)
            if tempScore > bestScore:
                bestScore = tempScore
            board[y][x] ='0'
            
    return bestScore

def minimax_not_heuristic(board):
    bestScore = float('-inf')
    bestMove=(-1,-1)
    moves = all_moves(board)
    # pprint(moves)
    if is_empty(board):
        bestMove = (SIZE/2,SIZE/2)
    else:
        for move in moves:
            y,x = move
            board[y][x] =AI
            tempScore = min_value_not_heuristic(board,move, 2)
            if tempScore > bestScore:
                bestScore = tempScore
                bestMove=move
            board[y][x] ='0'
    return bestMove
def not_heuristic(x,y):
    global board
   
    if not is_in(board, y, x) or board[y][x] != '0':
        return

    if board[y][x] == '0':
        draw_img(x, y, HUMAN)
        board[y][x] = 'b'


        move_history.append((x, y))

        game_res = CheckState(board).check_win((y,x),HUMAN,AI)
        if game_res in [ HUMAN,AI,DRAW]:
            print_game(game_res) 
            return

        ay, ax = minimax_not_heuristic(board)
        print(ay, ax)
        draw_img(ax,ay, AI)
        board[ay][ax] = 'w'
        print("board",board)

        pprint(board)

        move_history.append((ax, ay))
        game_res = CheckState(board).check_win((ay,ax),AI,HUMAN)
        print("game_res",game_res)
        pprint(board)
        if game_res in [ HUMAN,AI,DRAW]:
            print_game(game_res)
            return



# def minimax_not_heuristic():
def min_value_ab_not_heuristic(board,move, depth,alpha,beta):
    winner = CheckState(board).check_win(move,AI,HUMAN)
    # print("winner min",winner)
    if(winner==AI):
        return 100000
    elif(winner==HUMAN):
        return -100000
    elif(winner==DRAW):
        return 0
    # if (depth >= 3):
    #     state=evaluateState(board)
    #     print("state",state)
    #     return state
    bestScore = float('inf')

    moves = all_moves(board)
    if is_empty(board):
        bestMove = (SIZE/2,SIZE/2)
    else:
        for move in moves:
            y,x = move
            board[y][x] =HUMAN
            tempScore =  max_value_ab_not_heuristic(board,move,depth+1,alpha,beta)
            if tempScore < bestScore:
                bestScore = tempScore
            board[y][x] ='0'
            beta=min(beta,bestScore)
            if(beta<=alpha): break
    return bestScore
def max_value_ab_not_heuristic(board,move,depth,alpha,beta):
    winner = CheckState(board).check_win(move,HUMAN,AI)
    if(winner==AI):
        return 100000
    elif(winner==HUMAN):
        return -100000
    elif(winner==DRAW):
        return 0

    # if (depth >= 3):
    #     state=evaluateState(board)
    #     print("state",state)
    #     return state
    bestScore = float('-inf')

    moves = all_moves(board)
    # pprint(moves)
    if is_empty(board):
        bestMove = (SIZE/2,SIZE/2)
    else:
        for move in moves:
            y,x = move
            board[y][x] =AI
            tempScore = min_value_ab_not_heuristic(board,move, depth+1,alpha,beta)
            if tempScore > bestScore:
                bestScore = tempScore
            board[y][x] ='0'
            alpha=max(alpha,bestScore)
            if(beta<=alpha): break
            
    return bestScore

def minimax_ab_not_heuristic(board):
    alpha=float('-inf')
    beta=float('inf')
    bestScore = float('-inf')
    bestMove=(-1,-1)
    moves = all_moves(board)
    # pprint(moves)
    if is_empty(board):
        bestMove = (SIZE/2,SIZE/2)
    else:
        for move in moves:
            y,x = move
            board[y][x] =AI
            tempScore = min_value_ab_not_heuristic(board,move, 2,alpha,beta)
            if tempScore > bestScore:
                bestScore = tempScore
                bestMove=move
            board[y][x] ='0'
            alpha=max(alpha,bestScore)
            if(beta<=alpha): break
    return bestMove
def ab_not_heuristic(x,y):
    global board
   
    if not is_in(board, y, x) or board[y][x] != '0':
        return

    if board[y][x] == '0':
        draw_img(x, y, HUMAN)
        board[y][x] = 'b'


        move_history.append((x, y))

        game_res = CheckState(board).check_win((y,x),HUMAN,AI)
        if game_res in [ HUMAN,AI,DRAW]:
            print_game(game_res) 
            return

        ay, ax = minimax_ab_not_heuristic(board)
        print(ay, ax)
        draw_img(ax,ay, AI)
        board[ay][ax] = 'w'
        print("board",board)

        pprint(board)

        move_history.append((ax, ay))
        game_res = CheckState(board).check_win((ay,ax),AI,HUMAN)
        print("game_res",game_res)
        pprint(board)
        if game_res in [ HUMAN,AI,DRAW]:
            print_game(game_res)
            return

import button
font = pygame.font.SysFont('Georgia', 15)
minimax_heuristic = button.button(WIDTH /2, HEIGHT /2 - 50, font, 'Minimax+ heuristic')
minimax_alpha_beta_heuristic= button.button(WIDTH /2, HEIGHT /2 , font, 'Minimax +alpha beta heuristic')
heuristic_button = button.button(WIDTH /2, HEIGHT /2 +50 , font, 'heuristic')
minimax_button = button.button(WIDTH /2, HEIGHT /2 -150 , font, 'minimax')
minimax_alpha_beta_button = button.button(WIDTH /2, HEIGHT /2 -100 , font, 'minimax alpha beta')
bg = pygame.image.load("images/bg.jpg")
def print_game(winner):
    global win
    if winner==HUMAN: winner='human '
    if winner==AI: winner='ai '
    congra = button.button(HEIGHT /2, WIDTH /2, font, winner+"won")    
    congra.draw_button(screen)
    win=True
def initialize():
    mode=1    
    global board,win
    board=make_empty_board(SIZE)
    draw_grid()
    run = True
    # global playing
    playing = False
    drawGridCkeck = False
    while run:  
        for event in pygame.event.get():
            if drawGridCkeck:
                drawGridCkeck=False
                draw_grid()
            if(playing):
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    x,y=get_position()
                    if(win): break
                    if(mode==1) :
                        not_heuristic(x,y)
                    elif(mode==2) :
                        ab_not_heuristic(x,y)
                    elif(mode==3) :
                        find_minimax(x,y)
                    elif(mode==4) :
                        find_minimax_ab(x,y)
                    elif(mode==5) :
                        heuristic(x,y)
                    print("click",x,y)
            else:
                
                screen.blit(bg, (0, 0))
                if minimax_button.draw_button(screen):
                    playing = True
                    mode=1
                    drawGridCkeck=True
                    print('minimax')
                if minimax_alpha_beta_button.draw_button(screen):
                    print('minimax alpha beta')
                    playing = True
                    mode=2
                    drawGridCkeck=True
                if minimax_heuristic.draw_button(screen):
                    playing = True
                    mode=3
                    drawGridCkeck=True
                    print('heuristic + minimax')
                    drawGridCkeck=True
                if minimax_alpha_beta_heuristic.draw_button(screen):
                    playing = True
                    mode=4
                    drawGridCkeck=True
                    print('minimax alpha beta heuristic')
                if heuristic_button.draw_button(screen):
                    playing = True
                    mode=5
                    drawGridCkeck=True
                    print('heuristic')

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(30) 

initialize()