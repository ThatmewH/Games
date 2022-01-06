import pygame, time, random
from pygame.locals import *
from copy import deepcopy

def numMap(value, oldRangeMax, oldRangeMin, newRangeMax, newRangeMin):
    oldRange = oldRangeMax - oldRangeMin
    newRange = newRangeMax - newRangeMin
    return (((value - oldRangeMin) * newRange) / oldRange) + newRangeMin

pygame.init()
screen = pygame.display.set_mode((400,600), 0, 32)
boardPositions = []
Blocks = {0:[[[3,-3], [4,-3], [4,-2], [4,-1]], [[3,-2], [4,-2], [5,-2], [5,-3]], [[4,-3], [4,-2], [4,-1], [5,-1]], [[3,-1], [3,-2], [4,-2], [5,-2]]],
          1:[[[4,-3], [3,-2], [4,-2], [5,-2]], [[4,-3], [4,-2], [4,-1], [5,-2]], [[3,-2], [4,-2], [5,-2], [4,-1]], [[3,-2], [4,-3], [4,-2], [4,-1]]],
          2:[[[4,-4], [4,-3], [4,-2], [4,-1]], [[2,-3], [3,-3], [4,-3], [5,-3]], [[4,-4], [4,-3], [4,-2], [4,-1]], [[2,-3], [3,-3], [4,-3], [5,-3]]],
          3:[[[3,-3], [3,-2], [4,-2], [5,-2]], [[4,-3], [5,-3], [4,-2], [4,-1]], [[3,-2], [4,-2], [5,-2], [5,-1]], [[4,-3], [4,-2], [4,-1], [3,-1]]],
          4:[[[4,-3], [5,-3], [4,-2], [5,-2]], [[4,-3], [5,-3], [4,-2], [5,-2]], [[4,-3], [5,-3], [4,-2], [5,-2]], [[4,-3], [5,-3], [4,-2], [5,-2]]],
          5:[[[3,-2], [4,-2], [4,-3], [5,-3]], [[4,-3], [4,-2], [5,-2], [5,-1]], [[3,-1], [4,-1], [4,-2], [5,-2]], [[3,-3], [3,-2], [4,-2], [4,-1]]],
          6:[[[3,-3], [4,-3], [4,-2], [5,-2]], [[5,-3], [5,-2], [4,-2], [4,-1]], [[3,-2], [4,-2], [4,-1], [5,-1]], [[3,-1], [3,-2], [4,-2], [4,-3]]]}
SCORE = 0
DISPLAY_SCORE = 0
BLOCK_WIDTH = 25
DIFFICULTY = 1


BLOCK_FALL_SPEED = numMap(DIFFICULTY, 1, 10, 1, 0.1)


