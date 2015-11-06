import random
import pygame
import numpy as np
import pylab as pl
from random import randint

class DrawHandler:
    def drawWalker(self):
        # Initialize the game engine
        pygame.init()

        # Define the colors we will use in RGB format
        BLACK = (  0,   0,   0)
        WHITE = (255, 255, 255)
        BLUE =  (  0,   0, 255)
        GREEN = (  0, 255,   0)
        YELLOW =   (255,   255,   0)
        RED =   (255,   0,   0)
        ORANGE =   (255,   165,   0)

        # Set the height and width of the screen
        screenHeight = cellCountX
        screenWidth = cellCountY

        cellSize = screenHeight / cellCountX

        size = [int(screenHeight), int(screenWidth)]
        screen = pygame.display.set_mode(size)
        screen.fill(WHITE)

        #Loop until the user clicks the close button.
        clock = pygame.time.Clock()

        #while 1:
        # Make sure game doesn't run at more than 60 frames per second
        mainloop = True
        FPS = 60                           # desired max. framerate in frames per second.
        playtime = 0
        cycletime = 0
        interval = .15 # how long one single images should be displayed in seconds
        picnr = 0

        currentTimeStep = 0

        while mainloop:
            milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
            seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
            playtime += seconds
            cycletime += seconds
            if cycletime > interval:

                if currentTimeStep >= simulationIterations:
                    currentTimeStep = 0
                else:
                    currentTimeStep += 1

                picnr += 1
                if picnr > 5:
                    picnr = 0
                cycletime = 0

                currentColour = BLACK
                walker = Walker()
                for i in timeRange:
                    walker.draw()
                    screen.fill(currentColour,((walker.X, walker.Y), (1, 1)))
                    pygame.display.set_caption("TimeStep %3i:  " % walker.T)
                    pygame.display.flip()

                # This MUST happen after all the other drawing commands.
                # Go ahead and update the screen with what we've drawn.
                pygame.display.flip()

class Walker:
    def __init__(self):
        self.X = int(cellCountX/2)
        self.Y = int(cellCountY/2)
        self.T = 0
    def draw(self):
        self.T += 1
        universe = [[0 for x in range(cellCountX)] for x in range(cellCountY)]

        randChoice = randint(0,3)

        if randChoice == 0:
            if self.X < cellCountX - 1:
                self.X = self.X + 1
        elif randChoice == 1:
            if self.X > 0:
                self.X = self.X - 1
        elif randChoice == 2:
            if self.Y < cellCountY - 1:
                self.Y = self.Y + 1
        elif randChoice == 3:
            if self.Y > 0:
                self.Y = self.Y - 1

        # universe[self.X][self.Y] = 2
        # print "Time Step: " + str(self.T)
        # for universeRow in universe:
        #     print universeRow

timeStart = 0.0
timeEnd = 500
timeStep = 1
timeRange = np.arange(timeStart, timeEnd + timeStart, timeStep)
timeStart = 0
simulationIterations = int(timeStart + timeEnd)
cellCountX = 400
cellCountY = 400

universe = [[0 for x in range(cellCountX)] for x in range(cellCountY)]
universeTimeSeries = [0, universe]

# walker = Walker()

# for i in timeRange:
    # walker.draw()

universeDrawHandler = DrawHandler()
universeDrawHandler.drawWalker()


# universeDrawHanler = DrawHandler()
#universeDrawHanler.drawGenerationUniverse(cellCountX, cellCountY, universeTimeSeries)