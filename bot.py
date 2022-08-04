import math
import time
import copy


def print_board(board):
    board_ = board[0]
    print('  |',end='')
    for i in reversed(board_[7:13]):
        print(i,'|',end='')

    print()
    print(f'{board_[13]}{" "*21}{board_[6]}')
    print('  |',end='')
    for i in board_[:6]:
        print(i,'|',end='')

    print()
    print(f'###{board[1]}###')
    print('------')

    return ' '


def make_move(board,move):
    side = board[1]
    amount = board[0][move]

    boardi = board.copy()

    boardi[0][move] = 0
    adder = 0

    if side == 0:
        for i in range(1,amount+1):
            #if need to put stone in enemy put skip it
            if ((move+i+adder)%14) == 13:
                adder+=1

            boardi[0][(move+i+adder)%14] += 1

            if i == amount and ((move+i+adder)%14) == 6:
                boardi[1] = 1

            #stealll
            elif i == amount and boardi[0][((move+i+adder)%14)] == 1 and \
                    ((move+i+adder)%14) != 6 and ((move+i+adder)%14) != 13\
                    and ((move+i+adder)%14) < 6 :

                boardi[0][6] += boardi[0][12 - ((move+i+adder)%14)] + 1
                boardi[0][12 - ((move+i+adder)%14)] = 0
                boardi[0][((move+i+adder)%14)] = 0

    else:
        for i in range(1,amount+1):
            #if need to put stone in enemy put skip it
            if ((move+i+adder)%14) == 6:
                adder+=1
            boardi[0][(move+i+adder)%14] += 1

            if i == amount and ((move+i+adder)%14) == 13:
                boardi[1] = 0

            #stealll
            elif i == amount and boardi[0][((move+i+adder)%14)] == 1 and \
                    ((move+i+adder)%14) != 6 and ((move+i+adder)%14) != 13 \
                    and ((move+i+adder)%14) > 6:

                boardi[0][13] += boardi[0][12 - ((move+i+adder)%14)] + 1
                boardi[0][12 - ((move+i+adder)%14)] = 0
                boardi[0][((move+i+adder)%14)] = 0


    boardi[1] = int(not boardi[1])
    return boardi


def sort_board(board):
    board[0][6] += sum(board[0][:6])
    board[0][13] += sum(board[0][7:-1])

    board[0][:6] = [0,0,0,0,0,0]
    board[0][7:-1] = [0,0,0,0,0,0]
    return board

def check_win(board,shh = False):
    #return 1 if left side of board won
    #return -1 if right side of board won
    #return 0 if draw
    #return 0 if no one won

    _board = board.copy()
    if (_board[0][:6] == [0,0,0,0,0,0]) or \
       (_board[0][7:-1] == [0,0,0,0,0,0]):

        _board = sort_board(_board)

        if _board[0][6] > _board[0][-1]:
            #print('sssssssssssssssssssss')
            #print_board(board)
            return 1
        elif _board[0][6] < _board[0][-1]:
            return -1
        elif _board[0][6] == _board[0][-1] and shh:
            return 2

    return 0


def ilaigals_moves(board,move):
    if move == 6 or move == 13:
        return -1 #illegal move
    if move > 5 and board[1] == 0:
        return -1 #illegal move
    if move < 7 and board[1] == 1:
        return -1 #illegal move
    if board[0][move] == 0:
        return -1 # illegal move
    if move < 0:
        return -1 #illegal move

    return 0


def minimax(board,depth,maximaizingPlayer,score = 0,prvturn = 0):
    win = check_win(board)
    #print(depth,end=' ')
    if win == 1:
        score+=10 #winning
    elif win == -1:
        score-=10 #lossing
    if prvturn == board[1]:
        score+=5 #have multiple turns

    score+=(board[0][6] - board[0][13])*0.5 #have more stones then the enemy

    if depth == 0 or win != 0:
        return score

    if maximaizingPlayer:
        maxeval = -math.inf
        for mov in range(0,6):
            if ilaigals_moves(board,mov) == -1:
                continue #mov is ilaigal move

            _board = make_move(board,mov)
            eval = minimax(board = _board ,
                           depth=depth-1,maximaizingPlayer=not _board[1],score = score,prvturn=board[1])
            maxeval = max(maxeval,eval)

        return maxeval

    else:
        mineval = math.inf
        for mov in range(7,13):
            if ilaigals_moves(board,mov) == -1:
                continue #mov is ilaigal move
            _board = make_move(board,mov)
            eval = minimax(board = _board,
                           depth= depth-1,maximaizingPlayer= not _board[1],score = score,prvturn=board[1])
            mineval = min(mineval,eval)

        return mineval


def make_best_move(board):
    best_score = -math.inf
    best_move = None

    side = board[1]
    c_board = copy.deepcopy(board)
    if side == 0:
        for i in range(0,6):
            if ilaigals_moves(board,i):
                continue
            board = make_move(board,i)
            score = minimax(board,depth=15,maximaizingPlayer=(not board[1]))

            board = copy.deepcopy(c_board)
            if score > best_score:
                best_score = score
                best_move = i

    else:
        for i in range(7,13):
            if ilaigals_moves(board,i):
                continue

            board = make_move(board,i)
            score = minimax(board,depth=15,maximaizingPlayer=(not board[1]))
            board = copy.deepcopy(c_board)

            if score > best_score:
                best_score = score
                best_move = i

    return best_move,c_board

board = [[4,4,4,4,4,4, 0,
          4,4,4,4,4,4, 0],0]


win = 0
i = 0

d = {1:'you!',-1:'not you!',2:'Draw!'}


while win == 0:
    if True and board[1] == 1:
        print('the board:')
        print_board(board)
        move = int(input('please make your move:'))
    else:
        move,board = make_best_move(board)
        print(f'the best move for this board ({i,board[1]}): is:{move}')

    print_board(board)
    win = check_win(board,shh = True)
    if win == 2:
        print('Draw!')
        break
    board = make_move(board,move)
    win = check_win(board)
    i+=1

print('the winner is:',d[win])
print('the winnig board is:')
print_board(board)
