import pygame
from maze_assets import MakeAsset


class Maze(object):
    BRICK_SIZE = 13

    def __init__(self, screen, settings, maze, brickfile, shieldfile):
        self.screen = screen
        self.settings = settings
        self.filename = maze
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.bricks = []
        self.shields = []

        self.brick = MakeAsset(self.settings, self.screen, brickfile)
        self.shield = MakeAsset(self.settings, self.screen, shieldfile)

        self.deltax = self.deltay = Maze.BRICK_SIZE

        self.build()

    def build(self):
        b = self.brick.rect
        s = self.shield.rect
        w, h = b.width, b.height
        dx, dy = self.deltax, self.deltay

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                last = len(row) - 1
                rest = row[ncol+1:] if ncol < last - 2 else row[last]
                if col == 'X':
                    self.bricks.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                elif col == 's':
                    self.shields.append(pygame.Rect(ncol * dx, nrow * dy, w, h))

    def blit(self):
        for rect in self.bricks:
            self.screen.blit(self.brick.image, rect)
        for rect in self.shields:
            self.screen.blit(self.shield.image, rect)
