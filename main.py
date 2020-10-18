"""
simple solitaire with python and PyGame
by: Alex Chally
solitaire glossary: https://semicolon.com/Solitaire/Rules/Glossary.html

TO DO next:
[X] Structure out the piles, board, and game objects
[X] Finish all of the different pile types
[X] Test all of the different pile types
[X] Finalize retrieve and place methods for piles
[X] Test retrieve and place methods for piles
[X] Implement a move method that performs a move on board
[X] Finish Board class
[X] Implement basic game loop that user can play from command line
[!] At this point, game should be finished enough to hand over to Tommy for AI
[ ] Reorganize package/modules
[ ] Develop a game file that handles playing the game
[ ] Implement State Machine
[ ] Start GUI

"""


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
    # return [input("Retrieval Pile "), int(input("Retrieval Index ")), input("Destination Pile ")]

#============= GAME =============#
def main():
    brd = Board()
    brd.init_move_dict()

    new_deck = Deck()
    new_deck.shuffle()

    brd.deal(new_deck)

    while True:
        print('\n')
        print(brd)
        print()
        print(brd.attempt_move(get_move_from_user()))


def test2():
    # FOR TESTING, DONT USE
    test_pile = Pile([Card('H','7', True), Card('D','K', True), Card('H','6', True), Card('S','5', True)], FANNED)
    
    test_cards = [Card('S', '4', True), Card('D', '4', True), Card('S', '6', True), Card('C', 'K', True), Card('S', 'A', True)]
    
    test_tableau = Tableau()
    test_tableau.merge_pile(test_pile)
    test_tab_blank = Tableau()
    test_foundation = Foundation()
    test_foundation.merge_pile(test_pile)
    test_found_blank = Foundation()

    test_piles = [test_tableau, test_tab_blank, test_foundation, test_found_blank]

    for tp in test_piles:
        print()
        print(tp)
        for cd in test_cards:
            print(cd)
            print(tp.is_valid_placement(Pile([cd])))

    # print(test_tableau)
    # print(test_card)
    # print(test_tableau.is_valid_placement(Pile([test_card])))

def test():
    # FOR TESTING, DONT USE
    brd = Board()
    print(brd)
    print("------------------------")

    print("DEALING\n")
    # time.sleep(3)
    new_deck = Deck()
    new_deck.shuffle()
    brd.deal(new_deck)
    print(brd)
    brd.stock.deal_to_wp(brd.wp)
    # brd.tableaus[0].merge_pile(brd.tableaus[4].remove_cards(1))
    # brd.tableaus[3].reveal_top_card()
    # brd.tableaus[4].reveal_top_card()
    # brd.foundations[0].cards.append(Card('S', 'A', True))
    # print("------------------------")
    # print(brd)
    # print("------------------------")
    brd.init_move_dict()
    print(brd.move_dict)
    while True:
        print('\n')
        print(brd)
        print()
        print(brd.attempt_move(get_move_from_user()))
    # print(brd.foundations[0].is_valid_retrieval(0))
    # print(brd.wp.get_length())
    # print(brd.wp.is_valid_retrieval(0))

