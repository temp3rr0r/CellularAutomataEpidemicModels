""" A 2D CA model for SIR without mortality or birth """

import random
import numpy as np
import pylab as pl
import pygame


def get_random_number(distribution):

    returning_random_number = 0.0
    if distribution == 0:
        returning_random_number = np.random.uniform()  # UNIFORM
    elif distribution == 1:
        returning_random_number = np.random.normal(.5, .1)  # NORMAL
    elif distribution == 2:
        returning_random_number = (np.random.binomial(20, .5, 100) % 10) * 0.1  # BINOMIAL
    elif distribution == 3:
        returning_random_number = np.random.poisson(2) * .1  # POISSON
    return returning_random_number


def draw_square(screen, current_colour, current_column, cell_size, current_row):
    pygame.draw.rect(screen, current_colour, [current_column * cell_size, current_row * cell_size, (current_column + 1)
                                              * cell_size, (current_row + 1) * cell_size])


def draw_hexagon(screen, current_colour, current_column, cell_size, current_row):

    min_x = current_column * cell_size
    max_x = (current_column + 1) * cell_size
    min_y = current_row * cell_size
    max_y = (current_row + 1) * cell_size
    quarter_length = (max_y - min_y) / 4

    spacing =  (2 * quarter_length)

    if current_column > 1:
        min_x -= spacing * int(current_column / 2)
        max_x -= spacing * int(current_column / 2)

    if current_column % 2 == 1:
        min_x -= quarter_length
        max_x -= quarter_length
        min_y += spacing
        max_y += spacing

    center = [min_x + 2 * quarter_length, min_y + 2 * quarter_length]
    a = [min_x + quarter_length, min_y]
    b = [min_x + 3 * quarter_length, min_y]
    d = [max_x, min_y + 2 * quarter_length]
    e = [min_x + 3 * quarter_length, max_y]
    f = [min_x + quarter_length, max_y]
    g = [min_x, min_y + 2 * quarter_length]

    pygame.draw.polygon(screen, current_colour, [center, a, b])
    pygame.draw.polygon(screen, current_colour, [center, b, d])
    pygame.draw.polygon(screen, current_colour, [center, d, e])
    pygame.draw.polygon(screen, current_colour, [center, e, f])
    pygame.draw.polygon(screen, current_colour, [center, f, g])
    pygame.draw.polygon(screen, current_colour, [center, g, a])


def draw_generation_universe(cell_count_x, cell_count_y, universe_time_series):

    pygame.init()  # Initialize the game engine

    # Define the colors we will use in RGB format
    BLACK = (0,   0,   0)
    WHITE = (255, 255, 255)
    BLUE = (0,   0, 255)
    GREEN = (0, 255,   0)
    YELLOW = (255,   255,   0)
    RED = (255,   0,   0)
    ORANGE = (255,   165,   0)

    # Set the height and width of the screen
    screen_height = 800
    screen_width = 800

    cell_size = screen_height / cell_count_x
    if hexagon_layout:
        screen_height *= 0.85
        screen_width *= 1.04

    size = [int(screen_height), int(screen_width)]
    screen = pygame.display.set_mode(size)
    screen.fill(WHITE)

    clock = pygame.time.Clock()  # Loop until the user clicks the close button.

    #while 1:
    # Make sure game doesn't run at more than 60 frames per second
    mainloop = True
    FPS = 60  # desired max. framerate in frames per second.
    playtime = 0
    cycle_time = 0
    interval = .15  #.15 # how long one single images should be displayed in seconds
    picnr = 0

    #for currentStep in range(simulationIterations):
    current_time_step = 0

    while mainloop:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
        playtime += seconds
        cycle_time += seconds
        if cycle_time > interval:

            if current_time_step >= simulation_iterations:
                current_time_step = 0
            else:
                current_time_step += 1
            #pygame.time.delay(3000)
            pygame.display.set_caption("TimeStep %3i:  " % current_time_step)

            picnr += 1
            if picnr > 5:
                picnr = 0
            cycle_time = 0

            current_colour = BLACK
            for current_row in range(cell_count_y):  # Draw a solid rectangle
                for current_column in range (cell_count_x):
                    # rect(Surface, color, Rect, width=0) -> Rect
                    if 0 < current_time_step < simulation_iterations:
                        if universe_time_series[current_time_step][current_row][current_column] == '0':
                            current_colour = BLUE
                        if universe_time_series[current_time_step][current_row][current_column] == '1':
                            current_colour = YELLOW
                        if universe_time_series[current_time_step][current_row][current_column] == '2':
                            current_colour = RED
                        if universe_time_series[current_time_step][current_row][current_column] == '3':
                            current_colour = GREEN

                        if hexagon_layout:
                            draw_hexagon(screen, current_colour, current_column, cell_size, current_row)
                        else:
                            draw_square(screen, current_colour, current_column, cell_size, current_row)

        # This MUST happen after all the other drawing commands.
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        #pygame.time.delay(1)
        #time.sleep(3)


