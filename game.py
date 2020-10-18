"""
this will be the main module that will be used as an API
scoring information: http://hands.com/~lkcl/hp6915/Dump/Files/soltr.htm
"""

import sys
import pygame
from solitaire_objects import Board
from deck_of_cards import Deck, SUITS, RANKS, RANK_VALUES


#============= GLOBAL DEFINITIONS =============#
DEFAULT_DECKS = 1
DEFAULT_TABLEAUS = 7


# PyGame-Related Globals
WIDTH = 1600
HEIGHT = 900

STOCK_POS = (50, 50)
WASTE_POS = (250, 50)
FOUND_START_POS = (450, 50)
TABLEAU_START_POS = (50, 400)
CARD_HORI_DIST = 200
CARD_VERT_DIST = 30

CARD_BACK = 'assets/cards/cardBack_blue5.png'
CARD_BLANK = 'assets/cards/cardBlank.png'
CARD_PREFIX = 'assets/cards/card'
CARD_SUFFIX = '.png'
CARD_STRINGS = {'H': 'Hearts', 'S': 'Spades', 'D': 'Diamonds', 'C': 'Clubs',
                'A': 'A', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
                '7': '7', '8': '8', '9': '9', 'T': '10', 'J': 'J', 'Q': 'Q',
                'K': 'K'}



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

        if not self.api_use:
            # self.board_graphics = BoardGraphics(self.board)
            self.init_pygame()

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Solitaire")
        self.clock = pygame.time.Clock()

        self.bg = BoardGraphics(self.board, self.screen)

        self.game_loop()

    def game_loop(self):
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # update

            # draw
            self.bg.draw(self.screen)

            # apply draw
            pygame.display.update()



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
        # #     deck_list.append(Deck())
        deck_list = [Deck() for i in range(self.decks)]

        if len(deck_list) > 1:
            for deck in deck_list[1:]:
                deck_list[0].combine_decks(deck)

        return deck_list[0]


class BoardGraphics:

    def __init__(self, board, screen):
        self.board = board
        self.load_card_images(screen)

    def update(self):
        pass

    def draw(self, screen):
        stock_card = self.board.stock.get_topmost_card()
        waste_card = self.board.wp.get_topmost_card()
        foundations = self.board.foundations
        tableaus = self.board.tableaus

        self.draw_card(screen, stock_card, STOCK_POS)
        self.draw_card(screen, waste_card, WASTE_POS)

        for i, foundation in enumerate(foundations):
            self.draw_card(screen, foundation.get_topmost_card(), 
                            (FOUND_START_POS[0] + CARD_HORI_DIST*i, FOUND_START_POS[1]))

        # self.draw_card(screen, self.board.tableaus[0].cards[0], (200, 200))
        # self.draw_card(screen, self.board.tableaus[3].cards[1], (400, 200))

    def draw_card(self, screen, card_obj, pos):
        if card_obj is None:
            card_suit_rank = 'blank'
        elif card_obj.get_exposed():
            card_suit_rank = card_obj.get_suit() + card_obj.get_rank()
        else:
            card_suit_rank = 'back'
        card_surf = self.card_surfaces[card_suit_rank]
        card_rect = card_surf.get_rect(topleft=pos)
        screen.blit(card_surf, card_rect)

    def load_card_images(self, screen):
        self.card_surfaces = {}
        for suit in SUITS:
            for rank in RANKS:
                image_path = CARD_PREFIX + CARD_STRINGS[suit] + CARD_STRINGS[rank] + CARD_SUFFIX
                self.card_surfaces[suit+rank] = pygame.image.load(image_path)
        self.card_surfaces['back'] = pygame.image.load(CARD_BACK).convert_alpha()
        self.card_surfaces['blank'] = pygame.image.load(CARD_BLANK).convert_alpha()



#============= STATE MACHINE =============#
# Might not actually be necessary. We'll see
class StateMachine:
    pass


def main():
    game = Game()
    game.new_game(False, True, 1, 7)


if __name__ == "__main__":
    main()
