import copy
import random
import sys
import pygame
import numpy as np


from constants import *

#pygame_setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)

class Board:

    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_sqrs = self.squares # [squares]
        self.marked_sqrs = 0
    
    def final_state(self, show = False):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''

        #vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    ipos = (col * SQ_SIZE + SQ_SIZE // 2, 20)
                    fpos = (col * SQ_SIZE + SQ_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, ipos, fpos, LINE_WIDTH)
                return self.squares[0][col]
                
        #horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    ipos = (20, row * SQ_SIZE + SQ_SIZE // 2)
                    fpos = (WIDTH - 20, row * SQ_SIZE + SQ_SIZE // 2)
                    pygame.draw.line(screen, color, ipos, fpos, LINE_WIDTH)
                return self.squares[row][0]


        #descending diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                    color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                    ipos = (20, 20)
                    fpos = (WIDTH - 20, HEIGHT - 20)
                    pygame.draw.line(screen, color, ipos, fpos, LINE_WIDTH)
            return self.squares[1][1]

        #ascending diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                    color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                    ipos = (20, HEIGHT - 20)
                    fpos = (WIDTH - 20, 20)
                    pygame.draw.line(screen, color, ipos, fpos, LINE_WIDTH)
            return self.squares[1][1]

        return 0    

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs

    def is_full(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:
    def  __init__(self, level=1, player = 2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col)

    #minimax function

    def minimax(self, board, maximizing):
        #terminal case
        case = board.final_state()

        #player 1 wins
        if case == 1:
            return 1, None #eval, move

        #player 2 wins
        if case == 2:
            return -1, None #eval, move

        #draw
        elif board.is_full():
            return 0, None #eval, move

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for row, col in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move


    def eval(self, main_board):
        if self.level == 0:
            #random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            #minimax algo choice
            eval, move = self.minimax(main_board, False)
            
        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move # row, col

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 #1-cross #2-circles
        self.gamemode = 'ai' # pvp or ai
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):
        #bg
        screen.fill(BG_COLOR)

        #vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQ_SIZE, 0), (SQ_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQ_SIZE, 0), (WIDTH - SQ_SIZE, HEIGHT), LINE_WIDTH)

        #horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQ_SIZE), (WIDTH, SQ_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQ_SIZE), (WIDTH, HEIGHT - SQ_SIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            #draw cross

            # descending line 
            start_desc = (col * SQ_SIZE + OFFSET, row * SQ_SIZE + OFFSET)
            end_desc = ((col + 1) * SQ_SIZE - OFFSET, row * SQ_SIZE + SQ_SIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            # ascending line
            start_asc = (col * SQ_SIZE + OFFSET, row * SQ_SIZE + SQ_SIZE - OFFSET)
            end_asc = (col * SQ_SIZE + SQ_SIZE - OFFSET, row * SQ_SIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            #draw circle
            center = (col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1
        
    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()

    def reset(self):
        self.__init__()

def main():

    #object 
    game = Game()
    board = game.board
    ai = game.ai

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQ_SIZE
                col = pos[0] // SQ_SIZE

                if board.empty_sqr(row, col):
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

            if event.type == pygame.KEYDOWN:

                #g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                #r-reset
                if event.key == pygame.K_r:
                    #reset game
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0

                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            #update the screen
            pygame.display.update()

            #ai methods
            row, col = ai.eval(board)

            game.make_move(row, col)

        pygame.display.update()

main()