cameraOffset = [75,0]
# Text Setup
largeText = pygame.font.Font('freesansbold.ttf',100)
textSurface = largeText.render(str(DISPLAY_SCORE), True, (0,0,0))
textRect = textSurface.get_rect()
textRect.center = (400 // 2, 560)
downKey = False
leftKey = False
rightKey = False
gameRunning = False
class blockButton():
    def __init__(self,x,y,blockSize=25, blockWidth=3):
        self.x = x
        self.y = y
        self.blockSize = blockSize
        self.blockWidth = blockWidth
        self.map = [[1,1,5,0,1,0,0,0,4,1,5,0,1,0,1],
                    [1,0,1,0,1,0,0,0,1,0,1,0,1,0,1],
                    [1,1,3,0,1,0,0,0,1,1,1,0,2,1,3],
                    [1,0,0,0,1,0,0,0,1,0,1,0,0,1,0],
                    [1,0,0,0,1,1,5,0,1,0,1,0,0,1,0]]
        self.colour = [0,0,0]
        self.rect = pygame.Rect(self.x,self.y,len(self.map[0])*self.blockSize,len(self.map)*self.blockSize)
        self.cornerSurface = pygame.Surface((blockSize, blockSize))
    def update(self):
        for row in range(len(self.map)):
            for element in range(len(self.map[row])):
                if self.map[row][element] == 1:
                    pygame.draw.rect(screen, (int(self.colour[0]), int(self.colour[1]),int(self.colour[2])), (element*self.blockSize + self.x, row*self.blockSize + self.y, self.blockSize, self.blockSize))
                    pygame.draw.rect(screen, (30,30,30), (element*self.blockSize + self.x, row*self.blockSize + self.y, self.blockSize, self.blockSize), self.blockWidth)
                if self.map[row][element] == 2:
                    pygame.draw.polygon(screen, (int(self.colour[0]), int(self.colour[1]),int(self.colour[2])), [[element*self.blockSize + self.x - 1,row*self.blockSize + self.y - 1], [element*self.blockSize + self.x + self.blockSize - 1,row*self.blockSize + self.y - 1], [element*self.blockSize + self.x + self.blockSize - 1,row*self.blockSize + self.y + self.blockSize - 1]])
                    pygame.draw.polygon(screen, (30,30,30), [[element*self.blockSize + self.x - 1,row*self.blockSize + self.y - 1], [element*self.blockSize + self.x + self.blockSize - 1,row*self.blockSize + self.y - 1], [element*self.blockSize + self.x + self.blockSize - 1,row*self.blockSize + self.y + self.blockSize - 1]], 3)
                if self.map[row][element] == 3:
                    pygame.draw.polygon(screen, (int(self.colour[0]), int(self.colour[1]),int(self.colour[2])), [[element*self.blockSize + self.x,row*self.blockSize + self.y], [element*self.blockSize + self.x + self.blockSize,row*self.blockSize + self.y], [element*self.blockSize + self.x,row*self.blockSize + self.y + self.blockSize]])
                    pygame.draw.polygon(screen, (30,30,30), [[element*self.blockSize + self.x,row*self.blockSize + self.y], [element*self.blockSize + self.x + self.blockSize,row*self.blockSize + self.y], [element*self.blockSize + self.x,row*self.blockSize + self.y + self.blockSize]], 3)
                if self.map[row][element] == 4:
                    pygame.draw.polygon(screen, (int(self.colour[0]), int(self.colour[1]),int(self.colour[2])), [[element*self.blockSize + self.x + self.blockSize,row*self.blockSize + self.y], [element*self.blockSize + self.x + self.blockSize,row*self.blockSize + self.y + self.blockSize], [element*self.blockSize + self.x,row*self.blockSize + self.y + self.blockSize]])
                    pygame.draw.polygon(screen, (30,30,30), [[element*self.blockSize + self.x + self.blockSize,row*self.blockSize + self.y], [element*self.blockSize + self.x + self.blockSize,row*self.blockSize + self.y + self.blockSize], [element*self.blockSize + self.x,row*self.blockSize + self.y + self.blockSize]], 3)
                if self.map[row][element] == 5:
                    pygame.draw.polygon(screen, (int(self.colour[0]), int(self.colour[1]),int(self.colour[2])), [[element*self.blockSize + self.x,row*self.blockSize + self.y], [element*self.blockSize + self.x,row*self.blockSize + self.y + self.blockSize], [element*self.blockSize + self.x + self.blockSize,row*self.blockSize + self.y + self.blockSize]])
                    pygame.draw.polygon(screen, (30,30,30), [[element*self.blockSize + self.x,row*self.blockSize + self.y], [element*self.blockSize + self.x,row*self.blockSize + self.y + self.blockSize], [element*self.blockSize + self.x + self.blockSize,row*self.blockSize + self.y + self.blockSize]], 3)

        if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): self.colour[1] += 1
        else: self.colour[1] -= 0.2

        if self.colour[1] > 255: self.colour[1] = 255
        elif self.colour[1] < 0: self.colour[1] = 0
    def handleEvent(self, event):
        global activeState
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                activeState = 1
class Button():
    def __init__(self, pos, text):
        self.text = text
        self.pos = pos
