import pygame
import pygame.gfxdraw
import numpy as np

rng = np.random.default_rng()

class Display():
    
    def __init__(self, grid_size=3):

        # initialize pygame
        pygame.init()

        # window: high resolution, display on screen
        self.window_width = 500
        self.window_height = 500
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        # canvas: low resolution, draw on then draw to window
        self.canvas_width = 32
        self.canvas_height = 32
        self.grid_size = grid_size
        self.canvas_list = [pygame.Surface((self.canvas_width, self.canvas_height)) for i in range(self.grid_size**2)]

        # pygame settings
        pygame.display.set_caption("Model evolution")
        self.clock = pygame.time.Clock()
        self.tick = 1

        # state
        self.running = True
        self.action = False
        self.selected = []

    def event_handler(self):

        # loop over events
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.key == pygame.K_SPACE:
                    self.action = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # get mouse position
                x, y = pygame.mouse.get_pos()
                
                # get grid square

                # size of grid square in pixels
                square_width = self.window_width // self.grid_size
                square_height = self.window_height // self.grid_size

                # grid square of mouse
                i = y // square_height
                j = x // square_width

                # grid index
                idx = i*self.grid_size + j

                # toggle selection
                if idx in self.selected:
                    self.selected.remove(idx)
                else:
                    self.selected.append(idx)


    def draw_batch(self, population):
        '''Draw outputs of a population to the screen using a batched approach.'''

        # set refresh rate
        self.clock.tick(self.tick)

        # for each model / canvas
        for k in range(self.grid_size**2):

            # get model
            model = population[k]

            # get canvas
            canvas = self.canvas_list[k]

            # get model output over pixel grid
            colour_array = model.colour_batch(self.canvas_height, self.canvas_width)

            # darken if selected model
            if k in self.selected:
                colour_array = colour_array // 2

            # blit colour array to canvas
            pygame.surfarray.blit_array(canvas, colour_array)

        # blit each canvas to section on window
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                canvas = self.canvas_list[i*self.grid_size + j]
                self.window.blit(
                    pygame.transform.scale(
                        canvas,
                        (
                            self.window_width // self.grid_size - 1,
                            self.window_height // self.grid_size - 1
                        )
                    ),
                    (
                        j * (self.window_width // self.grid_size),
                        i * (self.window_height // self.grid_size)
                    )
                )

        # update display
        pygame.display.flip()


    def draw(self, population):
        '''Draw outputs of a population to the screen.'''

        # set refresh rate
        self.clock.tick(self.tick)

        # for each model / canvas
        for k in range(self.grid_size**2):

            # get model
            model = population[k]

            # get canvas
            canvas = self.canvas_list[k]

            # paint model outputs
            for i in range(self.canvas_height):
                for j in range(self.canvas_width):

                    # apply models
                    colour = model.colour(i, j)

                    # darken selected model colours
                    if k in self.selected:
                        colour = (colour[0] // 2, colour[1] // 2, colour[2] // 2)

                    # draw model to canvas
                    pygame.gfxdraw.pixel(canvas, j, i, colour)

        # blit each canvas to section on window
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                canvas = self.canvas_list[i*self.grid_size + j]
                self.window.blit(
                    pygame.transform.scale(
                        canvas,
                        (
                            self.window_width // self.grid_size - 1,
                            self.window_height // self.grid_size - 1
                        )
                    ),
                    (
                        j * (self.window_width // self.grid_size),
                        i * (self.window_height // self.grid_size)
                    )
                )

        # update display
        pygame.display.flip()