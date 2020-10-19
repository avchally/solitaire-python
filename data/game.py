"""
this will be the main module that will be used as an API
solitaire glossary: https://semicolon.com/Solitaire/Rules/Glossary.html
scoring information: http://hands.com/~lkcl/hp6915/Dump/Files/soltr.htm

API information:
1. Import with 'from data.game import Game'
2. Instantiate a Game object with one argument: api_use=True
3. Start a new game by calling the method .new_game()
    a. there are a couple of optional arguments that change the
       game options
    b. the most important argument is deal_3 and is a boolean
       that represents whether to deal out 3 cards at a time 
       (if True) or 1 card at a time (if False)
4. At this point you can create your loop, read data as needed,
   and make moves
    a. methods to read data:
        - .api_get_moves()          => returns how many moves has been made so far
        - .api_read_stock()         => returns an integer that represents how many cards are left in the stock
        - .api_read_waste_pile()    => returns a list of strings that represent what cards are in the waste
        - .api_read_foundations()   => returns a list of strings that represent what top level cards are in the foundations
        - .api_read_tableaus()      => returns a list of lists, with each enclosed list representing a single tableau and its cards
                                       NOTE: tableau index 0 is furthest left pile and the card index 0 is the very top card on the pile
    b. method to make a move:
        - .api_make_move(move)      => A list must be provided as input with the format ['RX', Y, 'DZ']
                                       R => pile type to retrieve a card from (T=tableau, F=foundation, W=waste, S=stock)
                                       X => the index number of the pile to retrieve a card from (starting at 0 from the left)
                                       Y => the index number of the card to be retrieved (0 being the card on top of the pile)
                                       D => pile type to place a card to (T=tableau, F=foundation, W=waste, S=stock)
                                       Z => the index number of the pile to place a card to (starting at 0 from the left)
                                       In order to draw cards from the stock, the required input is ['S0', 0, 'S0']
    c. Future methods (not yet implemented):
        - .api_is_won()             => will return True/False whether the game is won yet
5. Other notes:
    a. cards are returned as a string in format 'SR', S=suit and R=rank
        - examples: 'AH' => Ace of Hearts | 'TC' => Ten of Clubs | '7D' => Seven of Diamonds | 'QS' => Queen of Spades
    b. if a card is flipped down on the board, it will be returned as '--'
    c. if a pile is empty, None will be returned as the card

"""

import sys
import pygame
import time
from .solitaire_objects import Board
from .deck_of_cards import Deck, SUITS, RANKS, RANK_VALUES


#============= GLOBAL DEFINITIONS =============#
DEFAULT_DECKS = 1
DEFAULT_TABLEAUS = 7


# PyGame-Related Globals
WIDTH = 1500
HEIGHT = 1000

STOCK_POS = (50, 100)
STOCK_SPACING = 3
MAX_STOCK_DISPLAYED = 13

WASTE_POS = (325, 100)
WASTE_SPACING = 40

FOUND_START_POS = (650, 100)
TABLEAU_START_POS = (50, 350)
CARD_HORI_DIST = 60
CARD_VERT_DIST = 40

CARD_HEIGHT = 190
CARD_WIDTH = 140

MAT_IMG = 'assets/board.png'
CARD_BACK = 'assets/cards/cardBack_blue5.png'
CARD_BLANK = 'assets/cards/cardBlank2.png'
CARD_PREFIX = 'assets/cards/card'
CARD_SUFFIX = '.png'
CARD_STRINGS = {'H': 'Hearts', 'S': 'Spades', 'D': 'Diamonds', 'C': 'Clubs',
                'A': 'A', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
                '7': '7', '8': '8', '9': '9', 'T': '10', 'J': 'J', 'Q': 'Q',
                'K': 'K'}

