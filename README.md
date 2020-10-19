```# solitaire-python
simple solitaire with python and PyGame
by: Alex Chally
solitaire glossary: https://semicolon.com/Solitaire/Rules/Glossary.html
  
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
        - .api_is_won()             => returns True/False whether the game is won yet  
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
        - pass  
5. Other notes:  
    a. cards are returned as a string in format 'SR', S=suit and R=rank  
        - examples: 'AH' => Ace of Hearts | 'TC' => Ten of Clubs | '7D' => Seven of Diamonds | 'QS' => Queen of Spades  
    b. if a card is flipped down on the board, it will be returned as '--'  
    c. if a pile is empty, None will be returned as the card  
  

  
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
[X] Reorganize package/modules  
[X] Start a game file that handles playing the game  
[X] Start GUI in game.py  
[X] Finish a working version of the game with GUI (no menu, no restart, no other features)  
[X] Finalize preliminary API in game.py  
[X] Implement a is_won method that determines if the game has been won  
[X] Make a method that cycles through every card and if every card is exposed, game is winnable  
[ ] Implement State Machine in game.py  
 - [ ] Title Screen -> New Game | Options  
 - [ ] Pause Menu -> New Game | Quit  
 - [ ] Win Screen -> New Game | Options | Quit  

```
