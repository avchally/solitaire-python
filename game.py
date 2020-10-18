"""
this will be the main module that will be used as an API
scoring information: http://hands.com/~lkcl/hp6915/Dump/Files/soltr.htm
"""

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

    def __init__(self, api_use=False):
    	"""
    	api_use is only True if this module will be used as an API
    	"""
    	self.api_use = api_use

    def new_game(self, deal_3=False, auto_flip_tab=True, decks=DEFAULT_DECKS, tableau_qty=DEFAULT_TABLEAUS):
    	"""
    	initializes a new game
    	deal_3 is a boolean that determines whether the stock draws 3 or 1 card at a time
    	auto_flip_tab is a boolean that determines whether newly uncovered cards
    	    in the tableaus are automatically flipped up
    	decks is an integer that determines how many decks worth of cards to play with
    	tableau_qty is an integer that determines how man tableaus to play with (each
    		tableau is dealt out cards equal to what number tableau it is)
    	"""
    	self.deal_3 = deal_3
    	self.auto_flip_tab = auto_flip_tab
    	self.decks = decks
    	self.tableau_qty = tableau_qty

    	self.deck = self._init_decks()
    	self.deck.shuffle()

    	self.board = Board(num_tableaus=tableau_qty, num_decks=decks, deal_3=deal_3)
    	self.board.init_move_dict()
    	self.board.deal(self.deck)
    	print(self.board)

    def api_make_move(self, orig_pile='TN', orig_ind=-1, dest_pile='TN', special_action=None):
    	"""
    	special actions: 
    	"""
    	pass

    # !!! =========================================================================
    #     determine whether these should return pile object, list of card objects,
    #     list of card strings, or something else
    def api_read_waste_pile(self):
    	pass

    def api_read_foundations(self):
    	pass

    def api_read_tableaus(self):
    	pass
    # !!! =========================================================================


    def api_get_info(self):
    	"""
    	returns a bunch of information about the current game:
    	- moves
    	"""
    	pass

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
	game.new_game(False, True, 2, 10)


if __name__ == "__main__":
	main()
