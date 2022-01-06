import pygame, random
from options import *
pygame.init()
numText = pygame.font.Font('freesansbold.ttf', 15)
mineText = pygame.font.Font('freesansbold.ttf', 15)

SquarePos = {0:[-1,-1], 1:[0,-1], 2:[1,-1], 3:[1,0], 4:[1,1], 5:[0,1], 6:[-1,1], 7:[-1,0]}
x = 0
class Tile:
    def __init__(self, pos):
        self.pos = pos

        self.mine = False
        self.exposed = False
        self.flagged = False

        self.nearbyMines = 0
def createEmptyBoard():
    board = []
    for y in range(B_HEIGHT):
        row = []
        for x in range(B_WIDTH):
            row.append(Tile([x,y]))
        board.append(row)
    return board
def populateBoard(board, mineNum, startTile):
    possibleChoices = []
    for y in range(B_HEIGHT):
        for x in range(B_WIDTH):
            possibleChoices.append([x,y])
    possibleChoices.remove(startTile)
    sorroundVectors = getPossiblePositions(board, startTile)
    for sorroundKey in sorroundVectors:
        possibleChoices.remove([startTile[0] + sorroundVectors[sorroundKey][0],startTile[1]+ sorroundVectors[sorroundKey][1]])
    # Expose Star Shape On CLick
    if possibleChoices.__contains__([startTile[0], startTile[1]+2]):
        possibleChoices.remove([startTile[0], startTile[1]+2])
        board[startTile[1]+2][startTile[0]].exposed = True
    if possibleChoices.__contains__([startTile[0], startTile[1]-2]):
        possibleChoices.remove([startTile[0], startTile[1]-2])
        board[startTile[1]-2][startTile[0]].exposed = True
    if possibleChoices.__contains__([startTile[0]+2, startTile[1]]):
        possibleChoices.remove([startTile[0]+2, startTile[1]])
        board[startTile[1]][startTile[0]+2].exposed = True
    if possibleChoices.__contains__([startTile[0]-2, startTile[1]]):
        possibleChoices.remove([startTile[0]-2, startTile[1]])
        board[startTile[1]][startTile[0]-2].exposed = True

    for i in range(mineNum):
        mineTile = random.choice(possibleChoices)
        possibleChoices.remove(mineTile)

        board[mineTile[1]][mineTile[0]].mine = True
        addBombCount(board, mineTile)
def drawBoard(surface, board):
    for row in board:
        for tile in row:
            if tile.exposed:
                pygame.draw.rect(surface, (50,50,50), (tile.pos[0]*SQUARE_SIZE, tile.pos[1]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.rect(surface, (0,0,0), (tile.pos[0]*SQUARE_SIZE, tile.pos[1]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
                if tile.mine:
                    pygame.draw.circle(surface, (0,0,0), (tile.pos[0]*SQUARE_SIZE + SQUARE_SIZE//2, tile.pos[1]*SQUARE_SIZE + SQUARE_SIZE//2), 3)
                elif tile.nearbyMines > 0:
                    textSurface = numText.render(str(tile.nearbyMines), True, (0,0,0))
                    textRect = textSurface.get_rect()
                    textRect.center = (tile.pos[0]*SQUARE_SIZE + SQUARE_SIZE//2, tile.pos[1]*SQUARE_SIZE + SQUARE_SIZE//2)
                    surface.blit(textSurface, textRect)
            elif tile.flagged:
                pygame.draw.rect(surface, (100,100,100), (tile.pos[0]*SQUARE_SIZE, tile.pos[1]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.rect(surface, (0,0,0), (tile.pos[0]*SQUARE_SIZE, tile.pos[1]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
                pygame.draw.circle(surface, (255,0,0), (tile.pos[0]*SQUARE_SIZE + SQUARE_SIZE//2, tile.pos[1]*SQUARE_SIZE + SQUARE_SIZE//2), 3)
            else:
                pygame.draw.rect(surface, (100,100,100), (tile.pos[0]*SQUARE_SIZE, tile.pos[1]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.rect(surface, (0,0,0), (tile.pos[0]*SQUARE_SIZE, tile.pos[1]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
def getPossiblePositions(board, minePos):
    possibleChanges = SquarePos.copy()
    # Remove Non-Existant Squares
    if minePos[0] == 0:
        if 0 in possibleChanges: possibleChanges.pop(0)
        if 7 in possibleChanges: possibleChanges.pop(7)
        if 6 in possibleChanges: possibleChanges.pop(6)
    elif minePos[0] == B_WIDTH - 1:
        if 2 in possibleChanges: possibleChanges.pop(2)
        if 3 in possibleChanges: possibleChanges.pop(3)
        if 4 in possibleChanges: possibleChanges.pop(4)
    if minePos[1] == 0:
        if 0 in possibleChanges: possibleChanges.pop(0)
        if 1 in possibleChanges: possibleChanges.pop(1)
        if 2 in possibleChanges: possibleChanges.pop(2)
    elif minePos[1] == B_HEIGHT - 1:
        if 4 in possibleChanges: possibleChanges.pop(4)
        if 5 in possibleChanges: possibleChanges.pop(5)
        if 6 in possibleChanges: possibleChanges.pop(6)
    return possibleChanges
def addBombCount(board, minePos):
    sorroundingTiles = getPossiblePositions(board, minePos)
    for tileChange in sorroundingTiles:
        sorroundingTilePos = [minePos[0] + sorroundingTiles[tileChange][0], minePos[1] + sorroundingTiles[tileChange][1]]
        board[sorroundingTilePos[1]][sorroundingTilePos[0]].nearbyMines += 1
def exposeTile(tilePos, board):
    global x
    tile = board[tilePos[1]][tilePos[0]]
    if tile.nearbyMines > 0:
        tile.exposed = True
        deFlagTile(tile)
    if tile.nearbyMines == 0 and tile.exposed == False:
        tile.exposed = True
        deFlagTile(tile)
        sorroundingTiles = getPossiblePositions(board, tilePos)
        for tileKey in sorroundingTiles:
            futurePos = [tilePos[0] + sorroundingTiles[tileKey][0], tilePos[1] + sorroundingTiles[tileKey][1]]
            exposeTile(futurePos, board)
def deFlagTile(tile):
    global FLAG_NUM
    if tile.flagged:
        tile.flagged = False
        FLAG_NUM += 1
def flagTile(board, tilePos, FIRST_PRESS):
    global FLAG_NUM
    tile = board[tilePos[1]][tilePos[0]]
    if not(tile.exposed) and FLAG_NUM > 0 and not(FIRST_PRESS):
        tile.flagged = not(tile.flagged)
        if tile.flagged:
            FLAG_NUM -= 1
        else:
            FLAG_NUM += 1
def drawTextCenter(text, pos, surface):
    textSurface = numText.render(text, True, (0,0,0))
    textRect = textSurface.get_rect()
    textRect.center = pos
    surface.blit(textSurface, textRect)
def drawSide(surface):
    surface.fill((150, 150, 150))
    pygame.draw.circle(surface, (255,0,0), ((B_WIDTH*SQUARE_SIZE) + 20, int((B_HEIGHT*SQUARE_SIZE)*0.05)), 3)
    drawTextCenter(str(FLAG_NUM), ((B_WIDTH*SQUARE_SIZE) + 40, int((B_HEIGHT*SQUARE_SIZE)*0.05)), surface)
