from random import randint

evaluate_info = {
    'REVERSE_TRIPLE' : 'Player pays triple',
    'REVERSE_DOUBLE' : 'Player pays double',
    'TRIPLE' : 'Player gets triple',
    'DOUBLE' : 'Player gets double',
}

def calculate_potch(potch, bet, result, reverse=False):
    if result == 'TRIPLE':
        potch = potch + (bet * 3) if reverse == False else potch - (bet * 3)
    elif result == 'DOUBLE':
        potch = potch + (bet * 2) if reverse == False else potch - (bet * 2)
    elif result == 'REVERSE_TRIPLE':
        potch = potch - (bet * 3) if reverse == False else potch + (bet * 3)
    elif result == 'REVERSE_DOUBLE':
        potch = potch - (bet * 2) if reverse == False else potch + (bet * 2)

    return potch

def evaluate_text(result):
    if result in evaluate_info.keys():
        return evaluate_info[result]
    elif str(result).isdigit():
        return f'Player got {str(result)}'
    else:
        return 'No result'

def evaluate(dices):

    result = None

    if dices[0] + dices[1] + dices[2] == 3:
        # print('reverse storm / paying triple')
        result = 'REVERSE_TRIPLE'
    elif 1 in dices and 2 in dices and 3 in dices:
        # print('reverse double / paying double')
        result = 'REVERSE_DOUBLE'
    elif 4 in dices and 5 in dices and 6 in dices:
        # print('get double')
        result = 'DOUBLE'
    elif 1 not in dices and (dices[0] == dices[1] and dices[1] == dices[2]):
        # print('storm / get triple')
        result = 'TRIPLE'
    elif dices[0] == dices[1]:
        result = dices[2]
    elif dices[0] == dices[2]:
        result = dices[1]
    elif dices[2] == dices[1]:
        result = dices[0]

    return result

def roll():
    dice_1 = randint(1,6)
    dice_2 = randint(1,6)
    dice_3 = randint(1,6)

    dices = (dice_1, dice_2, dice_3)
    return dices

def play_confirm():
    play = None
    invalid = True

    while invalid:
        play = input('Do you want to play Chinchirorin? ')
        if play in ['y', 'yes', 'ya']:
            play = True
            invalid = False
        elif play in ['n', 'no', 'tidak']:
            play = False
            invalid = False
        else:
            print('wrong input')

    return play

def player_roll(player_name):
    result = None
    for i in range(3):
        dices = roll()
        print(f'{player_name} dices: {str(dices)} - {evaluate_text(evaluate(dices))}')
        result = evaluate(dices)
        if result is not None:
            break
    return result

def compare_player_result(potch, bet, p1_result, p2_result):
    if p1_result is None and p2_result is not None:
        print('tir wins')
        potch = potch + bet
    elif p1_result is not None and p2_result is None:
        print('gaspar wins')
        potch = potch - bet
    elif p1_result == p2_result:
        pass
    elif p1_result > p2_result:
        print('gaspar wins')
        potch = potch - bet
    elif p1_result < p2_result:
        print('tir wins')
        potch = potch + bet
    
    return potch

def game(potch):

    invalid = True
    while invalid:
        bet = input('How much you want to bet: ')
        if bet.isdigit():
            bet = int(bet)
            invalid = False
        elif bet.isdigit() and bet > potch:
            print('Bet cannot be more than your current potch')
        else:
            print('Wrong input...')

    p1_result = player_roll('Gaspar')

    if p1_result in ['REVERSE_TRIPLE', 'REVERSE_DOUBLE', 'DOUBLE', 'TRIPLE']:
        potch = calculate_potch(potch, bet, p1_result, reverse=True)
    else:
        p2_result = player_roll('Tir')
        if p2_result in ['REVERSE_TRIPLE', 'REVERSE_DOUBLE', 'DOUBLE', 'TRIPLE']:
            potch = calculate_potch(potch, bet, p2_result, reverse=False)
        else:
            potch = compare_player_result(potch, bet, p1_result, p2_result)

    return potch

def game_over_check(potch):
    return True if potch <= 0 or potch > 999999 else False

def potch_adjuster(potch):
    if potch <= 0:
        return 0
    elif potch > 999999:
        return 999999
    else:
        return potch

def start():
    potch = 10000
    game_over = False
    play = play_confirm()
    while play is True and game_over is False:
        print('Your potch:', potch)
        potch = game(potch)
        print('Current potch:', potch_adjuster(potch))
        game_over = game_over_check(potch)
        if game_over == False:
            play = play_confirm()

    print('Your final potch:', potch_adjuster(potch))

if __name__ == '__main__':
    start()