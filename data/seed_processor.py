"""
generates a deck of cards based on a given seed
can also generate a seed with a given deck of cards
"""
import random
from .deck_of_cards import Card, Deck

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
SUITS = "HSDC"
RANKS = "A23456789TJQK"

hash_dict = {'a': 'AH', 'b': '2H', 'c': '3H', 'd': '4H', 'e': '5H', 'f': '6H', 
			 'g': '7H', 'h': '8H', 'i': '9H', 'j': 'TH', 'k': 'JH', 'l': 'QH', 
			 'm': 'KH', 'n': 'AS', 'o': '2S', 'p': '3S', 'q': '4S', 'r': '5S', 
			 's': '6S', 't': '7S', 'u': '8S', 'v': '9S', 'w': 'TS', 'x': 'JS', 
			 'y': 'QS', 'z': 'KS', 'A': 'AD', 'B': '2D', 'C': '3D', 'D': '4D', 
			 'E': '5D', 'F': '6D', 'G': '7D', 'H': '8D', 'I': '9D', 'J': 'TD', 
			 'K': 'JD', 'L': 'QD', 'M': 'KD', 'N': 'AC', 'O': '2C', 'P': '3C', 
			 'Q': '4C', 'R': '5C', 'S': '6C', 'T': '7C', 'U': '8C', 'V': '9C', 
			 'W': 'TC', 'X': 'JC', 'Y': 'QC', 'Z': 'KC'}



def generate_hash_dict():
	""" only need to run this if hash_dict needs updated above """
	hash_dict = {}
	i = 0
	for suit in SUITS:
		for rank in RANKS:
			hash_dict[chars[i]] = f'{rank}{suit}'
			i += 1
	print(hash_dict)

def seed_to_list(seed):
	cards = []
	for char in seed:
		suit = hash_dict[char][1]
		rank = hash_dict[char][0]
		cards.append(Card(suit, rank))

	return cards

def seed_to_deck(seed):
	"""
	returns a new deck object with cards ordered by the input seed
	"""
	deck = Deck()
	deck.cards = seed_to_list(seed)

	return deck

def deck_to_seed(deck):
	"""
	takes a Deck object and returns its corresponding seed
	"""
	seed = ''
	for card in deck.cards:
		for char, crd in hash_dict.items():
			if crd == f'{card.get_rank()}{card.get_suit()}':
				seed += char

	return seed

def generate_random_seed():
	temp_list = list(hash_dict.keys())
	seed = ''
	for i in range(len(temp_list)):
		seed += temp_list.pop(random.randrange(len(temp_list)))

	return seed

# THIS PROGRAM SHOULD NOT BE RUN AS A SCRIPT
# def main():
# 	# deck = deck_of_cards.Deck()
# 	# deck.expose_all()
# 	# deck.shuffle()
# 	# print(deck)
# 	# print(deck_to_seed(deck))

# 	deck = seed_to_deck('aWRcXysfdHiGnIUVEDKQrwevjokpNqMbSgzZFCJTAuxPhOmLBYlt')
# 	deck.expose_all()
# 	print(deck)
# 	print()
# 	print()
# 	print(generate_random_seed())

# if __name__ == '__main__':
# 	main()