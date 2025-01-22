import os
import pygame
import pygame.gfxdraw
import numpy as np
import copy

# initialize pygame
pygame.init()

# window: high resolution, display on screen
window_width = 500
window_height = 500
window = pygame.display.set_mode((window_width, window_height))

# canvas: low resolution, draw on then draw to window
canvas_width = 64
canvas_height = 64
canvas = pygame.Surface((canvas_width, canvas_height))

# pygame settings
pygame.display.set_caption("Scrolling Image")
clock = pygame.time.Clock()

# script settings
running = True
rng = np.random.default_rng(34223)#(543)
splits = 5
ticks = 60

# sigmoid: float to [0, 1] float
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# [0, 1] float to [0, 255] int
def intensity(x):
    return int(x * 255)

# random model
def random_f(i, j, u_arr):
    i = (i / canvas_height) * 2 * np.pi
    j = (j / canvas_width) * 2 * np.pi
    val = 0
    for u in u_arr:
        match u:
            case 1: val += np.cos(i)
            case 2: val += np.sin(i)
            case 3: val += np.cos(j)
            case 4: val += np.sin(j)
            case 5: val += np.cos(i) * np.sin(j)
            case 6: val += np.cos(i) * np.cos(j)
            case 7: val += np.sin(i) * np.sin(j)
            case 8: val += np.sin(i) * np.cos(j)
            #case 9: val += np.abs(i / 2*np.pi) - np.abs(j / 2*np.pi)
            #case 10: val += np.abs(j / 2*np.pi) - np.abs(i / 2*np.pi)
            #case 11: val += np.abs(1 - i/2*np.pi) - np.abs(1 - j/2*np.pi)
            #case 12: val = np.abs(1 - j/2*np.pi) - np.abs(1 - i/2*np.pi)
            case 13: val += 0.5
            case 14: val -= 0.5
    return sigmoid(val)

# define base grid
base_grid = np.zeros((canvas_height, canvas_width, 3))
u1 = rng.integers(1, 15, 5)
u2 = rng.integers(1, 15, 5)
u3 = rng.integers(1, 15, 5)
for i in range(canvas_height):
    for j in range(canvas_width):
        base_grid[i, j, :] = (intensity(random_f(i, j, u1)), intensity(random_f(i, j, u2)), intensity(random_f(i, j, u3)))

# list of grids to display
grid_list = []

# current grid
current_grid = base_grid

# next grid
next_grid = base_grid

# loop
while running:

    # set refresh rate
    clock.tick(ticks)

    # loop over events
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # empty list
    if len(grid_list) == 0:

        # have reached next grid: store as current grid
        current_grid = copy.deepcopy(next_grid)

        # compute new next grid: shift current grid
        next_grid = np.roll(current_grid, shift=1, axis=(0, 1))

        # difference to current grid
        grid_diff = next_grid - current_grid

        # store intermediates
        for i in range(splits, -1, -1):
            grid_list.append(current_grid + i*(grid_diff / splits))
    
    # pop next grid to be drawn
    grid = grid_list.pop()

    # draw grid
    for i in range(canvas_height):
        for j in range(canvas_width):

            # array to tuple
            colour = (int(grid[i, j, 0]), int(grid[i, j, 1]), int(grid[i, j, 2]))

            # draw model to its canvas
            pygame.gfxdraw.pixel(canvas, j, i, colour)

    # blit canvas to window
    window.blit(pygame.transform.scale(canvas, (window_width, window_height)), (0, 0))

    # update display
    pygame.display.flip()