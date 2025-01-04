import os
import pygame
import pygame.gfxdraw
import numpy as np

# initialize pygame
pygame.init()

# window: high resolution, display on screen
window_width = 1000
window_height = 1000
window = pygame.display.set_mode((window_width, window_height))

# canvas: low resolution, draw on then draw to window
canvas_width = 32
canvas_height = 32
size = 3
canvas_list = [pygame.Surface((canvas_width, canvas_height)) for i in range(size**2)]

# pygame settings
pygame.display.set_caption("Random generation")
clock = pygame.time.Clock()

# script settings
running = True
rng = np.random.default_rng(5645)

# sigmoid: float to [0, 1] float
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

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
            case 9: val += np.abs(i / 2*np.pi) - np.abs(j / 2*np.pi)
            case 10: val += np.abs(j / 2*np.pi) - np.abs(i / 2*np.pi)
            case 11: val += 0.5
            case 12: val -= 0.5
    return sigmoid(val)

# [0, 1] float to [0, 255] int
def intensity(x):
    return int(x * 255)

# loop
while running:

    # set refresh rate
    clock.tick(0.5)

    # loop over events
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # for each model
    for canvas in canvas_list:

        # sample model seeds
        u1 = rng.integers(1, 13, 5)
        u2 = rng.integers(1, 13, 5)
        u3 = rng.integers(1, 13, 5)

        # draw model
        for i in range(canvas_height):
            for j in range(canvas_width):

                # apply models
                colour = (intensity(random_f(i, j, u1)), intensity(random_f(i, j, u2)), intensity(random_f(i, j, u3)))

                # greyscale version
                #val = intensity(random_f(i, j, u1))
                #colour = (val, val, val)

                # draw model to its canvas
                pygame.gfxdraw.pixel(canvas, i, j, colour)

    # blit each canvas to section on window
    for i in range(size):
        for j in range(size):
            canvas = canvas_list[i*size + j]
            window.blit(pygame.transform.scale(canvas, (window_width // size - 1, window_height // size - 1)), (i * (window_width // size), j * (window_height // size)))

    # update display
    pygame.display.flip()