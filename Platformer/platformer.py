import random, math, time, json
from pygame.locals import *
import pygame

# Blocks:
#   0 - Air
#   1 - Grass
#   2 - Dirt
#   3 - Plant
#   4 - Spike
#   5 - Player Spawn Point
pygame.init()
clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)

# pygame.mixer.set_num_channels(64)

pygame.display.set_caption("Platformer")
windowSize = (600,400)
screen = pygame.display.set_mode(windowSize, 0, 32)
display = pygame.Surface((300,200))
# World Code
grass_img = pygame.image.load('Game/Images/grass.png')
dirt_img = pygame.image.load('Game/Images/dirt.png')
plantImg = pygame.image.load('Game/Images/plant.png').convert()
spikeImg = pygame.image.load("Game/Images/spike.png").convert()
checkpointUnImg = pygame.image.load("Game/Images/checkpoint_unactive.png").convert()
checkpointAcImg = pygame.image.load("Game/Images/checkpoint_active.png").convert()
plantImg.set_colorkey((255,255,255))
spikeImg.set_colorkey((255,255,255))
checkpointUnImg.set_colorkey((255,255,255))
checkpointAcImg.set_colorkey((255,255,255))

tileIndex = {1:grass_img, 2: dirt_img, 3:plantImg, 4:spikeImg, 6:checkpointUnImg, 7:checkpointAcImg}
solidBlocks = [1,2,4,6]
generateingChunkPadding = (0, 0)
# Player Code
playerRect = pygame.Rect(0,100,5,13)
movingRight = False
movingLeft = False
isFlying = False
canFly = True
boostMax = 300
boostValue = 100

movingRightSwinging = False
movingLeftSwinging = False
movingUpSwinging = False
movingDownSwinging = False
isAccelerating = True

canGrapple = True
isGrappling = False
isSwinging = False
grappleAnimationLength = 0.00
grappleAngle = 0
grappleAngleVel = 0.0
grappleAngleAcc = 0.0

verticleMomentum = 0
playerJumpCount = 0
playerSpawnPoint = None

# Camera Movement Code
scroll = [0,0]
trueScroll = [0,0]
realScroll = [0,0]
# Parralax Effects
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

# Sounds
jumpSound = pygame.mixer.Sound('Game/sounds/jump.wav')
jumpSound.set_volume(0.1)
grassSounds = [pygame.mixer.Sound('Game/sounds/grass_0.wav'), pygame.mixer.Sound('Game/sounds/grass_1.wav')]
for sound in grassSounds:
    sound.set_volume(0.05)
grassSoundTimer = 0
# Music
pygame.mixer.music.load('Game/sounds/music.wav')
# pygame.mixer.music.play(-1)
def drawBar(maxValue, value, pos):
    barLength = int(maxValue * (value/maxValue))
    pygame.draw.rect(screen, (255,0,0), (pos[0],pos[1], barLength, 20))
    pygame.draw.rect(screen, (0,0,0), (pos[0],pos[1], maxValue, 20), 1)
def setSpawn():
    global playerSpawnPoint
    for chunk in game_map:
        for tile in game_map[chunk]:
            if tile[1] == 5:
                playerSpawnPoint = [tile[0][1], tile[0][0]]
                game_map[chunk].remove(tile)
def stopPlayer():
    global movingRight, movingLeft, isFlying, verticleMomentum, playerMovement
    movingLeft = False
    movingRight = False
    isFlying = False
    verticleMomentum = 0
    playerMovement = [0,0]
class Particle():
    def __init__(self, x, y, colours, radius):
        self.x = x + random.random() * 2 * random.choice([-1,1])
        self.y = y + random.random() * 2 * random.choice([-1,1])
        self.width = random.choice([2])
        self.height = random.choice([1])
        self.particleMomentum = 3
        self.colour = random.choice(colours)
        self.radius = radius
    def update(self):
        pygame.draw.circle(screen, self.colour, (int(self.x - scroll[0])*2, int(self.y - scroll[1])*2), self.radius)
        self.y += self.particleMomentum
        self.particleMomentum*=0.7
        if self.radius == 0:
            particleGroup.particleGroup.remove(self)
