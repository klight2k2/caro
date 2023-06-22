
import random
import time
import pygame
from pprint import pprint
import math

pygame.init()
HUMAN = 'b'
AI = 'w'
pygame.display.set_caption("Tic Tac Toe")  # the caption\
WIDTH = 800
HEIGHT = 800
ximg = pygame.image.load("images/X.png")
oimg = pygame.image.load("images/O.png")
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # screen setup
LINE_COLOR = (228, 231, 236)
clock = pygame.time.Clock()  # the Clock object for framerate
BACKGROUND = (254, 254, 254)

class BoardGame:
    def __init__(self, size):
        self.size = size
        self.board = self.make_empty_board(size)
        self.move_history = []
        self.win = False

    def make_empty_board(self, sz):
        board = []
        for _ in range(sz):
            board.append([" "] * sz)
        return board

    def is_empty(self):
        return self.board == [[' '] * self.size] * self.size

    def is_in(self, y, x):
        return 0 <= y < self.size and 0 <= x < self.size

    def is_win(self):
        black = self.score_of_col('b')
        white = self.score_of_col('w')

        self.sum_sumcol_values(black)
        self.sum_sumcol_values(white)

        if 5 in black and black[5] == 1:
            return 'Black won'
        elif 5 in white and white[5] == 1:
            return 'White won'

        if sum(black.values()) == black[-1] and sum(white.values()) == white[-1] or self.possible_moves() == []:
            return 'Draw'

        return 'Continue playing'

    def march(self, y, x, dy, dx, length):
        yf = y + length * dy
        xf = x + length * dx

        while not self.is_in(yf, xf):
            yf -= dy
            xf -= dx

        return yf, xf

    def score_ready(self, scorecol):
        sumcol = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
        for key in scorecol:
            for score in scorecol[key]:
                if key in sumcol[score]:
                    sumcol[score][key] += 1
                else:
                    sumcol[score][key] = 1

        return sumcol

    def sum_sumcol_values(self, sumcol):
        for key in sumcol:
            if key == 5:
                sumcol[5] = int(1 in sumcol[5].values())
            else:
                sumcol[key] = sum(sumcol[key].values())

    def score_of_list(self, lis, col):
        blank = lis.count(' ')
        filled = lis.count(col)

        if blank + filled < 5:
            return -1
        elif blank == 5:
            return 0
        else:
            return filled

    def row_to_list(self, y, x, dy, dx, yf, xf):
        row = []
        while y != yf + dy or x != xf + dx:
            row.append(self.board[y][x])
            y += dy
            x += dx
        return row

    def score_of_row(self, cordi, dy, dx, cordf, col):
        colscores = []
        y, x = cordi
        yf, xf = cordf
        row = self.row_to_list(y, x, dy, dx, yf, xf)

        for start in range(len(row) - 4):
            score = self.score_of_list(row[start:start + 5], col)
            colscores.append(score)

        return colscores

    def score_of_col(self, col):
        f = self.size
        scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}
        for start in range(self.size):
            scores[(0, 1)].extend(self.score_of_row((start, 0), 0, 1, (start, f - 1), col))
            scores[(-1, 1)].extend(self.score_of_row((0, start), 1, 1, (f - 1, start), col))
            scores[(1, 0)].extend(self.score_of_row((start, 0), 1, 0, (f - 1, start), col))
            scores[(1, 1)].extend(self.score_of_row((0, start), 1, 1, (start, f - 1), col))

        return self.score_ready(scores)

    def possible_moves(self):
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != ' ':
                    for x in range(max(0, i - 3), min(self.size, i + 4)):
                        for y in range(max(0, j - 3), min(self.size, j + 4)):
                            if self.board[x][y] == ' ':
                                moves.append((x, y))
        return moves

    def best_move(self, col):
        moves = self.possible_moves()
        best_score = -1
        best_move = None

        for move in moves:
            self.board[move[0]][move[1]] = col
            score = self.evaluate(col)
            self.board[move[0]][move[1]] = ' '

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def evaluate(self, col):
        score = self.score_of_col(col)
        return score[5] * 1000 + score[4] * 100 + score[3] * 10 + score[2]

    def play(self):
        while not self.win:
            # Player's turn
            print("Player's turn")
            y = int(input("Enter the y coordinate: "))
            x = int(input("Enter the x coordinate: "))

            if self.is_in(y, x) and self.board[y][x] == ' ':
                self.board[y][x] = 'b'
                self.move_history.append((y, x))
            else:
                print("Invalid move! Try again.")

            self.display()

            # Check for win or draw
            game_status = self.is_win()
            if game_status != 'Continue playing':
                self.win = True
                print(game_status)
                break

            # AI's turn
            print("AI's turn")
            move = self.best_move('w')
            self.board[move[0]][move[1]] = 'w'
            self.move_history.append(move)

            self.display()

            # Check for win or draw
            game_status = self.is_win()
            if game_status != 'Continue playing':
                self.win = True
                print(game_status)
                break

    def display(self):
        for row in self.board:
            print(" ".join(row))
        print()

game = BoardGame(15)
game.play()
