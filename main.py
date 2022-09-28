import os
import time
import keyboard
import random
from pygame import mixer

class Canvas:
    """Docstring for Canvas"""

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, EMPTY=" "):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.EMPTY = EMPTY
        self.initialField = [[self.EMPTY for i in range(SCREEN_WIDTH)] for i in range(SCREEN_HEIGHT)]
        self.field = self.deepCopyInitialField()
        mixer.init()
        mixer.music.load('jojo.mp3')
        mixer.music.play()


    def deepCopyInitialField(self):
        return [[i for i in j] for j in self.initialField]

    def getRandomPosition(self):
        return (random.randint(0, self.SCREEN_WIDTH), random.randint(0, self.SCREEN_HEIGHT))

    def draw(self):
        os.system('cls')

        s = ""
        for i in self.field:
            s += " ".join(i) + "\n"
        print(s)

        self.field = self.deepCopyInitialField()

    def normX(self, x):
        return x % self.SCREEN_WIDTH

    def normY(self, y):
        return y % self.SCREEN_HEIGHT

    def setPoint(self, x, y, c="o"):
        self.field[y%(self.SCREEN_HEIGHT)][x%(self.SCREEN_WIDTH)] = c

    def circle(self, x, y, r):
        x, y = self.normX(x), self.normY(y)

        for i in range(1):
            pass

    def rect(self, x, y, w, h, c="o"):
        x, y = self.normX(x), self.normY(y)

        for i in range(w):
            for j in range(h):
                self.setPoint(self.normX(i)+x, self.normY(j)+y, c=c)

    def ball(self, x, y, c="o"):
        #pos = getCoordinate((x, y))
        x, y = self.normX(x), self.normY(y)

        self.setPoint(x, y, c)
        self.setPoint(self.normX(x+1), y, c)
        self.setPoint(self.normX(x-1), y, c)

        self.setPoint(x, self.normY(y+1), c)
        self.setPoint(x, self.normY(y-1), c)

        self.setPoint(self.normX(x+1), self.normY(y+1), c)
        self.setPoint(self.normX(x-1), self.normY(y-1), c)

        self.setPoint(self.normX(x+1), self.normY(y-1), c)
        self.setPoint(self.normX(x-1), self.normY(y+1), c)

    def cross(self, x, y, c="x"):
        x, y = self.normX(x), self.normY(y)

        self.setPoint(x, y, c)

        #Plus sign
        self.setPoint(self.normX(x-1), y, c)
        self.setPoint(x, self.normY(y-1), c)
        self.setPoint(self.normX(x+1), y, c)
        self.setPoint(x, self.normY(y+1), c)

        #X
        # self.setPoint(self.normX(x-1), self.normY(y-1), c)
        # self.setPoint(self.normX(x+1), self.normY(y-1), c)
        # self.setPoint(self.normX(x+1), self.normY(y+1), c)
        # self.setPoint(self.normX(x-1), self.normY(y+1), c)




class Player:
    def __init__(self, canvas, x, y, vel=1, skin="ö"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.vel = vel
        self.skin = skin
        self.width = 6
        self.height = 6

    def move(self):
        if keyboard.is_pressed("w"):
            self.y -= self.vel
        if keyboard.is_pressed("d"):
            self.x += self.vel
        if keyboard.is_pressed("s"):
            self.y += self.vel
        if keyboard.is_pressed("a"):
            self.x -= self.vel

        self.x = self.canvas.normX(self.x)
        self.y = self.canvas.normY(self.y)

    def show(self):
        self.canvas.rect(self.x, self.y, self.width, self.height, self.skin)

    def detectCollision(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.canvas.field[self.canvas.normY(self.y + i)][self.canvas.normX(self.x + j)] == Comet.skin:
                    mixer.music.load("death.mp3")
                    mixer.music.play()
                    main()


class Comet:
    skin = "x"

    def __init__(self, canvas, x, y, velX=1, velY=1):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.velX = velX
        self.velY = velY

    def move(self):
        self.x = self.canvas.normX(self.x + self.velX)
        self.y = self.canvas.normY(self.y + self.velY)

    def show(self):
        #self.canvas.rect(self.x, self.y, 3, 3, Comet.skin)
        self.canvas.cross(self.x, self.y, c=Comet.skin)






def main():
    dt = 0.03
    totalTime = 0
    c = Canvas(100, 61)
    p = Player(c, int(c.SCREEN_WIDTH/2), int(c.SCREEN_HEIGHT/2), vel=2, skin="O")
    comets = []
    speedRange = [-4, -3, -2, -1, 1, 2, 3, 4]

    while True:
        if totalTime >= 1:
            #p.skin = "t"
            rX, rY = c.getRandomPosition()
            comets.append(Comet(c, 0, rY, velX=random.choice(speedRange), velY=random.choice(speedRange)))
            totalTime = 0

        for comet in comets:
            comet.move()
            comet.show()


        p.move()
        p.detectCollision()
        p.show()

        c.draw()
        time.sleep(dt)
        totalTime += dt



main()