FONT_FILE = 'assets/OpenSans-Regular.ttf'
FONT_SIZE = 40
DEFAULT_TEXT_COLOR = (0, 0, 0)


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

        if self.api_use:
            self.init_game_api()
        else:
            self.init_pygame()


    #============== API-Related Methods ==============#

    def init_game_api(self):
        print("Game is now started")
        print("Provide moves via the method .make_move()")
        print("The method return True if the move was successful and False if not")
        print("A list must be provided as input with the format ['RX', Y, 'DZ']")
        print("R => pile type to retrieve a card from (T=tableau, F=foundation, W=waste, S=stock)")
        print("X => the index number of the pile to retrieve a card from (starting at 0 from the left)")
        print("Y => the index number of the card to be retrieved (0 being the card on top of the pile)")
        print("D => pile type to place a card to (T=tableau, F=foundation, W=waste, S=stock)")
        print("Z => the index number of the pile to place a card to (starting at 0 from the left)")
        print("In order to draw cards from the stock, the required input is ['S0', 0, 'S0']")



    def api_make_move(self, move_input):
        """
        just calls the board's attemp move method and returns successful or not
        """
        return self.board.attempt_move(move_input)

    def api_get_moves(self):
        """returns how many moves has been made so far"""
        return self.board.moves

    def api_read_stock(self):
        """returns an integer of how many cards are left in the stock"""
        return self.board.stock.get_length()

    def api_read_waste_pile(self):
        """returns a list of strings that represent what cards are in the waste"""
        return [str(card) for card in self.board.wp.cards]

    def api_read_foundations(self):
        """returns a list of strings that represent what top level cards are in the foundations"""
        return [str(found.get_topmost_card()) for found in self.board.foundations]

    def api_read_tableaus(self):
        """
        returns a list of lists, with each enclosed list representing a single tableau and its cards
        NOTE: tableau index 0 is furthest left pile and the card index 0 is the very top card on the pile
        """
        return [[str(card) for card in tableau.cards][::-1] for tableau in self.board.tableaus]

    def api_get_info(self):
        """
        returns a bunch of information about the current game:
        - moves
        """
        pass

    #============== PyGame-Related Methods ==============#

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Solitaire")
        self.clock = pygame.time.Clock()

        self.bg = BoardGraphics(self.board, self.screen)

        self.game_loop()

    def game_loop(self):
        dragging = False
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    retrieval_move = self.bg.card_pos.detect_collision(pygame.mouse.get_pos())
                    dragging = True
                if event.type == pygame.MOUSEBUTTONUP:
                    destination_move = self.bg.card_pos.detect_collision(pygame.mouse.get_pos())
                    dragging = False
                    self.process_move(retrieval_move, destination_move)

            # update
            self.bg.update()

            # draw
            self.bg.draw(self.screen)

            # apply draw
            pygame.display.update()


    def process_move(self, retrieval, destination):
        """
        retrieval and destination should both be 2 element lists 
        provided from CardPosition.detect_collision
        """
        self.board.attempt_move([retrieval[0], retrieval[1], destination[0]])

    def _init_decks(self):
        deck_list = [Deck() for i in range(self.decks)]

        if len(deck_list) > 1:
            for deck in deck_list[1:]:
                deck_list[0].combine_decks(deck)

        return deck_list[0]


class CardPositions:

    def __init__(self, board):
        """
        determines clickable locations and stores positions 
        as rect's to make collision detection easy
        """
        self.board = board
        self.tableaus = []      # any exposed card is clickable
        self.foundations = []   # only top card is clickable
        self.waste = []         # only top card is clickable
        self.stock = []         # only top card is clickable

    def detect_collision(self, pos):
        """
        determines if a mouseclick is within any of the clickable 
        areas and returns a piece of an attempted move (to be used
        in the process_move method of Game class)
        """
        for rect in self.stock:
            if rect.collidepoint((pos)):
                return ['S0', 0]
        for rect in self.waste:
            if rect.collidepoint((pos)):
                return ['W0', 0]
        for i, rect in enumerate(self.foundations):
            if rect.collidepoint((pos)):
                return ['F'+str(i), 0]
        for rect in self.tableaus:
            if rect[0].collidepoint((pos)):
                return rect[1]

        return [0,0]

    def update_positions(self):
        self.get_stk_pos()
        self.get_wst_pos()
        self.get_fnd_pos()
        self.get_tab_pos()

    def get_tab_pos(self):
        """
        stores a list of lists as tableau positions
        [ [rect object, [TN, M]], ...] with [TN, M] being a move Nth index Tableau, Mth index Card
        """
        self.tableaus = []
        for tableau_index, tableau in enumerate(self.board.tableaus):
            x_pos = TABLEAU_START_POS[0] + tableau_index*(CARD_WIDTH+CARD_HORI_DIST)
            if tableau.get_length() == 0:
                y_pos = TABLEAU_START_POS[1]
                associated_move = ['T' + str(tableau_index), 0]
                self.tableaus.append([pygame.image.load(CARD_BLANK).get_rect(topleft=(x_pos, y_pos)), associated_move])
            for card_index in range(tableau.get_length())[::-1]:
                y_pos = TABLEAU_START_POS[1] + card_index*CARD_VERT_DIST
                associated_move = ['T' + str(tableau_index), tableau.get_length() - card_index - 1]
                self.tableaus.append([pygame.image.load(CARD_BLANK).get_rect(topleft=(x_pos, y_pos)), associated_move])

    def get_fnd_pos(self):
        self.foundations = []
        for i, foundation in enumerate(self.board.foundations):
            found_pos_topleft = (FOUND_START_POS[0] + i*(CARD_WIDTH+CARD_HORI_DIST), FOUND_START_POS[1])
            self.foundations.append(pygame.image.load(CARD_BLANK).get_rect(topleft=found_pos_topleft))

    def get_wst_pos(self):
        if self.board.wp.get_length() > 3:
            i = 3
        else:
            i = self.board.wp.get_length()

        waste_pos_topleft = (WASTE_POS[0] + (i-1)*WASTE_SPACING, WASTE_POS[1])
        self.waste = [pygame.image.load(CARD_BLANK).get_rect(topleft=waste_pos_topleft)]

    def get_stk_pos(self):
        if self.board.stock.get_length() > MAX_STOCK_DISPLAYED:
            i = MAX_STOCK_DISPLAYED
        else:
            i = self.board.stock.get_length()

        stock_pos_topleft = (STOCK_POS[0] + (i-1)*STOCK_SPACING, STOCK_POS[1])
        self.stock = [pygame.image.load(CARD_BLANK).get_rect(topleft=stock_pos_topleft)]


