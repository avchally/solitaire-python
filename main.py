"""
simple solitaire with python and PyGame
by: Alex Chally
solitaire glossary: https://semicolon.com/Solitaire/Rules/Glossary.html

runs the game in either command line or with GUI

"""

from data.game import Game
import data.seed_processor

#============= CUSTOM SEED STUFF =============#
"""
pass for now
"""


#============= GAME =============#
def main():
    options = {'g': False, 'c': True}
    choice = ''
    while choice not in ['g', 'c']:
        choice = input("Play with GUI or in the console? [g] or [c] ")

        gm = Game()
        gm.new_game(deal_3=False,
                    commandline=options[choice])
                    # custom_seed='aWRcXysfdHiGnIUVEDKQrwevjokpNqMbSgzZFCJTAuxPhOmLBYlt')


if __name__ == "__main__":
    main()
