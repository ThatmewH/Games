import pygame, time
from pygame.locals import *

def removeSpawnTile():
    global game_map
    for chunk in game_map:
        for tile in game_map[chunk]:
            if tile[1] == 5:
                game_map[chunk].remove(tile)

pygame.init()

CHUNK_SIZE = 8
BLOCK_SIZE = 16

movingUp = False
movingDown = False
movingLeft = False
movingRight = False
scrollTime = time.time()
scrollTimeMax = 0.05

placeBlocks = False
deleteBlocks = False
blockPlacedTime = time.time()
blockPlacedTimeMax = 0.01

file = open("Game/map.txt", "r")
data = file.read()
file.close()

game_map = eval(data)
screen = pygame.display.set_mode((640,416), 0, 32)
grass_img = pygame.image.load('Game/Images/grass.png')
dirt_img = pygame.image.load('Game/Images/dirt.png')
spawnImg = pygame.image.load('Game/player_animations/idle/idle_0.png')
plantImg = pygame.image.load('Game/Images/plant.png').convert()
spikeImg = pygame.image.load("Game/Images/spike.png").convert()
checkpointImg = pygame.image.load("Game/Images/checkpoint_unactive.png").convert()
plantImg.set_colorkey((255,255,255))
spikeImg.set_colorkey((255,255,255))
checkpointImg.set_colorkey((255,255,255))

tileIndex = {1:grass_img, 2: dirt_img, 3:plantImg, 4:spikeImg, 5:spawnImg, 6: checkpointImg}

currentTile = 1
currentTileRotation = 0

cursorImage = tileIndex[currentTile].copy().convert()
cursorImage.set_alpha(128)
scroll = [0,0]
while True:
    screen.fill((255,255,255))
    # Scroll Code
    if movingRight and time.time() - scrollTime > scrollTimeMax:
        scroll[0] += 16
        scrollTime = time.time()
    if movingLeft and time.time() - scrollTime > scrollTimeMax:
        scroll[0] -= 16
        scrollTime = time.time()
    if movingUp and time.time() - scrollTime > scrollTimeMax:
        scroll[1] -= 16
        scrollTime = time.time()
    if movingDown and time.time() - scrollTime > scrollTimeMax:
        scroll[1] += 16
        scrollTime = time.time()
    for event in pygame.event.get():
        if placeBlocks or deleteBlocks:
            targetChunkX = ((pygame.mouse.get_pos()[0] + scroll[0])//BLOCK_SIZE) // 8
            targetChunkY = ((pygame.mouse.get_pos()[1] + scroll[1])//BLOCK_SIZE) // 8
            blockX = (pygame.mouse.get_pos()[0] + scroll[0])//BLOCK_SIZE + 1
            blockY = (pygame.mouse.get_pos()[1] + scroll[1])//BLOCK_SIZE + 1
            if placeBlocks and time.time() - blockPlacedTime > blockPlacedTimeMax:
                try:
                # Check if block already exists, if it does remove it before appending another block
                    for tile in game_map[str(targetChunkX) + ";" + str(targetChunkY)]:
                        if tile[0] == [blockX, blockY]:
                            tileType = tile[1]
                            tileRotation = tile[2]
                            game_map[str(targetChunkX) + ";" + str(targetChunkY)].remove([[blockX, blockY], tileType, tileRotation])
                    # if currentTile == 5:
                    #     removeSpawnTile()
                    game_map[str(targetChunkX) + ";" + str(targetChunkY)].append([[blockX, blockY], currentTile, currentTileRotation])
                    blockPlacedTime = time.time()
                except:
                    if currentTile == 5:
                        removeSpawnTile()
                    game_map[str(targetChunkX) + ";" + str(targetChunkY)] = [[[blockX, blockY], currentTile, currentTileRotation]]
                    blockPlacedTime = time.time()
            if deleteBlocks:
                try:
                    for tile in game_map[str(targetChunkX) + ";" + str(targetChunkY)]:
                        if tile[0] == [blockX, blockY]:
                            tileType = tile[1]
                            tileRotation = tile[2]
                            game_map[str(targetChunkX) + ";" + str(targetChunkY)].remove([[blockX, blockY], tileType, tileRotation])
                except:
                    pass

        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_p:
                currentTile += 1
                if currentTile > len(tileIndex):
                    currentTile = 1
                cursorImage = tileIndex[currentTile].copy().convert()
                cursorImage.set_alpha(128)
            if event.key == K_o:
                currentTile -= 1
                if currentTile < 1:
                    currentTile = len(tileIndex)
                cursorImage = tileIndex[currentTile].copy().convert()
                cursorImage.set_alpha(128)

            if event.key == K_RIGHT:
                movingRight = True
            if event.key == K_LEFT:
                movingLeft = True
            if event.key == K_UP:
                movingUp = True
            if event.key == K_DOWN:
                movingDown = True

            if event.key == K_s:
                file = open("Game\map.txt", "w")
                file.write(str(game_map))
                file.close()
            if event.key == K_n:
                game_map = {}
                scroll = [0,0]
            if event.key == K_r:
                currentTileRotation -= 1
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                movingRight = False
            if event.key == K_LEFT:
                movingLeft = False
            if event.key == K_UP:
                movingUp = False
            if event.key == K_DOWN:
                movingDown = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                placeBlocks = True
            if event.button == 3:
                deleteBlocks = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                placeBlocks = False
            if event.button == 3:
                deleteBlocks = False
    for chunkX in range(scroll[0]//(8*16), (scroll[0]//(8*16)) + 6):
        for chunkY in range(scroll[1]//(8*16), (scroll[1]//(8*16)) + 5):
            try:
                for tile in game_map[str(chunkX) + ";" + str(chunkY)]:
                    screen.blit(pygame.transform.rotate(tileIndex[tile[1]],tile[2]*90), ((tile[0][0]-1) * BLOCK_SIZE - scroll[0], (tile[0][1]-1) * BLOCK_SIZE - scroll[1]))
            except:
                pass
    screen.blit(pygame.transform.rotate(cursorImage, currentTileRotation*90), (pygame.mouse.get_pos()[0]//16 * BLOCK_SIZE, pygame.mouse.get_pos()[1]//16 * BLOCK_SIZE))
    pygame.display.flip()