class ParticleGroup():
    def __init__(self, x, y, amount, deleteTimerMax, colours, radius):
        self.x = x
        self.y = y
        self.amount = 0
        self.particleGroup = []
        self.startTime = time.time()
        self.deleteTimerMax = deleteTimerMax
        self.deleteTimer = self.deleteTimerMax
        for x in range(amount):
            self.particleGroup.append(Particle(self.x, self.y, colours, radius))
    def updateGroup(self):
        if self.particleGroup == []:
            particleGroups.remove(self)
        for particle in self.particleGroup:
            particle.update()
            if self.deleteTimer == 0:
                particle.radius -= 1
                self.deleteTimer = self.deleteTimerMax
        if self.deleteTimer > 0:
            self.deleteTimer -= 1
def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile[0]):
            hit_list.append(tile)
    return hit_list

def checkHittingWall(rect, tiles):
    newRect = rect.copy()
    collisionsTrue = {'bottom':False,'right':False,'left':False}
    for tile in tiles:
        newRect.x -= 1
        if newRect.colliderect(tile[0]):
            collisionsTrue["right"] = True
        newRect = rect.copy()
        newRect.x += 1
        if newRect.colliderect(tile[0]):
            collisionsTrue["left"] = True
        newRect = rect.copy()
        newRect.y += 1
        if newRect.colliderect(tile[0]):
            collisionsTrue["bottom"] = True
        newRect = rect.copy()
    return collisionsTrue
