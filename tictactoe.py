import pygame, sys
from pygame.locals import *
# dimensions
global SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, LINE_WIDTH, BORDER, FPS
SCREEN_HEIGHT = SCREEN_WIDTH = 600
TILE_SIZE = SCREEN_HEIGHT/3
LINE_WIDTH = 5
BORDER = 10
FPS = 30
# colors
global BG_COLOR, LINE_COLOR, X_COLOR, O_COLOR
BG_COLOR = (100, 100, 100)
LINE_COLOR = (0, 0, 0)
X_COLOR = (0, 0, 200)
O_COLOR = (200, 0, 0)# game variables
global  X_MOVES, O_MOVES, GAME_MODE, X_TURN, WINNER, WIN_LINE
X_MOVES = []
O_MOVES = []
GAME_MODE = 'INTRO'
X_TURN = True
WINNER = '-'
WIN_LINE = None

def main():
    global X_MOVES, O_MOVES, GAME_MODE, X_TURN, WINNER, WIN_LINE
    global DISPLAY_SURF, FPS_CLOCK, GAME_MODE
    pygame.init()
    DISPLAY_SURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('TIC TAC TOE')
    FPS_CLOCK = pygame.time.Clock()
    GAME_MODE = 'INTRO'
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and GAME_MODE == 'PLAY':
                move = screenXYtoTile(event.pos[0], event.pos[1])
                if move not in X_MOVES and move not in O_MOVES:
                    if X_TURN:
                        X_MOVES.append(move)
                    else:
                        O_MOVES.append(move)
                    WINNER, WIN_LINE = ticTacToe(X_MOVES, O_MOVES)
                    if WINNER == '-':
                        X_TURN = not X_TURN
                    else:
                        GAME_MODE = 'WIN'
            elif event.type == KEYDOWN:
                # TO DO: ACTUAL INTRO TRANSITION
                if event.key == K_RETURN and GAME_MODE == 'INTRO':
                    GAME_MODE = 'PLAY'
        DISPLAY_SURF.fill(BG_COLOR)
        if GAME_MODE is not 'INTRO':
            drawLines(DISPLAY_SURF)
            drawXs(DISPLAY_SURF, X_MOVES)
            drawOs(DISPLAY_SURF, O_MOVES)
        if GAME_MODE == 'WIN':
            drawWinLine(DISPLAY_SURF, WINNER, WIN_LINE)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def drawLines(display):
    for i in range(1, 3):
        pygame.draw.line(display, LINE_COLOR, (i*TILE_SIZE, BORDER), (i*TILE_SIZE, SCREEN_HEIGHT-BORDER), LINE_WIDTH)
        pygame.draw.line(display, LINE_COLOR, (BORDER, i*TILE_SIZE), (SCREEN_WIDTH-BORDER, i*TILE_SIZE), LINE_WIDTH)

def drawXs(display, Xs):
    for x in Xs:
        if x[0] == 'A':
            left_x = BORDER
            right_x = TILE_SIZE-BORDER
        elif x[0] == 'B':
            left_x = TILE_SIZE + BORDER
            right_x = 2 * TILE_SIZE - BORDER
        elif x[0] == 'C':
            left_x = 2 * TILE_SIZE + BORDER
            right_x = SCREEN_WIDTH - BORDER
        if x[1] == '1':
            top_y = BORDER
            bottom_y = TILE_SIZE - BORDER
        elif x[1] == '2':
            top_y = TILE_SIZE + BORDER
            bottom_y = 2 * TILE_SIZE - BORDER
        elif x[1] == '3':
            top_y = 2 * TILE_SIZE + BORDER
            bottom_y = SCREEN_HEIGHT - BORDER
        pygame.draw.line(display, X_COLOR, (left_x, top_y), (right_x, bottom_y), LINE_WIDTH)
        pygame.draw.line(display, X_COLOR, (left_x, bottom_y), (right_x, top_y), LINE_WIDTH)

def drawOs(display, Os):
    for o in Os:
        if o[0] == 'A':
            center_x = TILE_SIZE / 2
        if o[0] == 'B':
            center_x = 3 * TILE_SIZE / 2
        if o[0] == 'C':
            center_x = 5 * TILE_SIZE / 2
        if o[1] == '1':
            center_y = TILE_SIZE / 2
        if o[1] == '2':
            center_y = 3 * TILE_SIZE / 2
        if o[1] == '3':
            center_y = 5 * TILE_SIZE / 2
        pygame.draw.circle(display, O_COLOR, (center_x, center_y), TILE_SIZE/2-BORDER, LINE_WIDTH)

