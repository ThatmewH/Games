from data import *
from pygame.locals import *
import random
import copy

class liveTile:
    def __init__(self, startPos, endHeight, colour):
        self.pos = startPos
        self.endHeight = endHeight
        self.colour = colour
        self.dy = 1
        self.falling = False
        self.angle = 0
    def update(self, list):
        if self.pos[1] < self.endHeight or self.falling:
            self.pos[1] += self.dy
            self.dy += 1
            if self.dy > 20:
                self.dy = 20
        if self.pos[1] > self.endHeight and not(self.falling):
            self.pos[1] = self.endHeight
            self.dy = 1
        if self.pos[1] > SCREEN_HEIGHT + 50:
            list.remove(self)
        rotatedImage, rotatedRect = rot_center(eval(self.colour), self.angle)
        screen.blit(rotatedImage, (self.pos[0], self.pos[1], rotatedRect.w, rotatedRect.h))
        self.angle += 3
def rot_center(image, angle):

    center = image.get_rect().center
    rotated_image = pygame.transform.rotate(image, angle).convert()
    new_rect = rotated_image.get_rect(center = center)

    return rotated_image, new_rect
def drawGame(screen, mousePos):
    pygame.draw.rect(screen, (0,0,75), (BOARD_OFFSET[0], BOARD_OFFSET[1], BOARD_SIZE[0], BOARD_SIZE[1]))
    # Draw Buttons
    screen.blit(red, (CIRCLE_POS_LEFT[0],CIRCLE_POS_LEFT[1]))
    screen.blit(yellow, (CIRCLE_POS_RIGHT[0],CIRCLE_POS_RIGHT[1]))
    # Draw Screen
    for liveTile in liveTiles:
        liveTile.update(liveTiles)
    screen.blit(boardImage, (BOARD_OFFSET[0],BOARD_OFFSET[1]))
    if playerPickup:
        screen.blit(eval(playerTurn), (mousePos[0] - (CIRCLE_SIZE[0])//2, mousePos[1] - (CIRCLE_SIZE[1])//2))

    redPlayerWins = smallFont.render(str(redWins), False, (255, 0, 0))
    redPlayerWinsRect = redPlayerWins.get_rect()
    redPlayerWinsRect.center = (CIRCLE_POS_LEFT[0] + CIRCLE_SIZE[0]//2,50)
    screen.blit(redPlayerWins, redPlayerWinsRect)

    yellowPlayerWins = smallFont.render(str(yellowWins), False, (200, 200, 0))
    yellowPlayerWinsRect = redPlayerWins.get_rect()
    yellowPlayerWinsRect.center = (CIRCLE_POS_RIGHT[0] + CIRCLE_SIZE[0]//2 -10,50)
    screen.blit(yellowPlayerWins, yellowPlayerWinsRect)

    # Drawn Winner
    if gameWinner:
        if gameWinner == "red":
            redWinnerRect = redWinner.get_rect()
            redWinnerRect.center = [SCREEN_WIDTH//2, SCREEN_HEIGHT*0.1]
            screen.blit(redWinner, redWinnerRect)
        if gameWinner == "yellow":
            yellowWinnerRect = yellowWinner.get_rect()
            yellowWinnerRect.center = [SCREEN_WIDTH//2, SCREEN_HEIGHT*0.1]
            screen.blit(yellowWinner, yellowWinnerRect)
def drawMenu(screen, mousePos):
    screen.blit(playImage, playImageRect)
def handleMouseDown(mousePos):
    global playerPickup

    if not(gameWinner):
        if pygame.Rect(CIRCLE_POS_LEFT[0], CIRCLE_POS_LEFT[1], CIRCLE_SIZE[0], CIRCLE_SIZE[1]).collidepoint(mousePos) and not(playerPickup) and playerTurn == 'red':
            playerPickup = True
        elif pygame.Rect(CIRCLE_POS_RIGHT[0], CIRCLE_POS_RIGHT[1], CIRCLE_SIZE[0], CIRCLE_SIZE[1]).collidepoint(mousePos)  and not(playerPickup) and playerTurn == 'yellow':
            playerPickup = True
    else:
        resetGame()
def handleMouseUp(mousePos):
    global playerPickup, gameBoard
    if not(gameWinner):
        if mousePos[1] < SCREEN_HEIGHT-BOARD_SIZE[1]:
            column = (mousePos[0] - BOARD_OFFSET[0]) // 70
            if column >= 0 and column <= BOARD_WIDTH-1:
                result, gameBoard = placeCircle(column, mousePos, gameBoard)
                circlePlaced(result)
    playerPickup = False
def placeCircle(column, mousePos, board, test=False):
    columnBoard = rowsToColumnBoard(board)
    for row in range(len(columnBoard[column])-1, -1, -1):
        if columnBoard[column][row] == '':
            board[row][column] = playerTurn
            if not(test):
                liveTiles.append(liveTile([column*SQUARE_SIZE[0] + BOARD_OFFSET[0]+6, mousePos[1]], row*SQUARE_SIZE[1] + BOARD_OFFSET[1] + 8, playerTurn))
            return True, board
    return False, board
def circlePlaced(result):
    if result:
        # Check Win
        winCheck = checkWin(gameBoard, playerTurn)
        if winCheck:
            setWinGame()
        else:
            switchTurn()
            if playerTurn == "yellow" and bot:
                getBotMove()
def switchTurn():
    global playerTurn
    if playerTurn == 'red':
        playerTurn = 'yellow'
    else:
        playerTurn = 'red'
def rowsToColumnBoard(rowBoard):
    columnBoard = []
    for columnNum in range(len(rowBoard[0])):
        column = []
        for rowNum in range(len(rowBoard)):
            column.append(rowBoard[rowNum][columnNum])
        columnBoard.append(column)
    return columnBoard
def get_rows(grid):
    return [[c for c in r] for r in grid]

def get_cols(grid):
    return zip(*grid)
def get_backward_diagonals(grid):
    b = [None] * (len(grid) - 1)
    grid = [b[i:] + r + b[:i] for i, r in enumerate(get_rows(grid))]
    return [[c for c in r if c is not None] for r in get_cols(grid)]
def get_forward_diagonals(grid):
    b = [None] * (len(grid) - 1)
    grid = [b[:i] + r + b[i:] for i, r in enumerate(get_rows(grid))]
    return [[c for c in r if c is not None] for r in get_cols(grid)]
def checkWin(gameBoard, colour):
    # Check 4 In A Row
    result = compareList(gameBoard, colour)
    if result: return True

    # Check 4 in A Column
    gameBoardColumn = rowsToColumnBoard(gameBoard)
    result = compareList(gameBoardColumn, colour)
    if result: return True

    # Check 4 In Left-Right Diagonals
    gameBoardLRDiag = get_backward_diagonals(gameBoard)
    result = compareList(gameBoardLRDiag, colour)
    if result: return True
    # Check 4 in Right-Left Diagonals
    gameBoardRLDiag = get_forward_diagonals(gameBoard)
    result = compareList(gameBoardRLDiag, colour)
    if result: return True
    return False
def compareList(gameBoard, colour):
    winRow = getWinRow(colour)
    for row in gameBoard:
        if userContains(winRow, row):
            return True
    return False
def getWinRow(colour):
    winRow = []
    for x in range(WIN_NUM):
        winRow.append(colour)
    return winRow
def userContains(small, big):
    for i in range(1 + len(big) - len(small)):
        if small == big[i:i+len(small)]:
            return i, i + len(small) - 1
    return False
def setWinGame():
    global gameWinner, redWins, yellowWins
    gameWinner = playerTurn
    if playerTurn == "red": redWins += 1
    else: yellowWins += 1
def resetGame():
    global playerTurn, gameWinner, gameBoard, liveTiles
    playerTurn = gameWinner
    gameWinner = None
    gameBoard = emptyBoard(BOARD_WIDTH, BOARD_HEIGHT)
    for tile in liveTiles:
        tile.falling = True
        tile.dy = 0
    if playerTurn == "yellow" and bot:
        getBotMove()
def getBotMove():
    global playerTurn, gameBoard
    avaiablePos = []
    badPos = []
    possibleWinPos = []
    blockPos = []
    gotToColumn = None
    for i in range(BOARD_WIDTH):
        playerTurn = "yellow"
        botBoard = copy.deepcopy(gameBoard)
        # Check Win
        result, botBoard = placeCircle(i, [0,10], botBoard, True)
        if result: avaiablePos.append(i)
        winResult = checkWin(botBoard, "yellow")
        if winResult:
            gotToColumn = i
            break
        # Check Next Turn Wins
        tempBotBoard = copy.deepcopy(botBoard)
        result, tempBotBoard = placeCircle(i, [0,10], tempBotBoard, True)
        if result:
            winResult = checkWin(tempBotBoard, "yellow")
            if winResult:
                avaiablePos.remove(i)
                possibleWinPos.append(i)
        # Check Red Win Positions After Yellow
        playerTurn = "red"
        result, botBoard = placeCircle(i, [0,10], botBoard, True)
        if result:
            winResult = checkWin(botBoard, "red")
            if winResult:
                badPos.append(i)
                if avaiablePos.__contains__(i):
                    avaiablePos.remove(i)
        # Check Positions To Block
        botBoard = copy.deepcopy(gameBoard)
        result, botBoard = placeCircle(i, [0,10], botBoard, True)
        if result:
            winResult = checkWin(botBoard, "red")
            if winResult:
                blockPos.append(i)
    playerTurn = "yellow"
    result = False
    if gotToColumn != None:
        result, gameBoard = placeCircle(gotToColumn, [0,-400], gameBoard)
    elif blockPos:
        result, gameBoard = placeCircle(blockPos[0], [0,-400], gameBoard)
    elif avaiablePos:
        result, gameBoard = placeCircle(random.choice(avaiablePos), [0,-400], gameBoard)
    elif possibleWinPos:
        result, gameBoard = placeCircle(possibleWinPos[0], [0,-400], gameBoard)
    elif badPos:
        result, gameBoard = placeCircle(badPos[0], [0,-400], gameBoard)
    if result:
        circlePlaced(result)
window = {"game": drawGame, "menu":drawMenu}
