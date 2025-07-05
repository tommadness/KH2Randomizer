import random

number_of_squares = 143

def has_bingo(board,drawn_numbers):
    # row 1
    if board[0] in drawn_numbers and \
        board[1] in drawn_numbers and \
        board[2] in drawn_numbers and \
        board[3] in drawn_numbers and \
        board[4] in drawn_numbers:
        return True
    # row 2
    if board[5] in drawn_numbers and \
        board[6] in drawn_numbers and \
        board[7] in drawn_numbers and \
        board[8] in drawn_numbers and \
        board[9] in drawn_numbers:
        return True
    # row 3
    if board[10] in drawn_numbers and \
        board[11] in drawn_numbers and \
        board[12] in drawn_numbers and \
        board[13] in drawn_numbers and \
        board[14] in drawn_numbers:
        return True
    # row 4
    if board[15] in drawn_numbers and \
        board[16] in drawn_numbers and \
        board[17] in drawn_numbers and \
        board[18] in drawn_numbers and \
        board[19] in drawn_numbers:
        return True
    # row 5
    if board[20] in drawn_numbers and \
        board[21] in drawn_numbers and \
        board[22] in drawn_numbers and \
        board[23] in drawn_numbers and \
        board[24] in drawn_numbers:
        return True
    # col 1
    if board[0] in drawn_numbers and \
        board[5] in drawn_numbers and \
        board[10] in drawn_numbers and \
        board[15] in drawn_numbers and \
        board[20] in drawn_numbers:
        return True
    # col 2
    if board[1] in drawn_numbers and \
        board[6] in drawn_numbers and \
        board[11] in drawn_numbers and \
        board[16] in drawn_numbers and \
        board[21] in drawn_numbers:
        return True
    # col 3
    if board[2] in drawn_numbers and \
        board[7] in drawn_numbers and \
        board[12] in drawn_numbers and \
        board[17] in drawn_numbers and \
        board[22] in drawn_numbers:
        return True
    # col 4
    if board[3] in drawn_numbers and \
        board[8] in drawn_numbers and \
        board[13] in drawn_numbers and \
        board[18] in drawn_numbers and \
        board[23] in drawn_numbers:
        return True
    # col 5
    if board[4] in drawn_numbers and \
        board[9] in drawn_numbers and \
        board[14] in drawn_numbers and \
        board[19] in drawn_numbers and \
        board[24] in drawn_numbers:
        return True
    # TLBR
    if board[0] in drawn_numbers and \
        board[6] in drawn_numbers and \
        board[12] in drawn_numbers and \
        board[18] in drawn_numbers and \
        board[24] in drawn_numbers:
        return True
    # BLTR
    if board[4] in drawn_numbers and \
        board[8] in drawn_numbers and \
        board[12] in drawn_numbers and \
        board[16] in drawn_numbers and \
        board[20] in drawn_numbers:
        return True

    return False

def bingo_game():
    square_possibilities = list(range(number_of_squares))
    bingo_board = random.sample(square_possibilities,k=25)
    random.shuffle(square_possibilities)
    for n in range(len(square_possibilities)):
        if has_bingo(bingo_board,square_possibilities[0:n+1]):
            return n+1,bingo_board,square_possibilities[0:n+1]
    return -1

game_counts = {}
for n in range(-1,number_of_squares+1):
    game_counts[n] = 0

for n in range(5000000):
    counter,board,called = bingo_game()
    game_counts[counter]+=1
    if n%10000==0:
        print(n)

for n in range(-1,number_of_squares+1):
    print(f"{n},{game_counts[n]}")

print(game_counts)
