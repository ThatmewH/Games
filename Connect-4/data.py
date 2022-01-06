import pygame
pygame.init()
pygame.font.init()

def emptyBoard(width, height):
    newEmptyBoard = []
    for y in range(height):
        emptyRow = []
        for x in range(width):
            emptyRow.append('')
        newEmptyBoard.append(emptyRow)
    return newEmptyBoard

BOARD_WIDTH = 7
BOARD_HEIGHT = 6

WIN_NUM = 4

# Load Screen Vairables
SQUARE_SIZE = [70, 72]

SCREEN_WIDTH = BOARD_WIDTH*SQUARE_SIZE[0]+300
SCREEN_HEIGHT = BOARD_HEIGHT*SQUARE_SIZE[1]+100
if SCREEN_WIDTH < 600:
    SCREEN_WIDTH = 600
if SCREEN_HEIGHT < 400:
    SCREEN_HEIGHT = 400
BOARD_SIZE = [SQUARE_SIZE[0]*BOARD_WIDTH, SQUARE_SIZE[1]*BOARD_HEIGHT]
BOARD_OFFSET = [(SCREEN_WIDTH-BOARD_SIZE[0])//2, (SCREEN_HEIGHT-BOARD_SIZE[1])]

CIRCLE_SIZE = [70,72]
CIRCLE_POS_LEFT = [(BOARD_OFFSET[0] - CIRCLE_SIZE[0])//2, SCREEN_HEIGHT-CIRCLE_SIZE[1] - 30]
CIRCLE_POS_RIGHT = [SCREEN_WIDTH - (BOARD_OFFSET[0] + CIRCLE_SIZE[0])//2, SCREEN_HEIGHT-CIRCLE_SIZE[1] - 30]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Images
squareImage = pygame.image.load("square.png").convert()
squareImage.set_colorkey((0,0,0))
red = pygame.image.load("red.png").convert()
red.set_colorkey((255,255,255))
yellow = pygame.image.load("yellow.png").convert()
yellow.set_colorkey((255,255,255))


# Load Text
bigFont = pygame.font.SysFont('Comic Sans MS', 60)
redWinner = bigFont.render('Red Player Wins!', False, (255, 0, 0))
yellowWinner = bigFont.render('Yellow Player Wins!', False, (255, 255, 0))

smallFont = pygame.font.SysFont('serrifsansbold', 60)

# Load Game Variables
playerTurn = "red"
playerPickup = False
gameWinner = None
bot = True
liveTiles = []
redWins = 0
yellowWins = 0

boardImage = pygame.Surface(BOARD_SIZE).convert()
boardImage.fill((255,255,255))
boardImage.set_colorkey((255,255,255))
for y in range(BOARD_HEIGHT):
    for x in range(BOARD_WIDTH):
        boardImage.blit(squareImage, [x*SQUARE_SIZE[0], y*SQUARE_SIZE[1]])

gameBoard = emptyBoard(BOARD_WIDTH, BOARD_HEIGHT)

currentWindow = "game"
