"""
testing API from game.py
"""
from data.game import Game

def main():
	gm = Game(api_use=True)
	gm.new_game()

	flip_stock = ['S0', 0, 'S0']
	gm.api_make_move(flip_stock)
	gm.api_make_move(flip_stock)
	gm.api_make_move(flip_stock)
	gm.api_make_move(flip_stock)
	gm.api_make_move(flip_stock)

	print(gm.board)

	print(gm.api_get_moves())
	print()
	print(gm.api_read_stock())
	print()
	print(gm.api_read_waste_pile())
	print()
	print(gm.api_read_foundations())
	print()
	print(gm.api_read_tableaus())

	input("Press enter to exit\n")

if __name__ == "__main__":
	main()