class BoardGraphics:

    def __init__(self, board, screen):
        self.board = board
        self.load_card_images(screen)
        self.main_font = pygame.font.Font(FONT_FILE, FONT_SIZE)
        self.card_pos = CardPositions(self.board)

    def update(self):
        self.card_pos.update_positions()

    def draw(self, screen):
        stock_card = self.board.stock.get_topmost_card()
        waste_card = self.board.wp.get_topmost_card()
        foundations = self.board.foundations
        tableaus = self.board.tableaus

        # draw playing mat
        mat_surf = pygame.image.load(MAT_IMG).convert_alpha()
        mat_surf = pygame.transform.scale(mat_surf, (WIDTH, HEIGHT))
        mat_rect = mat_surf.get_rect(topleft=(0,0))
        screen.blit(mat_surf, mat_rect)

        # draw text
        self.draw_text(screen, f'Moves: {self.board.moves}', (WIDTH/2, FOUND_START_POS[1]/2))

        # draw Stock at STOCK_POS
        if self.board.stock.get_length() > 1:
            for i in range(self.board.stock.get_length()):
                self.draw_card(screen, stock_card, (STOCK_POS[0] + STOCK_SPACING*i, STOCK_POS[1]))
                if i >= MAX_STOCK_DISPLAYED-1:
                    break
        else:
            self.draw_card(screen, stock_card, STOCK_POS)

        # draw Waste at WASTE_POS
        if self.board.wp.get_length() > 1:
            temp_list = []
            for i in range(self.board.wp.get_length()):
                temp_list.append(self.board.wp.get_n_card(i+1))
                if i >= 2:
                    break
            for i, crd in enumerate(temp_list[::-1]):
                self.draw_card(screen, crd, (WASTE_POS[0] + WASTE_SPACING*i, WASTE_POS[1]))
        else:
            self.draw_card(screen, waste_card, WASTE_POS)

        # draw Foundation piles at FOUND_START_POS
        for i, foundation in enumerate(foundations):
            draw_pos = (FOUND_START_POS[0] + (CARD_HORI_DIST+CARD_WIDTH)*i, FOUND_START_POS[1])
            self.draw_card(screen, foundation.get_topmost_card(), draw_pos)

        # draw Tableau piles at TABLEAU_START_POS
        tab_card_ind = 0
        remaining_tabs = len(tableaus)

        while remaining_tabs > 0:
            remaining_tabs = len(tableaus)
            for tab_ind, tableau in enumerate(tableaus):
                draw_pos = (TABLEAU_START_POS[0] + (CARD_HORI_DIST+CARD_WIDTH)*tab_ind, TABLEAU_START_POS[1] + CARD_VERT_DIST*tab_card_ind)
                if tableau.get_length() == 0 and tab_card_ind == 0:
                    self.draw_card(screen, None, draw_pos)
                if tab_card_ind < tableau.get_length():
                    self.draw_card(screen, tableau.cards[tab_card_ind], draw_pos)
                else:
                    remaining_tabs -= 1
            tab_card_ind += 1 

    def draw_text(self, screen, message, pos, color=DEFAULT_TEXT_COLOR):
        text_surf = self.main_font.render(message, True, color)
        text_rect = text_surf.get_rect(center=pos)
        screen.blit(text_surf, text_rect)

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
