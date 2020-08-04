import pygame as pg
import ChessEngine
import os
from itertools import cycle
from copy import deepcopy
pg.init()
pg.mixer.init()

ROOT_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(ROOT_DIR, 'images')
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // 8
MAX_FPS = 15
IMAGES = {}
WHITE = (215,215,215)
BLACK = (155,155,155)

def load_images():
    for file in os.listdir(IMAGE_DIR):
        IMAGES[file[:2]] = pg.transform.scale(pg.image.load(os.path.join(IMAGE_DIR, file)), (SQ_SIZE, SQ_SIZE) )


def main():
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    clock = pg.time.Clock()
    game = ChessEngine.GameState()
    load_images()
    running = True
    slctSq = ()
    playerClicks = []
    moves =  []
    while running:
        clock.tick(MAX_FPS)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_LEFT:
                    game.undo_move()

                if e.key == pg.K_RIGHT:
                    game.redo_move()
                
                if e.key == pg.K_BACKSPACE:
                    game.unmake_move()
     

            elif e.type == pg.MOUSEBUTTONDOWN:
                if game.viewmode:
                    game.viewboard = deepcopy(game.board)
                    game.viewmove = len(game.moveLog)
                    game.viewmode = False
                else:
                    location = pg.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if slctSq == (row, col):
                        slctSq = ()
                        playerClicks = []
                        moves = []
                    elif slctSq and (row, col) not in moves:
                        slctSq = ()
                        playerClicks = []
                        moves = []
                    elif len(slctSq) == 0 and game.board[row][col] == "--":
                        pass
                    else:
                        if slctSq:
                            slctSq  = (row, col)
                            playerClicks.append(slctSq)
                            pass
                        else:
                            if (game.board[row][col][0] == 'w' and game.whiteToMove) or (game.board[row][col][0] == 'b' and not game.whiteToMove):
                                moves = game.legal_moves(col, row)
                                slctSq  = (row, col)
                                playerClicks.append(slctSq)
                            else:
                                pass
            
                        

                    if len(playerClicks) == 2:
                        if game.board[playerClicks[0][0]][playerClicks[0][1]] != '--':
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], game.board)
                            print(move.get_chess_notation())
                            game.make_move(move)
                            slctSq = ()
                            playerClicks = []
                            moves = []
                        else:
                            slctSq = ()
                            playerClicks.pop(0)
        
        screen.fill(WHITE)
        draw_game(screen, game, moves)
        if playerClicks:
            if game.board[playerClicks[0][0]][playerClicks[0][1]] != '--':
                highlight(screen, playerClicks[0][0],playerClicks[0][1])
        pg.display.flip()

def highlight(screen, row, col):
    s = pg.Surface((SQ_SIZE,SQ_SIZE))  # the size of your rect
    s.set_alpha(128)                # alpha level
    s.fill((0,128,128))           # this fills the entire surface
    screen.blit(s, (col*SQ_SIZE,row*SQ_SIZE))


def draw_game(screen, game, moves):
    draw_board(screen)
    draw_pieces(screen, game)
    draw_moves(screen, moves)

def draw_board(screen):
    tile_color = cycle([WHITE, BLACK])
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            pg.draw.rect(screen, next(tile_color), (col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE,SQ_SIZE))
        next(tile_color)
    

def draw_pieces(screen, game):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if game.viewboard[row][col] != '--':
                screen.blit(IMAGES[game.viewboard[row][col]], (col*64,row*64))

def draw_moves(screen, moves):
    for i in moves:
        pg.draw.circle(screen, (168, 123, 116), (32+i[1]*64, 32+i[0]*64), 5)


if __name__ == '__main__':
    main()
    

    