class fallingBlock():
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
        self.dy = random.randint(-30,-10)
        self.angle = 0
        self.da = random.choice([-1,1]) * 3
        self.lastUpdate = time.time()
        self.originalBlockSurface = pygame.Surface((30,30), SRCALPHA)
        pygame.draw.rect(self.originalBlockSurface, (0,255,0), (0, 0, BLOCK_WIDTH, BLOCK_WIDTH))
        pygame.draw.rect(self.originalBlockSurface, (30,30,30), (0, 0, BLOCK_WIDTH, BLOCK_WIDTH), 3)
        self.blockSurface = pygame.transform.rotate(self.originalBlockSurface, self.angle)
    def update(self):
        if time.time() - self.lastUpdate > 0.02:
            self.lastUpdate = time.time()
            self.dy += 1
            self.y += self.dy
            self.x += self.dir

            if self.y > 600: fallingBlocks.remove(self)
            self.blockSurface = pygame.transform.rotate(self.originalBlockSurface, self.angle)
            self.angle += self.da
        screen.blit(self.blockSurface, (self.x, self.y))
def drawScore():
    global DISPLAY_SCORE, textSurface, textRect
    if DISPLAY_SCORE < SCORE:
        DISPLAY_SCORE += (SCORE - DISPLAY_SCORE) * 0.005
        textSurface = largeText.render(str(round(DISPLAY_SCORE)), True, (0,0,0))
        textRect = textSurface.get_rect()
        textRect.center = (400 // 2, 550)
    screen.blit(textSurface, textRect)
def drawBoard(boardWidth, boardHeight):
    for y in range(boardHeight):
        for x in range(boardWidth):
                pygame.draw.rect(screen, (30,30,30), (x*BLOCK_WIDTH + cameraOffset[0], y*BLOCK_WIDTH + cameraOffset[1], BLOCK_WIDTH, BLOCK_WIDTH), 2)
def drawBlocks(boardPositions):
    for position in boardPositions:
        pygame.draw.rect(screen, (0, 255, 0), (position[0]*BLOCK_WIDTH + cameraOffset[0],position[1]*BLOCK_WIDTH + cameraOffset[1],BLOCK_WIDTH,BLOCK_WIDTH))

def createActiveBlock():
    global block
    block = None
    block = activeBlock()
class activeBlock():
    def __init__(self):
        self.blockRotationId = 0
        self.blockId = random.randint(0,6)
        self.positions = deepcopy(Blocks[self.blockId][self.blockRotationId])
        self.yDifference = 0
        self.xDifference = 0
        self.lastUpdate = time.time()
        self.lastTranslate = time.time()
        self.hit = False
        if not(downKey):
            self.blockFallSpeed = BLOCK_FALL_SPEED
        else:
            self.blockFallSpeed = BLOCK_FALL_SPEED/10
    def update(self, leftKey, rightkey):
        # Moving Left And Right
        if (leftKey or rightKey) and time.time() - self.lastTranslate > 0.2:
            if leftKey:
                self.translate = -1
            else:
                self.translate = 1
            self.lastTranslate = time.time()
            nextPositons = deepcopy(self.positions)
            for position in nextPositons:
                position[0] += self.translate
            if not(self.checkCollisionRotateTranslate(nextPositons)):
                self.changePositions(self.translate, 0)

        for position in self.positions:
            pygame.draw.rect(screen, (0, 255, 0), (position[0]*BLOCK_WIDTH  + cameraOffset[0],position[1]*BLOCK_WIDTH + cameraOffset[1],BLOCK_WIDTH,BLOCK_WIDTH))
        if time.time() - self.lastUpdate > self.blockFallSpeed:

            self.nextPositions = deepcopy(self.positions)
            for position in self.nextPositions:
                position[1] += 1
            if not(self.checkCollisionDown(self.nextPositions)):
                self.changePositions(0,1)
            else:
                for position in self.positions:
                    boardPositions.append(position)
                createActiveBlock()
                self.checkCompleteRows()
            self.lastUpdate = time.time()
    def changePositions(self, xChange, yChange):
        self.yDifference += yChange
        self.xDifference += xChange
        for position in self.positions:
            position[0] += xChange
            position[1] += yChange
    def checkCollisionDown(self, positions):
        for position in positions:
            if position[1] > 19: return True
            for boardPosition in boardPositions:
                if position == boardPosition: return True
    def checkCollisionRotateTranslate(self, positions):
        for position in positions:
            if position[1] > 19: return True
            elif position[0] < 0: return True
            elif position[0] > 9: return True
            for boardPosition in boardPositions:
                if position == boardPosition:
                    return True
        return False
    def rotate(self):
        self.blockRotationId += 1
        if self.blockRotationId > 3:
            self.blockRotationId = 0
        self.nextPositions = deepcopy(Blocks[self.blockId][self.blockRotationId])
        for position in self.nextPositions:
            position[0] += self.xDifference
            position[1] += self.yDifference
        if not(self.checkCollisionRotateTranslate(self.nextPositions)):
            self.positions = deepcopy(self.nextPositions)
    def checkCompleteRows(self):
        global SCORE
        self.rowCount = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0}
        self.positionsToRemove = []
        self.rowsToRemove = []
        for position in boardPositions:
            if position[1] < 0:
                exit()
            self.rowCount[position[1]] += 1
        for row in self.rowCount:
            if self.rowCount[row] > 9:
                self.rowsToRemove.append(row)
                for pos in boardPositions:
                    if pos[1] == row:
                        self.positionsToRemove.append(pos)
        for position in self.positionsToRemove:
            boardPositions.remove(position)
            fallingBlocks.append(fallingBlock(position[0]*BLOCK_WIDTH + cameraOffset[0], position[1]*BLOCK_WIDTH + cameraOffset[1], random.randint(-5,5)))

        for removedRows in self.rowsToRemove:
            for row in range(removedRows-1, 0, -1):
                for position in boardPositions:
                    if position[1] == row:
                        position[1] += 1

        # Score
        if len(self.rowsToRemove) == 1: SCORE += 40
        elif len(self.rowsToRemove) == 2: SCORE += 100
        elif len(self.rowsToRemove) == 3: SCORE += 300
        elif len(self.rowsToRemove) == 4: SCORE += 1200
