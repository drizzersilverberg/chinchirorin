from random import randint
from utils import get_lang, clear_screen

MAX_POTCH = 999999
MIN_POTCH = 0

evaluate_info = {
    'REVERSE_TRIPLE' : get_lang('en', 'player_pays_triple'),
    'REVERSE_DOUBLE' : get_lang('en', 'player_pays_double'),
    'TRIPLE' : get_lang('en', 'player_gets_triple'),
    'DOUBLE' : get_lang('en', 'player_gets_double'),
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
        return get_lang('en', 'player_got_result', {'_RESULT_' : str(result)})
    else:
        return get_lang('en', 'no_result')

def evaluate(dices):

    result = None

    if dices[0] + dices[1] + dices[2] == 3:
        result = 'REVERSE_TRIPLE'
    elif 1 in dices and 2 in dices and 3 in dices:
        result = 'REVERSE_DOUBLE'
    elif 4 in dices and 5 in dices and 6 in dices:
        result = 'DOUBLE'
    elif 1 not in dices and (dices[0] == dices[1] and dices[1] == dices[2]):
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
        play = input(get_lang('en', 'do_you_want_to_play_chinchirorin'))
        if play in ['y', 'yes', 'ya']:
            play = True
            invalid = False
            clear_screen()
        elif play in ['n', 'no', 'tidak']:
            play = False
            invalid = False
        else:
            print(get_lang('en', 'wrong_input'))

    return play

def player_roll(player_name):
    result = None
    for i in range(3):
        dices = roll()
        print(f"{player_name} {get_lang('en', 'dices')}: {str(dices)} - {evaluate_text(evaluate(dices))}")
        result = evaluate(dices)
        if result is not None:
            break
    return result

def compare_player_result(potch, bet, p1_result, p2_result):
    if p1_result is None and p2_result is not None:
        print(get_lang('en', 'player_win', {'_PLAYER_': 'Tir'}))
        potch = potch + bet
    elif p1_result is not None and p2_result is None:
        print(get_lang('en', 'player_win', {'_PLAYER_': 'Gaspar'}))
        potch = potch - bet
    elif p1_result == p2_result:
        pass
    elif p1_result > p2_result:
        print(get_lang('en', 'player_win', {'_PLAYER_': 'Gaspar'}))
        potch = potch - bet
    elif p1_result < p2_result:
        print(get_lang('en', 'player_win', {'_PLAYER_': 'Tir'}))
        potch = potch + bet

    return potch

def game(potch):

    invalid = True
    while invalid:
        bet = input(get_lang('en','how_much_you_want_to_bet'))
        if bet.isdigit() and int(bet) > potch:
            clear_screen()
            print(get_lang('en', 'your_potch', {'_POTCH_': potch}))
            print(get_lang('en', 'bet_cannot_be_more_than_your_current_potch'))
        elif bet.isdigit():
            bet = int(bet)
            invalid = False
            clear_screen()
        else:
            print(get_lang('en','wrong_input'))

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
    return True if potch <= MIN_POTCH or potch > MAX_POTCH else False

def potch_adjuster(potch):
    if potch <= MIN_POTCH:
        return MIN_POTCH
    elif potch > MAX_POTCH:
        return MAX_POTCH
    else:
        return potch

def start():
    potch = 10000
    game_over = False
    play = play_confirm()
    while play is True and game_over is False:
        print(get_lang('en', 'your_potch', {'_POTCH_': potch_adjuster(potch)}))
        potch = game(potch)
        print(get_lang('en', 'current_potch', {'_POTCH_': potch_adjuster(potch)}))
        game_over = game_over_check(potch)
        if game_over == False:
            play = play_confirm()

    print(get_lang('en', 'your_final_potch', {'_POTCH_': potch_adjuster(potch)}))

if __name__ == '__main__':
    start()