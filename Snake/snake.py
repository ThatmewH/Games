import pygame, random, time, math
from pygame.locals import *

displayHeight = 800
displayWidth = 800
DISPLAY = pygame.display.set_mode((displayWidth,displayHeight))

class Apple:
    def __init__(self):
        self.radius = 10
        self.colour = (255,0,0)
        self.x = random.randint(0, displayWidth)
        self.y = random.randint(0, displayHeight)
    def update(self, s):
        pygame.draw.circle(DISPLAY, self.colour, (self.x,self.y), self.radius)
        distance = math.sqrt(abs((s.bodies[0][0] - self.x)**2 + (s.bodies[0][1] - self.y)**2))
        if distance < 30:
            for x in range(0,25):
                s.bodies[len(s.bodies)] = s.bodies[len(s.bodies) - 1]
            self.x = random.randint(0, displayWidth)
            self.y = random.randint(0, displayHeight)
class Snake:
    def __init__(self):
        self.radius = 20
        self.bodies = {0:[30,0]}
        self.direction = "Right"
        self.distance = 4
        self.turnedPosition = [0,-100]
        self.waitDistance = 1000
        self.score = 0
        self.highscore = 0
        self.colour = [0,0,0]
    def update(self):
        for body in self.bodies:
            if self.colour[1] > 0:
                self.colour[1] -= 1
            pygame.draw.circle(DISPLAY, self.colour, (self.bodies[body][0], self.bodies[body][1]), self.radius)
        for x in range(len(self.bodies) - 1, -1, -1):
            if x != 0:
                self.bodies[x] = self.bodies[x - 1]
        if self.direction == "Up":
            self.bodies[0] = [self.bodies[0][0], self.bodies[0][1] - self.distance]
        elif self.direction == "Down":
            self.bodies[0] = [self.bodies[0][0], self.bodies[0][1] + self.distance]
        elif self.direction == "Right":
            self.bodies[0] = [self.bodies[0][0] + self.distance, self.bodies[0][1]]
        elif self.direction == "Left":
            self.bodies[0] = [self.bodies[0][0] - self.distance, self.bodies[0][1]]

        if self.bodies[0][0] < 0:
            self.bodies[0][0] = displayWidth
        elif self.bodies[0][0] > displayWidth:
            self.bodies[0][0] = 0
        if self.bodies[0][1] < 0:
            self.bodies[0][1] = displayHeight
        elif self.bodies[0][1] > displayHeight:
            self.bodies[0][1] = 0

        for body in self.bodies:
            if body > 40:
                distance = math.sqrt(abs((self.bodies[0][0] - self.bodies[body][0])**2 + (self.bodies[0][1] - self.bodies[body][1])**2))
                if distance <= 40:
                    self.newBodies = {}
                    for x in range(0, len(self.bodies) - 5):
                        self.newBodies[x] = self.bodies[x]
                    self.bodies = self.newBodies
                    break
        self.score = len(self.bodies) - 1
        if self.score > self.highscore:
            self.highscore = self.score
def main():
    pygame.init()
    s = Snake()
    a = Apple()
    font = pygame.font.Font('freesansbold.ttf', 32)
    while True:
        DISPLAY.fill((255,255,255))

        keystate = pygame.key.get_pressed()
        if keystate[K_DOWN]:
            s.direction = "Down"
        elif keystate[K_UP]:
            s.direction = "Up"
        elif keystate[K_RIGHT]:
            s.direction = "Right"
        elif keystate[K_LEFT]:
            s.direction = "Left"

        for event in pygame.event.get():
            if event.type==MOUSEBUTTONDOWN:
                if event.button == 1:
                    for x in range(0,25):
                        s.bodies[len(s.bodies)] = s.bodies[len(s.bodies) - 1]
            if event.type==QUIT:
                pygame.quit()
                exit()
        text = font.render("Score: " + str(s.score), True, (0,0,0), (255,255,255))
        text2 = font.render("HighScore: " + str(s.highscore), True, (0,0,0), (255,255,255))
        DISPLAY.blit(text, (int(displayWidth*0.78), 0))
        DISPLAY.blit(text2, (40, 0))
        s.update()
        a.update(s)
        pygame.display.flip()
        pygame.time.wait(5)
main()
