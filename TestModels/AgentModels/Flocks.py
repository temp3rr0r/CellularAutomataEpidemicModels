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

        moverObjectCount = 20
        moverToMouseList = [ MoverToMouse() for i in range(moverObjectCount)]
        flockList = Flock(80)

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

                for i in timeRange:
                    event = pygame.event.poll()
                    if event.type == pygame.QUIT:
                        running = 0
                    elif event.type == pygame.MOUSEMOTION:
                        mouseX, mouseY = event.pos

                    mousePoint = PVector(mouseX, mouseY)

                    screen.fill(WHITE) # Refresh screen

                    flockList.run()
                    # for currentWalker in moverToMouseList:
                    #     mousePointDirection = PVector(mouseX, mouseY)
                    #     mousePointDirection.subtract(currentWalker.Location)
                    #     mousePointDirection.normalize()
                    #     mousePointDirection.multiply(2.5)
                    #
                    #     tempMousePoint = PVector(mouseX, mouseY)
                    #     tempMousePoint.subtract(currentWalker.Location)
                    #
                    #     currentWalker.walkVectorAcceleration(mousePointDirection)

                    for currentBoid in flockList.Boids:

                        # Draw point
                        #screen.fill(currentColour,((walker.X, walker.Y), (1, 1)))

                        # Draw triangle
                        # triangleSide = 8 # pixels
                        # a = [int(currentBoid.Location.X), int(currentBoid.Location.Y) - (triangleSide)]
                        # b = [int(currentBoid.Location.X) + (triangleSide /2 ), int(currentBoid.Location.Y) + (triangleSide /2 )]
                        # c = [int(currentBoid.Location.X) - (triangleSide /2 ), int(currentBoid.Location.Y) + (triangleSide /2 )]
                        # pygame.draw.polygon(screen, BLUE, [a, b, c])
                        # pygame.draw.polygon(screen, BLACK, [a, b, c], 1)
                        # Draw circle
                        circleRadius = 5
                        circleThickness = 1
                        pygame.draw.circle(screen, BLUE, (int(currentBoid.Location.X), int(currentBoid.Location.Y)), circleRadius, 0)
                        pygame.draw.circle(screen, BLACK, (int(currentBoid.Location.X), int(currentBoid.Location.Y)), circleRadius, circleThickness)

                    pygame.display.set_caption("TimeStep %3i:  " % flockList.T)

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
    def setMangitude(self, inputMagnitude):
        self.normalize()
        self.multiply(inputMagnitude)
    def normalize(self):
        m = self.magnitude()
        if (m != 0):
            self.divide(m)
    def getDistance(self, otherLocation):
        return np.sqrt((self.X - otherLocation.X)** 2 + (self.Y - otherLocation.Y)**2)

class Boid:
    def __init__(self, x, y):
        self.Location = PVector(cellCountX / 2, cellCountY / 2)#PVector(x, y)
        self.Velocity = PVector(random.uniform(-2, 2) * 4, random.uniform(-2, 2) * 4)#PVector(0, 0)
        self.Acceleration = PVector(-0.1, 1)#PVector(-0.01, 0.1)#PVector(0, 0)
        self.R = 3#1.0 # For size
        self.MaxForce = 0.2
        self.MaxSpeed = 3#0.1
        self.NeighbourDistance = 1.2

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

    def update(self):
        self.Velocity.add(self.Acceleration)
        self.Velocity.limit(self.MaxSpeed)
        self.Location.add(self.Velocity)
        self.Acceleration.multiply(0.0)

    def flock(self, inputBoids):
        separateVector = self.separate(inputBoids)
        alignVector = self.align(inputBoids)
        cohesionVector = self.cohesion(inputBoids)

        separateVector.multiply(1.5)
        alignVector.multiply(1)
        cohesionVector.multiply(1)

        self.applyForce(separateVector)
        self.applyForce(alignVector)
        self.applyForce(cohesionVector)
        self.checkEdges()
        self.update()

    def align(self, inputBoids):
        sum = PVector(0, 0)

        for currentBoid in inputBoids:
            sum.add(currentBoid.Velocity)

        sum.divide(len(inputBoids))
        sum.setMangitude(self.MaxSpeed)

        steer = PVector(sum.X, sum.Y)
        steer.subtract(self.Velocity)
        steer.limit(self.MaxForce)

        return steer

    def separate(self, inputBoids):
        desiredSeparation = self.R * 2
        sum = PVector(0, 0)
        count = 0
        for currentBoid in inputBoids:
            distance = self.Location.getDistance(currentBoid.Location)
            if distance > 0 and distance < desiredSeparation:
                diff = PVector(self.Location.X, self.Location.Y)
                diff.subtract(currentBoid.Location)
                diff.normalize()
                diff.divide(distance)
                sum.add(diff)
                count += 1
        if count > 0:
            sum.divide(count)
            sum.normalize()
            sum.multiply(self.MaxSpeed)
            steer = PVector(sum.X, sum.Y)
            steer.subtract(self.Velocity)
            steer.limit(self.MaxForce)
            return steer
        else:
            return PVector(0, 0)

    def cohesion(self, inputBoids):
        sum = PVector(0, 0)
        count = 0
        for currentBoid in inputBoids:
            distance = self.Location.getDistance(currentBoid.Location)
            if (distance > 0 and distance < self.NeighbourDistance):
                sum.add(currentBoid.Location)
                count += 1

        if count > 0:
            sum.divide(count)
            return self.seek(sum)
        else:
            return PVector(0, 0)

    def seek(self, targetVector):
        desired = targetVector
        desired.subtract(self.Location)
        desired.normalize()
        desired.multiply(self.MaxSpeed)

        steer = desired
        desired.subtract(self.Velocity)
        return desired

    def applyForce(self, inputForce):
        self.Acceleration.add(inputForce)

class Flock:
    def __init__(self, inputBoidCount):
        self.BoidCount = inputBoidCount
        self.Boids = [ Boid(10, 10) for i in range(self.BoidCount)]
        self.T = 0
    def run(self):
        self.T += 1
        for currentBoid in self.Boids:
            currentBoid.flock(self.Boids)

class MoverToMouse:
    def __init__(self):
        self.Location = PVector(random.randint(0, cellCountX), random.randint(0, cellCountY))
        self.Velocity = PVector(random.uniform(-2, 2) * 4, random.uniform(-2, 2) * 4)
        self.Acceleration = PVector(-0.01, 0.1)
        self.TopSpeed = 20
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

    def walkVectorAcceleration(self, acceleration):
        self.T += 1

        self.Acceleration = acceleration
        self.checkEdges()

        self.Velocity.add(self.Acceleration)
        self.Velocity.limit(self.TopSpeed)
        self.Location.add(self.Velocity)

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