def printGenerationUniverse(current_time_step, cell_count_x, cell_count_y, susceptible_character, exposed_character, infected_character, recoveredCharacter):
    """
    Print the current generation.
    :param current_time_step:
    :param cell_count_x:
    :param cell_count_y:
    :param susceptible_character:
    :param exposed_character:
    :param infected_character:
    :param recoveredCharacter:
    :return:
    """

    print("TimeStep %3i:  " % current_time_step)
    row_label = "  "
    for l in range(cell_count_x):
        row_label += str(l) + " "
    print(row_label)
    for current_row in range(cell_count_y):
        print("%s %s" % (current_row, universeList[current_row].replace('0', susceptible_character + " ").replace('1', exposedCharacter + " ").
                         replace('2', infected_character + " ").replace('3', recoveredCharacter + " ")))


def get_new_state2DHex(self_character, hex_neighbors):
    """
    This method calculates the new state of the cell based on Moore HEX neighborhood.
    :param self_character:
    :param hex_neighbors:
    :return:
    """

    new_state = self_character

    if self_character == '0': # If S and there is an Infected close, be Infected
        if hex_neighbors.count('2') > 0:
            beta_chance = get_random_number(0)
            if beta > beta_chance > 0:
                new_state = '2'
    elif self_character == '2':  # if Infected, calculate the probability to be Recovered
        gamma_chance = get_random_number(0)
        if gamma > gamma_chance > 0:
            new_state = '3'

    return new_state


def get_new_state2D(current_row_neighbors, upper_row_neighbors, lower_row_neighbors):
    """
    This method calculates the new state of the cell based on Moore neighborhood.
    :param current_row_neighbors:
    :param upper_row_neighbors:
    :param lower_row_neighbors:
    :return:
    """

    self_character = current_row_neighbors[1]
    new_state = self_character

    if self_character == '0': # If S and there is an Infected close, be Infected
        if current_row_neighbors.count('2') > 0 or upper_row_neighbors.count('2') > 0 or lower_row_neighbors.count('2') > 0:
            beta_chance = get_random_number(0)
            if beta > beta_chance > 0:
                new_state = '2'
    elif self_character == '2': # if Infected, calculate the probability to be Recovered
        gamma_chance = get_random_number(0)

        if gamma > gamma_chance > 0:
            new_state = '3'

    return new_state

# TODO: Add Seed parameter
# TODO: Add population density
# TODO: Non linearity coefficient?
# TODO: Add "Expected Numerical Results" graph versus "Spatial Results"

# SEIR Model Parameters

# Salmonela rates:
# E->I: 0.33
# S->E: 0.18
# E->I: 0.01

# Salmonela Cerro - Dairy herd http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2870801/
# S->E: 0.9
# Birt and Death: 0.03
# Indirect Transmission: 10^-12
# I->R: 0.14
# R->S: 0.22
# Environment pathogen removal: 10^9
# Pathogen addition to environment due to animal shedding: 0.99

# Rates - Units are 1/time in days
beta = .4247  # Transmission Rate: S -> E (or S->I) # TODO: Only different parameter vs the numerical model, others are the same
#sigma = .9 # Incubation Rate: E -> I (or epsilon)
gamma =.14286  #.2 # Recovery Rate: I -> R
#alpha = .22  # Immunity Loss Rate: I -> S
mu = 0  # TODO: Mortality Rate
muStart = 0  # TODO: Birth Rate
delta = 0  # TODO: Infectious Mortality Rate

simulation_iterations = 70
cell_count_x = 100
cell_count_y = 100
hexagon_layout = False

# Init values
susceptible_character = 'S'
exposedCharacter = 'E'
recoveredCharacter = 'R'
infected_character = 'I'
extremeEndValue = '0'
timeStart = 0.0
timeEnd = simulation_iterations
timeStep = 1
timeRange = np.arange(timeStart, timeEnd + timeStart, timeStep)
universeList = []

# Randomise first state
for currentColumn in range(cell_count_y):
    # if currentColumn == (cell_count_y / 2):
        # universe = ''.join('0' for universeColumn in range((cell_count_x / 2) - 1))
        # universe += '2'
        # universe += ''.join('0' for universeColumn in range(cell_count_x / 2))
    # else:
    #     universe = ''.join(random.choice('0') for universeColumn in range(cell_count_x))
    universe = ''.join(random.choice('000000000000000000000000000000000000000000000000000000000002') for universeColumn in range(cell_count_x))
    universeList.append(universe)

# TODO: Fix init state vars
InitSusceptibles = 0.0
InitInfected = 0.0
InitRecovered = 0.0
InitVariables = [InitSusceptibles, InitInfected, 0.0, 0.0, 0.0]

RES = [InitVariables]

universeTimeSeries = []

