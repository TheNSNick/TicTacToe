def tic_tac_toe(board):
    """Returns the squares of a tic-tac-toe or None if none exists."""
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
    if player == 'X':
        enemy = 'O'
    elif player == 'O':
        enemy = 'X'
    else:
        raise NameError('TTT.ideal_move(): Invalid player given.')
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
    if len(forks) > 0:
        return forks[0]
    # check for fork-block
    enemy_forks = forking_moves(board, enemy)
    if len(enemy_forks) > 0:
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
