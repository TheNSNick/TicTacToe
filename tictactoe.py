import pygame, sys, random
from pygame.locals import *

# CONSTANTS
# scalars
SCREEN_HEIGHT = SCREEN_WIDTH = 600
TILE_SIZE = SCREEN_HEIGHT / 3
LINE_WIDTH = 5
X_WIDTH = 10
O_WIDTH = 10
WIN_WIDTH = 25
BORDER = 10
FPS = 30
SLANT_FACTOR = 45  # how 'wobbly' the win line is
AI_MOVE_TIME = 750
# colors
BG_COLOR = (100, 100, 100)
INTRO_BG_COLOR = (200, 200, 200)
INTRO_TEXT_COLOR = (166, 166, 0)
LINE_COLOR = (0, 0, 0)
X_COLOR = (0, 0, 200)
O_COLOR = (200, 0, 0)

def main():
    # pygame inits
    pygame.init()
    DISPLAY_SURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('TIC TAC TOE')
    fps_clock = pygame.time.Clock()
    # game variables
    game_mode = 'INTRO'
    board = new_board()
    num_players = 1
    current_player = 'X'
    win_line_points = None
    intro_1 = create_intro_1()
    # main game loop
    while True:
        # (wait, then) AI move if applicable
        if num_players == 1 and current_player == 'O' and game_mode == 'PLAY':
            ai_move_row, ai_move_col = ideal_move(board, 'O')
            pygame.time.wait(AI_MOVE_TIME)
            if board[ai_move_row][ai_move_col] == '-':
                board[ai_move_row][ai_move_col] = 'O'
                win_squares = tic_tac_toe(board)
                if win_squares is not None:
                    game_mode = 'WIN'
                    win_line_points = set_win_line(win_squares)
                else:
                    current_player = change_player(current_player)
            elif ai_move_col == -1 and ai_move_row == -1:
                game_mode = 'TIE'
            else:
                raise SystemError('Invalid AI move. row,col: '+str(ai_move_row)+str(ai_move_col))
        # event handling
        for event in pygame.event.get():
            # exit
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # player move
            elif event.type == MOUSEBUTTONDOWN and game_mode == 'PLAY':
                tile_x, tile_y = screen_xy_to_tile_xy(event.pos[0], event.pos[1])
                if board[tile_y][tile_x] == '-':
                    board[tile_y][tile_x] = current_player
                    win_squares = tic_tac_toe(board)
                    if win_squares is not None:
                        game_mode = 'WIN'
                        win_line_points = set_win_line(win_squares)
                    else:
                        current_player = change_player(current_player)
            # game mode transitions
            elif event.type == KEYDOWN:
                # TO DO: ACTUAL INTRO TRANSITION
                if (event.key == K_1 or event.key == K_KP1) and game_mode == 'INTRO':
                    num_players = 1
                    game_mode = 'PLAY'
                elif (event.key == K_2 or event.key == K_KP2) and game_mode == 'INTRO':
                    num_players = 2
                    game_mode = 'PLAY'
                if (event.key == K_RETURN or event.key == K_KP_ENTER) and (game_mode == 'WIN' or game_mode == 'TIE'):
                    board = new_board()
                    current_player = 'X'
                    game_mode = 'INTRO'
        # drawing and updating surface
        DISPLAY_SURF.fill(BG_COLOR)
        if game_mode == 'INTRO':
            intro_1_rect = intro_1.get_rect()
            intro_1_rect.center = DISPLAY_SURF.get_rect().center
            DISPLAY_SURF.blit(intro_1, intro_1_rect)
        else:
            draw_lines(DISPLAY_SURF)
            draw_xs(DISPLAY_SURF, board)
            draw_os(DISPLAY_SURF, board)
        if game_mode == 'WIN':
            pygame.draw.line(DISPLAY_SURF, LINE_COLOR, win_line_points[0], win_line_points[1], WIN_WIDTH)
        if game_mode == 'TIE':
            pass
            # TO DO : TIE SCREEN
        pygame.display.update()
        fps_clock.tick(FPS)


def new_board():
    return [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]


def screen_xy_to_tile_xy(x, y):
    """Takes on-screen coordinates and returns tile coordinates.
    """
    if x < TILE_SIZE:
        tile_x = 0
    elif x < 2 * TILE_SIZE:
        tile_x = 1
    else:
        tile_x = 2
    if y < TILE_SIZE:
        tile_y = 0
    elif y < 2 * TILE_SIZE:
        tile_y = 1
    else:
        tile_y = 2
    return tile_x, tile_y


def change_player(player):
    if player == 'X':
        return 'O'
    elif player == 'O':
        return 'X'
    else:
        raise NameError('change_player(): Invalid player given.')


