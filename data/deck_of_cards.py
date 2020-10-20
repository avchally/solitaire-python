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

    def format_card(self):
        if self.exposed:
            return f'[{self.rank}{self.suit}]'
        else:
            return '[--]'

    def __str__(self):
        if self.exposed:
            return f'{self.rank}{self.suit}'
        else:
            return '--'


class Deck:
    """
    a full set of 52 cards
    will only be used at the beginning of the game
    remaining cards will be made into a Stock object
    
    can choose to input a custom seed to generate 
    a consistent deck every time

    to generate a seed from a deck, refer to 
    /data/seed_processor.py

    """

    def __init__(self, custom_seed=None):
        self.cards = []

        if custom_seed is None:
            for suit in SUITS:
                for rank in RANKS:
                    self.cards.append(Card(suit, rank))
        else:
            self.cards = seed_to_list(custom_seed)

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

    def combine_decks(self, other_deck):
        """
        combines all the cards from other_deck into this deck
        """
        self.cards.extend(other_deck.cards)

    def expose_all(self):
        for card in self.cards:
            card.set_exposed(True)

    def unexpose_all(self):
        for card in self.cards:
            card.set_exposed(False)

    def __str__(self):
        return str([f'{card}' for card in self.cards])
