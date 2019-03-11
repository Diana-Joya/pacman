import pygame
from pygame.sprite import Group, Sprite
import os
from vector import Vector
from settings import Settings
from numpy import loadtxt
from timer import Timer


class StarGroup(object):
    def __init__(self, screen, maze):
        self.screen = screen
        self.settings = Settings()
        self.star_group = Group()
        self.ss_group = Group()
        self.createStarList(maze)

    def is_empty_star(self):
        if len(self.star_group) == 0:
            return True
        return False

    def is_empty_super_star(self):
        if len(self.ss_group) == 0:
            return True
        return False

    def createStarList(self, maze):
        grid = loadtxt(maze, dtype=str)
        num_rows, num_columns = len(grid), len(grid[0])
        maze_offset = 17
        for row in range(num_rows):
            for col in range(num_columns):
                if grid[row][col] == "p" or grid[row][col] == "n":
                    new_star = Star(self.screen, maze_offset+col*self.settings.node_width,
                                    maze_offset+row*self.settings.node_height, 0)
                    self.star_group.add(new_star)
                if grid[row][col] == "P" or grid[row][col] == "N":
                    new_super_star = SuperStar(self.screen, maze_offset+col*self.settings.node_width,
                                               maze_offset+row*self.settings.node_height, 0)
                    self.ss_group.add(new_super_star)

    def render(self):
        self.star_group.draw(self.screen)
        self.ss_group.draw(self.screen)


class Star(Sprite):
    def __init__(self, screen, x, y, z):
        super(Star, self).__init__()
        self.screen = screen
        self.name = "star"
        self.position = Vector(x, y, z)
        self.image = pygame.image.load('images/star/star.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def render(self):
        self.screen.blit(self.image, self.rect)


class SuperStar(Sprite):
    def __init__(self, screen, x, y, z):
        super(SuperStar, self).__init__()
        self.screen = screen
        self.name = "Super Star"
        self.position = Vector(x, y, z)
        self.color = (0, 0, 255)

        self.images = self.frames()
        self.timer = Timer(self.images, wait=200)
        self.image = self.images[self.timer.frame_index()]

        self.rect = self.image.get_rect()
        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def render(self):
        self.rect.centerx = int(self.position.x)
        self.rect.centery = int(self.position.y)
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.image = self.images[self.timer.frame_index()]
        self.render()

    def frames(self):
        images = []
        path = 'images/super_star/'
        for file_name in os.listdir(path):
            ghost = pygame.image.load(path + os.sep + file_name)
            images.append(ghost)
        return images
