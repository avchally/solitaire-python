
#============= GLOBAL DEFINITIONS =============#
FANNED = 'fanned'
SQUARED = 'squared'
DEFAULT_DECKS = 1
DEFAULT_TABLEAUS = 7


#============= CLASS DEFINITIONS =============#
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

    def reverse_cards(self):
        """
        reverses the list of cards
        """
        self.cards.reverse()

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
        super().__init__([], SQUARED)
        self.deal_3 = deal_3

    def deal_to_wp(self, wp):
        """
        deals out the top card in the stock to the wastepile
        if stock is empty, it returns wastepile back to stock
        """
        if self.get_length() == 0:
            wp.move_to_stock(self)
        elif self.deal_3:
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
        temp_pile = self.remove_cards(len(self.cards), True)
        temp_pile.reverse_cards()
        stock.merge_pile(temp_pile)

    def is_valid_retrieval(self, card_index):
        """
        determines whether the pile can be picked up from the 
        provided index (index 0 being topmost card or last item in list)
        """
        return card_index == 0


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
        return card_index == 0


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
        if self.get_length() > card_index:
            return self.cards[-(card_index+1)].get_exposed()


class Board:
    """
    can only RETRIEVE cards from: Tableau, Foundation, Wastepile
    can only PLACE cards to: Tableau, Foundation
    """

    def __init__(self, num_tableaus=DEFAULT_TABLEAUS, num_decks=DEFAULT_DECKS, deal_3=False, auto_flip_tab=True):
        self.num_foundations = num_decks * 4
        self.num_tableaus = num_tableaus
        self.auto_flip_tab = auto_flip_tab
        self.foundations = []
        self.tableaus = []
        self.stock = Stock(deal_3)
        self.wp = Wastepile()
        self.move_dict = {}
        self.moves = 0

        for i in range(self.num_tableaus):
            self.tableaus.append(Tableau())
        for i in range(self.num_foundations):
            self.foundations.append(Foundation())

    def init_move_dict(self):
        """
        will create a dictionary where keys represent a command
        and values represent the pile associated with the command
        format is: {'TN': self.foundations[N],
                    'FN': self.foundations[N],
                    'W0': self.wp}
        """
        self.move_dict = {}
        for ind, tbl in enumerate(self.tableaus):
            self.move_dict["T"+str(ind)] = self.tableaus[ind]
        for ind, fnd in enumerate(self.foundations):
            self.move_dict["F"+str(ind)] = self.foundations[ind]
        self.move_dict["W0"] = self.wp

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
        *** ['T1', 3, 'F3'] => indicating grabbing cards from the third index (4th card from bottom) of
        ***                    the 2nd tableau (T0 representing 1st) and placing them on the 4th
        ***                    foundation (again, F0 representing 1st)
        *** First element options: 'TN', 'FN', 'W0'
        *** Second element options: any non-negative integer
        *** Third element options: 'TN', 'FN'
        ***
        *** Special Actions:
        *** ['S0', 0, 'S0'] => Draws card(s) from stock onto wastepile (also returns waste to stock)
        *** ['TN', 0, 'TN'] => Attempts to expose the top card (if it's flipped down)

        """

        # handle stock draw Special Action first
        if move_input == ['S0', 0, 'S0']:
            self.stock.deal_to_wp(self.wp)
            self.moves += 1
            return True

        # handle basic cases
        if len(move_input) != 3:
            return False
        if move_input[0] not in self.move_dict or move_input[2] not in self.move_dict:
            return False
        if type(move_input[1]) is not int:
            return False
        if move_input[2] == "W0":
            return False

        orig_pile = self.move_dict[move_input[0]]
        orig_ind = move_input[1]
        dest_pile = self.move_dict[move_input[2]]
        if orig_ind >= orig_pile.get_length():
            return False

        # handle flip tableau card Special Action
        if move_input[0][0] == 'T' and orig_pile == dest_pile and orig_ind == 0:
            orig_pile.reveal_top_card()

        # basic conditions have been met
        adj_ind = orig_pile.get_length() - orig_ind - 1
        if orig_pile.is_valid_retrieval(orig_ind):
            move_pile = orig_pile.remove_cards(orig_ind + 1)
            if dest_pile.is_valid_placement(move_pile):
                dest_pile.merge_pile(move_pile)
                if move_input[0][0] == 'T' and self.auto_flip_tab:
                    orig_pile.reveal_top_card()
                self.moves += 1
                return True
            else:
                orig_pile.merge_pile(move_pile)
                return False
        return False

    def str_tableaus(self):
        """
        draws tableaus horizontally
        """
        str_tab = ""
        for tab in self.tableaus:
            str_tab += "\n" + str(tab)
        return str_tab

    def str_tableaus_alt(self):
        """
        draws tableaus vertically
        """
        str_tab = ""
        for i in range(self.num_tableaus):
            str_tab += f'=T{i}= '
        str_tab += '\n'

        keep_drawing = True
        cur_card_ind = 0
        while keep_drawing:
            finished_tabs = 0
            for tbl in self.tableaus:
                if cur_card_ind < tbl.get_length():
                    str_tab += str(tbl.get_card_list()[cur_card_ind]) + " "
                else:
                    str_tab += "     "
                    finished_tabs += 1
            str_tab += "\n"
            cur_card_ind += 1
            if finished_tabs == self.num_tableaus:
                keep_drawing = False
        return str_tab

    def str_foundations(self):
        str_found = ""
        for found in self.foundations:
            if found is not None:
                str_found += str(found) + " "
            else:
                str_found += str([])
        return str_found

    def __str__(self):
        line1 = str(f'S0: {self.stock} W0: {self.wp} | F: {self.str_foundations()}\n\n')
        line2 = str(f'T: \n{self.str_tableaus_alt()}')

        return line1 + line2

