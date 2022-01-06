from functions import *

clock = pygame.time.Clock()

while True:
    screen.fill((163, 227, 215))
    window[currentWindow](screen, pygame.mouse.get_pos())
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                handleMouseDown(pygame.mouse.get_pos())
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                handleMouseUp(pygame.mouse.get_pos())
        if event.type == KEYDOWN:
            if event.key == K_n:
                pass
    clock.tick(60)
    pygame.display.flip()
