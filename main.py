"""
simple solitaire with python and PyGame
by: Alex Chally
solitaire glossary: https://semicolon.com/Solitaire/Rules/Glossary.html


this version plays the game from the command line

"""

import game, solitaire_objects, deck_of_cards


#============= HELPER FUNCTIONS =============#
def get_move_from_user():
    """
    when playing from a command line, allows the user to input moves 
    """
    move_list = input("Move: ").split(" ")
    try:
        move_list[1] = int(move_list[1])
    except:
        pass
    return move_list

#============= GAME =============#
def main():
    brd = solitaire_objects.Board()
    brd.init_move_dict()

    new_deck = deck_of_cards.Deck()
    new_deck.shuffle()

    brd.deal(new_deck)

    while True:
        print('\n')
        print(brd)
        print()
        print(brd.attempt_move(get_move_from_user()))


if __name__ == "__main__":
    main()
