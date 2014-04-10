import pygame, sys, math
from pygame import *
import random

pygame.init()
fpsClock = pygame.time.Clock()

width, height = 640, 480

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong - Adam Wells 2014")

blackColor = pygame.Color(0,0,0)
greenColor = pygame.Color(0,255,0)
padPos = 1
compScore = 0
playerScore = 0
fontObj = pygame.font.Font('freesansbold.ttf', 32)

class ball(object):
    radius = 15
    def __init__(self, xPos, yPos, xVel, yVel):
        self.xPos = xPos
        self.yPos = yPos
        self.xVel = xVel
        self.yVel = yVel

    def draw(self):
        pygame.draw.circle(window, greenColor, (self.xPos, self.yPos), self.radius, 0)

    def update(self):
        self.collisionCheck()
        self.xPos += int(self.xVel)
        self.yPos += int(self.yVel)

    def collisionCheck(self):
        global playerScore
        global compScore
        global the_paddle
        if (self.xPos <= self.radius):
            playerScore += 1
            self.reset()
        if (self.xPos >= width - self.radius):
            compScore += 1
            self.reset()
        if (self.yPos <= self.radius) or (self.yPos >= height - self.radius):
            self.yVel = self.yVel * -1

    def reset(self):
        self.xPos = width/2
        self.yPos = height/2
        self.xVel = random.uniform(5,15) * random.randrange(-1,2,2)
        self.yVel = math.sqrt(400 - self.xVel ** 2) * random.randrange(-1,2,2)

class paddle(object):
    direction = 0

    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos

    def draw(self):
        pygame.draw.rect(window, greenColor, (self.xPos, self.yPos, 10, 75))

    def update(self):
        self.yPos = self.yPos + self.direction

def paddleCollision(ball, paddle):
    if (ball.xPos >= paddle.xPos - 15 and ball.xPos < paddle.xPos and  ball.yPos >= paddle.yPos and ball.yPos <= paddle.yPos + 75):
        ball.xVel = ball.xVel * -1
    if (ball.xPos <= paddle.xPos + 25 and ball.xPos > paddle.xPos and ball.yPos >= paddle.yPos and ball.yPos <= paddle.yPos + 75):
        ball.xVel = ball.xVel * -1
        
def artificialInt(ball, paddle):
    if ball.yPos - (paddle.yPos + 75/2) > 10:
        paddle.direction = 4
    elif ball.yPos - (paddle.yPos + 75/2) < -10:
        paddle.direction = -4
    else:
        paddle.direction = 0
    
the_ball = ball(16, 16, 5, 5)
the_ball.reset()
the_paddle = paddle(width - 30, height/2)
comp_paddle = paddle (20, height/2)

while True:
    window.fill(blackColor)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                the_paddle.direction = 10
            if event.key == K_UP:
                the_paddle.direction = -10
    
        elif event.type == KEYUP:
            the_paddle.direction = 0
    
    score = '%s' % playerScore
    opponent = '%s' % compScore

    msgSurfaceObj1 = fontObj.render(score, 1, greenColor)
    msgSurfaceObj2 = fontObj.render(opponent, 1, greenColor)
    msgRectObj1 = msgSurfaceObj1.get_rect()
    msgRectObj2 = msgSurfaceObj2.get_rect()
    msgRectObj1.topleft = (width - 60, 30)
    msgRectObj2.topleft = (40, 30)
    window.blit(msgSurfaceObj1, msgRectObj1)
    window.blit(msgSurfaceObj2, msgRectObj2)

    the_ball.update()
    the_ball.draw()

    the_paddle.update()
    the_paddle.draw()

    artificialInt(the_ball, comp_paddle)
    comp_paddle.update()
    comp_paddle.draw()
    
    paddleCollision(the_ball, the_paddle)
    paddleCollision(the_ball, comp_paddle)

    pygame.display.update()
    fpsClock.tick(30)
