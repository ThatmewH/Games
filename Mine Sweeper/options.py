B_WIDTH = 50
B_HEIGHT = 30

DIFFICULITY = "easy" # {easy, medium, hard}
SQUARE_SIZE = 20

######################################################
DIFF = {"easy":0.1, "medium":0.15, "hard":0.2}
MINE_NUM = int(B_HEIGHT * B_WIDTH * DIFF[DIFFICULITY])

SCREEN_WIDTH = B_WIDTH * SQUARE_SIZE
SCREEN_HEIGHT = B_HEIGHT * SQUARE_SIZE

FLAG_NUM = MINE_NUM

FIRST_PRESS = True
