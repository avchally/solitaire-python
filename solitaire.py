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
[ ] Implement a move method that performs a move on board
[ ] Finish Board class
[ ] Implement basic game loop that user can play from command line
[!] At this point, game should be finished enough to hand over to Tommy for AI
[ ] Implement State Machine
[ ] Start GUI

"""

import random
import time

#============= GLOBAL DEFINITIONS =============#
SUITS = "HSDC"
RANKS = "A23456789TJQK"
RANK_VALUES = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
			   "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13}
COLORS = {"H": "red",
		  "S": "black",
		  "D": "red",
		  "C": "black"}

FANNED = 'fanned'
SQUARED = 'squared'


#============= CLASS DEFINITIONS =============#
class Card:
	"""
	many of the methods here are present to avoid
	accessing an internal variable externally
	"""
	
	def __init__(self, suit, rank, exposed=False):
		self.suit = suit
		self.rank = rank
		self.exposed = exposed
		self.color = COLORS[self.suit]
		self.rank_value = RANK_VALUES[self.rank]

	def get_suit(self):
		return self.suit

	def get_rank(self):
		return self.rank

	def get_rank_value(self):
		return self.rank_value

	def get_color(self):
		return self.color

	def get_exposed(self):
		return self.exposed

	def set_exposed(self, expose_boolean):
		self.exposed = expose_boolean

	def flip_card(self):
		self.exposed = not self.exposed

	def can_move(self):
		"""
		method to determine if this card has a legal move somewhere on board
		"""
		pass

	def __str__(self):
		if self.exposed:
			return f'[{self.rank}{self.suit}]'
		else:
			return '[XX]'


class Deck:
	"""
	a full set of 52 cards
	will only be used at the beginning of the game
	remaining cards will be made into a Stock object
	"""

	def __init__(self):
		self.cards = []
		for suit in SUITS:
			for rank in RANKS:
				self.cards.append(Card(suit, rank))

	def shuffle(self):
		temp_list = []
		for i in range(len(self.cards)):
			temp_list.append(self.cards.pop(random.randrange(len(self.cards))))
		self.cards = temp_list

	def pull_card(self, expose=False):
		if expose:
			card = self.cards.pop()
			card.flip_card()
			return card
		else:
			return self.cards.pop()

	def dump_cards(self, expose=False):
		"""
		removes all the cards in the deck and returns them as a list
		"""
		temp_list = self.cards[:]
		self.cards = []
		if not expose:
			return temp_list
		else:
			for card in temp_list:
				card.flip_card() 

	def __str__(self):
		return str([f'{card}' for card in self.cards])


class Pile:
	"""
	A group of card objects that serve as the foundation for 
	the various different types of groups of cards on the board
	"""

	def __init__(self, cards, stack_style=SQUARED):
		"""
		stack_style is either 'squared' (pile is stacked with only the top card visible)
		or 'fanned' (pile is slightly fanned out, with every card slightly visible)
		"""
		self.cards = cards
		self.stack_style = stack_style

	def remove_cards(self, num_cards, flip_cards=False):
		"""
		removes the num_cards amount from top (end) of pile 
		and returns them as another pile object
		"""
		temp_list = self.cards[len(self.cards) - num_cards:]
		self.cards = self.cards[:len(self.cards) - num_cards]

		if flip_cards:
			for card in temp_list:
				card.flip_card()

		return Pile(temp_list)

	def merge_pile(self, pile_of_cards):
		"""
		takes a pile object as input and adds it to the current pile
		"""
		self.cards.extend(pile_of_cards.get_card_list())

	def add_card(self, card):
		"""
		takes a card object as input and adds it to the current pile
		"""
		self.cards.append(card)

	def get_card_list(self):
		"""
		this method is present to disuade from referencing an object's internal variable directly
		"""
		return self.cards

	def get_n_card(self, n):
		"""
		gets the nth (from the top) card in the pile, but DOES NOT remove it from pile
		"""
		if len(self.cards) > 0:
			return self.cards[-n]
		else:
			return None

	def get_topmost_card(self):
		"""
		returns top card in the pile, but DOES NOT remove it from pile
		"""
		if len(self.cards) > 0:
			return self.cards[-1]
		else:
			return None

	def get_bottommost_card(self):
		"""
		returns bottom card in the pile, but DOES NOT remove it from pile
		"""
		if len(self.cards) > 0:
			return self.cards[0]
		else:
			return None

	def get_length(self):
		"""
		returns the number of cards contained in the pile
		"""
		return len(self.cards)

	def __str__(self):
		if self.stack_style == 'squared':
			if self.get_topmost_card() == None:
				return str([])
			else:
				return str(self.get_topmost_card())
		if self.stack_style == 'fanned':
			if len(self.cards) > 0:
				return ' '.join([f'{card}' for card in self.cards])
			else:
				return str([])


class Stock(Pile):
	"""
	Stock is the official term for the pile that cards are drawn from
	can either deal out in increments of 1 or 3 cards depending on
	game configuration
	"""
	
	def __init__(self, deal_3=False):
		super().__init__([], FANNED)
		self.deal_3 = deal_3

	def deal_to_wp(self, wp):
		"""
		deals out the top card in the stock to the wastepile
		"""
		if self.deal_3:
			if len(self.cards) > 2:
				wp.merge_pile(self.remove_cards(3, True))
			elif len(self.cards) > 0:
				wp.merge_pile(self.remove_cards(len(self.cards), True))
		else:
			if len(self.cards) > 0:
				wp.merge_pile(self.remove_cards(1, True))


class Wastepile(Pile):
	"""
	a pile of cards taken from the stock and placed faceup
	the topmost card can be taken and used
	"""

	def __init__(self):
		super().__init__([], SQUARED)

	def move_to_stock(self, stock):
		"""
		flips cards and puts them all back into the stock
		"""
		stock.merge_pile(self.remove_cards(len(self.cards), True))

	def is_valid_retrieval(self, card_index):
		"""
		determines whether the pile can be picked up from the 
		provided index (index 0 being topmost card or last item in list)
		"""
		return self.get_length() == card_index + 1


class Foundation(Pile):
	"""
	The 4 locations where piles of cards are built based on suit
	Game is finished when all Foundations are filled
	Starts empty
	"""
	
	def __init__(self):
		super().__init__([], SQUARED)

	def is_valid_placement(self, other_pile):
		"""
		takes a pile object as input and returns True/False if
		the pile can be placed on the pile
		for a Foundation:
		* only a pile of size 1 can be placed on it
		* if foundation pile is empty, only an ace (value 1) can 
		  be placed
		* otherwise, the card must be same suit and 1 rank
		  higher than the topmost card in foundation pile
		"""
		if other_pile.get_length() == 1:
			card = other_pile.get_bottommost_card()
			if self.get_length() == 0:
				return card.get_rank_value() == 1
			else:
				return (self.get_topmost_card().get_suit() == card.get_suit() and
					    self.get_topmost_card().get_rank_value() + 1 == card.get_rank_value())
		else:
			return False

	def is_valid_retrieval(self, card_index):
		"""
		determines whether the pile can be picked up from the 
		provided index (index 0 being topmost card or last item in list)
		"""
		return self.get_length() == card_index + 1


class Tableau(Pile):
	"""
	The 7 locations where piles of cards are built down by alternate colors
	Referred to by number, left to right in ascending order
	"""

	def __init__(self):
		super().__init__([], FANNED)

	def reveal_top_card(self):
		"""
		when called, will expose the top card if not already exposed
		"""
		if not self.get_topmost_card().get_exposed():
			self.get_topmost_card().flip_card()

	def is_valid_placement(self, other_pile):
		"""
		takes a pile object as input and returns True/False if
		it can be placed on this pile
		for a Tableau:
		* any size pile, topmost card must be opposite color and 
		  one less rank of the bottommost card of tableau pile
		* if tableau pile is empty, topmost card of other pile
		  must be King (value 13)
		"""
		card = other_pile.get_bottommost_card()
		if self.get_length() == 0:
			return card.get_rank_value() == 13
		else:
			return (self.get_topmost_card().get_color() != card.get_color() and
					self.get_topmost_card().get_rank_value() - 1 == card.get_rank_value())

	def is_valid_retrieval(self, card_index):
		"""
		determines whether the pile can be picked up from the 
		provided index (index 0 being topmost card or last item in list)
		"""
		if self.get_length() > index:
			return self.cards[:-index].get_exposed


class FoundationGroup:
	"""
	class to manage all 4 foundations
	"""

	def __init__(self):
		self.foundations = [Foundation()]*4


class TableauGroup:
	"""
	class to manage all 7 tableaus
	"""

	def __init__(self):
		self.tableaus = [Tableau()]*7


class Board:
	"""
	can only RETRIEVE cards from: Tableau, Foundation, Wastepile
	can only PLACE cards to: Tableau, Foundation
	"""

	def __init__(self):
		self.num_foundations = 4
		self.num_tableaus = 7
		self.foundations = []
		self.tableaus = []
		self.stock = Stock()
		self.wp = Wastepile()

		for i in range(self.num_tableaus):
			self.tableaus.append(Tableau())
		for i in range(self.num_foundations):
			self.foundations.append(Foundation())

	def deal(self, deck):
		"""
		deals cards from a deck onto the board,
		making the board ready for play
		"""
		dealt = False
		tab_num = 0
		while not dealt:
			current_tableau = self.tableaus[tab_num]
			tableau_length = current_tableau.get_length()

			# if tableau isn't full, add card
			if tableau_length < tab_num + 1:
				expose_card = tableau_length == tab_num
				current_tableau.add_card(deck.pull_card(expose_card))

			# if last tableau is full, stop dealing
			if self.tableaus[self.num_tableaus-1].get_length() == self.num_tableaus:
				dealt = True

			# increment, then loop back to start if end reached
			tab_num += 1
			if tab_num >= self.num_tableaus:
				tab_num = 0

		# dump rest of cards into stock
		self.stock.merge_pile(Pile(deck.dump_cards()))

	def attempt_move(self, move_input):
		"""
		attempts to move a pile of some length from one spot on the board
		to another
		return True if the move was successful and False if not

		*** currently, move_input is a 3-element list formatted as follows (likely to change):
		*** [retrieval pile, retrieval index in the pile, destination pile]
		*** each pile will have its own key
		*** example move_input: 
		*** ['T1', 3, 'F3'] => indicating grabbing cards from the third index (4th card) of the
		***					   2nd tableau (T0 representing 1st) and placing them on the 4th
		***					   foundation (again, F0 representing 1st)

		"""
		pass

	def str_tableaus(self):
		str_tab = ""
		for tab in self.tableaus:
			str_tab += "\n" + str(tab)
		return str_tab

	def str_foundations(self):
		str_found = ""
		for found in self.foundations:
			if found is not None:
				str_found += "\n" + str(found)
			else:
				str_found += str([])
		return str_found

	def __str__(self):
		line1 = str(f'Foundations: {self.str_foundations()}\n\n')
		line2 = str(f'Tableaus: {self.str_tableaus()}\n\n')
		line3 = str(f'Stock: {self.stock}\n\n')
		line4 = str(f'Wastepile: {self.wp}')
		return line1 + line2 + line3 + line4


class Game:
	"""
	possible game options/features that user can modify
	- draw [3] or [1] card(s) from stock to wastepile
	- auto flip up a new card in tableaus
	- auto complete when there are no more unexposed cards on board
	- provide possible moves for a given card (or perhaps moreso, 
	  determine if any legal move exists on the board)
	"""
	pass


#============= STATE MACHINE =============#
# Might not actually be necessary. We'll see
class StateMachine:
	pass


#============= GAME =============#
def main():
    pass

def test2():
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
	brd.tableaus[0].merge_pile(brd.tableaus[4].remove_cards(1))
	brd.tableaus[3].reveal_top_card()
	brd.tableaus[4].reveal_top_card()
	# brd.foundations[0].cards.append(Card('S', 'A', True))
	print(brd)
	# print(brd.foundations[0].is_valid_retrieval(0))
	# print(brd.wp.get_length())
	# print(brd.wp.is_valid_retrieval(0))
	print("------------------------")


if __name__ == "__main__":
    test()
