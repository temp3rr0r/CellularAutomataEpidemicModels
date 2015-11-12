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
        mouseX = 0
        mouseY = 0
        mousePoint = PVector(0, 0)  # Point of mouse vector

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
                walker = Mover()
                for i in timeRange:
                    #walker.walk()
                    #walker.walkStep()
                    #walker.walkStepRight()
                    #walker.walkDistribution()
                    #walker.walkPerlinNoise()
                    walker.walkVector()

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
                    pygame.draw.circle(screen, BLUE, (int(walker.Location.X), int(walker.Location.Y)), circleRadius, 0)
                    pygame.draw.circle(screen, BLACK, (int(walker.Location.X), int(walker.Location.Y)), circleRadius, circleThickness)

                    pygame.display.set_caption("TimeStep %3i:  " % walker.T)

                    event = pygame.event.poll()
                    if event.type == pygame.QUIT:
                        running = 0
                    elif event.type == pygame.MOUSEMOTION:
                        mouseX, mouseY = event.pos

                    mousePoint = PVector(mouseX, mouseY)
                    tempMousePoint = PVector(mouseX, mouseY)
                    tempMousePoint.subtract(walker.Location)

                    label4 = myfont.render("Magnitude from mouse: " + str(tempMousePoint.magnitude()), 1, RED)
                    screen.blit(label4, (10, 35)) # Draw the text

                    center = PVector(cellCountX / 2, cellCountY / 2)
                    center.subtract(walker.Location)
                    label = myfont.render("Magnitude from Center: " + str(center.magnitude()), 1, RED)
                    label2 = myfont.render("Magnitude from 0,0: " + str(walker.Location.magnitude()), 1, RED)
                    label3 = myfont.render("Magnitude of Velocity: " + str(walker.Velocity.magnitude()), 1, RED)
                    screen.blit(label, (10, 5)) # Draw the text
                    screen.blit(label2, (10, 15)) # Draw the text
                    screen.blit(label3, (10, 25)) # Draw the text

                    pygame.time.wait(delayAmount) # Delay the update of the walker

                    pygame.display.flip()

                # This MUST happen after all the other drawing commands.
                # Go ahead and update the screen with what we've drawn.
                pygame.display.flip()

class PVector:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
    def add(self, inputVector):
        self.X += inputVector.X
        self.Y += inputVector.Y
    def subtract(self, inputVector):
        self.X -= inputVector.X
        self.Y -= inputVector.Y
    def multiply(self, inputNumber):
        self.X *= inputNumber
        self.Y *= inputNumber
    def divide(self, inputNumber):
        self.X /= inputNumber
        self.Y /= inputNumber
    def random2D(self):
        self.X = random.random()
        self.Y = random.random()
    def magnitude(self):
        return np.sqrt(self.X * self.X + self.Y * self.Y)
    def limit(self, max):
        if self.magnitude() > max:
            self.normalize()
            self.multiply(max)
    def normalize(self):
        m = self.magnitude()
        if (m != 0):
            self.divide(m)

class Mover:
    def __init__(self):
        self.Location = PVector(random.randint(0, cellCountX), random.randint(0, cellCountY))
        self.Velocity = PVector(random.uniform(-2, 2) * 4, random.uniform(-2, 2) * 4)
        self.Acceleration = PVector(-0.01, 0.1)
        self.TopSpeed = 50
        self.T = 0

    def update(self):
        self.Location.add(self.Velocity)

    def invertEdges(self):
        if self.Location.X <= 0 or self.Location.X > cellCountX - 1:
            self.Velocity.X *= -1
        if self.Location.Y <= 0 or self.Location.Y > cellCountY - 1:
            self.Velocity.Y *= -1

    def wrapEdges(self):
        if self.Location.X <= 0:
            self.Location.X = cellCountX
        if self.Location.X > cellCountX - 1:
            self.Location.X = 0
        if self.Location.Y <= 0:
            self.Location.Y = cellCountY
        if self.Location.Y > cellCountY - 1:
            self.Location.Y = 0

    def checkEdges(self):
        #self.invertEdges()
        self.wrapEdges()

    def walkVector(self):
        self.T += 1

        self.checkEdges()

        self.Acceleration.random2D()
        accelerationFactor = random.uniform(-5, 5)
        self.Acceleration.multiply(accelerationFactor)

        self.Velocity.add(self.Acceleration)
        self.Velocity.limit(self.TopSpeed)
        self.Location.add(self.Velocity)

    def walkAcceleratingVector(self):
        self.T += 1

        self.checkEdges()
        self.Velocity.add(self.Acceleration)
        self.Velocity.limit(self.TopSpeed)
        self.Location.add(self.Velocity)

    def walkVectorNormalize(self):
        self.T += 1

        self.checkEdges()

        self.Velocity.normalize()
        self.Velocity.multiply(10)

        self.update()

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