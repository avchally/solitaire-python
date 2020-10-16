"""
simple solitaire with python and PyGame
by: Alex Chally
"""

import random

#============= GLOBAL DEFINITIONS =============#
SUITS = "HSDC"
RANKS = "A23456789TJQK"
RANK_VALUES = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
			   "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13}
COLORS = {"H": "red",
		  "S": "black",
		  "D": "red",
		  "C": "black"}


#============= CLASS DEFINITIONS =============#
class Card:
	
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

	def set_exposed(self, expose_boolean):
		self.exposed = expose_boolean

	def __str__(self):
		return f'{self.rank}{self.suit}'


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

	def pull_card(self):
		return self.cards.pop()

	def __str__(self):
		return str([f'{card}' for card in self.cards])


class Pile:
	"""
	A group of card objects that serve as the foundation for 
	the various different types of groups of cards on the board
	"""

	def __init__(self, cards, stack_style='squared'):
		"""
		stack_style is either 'squared' (pile is stacked with only the top card visible)
		or 'fanned' (pile is slightly fanned out, with every card slightly visible)
		"""
		self.cards = cards
		self.stack_style = stack_style

	def remove_cards(self, num_cards):
		"""
		removes the num_cards amount from top (end) of pile 
		and returns them as another pile object
		"""
		temp_list = self.cards[len(self.cards) - num_cards:]
		self.cards = self.cards[:len(self.cards) - num_cards]
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

	def get_topmost_card(self):
		"""
		returns top card in the pile, but DOES NOT remove it from pile
		"""
		return self.cards[-1]

	def get_bottommost_card(self):
		"""
		returns bottom card in the pile, but DOES NOT remove it from pile
		"""
		return self.cards[0]

	def __str__(self):
		return str([f'{card}' for card in self.cards])


class Stock(Pile):
	"""
	Stock is the official term for the pile that cards are drawn from
	"""
	
	def __init__(self):
		super().__init__([])


class Wastepile(Pile):
	"""
	a pile of cards taken from the stock and placed faceup
	the topmost card can be taken and used
	"""

	def __init__(self):
		super().__init__([])


class Foundation(Pile):
	"""
	The 4 locations where piles of cards are built based on suit
	Game is finished when all Foundations are filled
	Starts empty
	"""
	
	def __init__(self):
		super().__init__([])

	def is_valid_move(self, card):
		"""
		takes a card object as input and returns True/False if
		the card can be placed on the pile
		"""
		return (self.get_topmost_card().get_suit() == card.get_suit() and
			    self.get_topmost_card().get_rank_value() - 1 == card.get_rank_value())


class Tableau(Pile):
	"""
	The 7 locations where piles of cards are built down by alternate colors
	Referred to by number, left to right in ascending order
	"""

	def __init__(self):
		super().__init__([])

	def is_valid_move(self, card):
		"""
		takes a card object as input and returns True/False if
		the card can be placed on the pile
		"""
		return (self.get_topmost_card().get_color() != card.get_color() and
				self.get_topmost_card().get_rank_value + 1 == card.get_rank_value())


class FoundationGroup:
	pass


class TableauGroup:
	pass


#============= GAME =============#
def main():
    pass

def test():
	dk = Deck()
	# print(dk)
	dk.shuffle()
	print(dk)

	tabl = Tableau()
	tabl.add_card(dk.pull_card())
	tabl.add_card(dk.pull_card())
	tabl.add_card(dk.pull_card())
	tabl.add_card(dk.pull_card())
	tabl.add_card(dk.pull_card())
	tabl.add_card(dk.pull_card())
	tabl.add_card(dk.pull_card())
	tabl.add_card(dk.pull_card())
	
	print(tabl)
	print(dk)

	this_card = dk.pull_card()
	print(this_card)
	print(this_card.get_color())
	print(this_card.get_rank())
	print(this_card.get_rank_value())
	print(this_card.get_suit())


if __name__ == "__main__":
    test()
