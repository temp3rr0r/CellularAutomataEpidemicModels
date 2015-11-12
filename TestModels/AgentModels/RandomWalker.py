import pygame
import numpy as np
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

        size = [int(screenHeight), int(screenWidth)]
        screen = pygame.display.set_mode(size)
        screen.fill(WHITE)

        #Loop until the user clicks the close button.
        clock = pygame.time.Clock()


        myfont = pygame.font.SysFont("monospace", 15)


        #while 1:
        # Make sure game doesn't run at more than 60 frames per second
        mainloop = True
        maxFPS = 60 # desired max. framerate in frames per second.
        cycletime = 0
        interval = .15#.15 # how long one single images should be displayed in seconds
        delayAmount = 50
        currentTimeStep = 0

        while mainloop:

            milliseconds = clock.tick(maxFPS)  # milliseconds passed since last frame
            seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
            cycletime += seconds
            if cycletime > interval:
                cycletime = 0
                if currentTimeStep >= simulationIterations:
                    currentTimeStep = 0
                else:
                    currentTimeStep += 1


                currentColour = BLACK
                walker = Walker()
                for i in timeRange:
                    walker.walk()
                    screen.fill(currentColour,((walker.X, walker.Y), (1, 1)))
                    pygame.display.set_caption("TimeStep %3i:  " % walker.T)
                    pygame.display.flip()

                    #label = myfont.render(str(milliseconds) + " ms", 1, RED)
                    #screen.blit(label, (20, 20)) # Draw the text
                    pygame.time.wait(delayAmount) # Delay the update of the walker

                # This MUST happen after all the other drawing commands.
                # Go ahead and update the screen with what we've drawn.
                pygame.display.flip()

class Walker:
    def __init__(self):
        self.X = int(cellCountX/2)
        self.Y = int(cellCountY/2)
        self.T = 0
        #self.Universe = [[0 for x in range(cellCountX)] for x in range(cellCountY)]
    def walkStep(self):
        self.T += 1
        stepX = randint(-1,1)
        stepY = randint(-1,1)

        newX = self.X + stepX
        newY = self.Y + stepY

        if newX >= 0 and newX < cellCountX - 1:
            self.X = newX
        if newY >= 0 and newY < cellCountY - 1:
            self.Y = newY

    def walk(self):
        self.T += 1
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

timeStart = 0.0
timeEnd = 5000
timeStep = 1
timeRange = np.arange(timeStart, timeEnd + timeStart, timeStep)
timeStart = 0
simulationIterations = int(timeStart + timeEnd)
cellCountX = 400
cellCountY = 400

universeDrawHandler = DrawHandler()
universeDrawHandler.drawWalker()