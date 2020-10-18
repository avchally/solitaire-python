from solitaire_objects import Board
from deck_of_cards import Deck


#============= GLOBAL DEFINITIONS =============#
DEFAULT_DECKS = 1
DEFAULT_TABLEAUS = 7


#============= CLASS DEFINITIONS =============#
class Game:
    """
    possible game options/features that user can modify
    - draw [3] or [1] card(s) from stock to wastepile
    - auto flip up a new card in tableaus
    - auto complete when there are no more unexposed cards on board
    - provide possible moves for a given card (or perhaps moreso, 
      determine if any legal move exists on the board)
    """

    def __init__(self):
    	pass

    def new_game(self, deal_3=False, auto_flip_tab=False, decks=DEFAULT_DECKS, tableau_qty=DEFAULT_TABLEAUS):
    	self.deal_3 = deal_3
    	self.auto_flip_tab = auto_flip_tab
    	self.decks = decks
    	self.tableau_qty = tableau_qty

    	self.deck = self._init_decks()
    	self.deck.shuffle()

    	self.board = Board(tableau_qty, decks)
    	self.board.init_move_dict()
    	self.board.deal(self.deck)
    	print(self.board)


    def _init_decks(self):
    	# deck_list = []
    	# # for i in range(decks):
    	# # 	deck_list.append(Deck())
    	deck_list = [Deck() for i in range(self.decks)]

    	if len(deck_list) > 1:
    		for deck in deck_list[1:]:
    			deck_list[0].combine_decks(deck)

    	return deck_list[0]





#============= STATE MACHINE =============#
# Might not actually be necessary. We'll see
class StateMachine:
    pass


def main():
	game = Game()
	game.new_game()


if __name__ == "__main__":
	main()