def runGame():
    pygame.draw.rect(screen, (40,40,40), (0 + cameraOffset[0], 0 + cameraOffset[1], 25*10, 25*20))
    drawBlocks(boardPositions)
    block.update(leftKey, rightKey)
    drawBoard(10,20)
    drawScore()
    for fallingBlo in fallingBlocks:
        fallingBlo.update()
def runMenu():
    textSurface = largeText.render(str(DIFFICULTY), True, (0,0,0))
    screen.blit(textSurface, (200,500))

    play.update()
play = blockButton(60,400, 20, 3)
activeState = 0
createActiveBlock()
fallingBlocks = []
gameStates = [runMenu,runGame]
while True:
    screen.fill((100,100,100))
    for event in pygame.event.get():
        if activeState == 0:
            play.handleEvent(event)
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                leftKey = True
            if event.key == K_RIGHT:
                rightKey = True
            if event.key == K_UP:
                block.rotate()
            if event.key == K_DOWN:
                block.blockFallSpeed = BLOCK_FALL_SPEED/10
                downKey = True
        if event.type == KEYUP:
            if event.key == K_DOWN:
                block.blockFallSpeed = BLOCK_FALL_SPEED
                downKey = False
            if event.key == K_LEFT: leftKey = False
            if event.key == K_RIGHT: rightKey = False
    gameStates[activeState]()
    pygame.display.flip()