def create_intro_1():
    intro_surface = pygame.Surface((3 * SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2))
    intro_surface.fill(INTRO_BG_COLOR)
    intro_font_large = pygame.font.SysFont(None, 36)
    intro_font_small = pygame.font.SysFont(None, 24)
    intro_text_1 = intro_font_large.render('Tic Tac Toe', True, INTRO_TEXT_COLOR, INTRO_BG_COLOR)
    intro_text_1_rect = intro_text_1.get_rect()
    intro_text_1_rect.midtop = (intro_surface.get_width() / 2, BORDER)
    intro_text_2 = intro_font_small.render('Press 1 for 1P or 2 for 2P.', True, INTRO_TEXT_COLOR, INTRO_BG_COLOR)
    intro_text_2_rect = intro_text_2.get_rect()
    intro_text_2_rect.midtop = (intro_surface.get_width() / 2, intro_text_1_rect.bottom + BORDER)
    intro_surface.blit(intro_text_1, intro_text_1_rect)
    intro_surface.blit(intro_text_2, intro_text_2_rect)
    return intro_surface


def draw_lines(display):
    for i in range(1, 3):
        pygame.draw.line(display, LINE_COLOR, (i*TILE_SIZE, BORDER), (i*TILE_SIZE, SCREEN_HEIGHT-BORDER), LINE_WIDTH)
        pygame.draw.line(display, LINE_COLOR, (BORDER, i*TILE_SIZE), (SCREEN_WIDTH-BORDER, i*TILE_SIZE), LINE_WIDTH)


def draw_xs(display, board):
    left_xs = [k * TILE_SIZE + BORDER for k in range(3)]
    right_xs = [(k + 1) * TILE_SIZE - BORDER for k in range(3)]
    top_ys = [k * TILE_SIZE + BORDER for k in range(3)]
    bottom_ys = [(k + 1) * TILE_SIZE - BORDER for k in range(3)]
    for i in range(3):
        for j in range(3):
            if board[j][i] == 'X':
                pygame.draw.line(display, X_COLOR, (left_xs[i], top_ys[j]), (right_xs[i], bottom_ys[j]), X_WIDTH)
                pygame.draw.line(display, X_COLOR, (right_xs[i], top_ys[j]), (left_xs[i], bottom_ys[j]), X_WIDTH)


def draw_os(display, board):
    center_xs = [(2*k + 1) * TILE_SIZE / 2 for k in range(3)]
    center_ys = [(2*k + 1) * TILE_SIZE / 2 for k in range(3)]
    for i in range(3):
        for j in range(3):
            if board[j][i] == 'O':
                pygame.draw.circle(display, O_COLOR, (center_xs[i], center_ys[j]), TILE_SIZE/2-BORDER, O_WIDTH)


def set_win_line(win_squares):
    if win_squares[0][0] == win_squares[1][0]:
        # horizontal line
        x_1 = random.randint(BORDER, TILE_SIZE/4)
        x_2 = random.randint(10*TILE_SIZE/4, SCREEN_WIDTH-BORDER)
        y_1 = random.randint((2*win_squares[0][0]+1)*TILE_SIZE/2-SLANT_FACTOR, (2*win_squares[0][0]+1)*TILE_SIZE/2+SLANT_FACTOR)
        y_2 = random.randint((2*win_squares[0][0]+1)*TILE_SIZE/2-SLANT_FACTOR, (2*win_squares[0][0]+1)*TILE_SIZE/2+SLANT_FACTOR)
    elif win_squares[0][1] == win_squares[1][1]:
        # vertical line
        x_1 = random.randint((2*win_squares[0][1]+1)*TILE_SIZE/2-SLANT_FACTOR, (2*win_squares[0][1]+1)*TILE_SIZE/2+SLANT_FACTOR)
        x_2 = random.randint((2*win_squares[0][1]+1)*TILE_SIZE/2-SLANT_FACTOR, (2*win_squares[0][1]+1)*TILE_SIZE/2+SLANT_FACTOR)
        y_1 = random.randint(BORDER, TILE_SIZE/4)
        y_2 = random.randint(10*TILE_SIZE/4, SCREEN_HEIGHT-BORDER)
    elif (0, 0) in win_squares:
        # diagonal down
        x_1 = random.randint(BORDER, TILE_SIZE/4)
        x_2 = random.randint(10*TILE_SIZE/4, SCREEN_WIDTH-BORDER)
        y_1 = random.randint(BORDER, TILE_SIZE/4)
        y_2 = random.randint(10*TILE_SIZE/4, SCREEN_WIDTH-BORDER)
    elif (0, 2) in win_squares:
        # diagonal up
        x_1 = random.randint(BORDER, TILE_SIZE/4)
        x_2 = random.randint(10*TILE_SIZE/4, SCREEN_WIDTH-BORDER)
        y_1 = random.randint(10*TILE_SIZE/4, SCREEN_WIDTH-BORDER)
        y_2 = random.randint(BORDER, TILE_SIZE/4)
    else:
        raise SystemError('draw_win_line(): Could not find winning line.')
    return (x_1, y_1), (x_2, y_2)