def drawWinLine(display, winner, line):
    if winner == 'X':
        line_color = X_COLOR
    elif winner == 'O':
        line_color = O_COLOR
    if line == 'HT':
        begin = (BORDER, TILE_SIZE/2)
        end = (SCREEN_WIDTH-BORDER, TILE_SIZE/2)
    elif line == 'HM':
        begin = (BORDER, 3*TILE_SIZE/2)
        end = (SCREEN_WIDTH-BORDER, 3*TILE_SIZE/2)
    elif line == 'HB':
        begin = (BORDER, 5*TILE_SIZE/2)
        end = (SCREEN_WIDTH-BORDER, 5*TILE_SIZE/2)
    elif line == 'VL':
        begin = (TILE_SIZE/2, BORDER)
        end = (TILE_SIZE/2, SCREEN_HEIGHT-BORDER)
    elif line == 'VM':
        begin = (3*TILE_SIZE/2, BORDER)
        end = (3*TILE_SIZE/2, SCREEN_HEIGHT-BORDER)
    elif line == 'VR':
        begin = (5*TILE_SIZE/2, BORDER)
        end = (5*TILE_SIZE/2, SCREEN_HEIGHT-BORDER)
    elif line == 'DD':
        begin = (TILE_SIZE/4, TILE_SIZE/4)
        end = (11*TILE_SIZE/4, 11*TILE_SIZE/4)
    elif line == 'DU':
        begin = (TILE_SIZE/4, 11*TILE_SIZE/4)
        end = (11*TILE_SIZE/4, TILE_SIZE/4)
    pygame.draw.line(display, line_color, begin, end, LINE_WIDTH*2)

def screenXYtoTile(x, y):
    tile = ''
    if x < TILE_SIZE:
        tile += 'A'
    elif x < 2 * TILE_SIZE:
        tile += 'B'
    else:
        tile += 'C'
    if y < TILE_SIZE:
        tile += '1'
    elif y < 2 * TILE_SIZE:
        tile += '2'
    else:
        tile += '3'
    return tile

def ticTacToe(x, o):
    """Returns WINNER, LINE"""
    winner = '-'
    line = None
    if 'A1' in x and 'A2' in x and 'A3' in x:
        winner = 'X'
        line = 'VL'
    elif 'B1' in x and 'B2' in x and 'B3' in x:
        winner = 'X'
        line = 'VM'
    elif 'C1' in x and 'C2' in x and 'C3' in x:
        winner = 'X'
        line = 'VR'
    elif 'A1' in x and 'B1' in x and 'C1' in x:
        winner = 'X'
        line = 'HT'
    elif 'A2' in x and 'B2' in x and 'C2' in x:
        winner = 'X'
        line = 'HM'
    elif 'A3' in x and 'B3' in x and 'C3' in x:
        winner = 'X'
        line = 'HB'
    elif 'A1' in x and 'B2' in x and 'C3' in x:
        winner = 'X'
        line = 'DD'
    elif 'A3' in x and 'B2' in x and 'C1' in x:
        winner = 'X'
        line = 'DU'
    if 'A1' in o and 'A2' in o and 'A3' in o:
        winner = 'O'
        line = 'VL'
    elif 'B1' in o and 'B2' in o and 'B3' in o:
        winner = 'O'
        line = 'VM'
    elif 'C1' in o and 'C2' in o and 'C3' in o:
        winner = 'O'
        line = 'VR'
    elif 'A1' in o and 'B1' in o and 'C1' in o:
        winner = 'O'
        line = 'HT'
    elif 'A2' in o and 'B2' in o and 'C2' in o:
        winner = 'O'
        line = 'HM'
    elif 'A3' in o and 'B3' in o and 'C3' in o:
        winner = 'O'
        line = 'HB'
    elif 'A1' in o and 'B2' in o and 'C3' in o:
        winner = 'O'
        line = 'DD'
    elif 'A3' in o and 'B2' in o and 'C1' in o:
        winner = 'O'
        line = 'DU'
    return winner, line

if __name__ == '__main__':
    main()