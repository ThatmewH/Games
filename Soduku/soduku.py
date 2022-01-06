import pygame, random, copy, time
from pygame.locals import *
pygame.init()

WIDTH = 600
HEIGHT = 600
display = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32)
clock = pygame.time.Clock()

REMOVE_NUM = 81-30
SQUARE_SIZE = 50
boardLength = 9*SQUARE_SIZE
BOARD_OFFSET = [(WIDTH//2) - (boardLength/2), (HEIGHT//2) - (boardLength/2)]
# Fonts
bigNumberFont = pygame.font.Font('freesansbold.ttf', 30)
smallNumberFont = pygame.font.Font('freesansbold.ttf', 15)

winTextSurface = bigNumberFont.render("WINNER!", True, (0,0,0))
winTextSurfaceRect = winTextSurface.get_rect()
winTextSurfaceRect.center = (WIDTH//2, HEIGHT*0.1)

#
autoCompleteFinished = False
gameWon = False

board = []
fallingNumbers = []
sideNumPositions = {0:[int(SQUARE_SIZE*0.15), int(SQUARE_SIZE*0.2)], 1:[int(SQUARE_SIZE*0.5), int(SQUARE_SIZE*0.2)], 2:[int(SQUARE_SIZE*0.85), int(SQUARE_SIZE*0.2)], 3:[int(SQUARE_SIZE*0.15), int(SQUARE_SIZE*0.5)], 4:[int(SQUARE_SIZE*0.5), int(SQUARE_SIZE*0.5)], 5:[int(SQUARE_SIZE*0.85), int(SQUARE_SIZE*0.5)], 6:[int(SQUARE_SIZE*0.15), int(SQUARE_SIZE*0.85)], 7:[int(SQUARE_SIZE*0.5), int(SQUARE_SIZE*0.85)], 8:[int(SQUARE_SIZE*0.85), int(SQUARE_SIZE*0.85)], }
class Square:
    def __init__(self, number=None):
        self.number = number
        self.sideNumbers = [None, None, None, None, None, None, None, None, None]
        self.canEdit = True
class NumFalling:
    def __init__(self, number, pos, colour):
        self.pos = pos
        self.vel = [random.randint(-4,4),random.randint(-15,-5)]
        self.yAcc = random.choice([0.3,0.4,0.5])
        self.number = number
        self.colour = colour

        self.canJump = True
        self.maxJumps = random.randint(0,4)
        self.numJumps = 0

        self.textSurface = bigNumberFont.render(str(self.number), True, (0,0,0))
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = (pos[0] + (SQUARE_SIZE//2), pos[1] + (SQUARE_SIZE//2))

    def update(self):
        global fallingNumbers
        # Check If Number Can Jump Anymore
        if self.numJumps > self.maxJumps:
            self.canJump = False
        # Add Acceleration And Velocty
        self.vel[1] += self.yAcc

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # Jump The Numbers
        if self.canJump:
            if self.pos[1] + (SQUARE_SIZE//2) > HEIGHT:
                self.vel[1] *= -1
                self.pos[1] = HEIGHT - (SQUARE_SIZE//2)
                self.numJumps += 1
            if self.pos[0] + (SQUARE_SIZE//2) > WIDTH:
                self.vel[0] *= -1
                self.pos[0] = WIDTH - (SQUARE_SIZE//2)
            if self.pos[0] + (SQUARE_SIZE//2) < 0:
                self.vel[0] *= -1
                self.pos[0] = 0 - (SQUARE_SIZE//2)

        self.textRect.center = (self.pos[0] + (SQUARE_SIZE//2), self.pos[1] + (SQUARE_SIZE//2))
        display.blit(self.textSurface, self.textRect)

        if self.pos[1] > HEIGHT + 10:
            # Delete Itself
            fallingNumbers.remove(self)
def genEmptyBoard():
    board = []
    for y in range(9):
        row = []
        for x in range(9):
            row.append(Square())
        board.append(row)
    return board
def populateBoard(board):
    for y in range(9):
        rowNumbers = [1,2,3,4,5,6,7,8,9]
        for x in range(9):
            possibleNumbers = copy.deepcopy(rowNumbers)
            columnNumbers = getColumnNumbers(board, x)
            boxNumbers = getSquareNumbers(board, y, x)
            for number in columnNumbers:
                if possibleNumbers.__contains__(number):
                    possibleNumbers.remove(number)
            for number in boxNumbers:
                if possibleNumbers.__contains__(number):
                    possibleNumbers.remove(number)
            try:
                randomNum = random.choice(possibleNumbers)
                rowNumbers.remove(randomNum)
                board[y][x].number = randomNum
                board[y][x].canEdit = False
            except:
                break
def updateBoard():
    # Draw Lines
    lineLength = 9*SQUARE_SIZE
    lineSurface = pygame.Surface((lineLength, lineLength))
    lineSurface.fill((255,255,255))
    # Draw Grey Lines
    for row in range(9):
        width = 2
        colour = (200,200,200)
        if row % 3 == 0:
            continue
        pygame.draw.line(lineSurface, colour, (0, row*SQUARE_SIZE), (lineLength, row*SQUARE_SIZE), width)
    for column in range(9):
        width = 2
        colour = (200,200,200)
        if column % 3 == 0:
            continue
        pygame.draw.line(lineSurface, colour, (column*SQUARE_SIZE, 0), (column*SQUARE_SIZE, lineLength), width)
    # Draw Black Lines
    for row in [3,6]:
        pygame.draw.line(lineSurface, (0,0,0), (0, row*SQUARE_SIZE), (lineLength, row*SQUARE_SIZE), 3)
        pygame.draw.line(lineSurface, (0,0,0), (row*SQUARE_SIZE, 0), (row*SQUARE_SIZE, lineLength), 3)

    pygame.draw.line(lineSurface, (0,0,0), (lineLength, 0), (lineLength, lineLength), 8)
    pygame.draw.line(lineSurface, (0,0,0), (0, lineLength), (lineLength, lineLength), 8)
    pygame.draw.line(lineSurface, (0,0,0), (0, 0), (lineLength, 0), 4)
    pygame.draw.line(lineSurface, (0,0,0), (0, 0), (0, lineLength), 4)
    # Draw Numbers
    for row in range(9):
        for x in range(9):
            if board[row][x].number:
                if board[row][x].canEdit:
                    textSurface = bigNumberFont.render(str(board[row][x].number), True, (0,0,0))
                else:
                    textSurface = bigNumberFont.render(str(board[row][x].number), True, (100,100,100))
                textRect = textSurface.get_rect()
                textRect.center = (x*SQUARE_SIZE + (SQUARE_SIZE//2), row*SQUARE_SIZE + (SQUARE_SIZE//2))
                lineSurface.blit(textSurface, textRect)
            if board[row][x].sideNumbers:
                sideNumPos = 0
                for sideNumber in board[row][x].sideNumbers:
                    if sideNumber:
                        textSurface = smallNumberFont.render(str(sideNumber), True, (0,0,0))
                        textRect = textSurface.get_rect()
                        textRect.center = (x*SQUARE_SIZE + sideNumPositions[sideNumPos][0], row*SQUARE_SIZE + sideNumPositions[sideNumPos][1])
                        lineSurface.blit(textSurface, textRect)
                    sideNumPos += 1
    return lineSurface.convert()
def drawScreen(display):
    global ellapsedTime
    if not(gameWon):
        ellapsedTime = time.time() - timeStart
        display.fill((255,255,255))
        if bigNumMode:
            display.blit(lineSurface, (0 + BOARD_OFFSET[0],0 + BOARD_OFFSET[1]))
            if selectedSquare:
                pygame.draw.circle(display, (150,0,0), (int((selectedSquare[0]*SQUARE_SIZE+BOARD_OFFSET[0]) + (SQUARE_SIZE//2)), (int(selectedSquare[1]*SQUARE_SIZE+BOARD_OFFSET[1]) + (SQUARE_SIZE//2))), 3)
        else:
            display.blit(lineSurface, (0 + BOARD_OFFSET[0],0 + BOARD_OFFSET[1]))
            if selectedSquare:
                pygame.draw.circle(display, (150,0,0), (int((selectedSquare[0]*SQUARE_SIZE+BOARD_OFFSET[0]) + sideNumPositions[smallNumPos][0]), (int(selectedSquare[1]*SQUARE_SIZE+BOARD_OFFSET[1]) + sideNumPositions[smallNumPos][1])), 3)
    else:
        display.fill((255,255,255))
        display.blit(emptyBoardSurface, (0 + BOARD_OFFSET[0],0 + BOARD_OFFSET[1]))
        for fallingNum in fallingNumbers:
            fallingNum.update()
        display.blit(winTextSurface, winTextSurfaceRect)

    TimeSurface = bigNumberFont.render("Time: " + str(round(ellapsedTime,2)), True, (0,0,0))
    TimeSurfaceRect = winTextSurface.get_rect()
    TimeSurfaceRect.center = (WIDTH//2, BOARD_OFFSET[1] + (9*SQUARE_SIZE) + 25)

    display.blit(TimeSurface, TimeSurfaceRect)

    pygame.display.flip()
def setSquare(number):
    global lineSurface, smallNumPos
    if selectedSquare:
        square = board[int(selectedSquare[1])][int(selectedSquare[0])]
        if square.canEdit:
            if bigNumMode:
                square.number = number
                square.sideNumbers = [None, None, None, None, None, None, None, None, None]
            else:
                smallNumPos = number-1
                if square.sideNumbers[number-1]:
                    square.sideNumbers[number-1] = None
                else:
                    square.number = None
                    square.sideNumbers[number-1] = number
            lineSurface = updateBoard()
            checkWin(board)
def deleteNumber():
    global lineSurface
    if selectedSquare:
        if bigNumMode and board[int(selectedSquare[1])][int(selectedSquare[0])].canEdit:
            board[int(selectedSquare[1])][int(selectedSquare[0])].number = None
        else:
            board[int(selectedSquare[1])][int(selectedSquare[0])].sideNumbers[smallNumPos] = None
    lineSurface = updateBoard()
def checkIfDuplicates_1(list):
    ''' Check if given list contains any duplicates '''
    if len(list) == len(set(list)):
        return False
    else:
        return True
def checkWin(board):
    global gameWon
    # Check if board is full or not
    for row in board:
        for square in row:
            if square.number == None:
                return False
    # # Check Each Row For Duplicates
    for row in board:
        numbers = []
        for square in row:
            if square.number:
                numbers.append(square.number)
        if checkIfDuplicates_1(numbers):
            return False
    # Check Each Column For Duplicates
    for columnNumber in range(9):
        numbers = []
        for rowNumber in range(9):
            if board[rowNumber][columnNumber].number:
                numbers.append(board[rowNumber][columnNumber].number)
        if checkIfDuplicates_1(numbers):
            return False
    # Check Each Square
    gameWon = True
    for y in range(len(board)):
        for x in range(len(board[0])):
            tempColour = (0,0,0)
            if not(board[y][x].canEdit):
                tempColour = (100,100,100)
            fallingNumbers.append(NumFalling(board[y][x].number, [x*SQUARE_SIZE + BOARD_OFFSET[0], y*SQUARE_SIZE + BOARD_OFFSET[1]], tempColour))
def getColumnNumbers(board, x):
    numbers = []
    for rowNumber in range(9):
        if board[rowNumber][x].number:
            numbers.append(board[rowNumber][x].number)
    return numbers
def getSquareNumbers(board, y, x):
    if y <= 2:
        if x <= 2:
            xRange = [0,2]
            yRange = [0,2]
        elif x <= 5:
            xRange = [3,5]
            yRange = [0,2]
        elif x <= 8:
            xRange = [6,8]
            yRange = [0,2]
    elif y <= 5:
        if x <= 2:
            xRange = [0,2]
            yRange = [3,5]
        elif x <= 5:
            xRange = [3,5]
            yRange = [3,5]
        elif x <= 8:
            xRange = [6,8]
            yRange = [3,5]
    elif y <= 8:
        if x <= 2:
            xRange = [0,2]
            yRange = [6,8]
        elif x <= 5:
            xRange = [3,5]
            yRange = [6,8]
        elif x <= 8:
            xRange = [6,8]
            yRange = [6,8]
    numbers = []
    for tempY in range(yRange[0], yRange[1]+1):
        for tempX in range(xRange[0], xRange[1]+1):
            if board[tempY][tempX].number:
                numbers.append(board[tempY][tempX].number)
    return numbers
def getRowNumbers(board, y):
    numbers = []
    for square in board[y]:
        if square.number:
            numbers.append(square.number)
    return numbers
def checkBoardFull(board):
    for row in board:
        for square in row:
            if square.number == None:
                return False
    return True
def makeBoard():
    global board
    while True:
        board = genEmptyBoard()
        populateBoard(board)
        if checkBoardFull(board):
            break
    dePopulateBoard(board, REMOVE_NUM)
def dePopulateBoard(board, numToRemove):
    positions = []
    for i in range(81):
        positions.append(i)
    for i in range(numToRemove):
        randPos = random.choice(positions)
        positions.remove(randPos)
        y = randPos//9
        x = randPos%9

        board[y][x].number = None
        board[y][x].canEdit = True
def handleArrowMovement(event):
    global selectedSquare, smallNumPos
    if not(selectedSquare):
        selectedSquare = [0,0]
    if event.key == K_UP:
        selectedSquare[1] -= 1
        if selectedSquare[1] < 0: selectedSquare[1] = 0
    elif event.key == K_DOWN:
        selectedSquare[1] += 1
        if selectedSquare[1] > 8: selectedSquare[1] = 8
    elif event.key == K_LEFT:
        selectedSquare[0] -= 1
        if selectedSquare[0] < 0: selectedSquare[0] = 0
    elif event.key == K_RIGHT:
        selectedSquare[0] += 1
        if selectedSquare[0] > 8: selectedSquare[0] = 8
def autoComplete(board, x,y):
    global autoCompleteFinished, lineSurface
    if board[y][x].canEdit and not(board[y][x].number):
        possibleNum = [1,2,3,4,5,6,7,8,9]
        while not(autoCompleteFinished):
            rowNums = getRowNumbers(board, y)
            colNums = getColumnNumbers(board, x)
            squareNums = getSquareNumbers(board, y, x)
            for num in rowNums:
                if possibleNum.__contains__(num):
                    possibleNum.remove(num)
            for num in colNums:
                if possibleNum.__contains__(num):
                    possibleNum.remove(num)
            for num in squareNums:
                if possibleNum.__contains__(num):
                    possibleNum.remove(num)
            if len(possibleNum) < 1:
                board[y][x].number = None
                return
            board[y][x].number = possibleNum[0]
            possibleNum.pop(0)
            nextX = x + 1
            nextY = y
            if nextX > 8:
                nextX = 0
                nextY += 1
                if checkBoardFull(board):
                    autoCompleteFinished = True
                    return

            autoComplete(board, nextX, nextY)
            lineSurface = updateBoard()
            drawScreen(display)
    else:
        nextX = x + 1
        nextY = y
        if nextX > 8:
            nextX = 0
            nextY += 1
            if checkBoardFull(board):
                autoCompleteFinished = True
                return
        autoComplete(board, nextX, nextY)
def drawEmptyBoard():
    lineLength = 9*SQUARE_SIZE
    boardSurface = pygame.Surface((lineLength, lineLength))
    boardSurface.fill((255,255,255))
    # Draw Grey Lines
    for row in range(9):
        width = 2
        colour = (200,200,200)
        if row % 3 == 0:
            continue
        pygame.draw.line(boardSurface, colour, (0, row*SQUARE_SIZE), (lineLength, row*SQUARE_SIZE), width)
    for column in range(9):
        width = 2
        colour = (200,200,200)
        if column % 3 == 0:
            continue
        pygame.draw.line(boardSurface, colour, (column*SQUARE_SIZE, 0), (column*SQUARE_SIZE, lineLength), width)
    # Draw Black Lines
    for row in [3,6]:
        pygame.draw.line(boardSurface, (0,0,0), (0, row*SQUARE_SIZE), (lineLength, row*SQUARE_SIZE), 3)
        pygame.draw.line(boardSurface, (0,0,0), (row*SQUARE_SIZE, 0), (row*SQUARE_SIZE, lineLength), 3)

    pygame.draw.line(boardSurface, (0,0,0), (lineLength, 0), (lineLength, lineLength), 8)
    pygame.draw.line(boardSurface, (0,0,0), (0, lineLength), (lineLength, lineLength), 8)
    pygame.draw.line(boardSurface, (0,0,0), (0, 0), (lineLength, 0), 4)
    pygame.draw.line(boardSurface, (0,0,0), (0, 0), (0, lineLength), 4)
    return boardSurface.convert()

makeBoard()
lineSurface = updateBoard()
emptyBoardSurface = drawEmptyBoard()

bigNumMode = True # big / little
selectedSquare = None
smallNumPos = 0

numbers = [K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9]


timeStart = time.time()
ellapsedTime = time.time() - timeStart

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        # Switch Number Modes With Tab
        if event.type == KEYDOWN:
            if event.key == K_TAB:
                bigNumMode = not(bigNumMode)
            if event.key == K_n:
                gameWon = False
                makeBoard()
                lineSurface = updateBoard()
                fallingNumbers = []
                timeStart = time.time()
            if event.key == K_c:
                board = genEmptyBoard()
                lineSurface = updateBoard()
            if event.key == K_a:
                autoCompleteFinished = False
                autoComplete(board, 0, 0)
                lineSurface = updateBoard()
            if numbers.__contains__(event.key):
                pressedNumber = event.key - 48
                setSquare(pressedNumber)
            if event.key == K_DELETE or event.type == K_BACKSPACE:
                deleteNumber()
            handleArrowMovement(event)
        if event.type == MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            mousePosRelative = [mousePos[0] - BOARD_OFFSET[0], mousePos[1] - BOARD_OFFSET[1]]
            clickedSquare = [mousePosRelative[0]//SQUARE_SIZE, mousePosRelative[1]//SQUARE_SIZE]
            # Check if mouse Click Was Outside Board
            if clickedSquare[0] > 8 or clickedSquare[0] < 0 or clickedSquare[1] > 8 or clickedSquare[1] < 0:
                selectedSquare = None
            else:
                selectedSquare = clickedSquare
    drawScreen(display)
    clock.tick(60)