def tic_tac_toe(board):
    """Returns the squares of a tic-tac-toe or None if none exists.
    """
    for i in range(3):
        row = board[i]
        if row[0] != '-' and row[0] == row[1] and row[0] == row[2]:
            return [(i, j) for j in range(3)]
        col = [board[j][i] for j in range(3)]
        if col[0] != '-' and col[0] == col[1] and col[0] == col[2]:
            return [(j, i) for j in range(3)]
    diag_ups = [board[j][2-j] for j in range(3)]
    if diag_ups[0] != '-' and diag_ups[0] == diag_ups[1] and diag_ups[0] == diag_ups[2]:
        return [(j, 2-j) for j in range(3)]
    diag_downs = [board[j][j] for j in range(3)]
    if diag_downs[0] != '-' and diag_downs[0] == diag_downs[1] and diag_downs[0] == diag_downs[2]:
        return [(j, j) for j in range(3)]
    return None


def winning_moves(board, player):
    """Given the board and player, returns all winning squares.
    """
    moves = []
    for i in range(3):
        r_count = 0
        r_move = None
        for r in board[i]:
            if r == player:
                r_count += 1
            elif r == '-':
                r_move = board[i].index(r)
            else:
                r_move = None
                break
        if r_move is not None and r_count == 2:
            if (i, r_move) not in moves:
                moves.append((i, r_move))
        c_count = 0
        c_move = None
        c_list = [board[0][i], board[1][i], board[2][i]]
        for c in c_list:
            if c == player:
                c_count += 1
            elif c == '-':
                c_move = c_list.index(c)
            else:
                c_move = None
                break
        if c_move is not None and c_count == 2:
            if (c_move, i) not in moves:
                moves.append((c_move, i))
        diag_down_count = 0
        diag_down_move = None
        diag_down_list = [board[0][0], board[1][1], board[2][2]]
        for dd in diag_down_list:
            if dd == player:
                diag_down_count += 1
            elif dd == '-':
                diag_down_move = diag_down_list.index(dd)
            else:
                diag_down_move = None
                break
        if diag_down_move is not None and diag_down_count == 2:
            if (diag_down_move, diag_down_move) not in moves:
                moves.append((diag_down_move, diag_down_move))
        diag_up_count = 0
        diag_up_move = None
        diag_up_list = [board[0][2], board[1][1], board[2][0]]
        for du in diag_up_list:
            if du == player:
                diag_up_count += 1
            elif du == '-':
                diag_up_move = diag_up_list.index(du)
            else:
                diag_up_move = None
                break
        if diag_up_move is not None and diag_up_count == 2:
            if (diag_up_move, 2-diag_up_move) not in moves:
                moves.append((diag_up_move, 2-diag_up_move))
    return moves


def forking_moves(board, player):
    """Given a board and player, returns all forking moves.
    """
    moves = []
    for row in range(3):
        for col in range(3):
            move_sq = (row, col)
            if board[row][col] == '-':
                board[row][col] = player
                if len(winning_moves(board, player)) >= 2 and move_sq not in moves:
                    moves.append(move_sq)
                board[row][col] = '-'
    return moves

def ideal_move(board, player):
    """Given a board and player, returns the ideal move to make.
    """
    if player == 'X':
        enemy = 'O'
    elif player == 'O':
        enemy = 'X'
    else:
        raise NameError('ideal_move(): Invalid player given.')
    # check for win
    wins = winning_moves(board, player)
    if len(wins) > 0:
        return wins[0]
    # check for block
    enemy_wins = winning_moves(board, enemy)
    if len(enemy_wins) > 0:
        return enemy_wins[0]
    # check for fork
    forks = forking_moves(board, player)
    if len(forks) > 1:
        return forks[0]
    # check for fork-block
    enemy_forks = forking_moves(board, enemy)
    if len(enemy_forks) > 1:
        for side in [(0, 1), (1, 0), (1, 2), (2, 1)]:
            if board[side[0]][side[1]] == '-':
                return side
    elif len(enemy_forks) == 1:
        return enemy_forks[0]
    # check for empty center
    if board[1][1] == '-':
        return (1, 1)
    # opposite corner
    for corner in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if board[corner[0]][corner[1]] == '-' and board[2-corner[0]][2-corner[1]] == enemy:
            return (corner[0], corner[1])
    # empty corner
    for corner in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if board[corner[0]][corner[1]] == '-':
            return (corner[0], corner[1])
    # side
    for side in [(0, 1), (1, 0), (1, 2), (2, 1)]:
        if board[side[0]][side[1]] == '-':
            return (side[0], side[1])
    # no spaces left
    return (-1, -1)

if __name__ == '__main__':
    main()
