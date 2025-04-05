from random import randint
from utils import get_lang, clear_screen, get_locales

MAX_POTCH       = 999999
MIN_POTCH       = 0
LOCALES         = get_locales()
DEFAULT_LOCALE  = 'en'

evaluate_info = {
    'REVERSE_TRIPLE' : 'player_pays_triple',
    'REVERSE_DOUBLE' : 'player_pays_double',
    'TRIPLE' : 'player_gets_triple',
    'DOUBLE' : 'player_gets_double',
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

def evaluate_text(result, locale='en'):
    if result in evaluate_info.keys():
        return get_lang(evaluate_info[result], locale=locale)
    elif str(result).isdigit():
        return get_lang('player_got_result', replacer={'_RESULT_' : str(result)}, locale=locale)
    else:
        return get_lang('no_result', locale=locale)

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

def play_confirm(locale='en'):
    play = None
    invalid = True

    while invalid:
        play = str(input(get_lang('do_you_want_to_play_chinchirorin', locale=locale))).lower()
        if play in ['y', 'yes', 'ya']:
            play = True
            invalid = False
            clear_screen()
        elif play in ['n', 'no', 'tidak']:
            play = False
            invalid = False
        else:
            print(get_lang('wrong_input', locale=locale))

    return play

def player_roll(player_name, locale='en'):
    result = None
    for i in range(3):
        dices = roll()
        print(f"{player_name} {get_lang('dices', locale=locale)}: {str(dices)} - {evaluate_text(evaluate(dices), locale=locale)}")
        result = evaluate(dices)
        if result is not None:
            break
    return result

def compare_player_result(potch, bet, p1_result, p2_result, locale='en'):
    if p1_result is None and p2_result is not None:
        print(get_lang('player_win', replacer={'_PLAYER_': 'Tir'}, locale=locale))
        potch = potch + bet
    elif p1_result is not None and p2_result is None:
        print(get_lang('player_win', replacer={'_PLAYER_': 'Gaspar'}, locale=locale))
        potch = potch - bet
    elif p1_result == p2_result:
        print(get_lang('its_a_tie', locale=locale))
    elif p1_result > p2_result:
        print(get_lang('player_win', replacer={'_PLAYER_': 'Gaspar'}, locale=locale))
        potch = potch - bet
    elif p1_result < p2_result:
        print(get_lang('player_win', replacer={'_PLAYER_': 'Tir'}, locale=locale))
        potch = potch + bet

    return potch

def game(potch, locale='en'):

    invalid = True
    while invalid:
        bet = input(get_lang('how_much_you_want_to_bet', locale=locale))
        if bet.isdigit() and int(bet) > potch:
            clear_screen()
            print(get_lang('your_potch', replacer={'_POTCH_': potch}, locale=locale))
            print(get_lang('bet_cannot_be_more_than_your_current_potch', locale=locale))
        elif bet.isdigit():
            bet = int(bet)
            invalid = False
            clear_screen()
        else:
            print(get_lang('wrong_input', locale=locale))

    p1_result = player_roll('Gaspar', locale=locale)

    if p1_result in ['REVERSE_TRIPLE', 'REVERSE_DOUBLE', 'DOUBLE', 'TRIPLE']:
        potch = calculate_potch(potch, bet, p1_result, reverse=True)
    else:
        p2_result = player_roll('Tir', locale=locale)
        if p2_result in ['REVERSE_TRIPLE', 'REVERSE_DOUBLE', 'DOUBLE', 'TRIPLE']:
            potch = calculate_potch(potch, bet, p2_result, reverse=False)
        else:
            potch = compare_player_result(potch, bet, p1_result, p2_result, locale=locale)

    return potch

def game_over_check(potch):
    return True if potch <= MIN_POTCH or potch >= MAX_POTCH else False

def potch_adjuster(potch):
    if potch <= MIN_POTCH:
        return MIN_POTCH
    elif potch >= MAX_POTCH:
        return MAX_POTCH
    else:
        return potch

def lang_confirm():
    clear_screen()
    invalid = True
    locale = None
    while invalid == True:
        locale = str(input('languages (en/id) : ')).lower()
        if locale not in LOCALES:
            print(get_lang('wrong_input', locale=locale))
        else:
            invalid = False
            clear_screen()

    return locale

def start():
    locale = lang_confirm()
    potch = 10000
    game_over = False
    play = play_confirm(locale=locale)
    while play is True and game_over is False:
        print(get_lang('your_potch', replacer={'_POTCH_': potch_adjuster(potch)}, locale=locale))
        potch = game(potch, locale=locale)
        print(get_lang('current_potch', replacer={'_POTCH_': potch_adjuster(potch)}, locale=locale))
        game_over = game_over_check(potch)
        if game_over == False:
            play = play_confirm(locale=locale)

    print(get_lang('your_final_potch', replacer={'_POTCH_': potch_adjuster(potch)}, locale=locale))
    input()

if __name__ == '__main__':
    start()