# Main Execution loop
for current_time_step in range(simulation_iterations):

    # Print the current generation
    if current_time_step < 0:
        printGenerationUniverse(current_time_step, cell_count_x, cell_count_y, susceptible_character, exposedCharacter, infected_character, recoveredCharacter)

    # Store the counts of I, S and the time iteration
    zeroCount = 0
    oneCount = 0
    twoCount = 0
    threeCount = 0
    for current_row in range(cell_count_y):
        zeroCount += universeList[current_row].count('0')
        oneCount += universeList[current_row].count('1')
        twoCount += universeList[current_row].count('2')
        threeCount += universeList[current_row].count('3')
    RES.append([zeroCount, oneCount, twoCount, threeCount, current_time_step])

    # Put extreme ends neighbouring cells temporarily on the old universe
    oldUniverseList = []
    toCopyUniverseList = []
    for current_row in range(cell_count_y):
        if hexagon_layout:
            oldUniverseList.append(universeList[current_row])
        else:
            oldUniverseList.append(extremeEndValue + universeList[current_row] + extremeEndValue)
        toCopyUniverseList.append(universeList[current_row])

    universeTimeSeries.append(toCopyUniverseList)

    for current_row in range(cell_count_y):
        newUniverseRow = ''
        for currentColumn in range(cell_count_x):

            if hexagon_layout:
                # HEX
                hex_neighbours = list("000000") # list of characters

                # Top/bottom CELL 2 & CELL 3 - Same for ODD and EVEN
                if (current_row - 1) >= 0: # CELL 2
                    hex_neighbours[2] = oldUniverseList[current_row - 1][currentColumn]
                if (current_row + 1) < cell_count_y: # CELL 3
                    hex_neighbours[3] = oldUniverseList[current_row + 1][currentColumn]

                if (currentColumn % 2 == 0):
                    if (currentColumn - 1) >= 0: # CELL 1 EVEN
                        hex_neighbours[1] = oldUniverseList[current_row][currentColumn - 1]
                        if (current_row - 1) >= 0: # CELL 0 EVEN
                            hex_neighbours[0] = oldUniverseList[current_row - 1][currentColumn - 1]
                    if (currentColumn + 1) < cell_count_x: # CELL 5 EVEN
                        hex_neighbours[5] = oldUniverseList[current_row][currentColumn + 1]
                        if (current_row - 1) >= 0: # CELL 4 EVEN
                            hex_neighbours[4] = oldUniverseList[current_row - 1][currentColumn + 1]
                else:
                    # Make string of ODD neighbours - Check ranges
                    if (currentColumn - 1) >= 0: # CELL 0 ODD
                        hex_neighbours[0] = oldUniverseList[current_row][currentColumn - 1]
                        if (current_row - 1) >= 0: # CELL 1 ODD
                            hex_neighbours[1] = oldUniverseList[current_row - 1][currentColumn - 1]
                    if (currentColumn + 1) < cell_count_x: # CELL 4 ODD
                        hex_neighbours[4] = oldUniverseList[current_row][currentColumn + 1]
                        if (current_row + 1) < cell_count_y: # CELL 5 ODD
                            hex_neighbours[5] = oldUniverseList[current_row + 1][currentColumn + 1]

                # Get the new state by sending the currentCell value + string of all neighbours
                hex_neighbours = "".join(hex_neighbours) # join the characters into 1 string
                newUniverseRow += get_new_state2DHex(oldUniverseList[current_row][currentColumn], hex_neighbours)
                universeList[current_row] = newUniverseRow
            else:
                # SQUARE
                upper_row_neighbours = '000'
                lower_row_neighbours = '000'
                current_row_neighbours = oldUniverseList[current_row][currentColumn:currentColumn+3]
                if (current_row - 1) >= 0:
                    upper_row_neighbours = oldUniverseList[current_row-1][currentColumn:currentColumn+3]
                if (current_row + 1) < cell_count_y:
                    lower_row_neighbours = oldUniverseList[current_row+1][currentColumn:currentColumn+3]

                newUniverseRow += get_new_state2D(current_row_neighbours, upper_row_neighbours, lower_row_neighbours)
                universeList[current_row] = newUniverseRow

                # TODO: Square neighbours to list of characters
                #squareNeighbours = list("00000000") # list of characters

# print RES
# print(universeTimeSeries)
RES = np.array(RES)

# Ploting
pl.subplot(1, 1, 1)
pl.plot(RES[:, 4], RES[:, 2], '-r', label='Infected')
pl.plot(RES[:, 4], RES[:, 0], '-b', label='Susceptibles')
pl.plot(RES[:, 4], RES[:, 3], '-g', label='Recovered')
pl.legend(loc=0)
pl.title('CA SIR')
pl.xlabel('Time')
pl.ylabel('Count')

"""
pl.subplot(2, 1, 2)
pl.plot(map(itemgetter(4), RES), map(itemgetter(2), RES), '-r', label='Infected')
pl.plot(map(itemgetter(4), RES), map(itemgetter(0), RES), '-b', label='Susceptibles')
pl.legend(loc=0)
pl.title('Infected and Susceptibles')
pl.xlabel('Infected')
pl.ylabel('Susceptibles')
"""
pl.show()

draw_generation_universe(cell_count_x, cell_count_y, universeTimeSeries)
