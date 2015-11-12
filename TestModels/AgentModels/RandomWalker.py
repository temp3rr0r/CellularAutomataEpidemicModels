import pygame
import numpy as np
import random
from noise import pnoise1

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
                    #walker.walk()
                    #walker.walkStep()
                    #walker.walkStepRight()
                    #walker.walkDistribution()
                    walker.walkPerlinNoise()

                    screen.fill(WHITE) # Refresh screen

                    # Draw point
                    #screen.fill(currentColour,((walker.X, walker.Y), (1, 1)))

                    # Draw triangle
                    # triangleSide = 10 # pixels
                    # a = [walker.X, walker.Y - (triangleSide /2 )]
                    # b = [walker.X + (triangleSide /2 ), walker.Y + (triangleSide /2 )]
                    # c = [walker.X - (triangleSide /2 ), walker.Y + (triangleSide /2 )]
                    # pygame.draw.polygon(screen, currentColour, [a, b, c])

                    # Draw circle
                    circleRadius = 15
                    circleThickness = 3
                    pygame.draw.circle(screen, BLUE, (walker.X, walker.Y), circleRadius, 0)
                    pygame.draw.circle(screen, BLACK, (walker.X, walker.Y), circleRadius, circleThickness)


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

    def walkPerlinNoise(self):
        self.T += 1

        stepX = int(self.perlinNoiseNumber(self.T, timeEnd) * 7)
        stepY = int(self.perlinNoiseNumber(abs(timeEnd - self.T), timeEnd) * 12)

        newX = self.X + stepX
        newY = self.Y + stepY
        self.updateLocation(newX, newY)


    def walkDistribution(self):
        self.T += 1
        randomFloat = self.getRandomNumber(4)

        stepX = 0
        stepY = 0

        if randomFloat < 0.25:
            stepX = 1
        elif randomFloat < 0.5:
            stepX = -1
        elif randomFloat < 0.75:
            stepY = -1
        else:
            stepY = 1

        newX = self.X + stepX
        newY = self.Y + stepY
        self.updateLocation(newX, newY)

    def updateLocation(self, newX, newY):
        if newX >= 0 and newX < cellCountX - 1:
            self.X = newX
        if newY >= 0 and newY < cellCountY - 1:
            self.Y = newY

    def walkStepRight(self):
        self.T += 1
        randomFloat = random.random()

        stepX = 0
        stepY = 0

        if randomFloat < 0.4:
            stepX = 1
        elif randomFloat < 0.6:
            stepX = -1
        elif randomFloat < 0.8:
            stepY = 1
        else:
            stepY = -1
        newX = self.X + stepX
        newY = self.Y + stepY
        self.updateLocation(newX, newY)

    def updateLocation(self, newX, newY):
        if newX >= 0 and newX < cellCountX - 1:
            self.X = newX
        if newY >= 0 and newY < cellCountY - 1:
            self.Y = newY

    def walkStep(self):
        self.T += 1
        stepX = random.randint(-1,1)
        stepY = random.randint(-1,1)
        newX = self.X + stepX
        newY = self.Y + stepY
        self.updateLocation(newX, newY)

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

    def monteCarlo(self):
        r1 = 0.0
        while(True):
            # Pick a random value.
            r1 = np.random.uniform()
            if np.random.uniform() < r1:
                return r1

    # PERLIN NOISE 1 to -1
    def perlinNoiseNumber(self, timeStep, maxTimeStep, octaves = 10, timeSpan = 300):
        base = 0.5
        x = float(timeStep) * timeSpan / maxTimeStep - 0.5 * timeSpan
        y = pnoise1(x + base, octaves)
        return y

    def getRandomNumber(self, distribution = 0):
        returningRandomNumber = 0.0
        if distribution == 0:
            returningRandomNumber = np.random.uniform() # UNIFORM
        elif distribution == 1:
            returningRandomNumber = np.random.normal(.5, .1) # NORMAL
        elif distribution == 2:
            returningRandomNumber = (np.random.binomial(20, .5, 100) % 10) * 0.1 # BINOMIAL
        elif distribution == 3:
            returningRandomNumber = np.random.poisson(2) * .1 # POISSON
        elif distribution == 4:
            returningRandomNumber = self.monteCarlo() # MONTE CARLO METHOD
        return returningRandomNumber

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