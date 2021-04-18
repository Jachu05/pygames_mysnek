from typing import List

import pygame
from dataclasses import dataclass
import random


@dataclass
class Window:
    width = 500
    rows = 20

    def __new__(cls, *args, **kwargs):
        return pygame.display.set_mode((Window.width, Window.width))

    @staticmethod
    def draw_grid(w, rows, surface):
        size_btwn = w // rows

        x = 0
        y = 0
        for l in range(rows):
            x = x + size_btwn
            y = y + size_btwn

            pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
            pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


@dataclass
class Cube:
    current_pos_x: int = 0
    current_pos_y: int = 0
    color: tuple = (0, 255, 0)
    last_valid_heading_x = 1
    last_valid_heading_y = 0
    f_side_change = False

    def draw(self, window):
        dis = Window.width // Window.rows
        i = self.current_pos_x
        j = self.current_pos_y

        pygame.draw.rect(window, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

    def get_new_pos_from_dir(self, dir_x, dir_y):
        new_pos_x = self.current_pos_x + dir_x
        new_pos_y = self.current_pos_y + dir_y

        if new_pos_x >= Window.rows:
            new_pos_x = 0
        elif new_pos_x < 0:
            new_pos_x = Window.rows - 1

        if new_pos_y >= Window.rows:
            new_pos_y = 0
        elif new_pos_y < 0:
            new_pos_y = Window.rows - 1

        return new_pos_x, new_pos_y

    def move_to_pos_and_get_prev_pos(self, new_pos_x, new_pos_y):
        prev_pos_x = self.current_pos_x
        prev_pos_y = self.current_pos_y

        self.current_pos_x = new_pos_x
        self.current_pos_y = new_pos_y

        return prev_pos_x, prev_pos_y


@dataclass
class Head(Cube):
    color: tuple = (0, 120, 0)
    current_pos_x: int = 10
    current_pos_y: int = 10
    last_valid_heading_x = 1
    last_valid_heading_y = 0


class Snek:
    def __init__(self):
        self.body: List[Cube] = [Head(), Cube(current_pos_x=9, current_pos_y=10)]

    def draw(self, window):
        for elem in self.body:
            elem.draw(window)

    def add_cube(self):
        cube1 = self.body[-1]
        cube2 = self.body[-2]

        dir_x = cube2.current_pos_x - cube1.current_pos_x
        dir_y = cube2.current_pos_y - cube1.current_pos_y

        cube_new_pos_x = cube1.current_pos_x - dir_x
        cube_new_pos_y = cube1.current_pos_y - dir_y

        new_cube = Cube(cube_new_pos_x, cube_new_pos_y)
        self.body.append(new_cube)

    def move(self, dir_x, dir_y):
        head = self.body[0]

        # take new head positions
        new_exp_pos_x, new_exp_pos_y = head.get_new_pos_from_dir(dir_x, dir_y)
        # check if new head position is valid, do not allow to situation where user will move inside body
        if new_exp_pos_x == self.body[1].current_pos_x and new_exp_pos_y == self.body[1].current_pos_y:
            # if so take new position based of recent valid direction
            dir_x = head.last_valid_heading_x
            dir_y = head.last_valid_heading_y
            new_exp_pos_x, new_exp_pos_y = head.get_new_pos_from_dir(dir_x, dir_y)

        # move head and remember last valid direction for head
        prev_pos_x, prev_pos_y = head.move_to_pos_and_get_prev_pos(new_exp_pos_x, new_exp_pos_y)
        head.last_valid_heading_x = dir_x
        head.last_valid_heading_y = dir_y

        # move rest body
        for elem in self.body[1:]:
            prev_pos_x, prev_pos_y = elem.move_to_pos_and_get_prev_pos(prev_pos_x, prev_pos_y)

    def check_colision(self):
        head_pos_x = self.body[0].current_pos_x
        head_pos_y = self.body[0].current_pos_y

        for elem in self.body[1:]:
            cube_pos_x = elem.current_pos_x
            cube_pos_y = elem.current_pos_y
            if head_pos_x == cube_pos_x and head_pos_y == cube_pos_y:
                return True
        return False


def main():
    window = Window()

    dir_x = 1
    dir_y = 0

    snek = Snek()

    snack = Cube(current_pos_x=random.randint(0, 19), current_pos_y=random.randint(0, 19), color=(0, 0, 255))

    while True:
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for _ in keys:
                if keys[pygame.K_LEFT]:
                    dir_x = -1
                    dir_y = 0

                elif keys[pygame.K_RIGHT]:
                    dir_x = 1
                    dir_y = 0

                elif keys[pygame.K_UP]:
                    dir_x = 0
                    dir_y = -1

                elif keys[pygame.K_DOWN]:
                    dir_x = 0
                    dir_y = 1
        snek.move(dir_x, dir_y)

        if snek.check_colision():
            snek = Snek()

        if snek.body[0].current_pos_x == snack.current_pos_x and snek.body[0].current_pos_y == snack.current_pos_y:
            snek.add_cube()
            snack = Cube(current_pos_x=random.randint(0, 19), current_pos_y=random.randint(0, 19), color=(0, 0, 255))

        window.fill((0, 0, 0))
        snek.draw(window)
        snack.draw(window)

        Window.draw_grid(Window.width, Window.rows, window)
        pygame.display.update()


main()