def specialCollisions(hit_list, movement):
    for tile in hit_list:
        if tile[1] == 6:
                chunkX = tile[0][0]//(8*16)
                chunkY = tile[0][1]//(8*16)
                for realTile in game_map[str(chunkX) + ";" + str(chunkY)]:
                    if realTile[0] == [tile[0].x//16, tile[0].y//16]:
                        realTile[1] = 7
                        playerSpawnPoint[1] = realTile[0][0]
                        playerSpawnPoint[0] = realTile[0][1]
def move(rect,movement,tiles):
    global playerJumpCount, verticleMomentum, isFlying, isSwinging
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    specialCollisions(hit_list, movement)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile[0].left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile[0].right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    specialCollisions(hit_list, movement)
    for tile in hit_list:
        if tile[1] == 6:
            chunkX = tile[0][0]//(8*16)
            chunkY = tile[0][1]//(8*16)
            for realTile in game_map[str(chunkX) + ";" + str(chunkY)]:
                if realTile[0] == [tile[0].x//16, tile[0].y//16]:
                    realTile[1] = 7
                    playerSpawnPoint[1] = realTile[0][0]
                    playerSpawnPoint[0] = realTile[0][1]
        if movement[1] > 0:
            if tile[1] == 4:
                resetPlayer()
                resetCamera()
            rect.bottom = tile[0].top
            collision_types['bottom'] = True
            if playerJumpCount > 0:
                playerJumpCount = 0
            if verticleMomentum > 0:
                verticleMomentum = 0
            isFlying = False
        elif movement[1] < 0:
            rect.top = tile[0].bottom
            collision_types['top'] = True
            verticleMomentum = 1
    return rect, collision_types

def loadAnimation(path, frames_durations):
    global animationFrames
    animationName = path.split("/")[-1]
    animationFrameData = []
    n = 0
    for frame in frames_durations:
        animationFrameId = animationName + "_" + str(n)
        img_loc = path + "/" + animationFrameId + ".png"
        animationImage = pygame.image.load(img_loc).convert()
        animationImage.set_colorkey((255,255,255))
        animationFrames[animationFrameId] = animationImage.copy()
        for i in range(frame):
            animationFrameData.append(animationFrameId)
        n += 1
    return animationFrameData
# Load Animations Code
animationFrames = {}
animationDatabase = {}
animationDatabase["idle"] = loadAnimation("Game/player_animations/idle", [7,7,40])
animationDatabase["run"] = loadAnimation("Game/player_animations/run", [7,7])
playerAction = "idle"
playerFrame = 0
playerFlip = False
particleGroups = []
def changeAction(actionVar, frame, newValue):
    if actionVar != newValue:
        actionVar = newValue
        frame = 0
    return actionVar, frame

CHUNK_SIZE = 8
def generateChunk(x,y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0 # nothing
            if tile_type != 0:
                chunk_data.append([[target_x,target_y],tile_type])
    return chunk_data
def resetCamera():
    trueScroll[0] = playerRect.x - 152
    trueScroll[1] = playerRect.y - 106
def resetPlayer():
    global playerRect, verticleMomentum, playerMovement
    playerRect.x = playerSpawnPoint[1] * 16 + 8
    playerRect.y = playerSpawnPoint[0] * 16
    verticleMomentum = 0
    playerMovement = [0,0]
def loadWorldFromFile(path):
    global playerSpawnPoint
    try:
        filePath = path
        file = open(filePath, "r")
        data = file.read().split("\n")
        file.close()

        maxChunksX = int(len(data[0])/8)
        maxChunksY = int(len(data)/8)

        transparentBlocks = ["0", "3", "5"]

        tempWorld = {}
        for chunkNumY in range(0, maxChunksY):
            for chunkNumX in range(0,maxChunksX):
                tempChunkData = []
                for tileX in range(1,9):
                    for tileY in range(1,9):
                        if int(data[tileY - 1 + (8 * chunkNumY)][tileX - 1 + (8 * chunkNumX)]) != 0:
                            if int(data[tileY - 1 + (8 * chunkNumY)][tileX - 1 + (8 * chunkNumX)]) != 5:
                                targetX = chunkNumX * 8 + tileX
                                targetY = chunkNumY * 8 + tileY

                                fileY = tileY - 1 + (8 * chunkNumY)
                                fileX = tileX - 1 + (8 * chunkNumX)
                                try:
                                    if data[fileY + 1][fileX] not in transparentBlocks and data[fileY - 1][fileX] not in transparentBlocks and data[fileY][fileX + 1] not in transparentBlocks and data[fileY][fileX - 1] not in transparentBlocks:
                                        tempChunkData.append([[targetX,targetY], 5])
                                    else:
                                        tempChunkData.append([[targetX,targetY], int(data[tileY - 1 + (8 * chunkNumY)][tileX - 1 + (8 * chunkNumX)])])
                                except:
                                    tempChunkData.append([[targetX,targetY], int(data[tileY - 1 + (8 * chunkNumY)][tileX - 1 + (8 * chunkNumX)])])
                            else:
                                playerSpawnPoint = [tileY - 1 + (8 * chunkNumY),tileX - 1 + (8 * chunkNumX) + 1]
                tempWorld[str(chunkNumX) + ";" + str(chunkNumY)] = tempChunkData
        return tempWorld
    except:
        return game_map
file = open("Game/map.txt", "r")
data = file.read()
file.close()

game_map = eval(data)


setSpawn()
playerRect.x = playerSpawnPoint[1] * 16
playerRect.y = playerSpawnPoint[0] * 16
resetCamera()
while True:
    # Draw Background
    display.fill((146,244,255))
    for backgroundObject in background_objects:
        obj_rect = pygame.Rect(backgroundObject[1][0] - scroll[0] * backgroundObject[0], backgroundObject[1][1] - scroll[1] * backgroundObject[0], backgroundObject[1][2], backgroundObject[1][3])
        pygame.draw.rect(display, (7, 255*backgroundObject[0], 75), obj_rect)
    pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0,160,300,80))
    # Draw World
    tileRects = []
    for y in range(4):
        for x in range(4):
            targetX = x  - 1+ int(round(scroll[0]/(CHUNK_SIZE*16)))
            targetY = y  - 1+ int(round(scroll[1]/(CHUNK_SIZE*16)))
            targetChunk = str(targetX) + ";" + str(targetY)
            # If Target Chunk doesn't exist, generate chunk
            if targetChunk not in game_map:
                game_map[targetChunk] = generateChunk(targetX, targetY)
            for tile in game_map[targetChunk]:
                if tile[1] == 4:
                    display.blit(pygame.transform.rotate(tileIndex[tile[1]], tile[2]*90), (tile[0][0]*16-scroll[0], tile[0][1]*16-scroll[1] + 2))
                    tileRects.append([pygame.Rect(tile[0][0]*16, tile[0][1]*16 + 10, 16, tileIndex[tile[1]].get_rect().size[1]), tile[1]])
                else:
                    display.blit(pygame.transform.rotate(tileIndex[tile[1]], tile[2]*90), (tile[0][0]*16-scroll[0], tile[0][1]*16-scroll[1]))
                    if tile[1] in solidBlocks:
                        tileRects.append([pygame.Rect(tile[0][0]*16, tile[0][1]*16, 16, tileIndex[tile[1]].get_rect().size[1]), tile[1]])
    # Draw Player
    playerFrame += 1
    if playerFrame >= len(animationDatabase[playerAction]):
        playerFrame = 0
    playerImageId = animationDatabase[playerAction][playerFrame]
    playerImage = animationFrames[playerImageId]
    display.blit(pygame.transform.flip(playerImage, playerFlip, False), (playerRect.x - scroll[0], playerRect.y - scroll[1]))
    # Draw Grappling Hook
    if isGrappling:
        hookPosDifference = [hookPos[0] - playerRect.x, hookPos[1] - playerRect[1]]
        pygame.draw.line(display, (0,0,0), (playerRect.x - scroll[0], playerRect.y - scroll[1]),(playerRect.x - scroll[0] + (hookPosDifference[0] * grappleAnimationLength), playerRect.y - scroll[1] + (hookPosDifference[1] * grappleAnimationLength)), 3)
        grappleAnimationLength += 0.1
        if grappleAnimationLength >= 1:
            grappleLength = math.sqrt(hookPosDifference[0]**2 + hookPosDifference[1]**2)
            isGrappling = False
            isSwinging = True
            isAccelerating = True
            grappleAngleAcc = 0
            if hookPosDifference[0] < 0:
                grappleAngle = math.degrees(math.atan((hookPos[1]-playerRect.y)/(hookPos[0]-playerRect.x)))
                grappleAngleVel = playerMovement[1]*0.5
            else:
                grappleAngle = math.degrees(math.atan((playerRect.y-hookPos[1])/(playerRect.x-hookPos[0]))) + 180
                grappleAngleVel = playerMovement[1]*-0.5
            stopPlayer()
    if isSwinging:
        pygame.draw.line(display, (0,0,0), (playerRect.x - scroll[0], playerRect.y - scroll[1]),(int(hookPos[0] - scroll[0]), int(hookPos[1] - scroll[1])), 3)
    # Camera Scroll Code
    realScroll[0] = int((playerRect.x))
    realScroll[1] = int((playerRect.y))
    trueScroll[0] += (playerRect.x - trueScroll[0] - 152)*0.05
    trueScroll[1] += (playerRect.y - trueScroll[1] - 106)*0.05
    # trueScroll[0] += 1.5
    scroll[0] = int(trueScroll[0])
    scroll[1] = int(trueScroll[1])
    if scroll[0] - playerRect.x > 100:
        resetPlayer()
        resetCamera()
    if trueScroll[0] - playerRect.x < -260:
        trueScroll[0] += (playerRect.x - 152 - trueScroll[0])*0.004
    # Player Movement
    playerMovement = [0,0]
    if movingRight == True:
        playerMovement[0] += 2
    if movingLeft == True:
        playerMovement[0] -= 2
    if isFlying and canFly and  boostValue > 5:
        boostValue -= 3
        verticleMomentum -= 0.4
        particleGroups.append(ParticleGroup(playerRect.x + playerRect.w*0.5, playerRect.y + playerRect.h , 5, 1, [(255,0,0),(255,69,0),(255,165,0)], 2))
    runningInto = checkHittingWall(playerRect, tileRects)
    if runningInto["right"] and not(runningInto["bottom"]) and verticleMomentum > 0 and (movingLeft or movingRight) or runningInto["left"] and not(runningInto["bottom"]) and verticleMomentum > 0 and (movingLeft or movingRight):
        verticleMomentum = 1
        playerJumpCount = 0
        particleX = playerRect.x
        isFlying = False
        if not(playerFlip):
            particleX += playerRect.w + 2
        particleGroups.append(ParticleGroup(particleX, playerRect.y, 2, 5, [(194, 175, 138), (163, 154, 137), (135, 134, 131)], 2))
    playerMovement[1] += verticleMomentum
    verticleMomentum += 0.2

    # Max Movement Values
    if verticleMomentum > 5:
        verticleMomentum = 5
    if isFlying:
        if verticleMomentum < -2:
            verticleMomentum = -2

    # Collisions
    playerRect,collisions = move(playerRect, playerMovement, tileRects)

    # Change Player Animations
    if playerMovement[0] > 0:
        playerAction = "run"
        playerFlip = False
    elif playerMovement[0] < 0:
        playerAction = "run"
        playerFlip = True
    else:
        playerAction = "idle"

    # Sound Timers
    if grassSoundTimer > 0:
        grassSoundTimer -= 1
    if collisions['bottom'] == True:
        if playerMovement[0] != 0 and grassSoundTimer == 0:
            grassSoundTimer = 30
            random.choice(grassSounds).play()
    # Key Input
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                movingRight = True
                if isSwinging:
                    movingRightSwinging = True
                    isAccelerating = True
            if event.key == K_LEFT:
                movingLeft = True
                if isSwinging:
                    movingLeftSwinging = True
                    isAccelerating = True
            if event.key == K_UP or event.key == K_SPACE:
                if not isSwinging:
                    if playerJumpCount < 2:
                        jumpSound.play()
                        verticleMomentum = -5
                        playerJumpCount += 1
                    elif canFly:
                        isFlying = True
                else:
                    movingUpSwinging = True
            if event.key == K_DOWN:
                if isSwinging:
                    movingDownSwinging = True

            if event.key == K_r:
                resetPlayer()
                resetCamera()

            if event.key == K_f:
                canFly = not(canFly)

        # Key Up Input
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                movingRight = False
                if isSwinging:
                    movingRightSwinging = False
            if event.key == K_LEFT:
                movingLeft = False
                if isSwinging:
                    movingLeftSwinging = False
            if event.key == K_UP or event.key == K_SPACE:
                if not isSwinging:
                    isFlying = False
                else:
                    movingUpSwinging = False
            if event.key == K_DOWN:
                if isSwinging:
                    movingDownSwinging = False

        # Mouse Button Inout
        if event.type == MOUSEBUTTONDOWN:
            isGrappling = True
            hookPos = [pygame.mouse.get_pos()[0] * 0.5 + scroll[0], pygame.mouse.get_pos()[1] * 0.5 + scroll[1]]
        if event.type == MOUSEBUTTONUP:
            if isSwinging or isGrappling:
                isGrappling = False
                isSwinging = False
                grappleAnimationLength = 0.00
                grappleAngleVel = 0
                if isSwinging:
                    verticleMomentum = (futurePos[1] - playerRect.y) * -5
    screen.blit(pygame.transform.scale(display, windowSize), (0,0))
    for particleGroup in particleGroups:
        particleGroup.updateGroup()
    drawBar(boostMax, boostValue, (25,25))
    pygame.display.flip()
    if boostValue < boostMax:
        boostValue += 1
    clock.tick_busy_loop(65)

