import pygame as pg
import time
import random
from copy import deepcopy
# expanded for video ;)
colors = {'food': 'green',
          0: 'black',
          1: 'white',
          2: 'red',
          3: 'yellow',
          4: 'blue'}  # Pheremones are numbered
def_brain = {'food': [1, 1],
             0: [1, 1],
             1: [-1, 0]}  # input: [rotation, output]


def mutate(new_brain):  # Tried putting in Ant class. Did not work :(
    for i in list(new_brain.keys()):  # For every input
        if not random.randint(0, 9):  # Whether it mutates
            if not random.randint(0, 1):  # Whether rotation changes
                new_brain[i][0] = random.randint(-1, 2)
            if not random.randint(0, 1):  # Whether output changes
                new_brain[i][1] = random.randint(0, 4)
        if (not random.randint(0, 19)) and (type(i) == int):  # Whether it deletes
            del new_brain[i]
            if not i: new_brain[i] = [1, 1]
    if not random.randint(0, 9):  # Whether one adds/overwrites completely
        new_brain[random.randint(0, 4)] = [random.randint(-1, 2), random.randint(0, 4)]  # Only works for pheremones
    print('NEW BRAIN:')
    for i in new_brain.keys(): print(i, ':', new_brain[i])
    return new_brain


class Ant:
    def __init__(self, app, pos, brain=None, facing_dir=[0, 1], age=0):
        if brain is None:
            brain = def_brain
        self.brain = brain
        # {0: [1, 0],  Input value value: [turning direction, output value]
        #  1: [-1, 0]}
        self.app = app
        self.x = pos[0]
        self.y = pos[1]
        self.facing_dir = facing_dir
        self.CELL_SIZE = self.app.CELL_SIZE
        self.age = age

    def turn(self, t_dir):  # Handles the annoying turning calculations
        if t_dir == -1:  # Anticlockwise
            if self.facing_dir == [0, 1]:  # [x, y]
                self.facing_dir = [-1, 0]
            elif self.facing_dir == [1, 0]:
                self.facing_dir = [0, 1]
            elif self.facing_dir == [0, -1]:
                self.facing_dir = [1, 0]
            elif self.facing_dir == [-1, 0]:
                self.facing_dir = [0, -1]
        elif t_dir == 1:  # Clockwise
            if self.facing_dir == [0, 1]:
                self.facing_dir = [1, 0]
            elif self.facing_dir == [1, 0]:
                self.facing_dir = [0, -1]
            elif self.facing_dir == [0, -1]:
                self.facing_dir = [-1, 0]
            elif self.facing_dir == [-1, 0]:
                self.facing_dir = [0, 1]
        elif t_dir == 0:  # Straight
            pass
        else:  # Like if it's 2, 180
            self.facing_dir = [-i for i in self.facing_dir]

    def run(self):
        rect = self.x * self.CELL_SIZE, self.y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE

        in_val = self.app.grid[self.y][self.x]  # Value ant sees
        if in_val not in self.brain:
            in_val = 0
        if in_val == 'food':
            self.app.ants += [Ant(app=self.app,
                                  pos=[self.x, self.y],
                                  brain=mutate(deepcopy(self.brain)),
                                  facing_dir=self.facing_dir)]
        self.app.grid[self.y][self.x] = self.brain[in_val][1]  # Value ant leaves
        pg.draw.rect(self.app.screen, colors[self.brain[in_val][1]], rect)
        self.turn(self.brain[in_val][0])  # Turn in brain's direction
        self.x = (self.x + self.facing_dir[0]) % self.app.COLS
        self.y = (self.y + self.facing_dir[1]) % self.app.ROWS
        self.age += 1
        if self.age >= 20000:
            self.app.ants.remove(self)


class App:
    def __init__(self, WIDTH=850, HEIGHT=687, CELL_SIZE=4):
        pg.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        self.clock = pg.time.Clock()
        self.iterations = 0

        self.CELL_SIZE = CELL_SIZE
        self.ROWS = HEIGHT // CELL_SIZE
        self.COLS = WIDTH // CELL_SIZE
        # self.grid = [[0 for row in range(self.ROWS)] for col in range(self.COLS)]
        self.grid = [[0 for col in range(self.COLS)] for row in range(self.ROWS)]
        self.grid[100][100] = 'food'

        self.ants = [Ant(app=self, pos=[self.COLS // 2, self.ROWS // 2])]

        for i in range(len(self.grid)):  # Initial render
            for j in range(len(self.grid[i])):
                rect = j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE
                pg.draw.rect(self.screen, colors[self.grid[i][j]], rect)

    def run(self):
        while True:
            # time.sleep(1)
            for ant in self.ants:
                ant.run()

            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick()
            if not self.ants:
                self.ants = [Ant(app=self, pos=[self.COLS // 2, self.ROWS // 2])]

            if not self.iterations % 1000:
                new_food = (random.randint(0, self.COLS - 1), random.randint(0, self.ROWS - 1))
                self.grid[new_food[1]][new_food[0]] = 'food'
                rect = new_food[0] * self.CELL_SIZE, new_food[1] * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE
                pg.draw.rect(self.screen, colors[self.grid[new_food[1]][new_food[0]]], rect)

            self.iterations += 1


if __name__ == '__main__':
    app = App()
    time.sleep(20)
    app.run()
