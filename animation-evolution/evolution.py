from population import Population
from display import Display

num = 4

# create a population
population = Population(size=num**2)
population.initialize()

# create a display
display = Display(grid_size=num)

# time
t = 0
display.tick = 10

while display.running:

    display.event_handler()

    display.draw(population.population, t)

    # user action prompts new generation
    if display.action:

        # evolve new population
        population.evolve(selected=display.selected)

        # reset flag
        display.action = False

        # reset selection
        display.selected = []

        # reset time
        t = 0

    # increment time
    t = (t + 1) % display.canvas_width