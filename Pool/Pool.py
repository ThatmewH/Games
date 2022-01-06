import pygame, random, time, math
from pygame.locals import *
displayHeight = 500
displayWidth = 1000
DISPLAY = pygame.display.set_mode((displayWidth,displayHeight),0,32)
balls = []
holes = []
gravity = 0
colours = ["red", "yellow", "blue","green", "orange", "purple", "pink", "brown"]
def generateBalls():
    origin = displayWidth*0.25,displayHeight*0.3
    for x in range(0,5):
        balls.append(Ball(origin[0], origin[1] + (x * 31),color=(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
    for x in range(0,4):
        balls.append(Ball(origin[0]+30, origin[1] + 15 + (x * 31),color=(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
    for x in range(0,3):
        balls.append(Ball(origin[0]+60, origin[1] + 30 + (x * 31),color=(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
    for x in range(0,2):
        balls.append(Ball(origin[0]+90, origin[1] + 45 + (x * 31),color=(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
    for x in range(0,1):
        balls.append(Ball(origin[0]+120, origin[1] + 60 + (x * 31),color=(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
    balls.append(Ball(displayWidth*0.8, displayHeight*0.5, color=(255, 255, 255), whiteBall=True))
    for ball in balls:
        ball.active = True
        ball.initiate = False
def mouseOverlappingBalls():
    for ball in balls:
        if distance((ball.x,ball.y), pygame.mouse.get_pos()) < ball.width:
            return (ball, True)
def mouseBallDistance(ballPos):
    ballxD = ballPos[0] - pygame.mouse.get_pos()[0]
    ballyD = ballPos[1] - pygame.mouse.get_pos()[1]
    return ballxD, ballyD
def distance(pos1, pos2):
    differenceX = pos1[0] - pos2[0]
    differenceY = pos1[1] - pos2[1]
    difference = math.sqrt(differenceX**2 + differenceY**2)
    return difference
class Hole():
    def __init__(self, x=0, y=0, width=30):
        self.x = x
        self.y = y
        self.colour = (0,0,0)
        self.width = width
    def draw(self):
        pygame.draw.circle(DISPLAY, self.colour, (int(self.x),int(self.y)), self.width)
    def checkCollide(self):
        for ball in balls:
            if distance((self.x, self.y), (ball.x, ball.y)) <= self.width and ball != self:
                ball.shrink = True
holes.append(Hole(width=40))
holes.append(Hole(displayWidth*0.5))
holes.append(Hole(displayWidth, width=40))
holes.append(Hole(0,displayHeight, width=40))
holes.append(Hole(displayWidth*0.5, displayHeight))
holes.append(Hole(displayWidth, displayHeight, width=40))
class Ball():
    def __init__(self, x=0, y=0, color=(0,0,255), whiteBall=False):
        if x == 0:
            self.x = pygame.mouse.get_pos()[0]
        else:
            self.x = x
        if y == 0:
            self.y = pygame.mouse.get_pos()[1]
        else:
            self.y = y
        self.whiteBall = whiteBall
        self.width = 15
        self.friction = 0.8
        self.dy = 0
        self.dx = 0
        self.colour = color
        self.active = False
        self.initiate = True
        self.followMouse = False
        self.shrink = False
        self.mass = self.width
    def draw(self):
        if self.shrink:
            if self.width == 1 and self.whiteBall:
                self.shrink = False
                self.width = 15
                self.x = displayWidth*0.8
                self.y = displayHeight*0.5
                self.dx = 0
                self.dy = 0
            else:
                self.width -= 2
        if self.dx < -15:
            self.dx = -15
        elif self.dx > 15:
            self.dx = 15
        if self.dy < -15:
            self.dy = -15
        elif self.dy > 15:
            self.dy = 15
        try:
            # pygame.draw.rect(DISPLAY, self.colour, pygame.Rect(int(self.x),int(self.y),self.width,self.width))
            pygame.draw.circle(DISPLAY, self.colour, (int(self.x),int(self.y)), self.width)
        except:
            pass
        if self.followMouse:
            self.x = pygame.mouse.get_pos()[0]
            self.y = pygame.mouse.get_pos()[1]
        elif self.active:
            if self.y + int(self.width) > displayHeight:
                self.dy *= -1
                self.dy *= self.friction
                self.dx *= 0.92
                self.y = displayHeight - self.width
                # self.dy += 2
            else:
                self.y += self.dy
                self.x += self.dx
                self.dy += gravity
            # if self.dy < 1 and self.dy > 0 and self.y + self.width == displayHeight and self.dx < 0.1 and self.dx > -0.1:
            #     self.active = False
            if self.x + self.width > displayWidth:
                self.dx *= -1
                self.x = displayWidth - self.width
            elif self.x - self.width < 0:
                self.dx *= -1
                self.x = self.width
            if self.y - self.width <= 0:
                self.y = self.width
                self.dy *= -1
        elif self.initiate:
            distanceX = self.x - pygame.mouse.get_pos()[0]
            distanceY = self.y - pygame.mouse.get_pos()[1]
            pygame.draw.line(DISPLAY, (255,0,0), (self.x,self.y), (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]))
            pygame.draw.line(DISPLAY, (0,0,0), (self.x,self.y), (pygame.mouse.get_pos()[0] + 1.2*(distanceX),pygame.mouse.get_pos()[1] + 1.2*(distanceY)))
        self.dx *= 0.99
        self.dy *= 0.99
    def checkCollide(self):
        for ball in balls:
            if distance((self.x, self.y), (ball.x, ball.y)) <= ball.width + self.width and ball != self:
                distanceee = math.sqrt((self.x - ball.x)**2 + (self.y - ball.y)**2)
                if distanceee != 0:
                    overlap = 0.5 * (distanceee - self.width - ball.width)
                    self.x -= overlap * (self.x - ball.x) / distanceee
                    self.y -= overlap * (self.y - ball.y) / distanceee
                    self.dx *= 0.9
                    self.dy *= 0.9
                    ball.x += overlap * (self.x - ball.x) / distanceee
                    ball.y -= overlap * (self.y - ball.y) / distanceee
                    nx = (ball.x - self.x) / distanceee
                    ny = (ball.y - self.y) / distanceee
                else:
                    nx = 0
                    ny = 0
                tx = -ny
                ty = nx

                dpTan1 = self.dx * tx + self.dy * ty
                dpTan2 = ball.dx * tx + ball.dy * ty

                dpNorm1 = self.dx * nx + self.dy * ny
                dpNorm2 = ball.dx * nx + ball.dy * ny

                m1 = (dpNorm1 * (self.mass - ball.mass) + 2.0 * ball.mass * dpNorm2) / (self.mass + ball.mass)
                m2 = (dpNorm2 * (ball.mass - self.mass) + 2.0 * self.mass * dpNorm1) / (self.mass + ball.mass)

                self.dx = tx * dpTan1 + nx * m1
                self.dy = ty * dpTan1 + ny * m1
                ball.dx = tx * dpTan2 + nx * m2
                ball.dy = tx * dpTan2 + ny * m2
def main():
    global gravity
    generateBalls()
    pygame.init()
    DARK_GREEN=(0, 48, 13)
    DISPLAY.fill(DARK_GREEN)
    while True:
        timeBefore = time.time()
        for event in pygame.event.get():
            if event.type==MOUSEBUTTONDOWN:
                # if event.button == 2:
                #     if not mouseOverlappingBalls():
                #         balls.append(Ball())
                #     else:
                #         mouseOverlappingBalls()[0].followMouse = True
                #         mouseOverlappingBalls()[0].dx = 0
                #         mouseOverlappingBalls()[0].dy = 0
                #     if mouseOverlappingBalls():
                #         ball.x = pygame.mouse.get_pos()[0]
                if event.button == 1:
                    if mouseOverlappingBalls():
                        if mouseOverlappingBalls()[0].whiteBall:
                            mouseOverlappingBalls()[0].active = False
                            mouseOverlappingBalls()[0].initiate = True

            if event.type==QUIT:
                pygame.quit()
                exit()
            for ball in balls:
                if event.type==MOUSEBUTTONUP and ball.initiate:
                    ball.initiate = False
                    ball.active = True
                    ball.dx = (mouseBallDistance((ball.x, ball.y))[0]/25)
                    ball.dy = (mouseBallDistance((ball.x, ball.y))[1]/25)
            if event.type==MOUSEBUTTONUP:
                if mouseOverlappingBalls():
                    mouseOverlappingBalls()[0].followMouse = False
        DISPLAY.fill(DARK_GREEN)
        for hole in holes:
            hole.draw()
            hole.checkCollide()
        for ball in balls:
            ball.draw()
            ball.checkCollide()
            if ball.width <= 0:
                balls.remove(ball)
        pygame.display.update()
        timeAfter = time.time()
        delay = timeAfter - timeBefore
        if delay < 0.005:
            pygame.time.wait(8)
        else:
            pass
main()


