from pygame.locals import *
from tile import *
import sys

sys.setrecursionlimit(1500)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH+100, SCREEN_HEIGHT), 0, 32)
boardSurface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()

clock = pygame.time.Clock()

BOARD = createEmptyBoard()
drawBoard(boardSurface, BOARD)

while True:
    global FIRST_PRESS
    drawSide(screen)

    mousePos = pygame.mouse.get_pos()
    squarePos = [mousePos[0]//SQUARE_SIZE, mousePos[1]//SQUARE_SIZE]
    if squarePos[0] > B_WIDTH-1:
        squarePos[0] = B_WIDTH-1

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if FIRST_PRESS:
                    populateBoard(BOARD, MINE_NUM, squarePos)
                    FIRST_PRESS = False
                exposeTile(squarePos, BOARD)
            elif event.button == 3:
                flagTile(BOARD, squarePos, FIRST_PRESS)
            drawBoard(boardSurface, BOARD)
        if event.type == KEYDOWN:
            if event.key == K_n:
                BOARD = createEmptyBoard()
                drawBoard(boardSurface, BOARD)
                FIRST_PRESS = True
                MINE_NUM = int(B_HEIGHT * B_WIDTH * DIFF[DIFFICULITY])
                FLAG_NUM = MINE_NUM

    screen.blit(boardSurface, (0,0))
    pygame.draw.rect(screen, (0,0,0), (squarePos[0]*SQUARE_SIZE, squarePos[1]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

    clock.tick(60)
    pygame.display.flip()
