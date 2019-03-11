import pygame
import os
from pygame.sprite import Sprite
from timer import Timer, TimerDual


class TesterGhost(Sprite):
    def __init__(self, settings, screen, nodes):
        super(TesterGhost, self).__init__()
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()
        self.nodes = nodes
        self.node = nodes.nodeList[64]

        self.images = self.frames('right')
        self.timer = Timer(self.images, wait=200)
        self.image = self.images[self.timer.frame_index()]

        self.in_danger = False
        self.rect = self.image.get_rect()

    def game_active(self):
        self.node = self.nodes.nodeList[64]
        self.rect.centerx = self.setPosition().x
        self.rect.centery = self.setPosition().y

        self.center = float(self.rect.centerx)
        self.top = self.rect.centery

        self.current = self.node
        # self.target = self.nodes.nodeList[14]
        self.prevdeltax = 1000
        self.prevdeltay = 1000

        self.images = self.frames('right')
        self.timer = Timer(self.images, wait=200)
        self.image = self.images[self.timer.frame_index()]

        self.rect = self.image.get_rect()

    def setPosition(self):
        position = self.node.position.copy()
        return position

    def frames(self, op_path):
        images = []
        path = 'images/Tester/' + op_path
        for file_name in os.listdir(path):
            ghost = pygame.image.load(path + os.sep + file_name)
            images.append(ghost)
        return images

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if not self.in_danger:
            self.image = self.images[self.timer.frame_index()]
            if self.node is not None:
                self.prev = self.node
                #if self.node is not self.target:
                  #  self.move_to_target()
                   # self.node = self.current
                self.rect.centerx = self.setPosition().x
                self.rect.centery = self.setPosition().y
            else:
                #self.node = self.prev
                self.node = self.node
        else:
            self.image = self.images[self.timer.frame_index()]

    '''''
    def move_to_target(self):
        deltax = self.target.position.x - self.current.position.x
        deltay = self.target.position.y - self.current.position.y
        if deltax < self.prevdeltax and deltay < self.prevdeltay:
            self.prev = self.current
            self.current = self.node.neighbors[self.nodes.settings.up]
            if deltax < 0:
                deltax *= -1
            if deltay < 0:
                deltax*= -1
            self.prevdeltax = deltax
            self.prevdeltay = deltay
        else:
            self.current = self.prev
'''''
    def danger(self):
        self.images_blue = self.frames('blue-dead')
        self.images_white = self.frames('danger-white')
        self.images = self.images_blue + self.images_white
        self.timer = TimerDual(self.images_blue, self.images_white)

    def retreat(self):
        self.in_danger = False
        self.images = self.frames('retreat')
        self.timer = Timer(self.images)
        self.node = self.nodes.nodeList[64]


class Red(Sprite):
    def __init__(self, settings, screen, nodes):
        super(Red, self).__init__()
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()
        self.nodes = nodes
        self.node = nodes.nodeList[69]

        self.images = self.frames('right')
        self.timer = Timer(self.images, wait=200)
        self.image = self.images[self.timer.frame_index()]

        self.in_danger = False
        self.rect = self.image.get_rect()

    def game_active(self):
        self.node = self.nodes.nodeList[69]
        self.rect.centerx = self.setPosition().x
        self.rect.centery = self.setPosition().y

        self.center = float(self.rect.centerx)
        self.top = self.rect.centery

        self.current = self.node
        # self.target = self.nodes.nodeList[14]
        self.prevdeltax = 1000
        self.prevdeltay = 1000

        self.images = self.frames('right')
        self.timer = Timer(self.images, wait=200)
        self.image = self.images[self.timer.frame_index()]

        self.rect = self.image.get_rect()

    def setPosition(self):
        position = self.node.position.copy()
        return position

    def frames(self, op_path):
        images = []
        path = 'images/Blinky/' + op_path
        for file_name in os.listdir(path):
            ghost = pygame.image.load(path + os.sep + file_name)
            images.append(ghost)
        return images

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if not self.in_danger:
            self.image = self.images[self.timer.frame_index()]
            if self.node is not None:
                self.prev = self.node
                # if self.node is not self.target:
                #  self.move_to_target()
                # self.node = self.current
                self.rect.centerx = self.setPosition().x
                self.rect.centery = self.setPosition().y
            else:
                # self.node = self.prev
                self.node = self.node
        else:
            self.image = self.images[self.timer.frame_index()]

    '''''
    def move_to_target(self):
        deltax = self.target.position.x - self.current.position.x
        deltay = self.target.position.y - self.current.position.y
        if deltax < self.prevdeltax and deltay < self.prevdeltay:
            self.prev = self.current
            self.current = self.node.neighbors[self.nodes.settings.up]
            if deltax < 0:
                deltax *= -1
            if deltay < 0:
                deltax*= -1
            self.prevdeltax = deltax
            self.prevdeltay = deltay
        else:
            self.current = self.prev
'''''

    def danger(self):
        self.images_blue = self.frames('blue-dead')
        self.images_white = self.frames('danger-white')
        self.images = self.images_blue + self.images_white
        self.timer = TimerDual(self.images_blue, self.images_white)

    def retreat(self):
        self.in_danger = False
        self.images = self.frames('retreat')
        self.timer = Timer(self.images)
        self.node = self.nodes.nodeList[69]


class Pink(Sprite):
    def __init__(self, settings, screen, nodes):
        super(Pink, self).__init__()
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()
        self.nodes = nodes
        self.node = nodes.nodeList[70]

        self.images = self.frames('right')
        self.timer = Timer(self.images, wait=200)
        self.image = self.images[self.timer.frame_index()]

        self.in_danger = False
        self.rect = self.image.get_rect()

    def game_active(self):
        self.node = self.nodes.nodeList[70]
        self.rect.centerx = self.setPosition().x
        self.rect.centery = self.setPosition().y

        self.center = float(self.rect.centerx)
        self.top = self.rect.centery

        self.current = self.node
        # self.target = self.nodes.nodeList[14]
        self.prevdeltax = 1000
        self.prevdeltay = 1000

        self.images = self.frames('right')
        self.timer = Timer(self.images, wait=200)
        self.image = self.images[self.timer.frame_index()]

        self.rect = self.image.get_rect()

    def setPosition(self):
        position = self.node.position.copy()
        return position

    def frames(self, op_path):
        images = []
        path = 'images/Pinky/' + op_path
        for file_name in os.listdir(path):
            ghost = pygame.image.load(path + os.sep + file_name)
            images.append(ghost)
        return images

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if not self.in_danger:
            self.image = self.images[self.timer.frame_index()]
            if self.node is not None:
                self.prev = self.node
                # if self.node is not self.target:
                #  self.move_to_target()
                # self.node = self.current
                self.rect.centerx = self.setPosition().x
                self.rect.centery = self.setPosition().y
            else:
                # self.node = self.prev
                self.node = self.node
        else:
            self.image = self.images[self.timer.frame_index()]

    '''''
    def move_to_target(self):
        deltax = self.target.position.x - self.current.position.x
        deltay = self.target.position.y - self.current.position.y
        if deltax < self.prevdeltax and deltay < self.prevdeltay:
            self.prev = self.current
            self.current = self.node.neighbors[self.nodes.settings.up]
            if deltax < 0:
                deltax *= -1
            if deltay < 0:
                deltax*= -1
            self.prevdeltax = deltax
            self.prevdeltay = deltay
        else:
            self.current = self.prev
'''''

    def danger(self):
        self.images_blue = self.frames('blue-dead')
        self.images_white = self.frames('danger-white')
        self.images = self.images_blue + self.images_white
        self.timer = TimerDual(self.images_blue, self.images_white)

    def retreat(self):
        self.in_danger = False
        self.images = self.frames('retreat')
        self.timer = Timer(self.images)
        self.node = self.nodes.nodeList[70]


class Orange(Sprite):
    def __init__(self, settings, screen, nodes):
        super(Orange, self).__init__()
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()
        self.nodes = nodes
        self.node = nodes.nodeList[68]

        self.images = self.frames('right')
        self.timer = Timer(self.images, wait=200)
        self.image = self.images[self.timer.frame_index()]

        self.in_danger = False
        self.rect = self.image.get_rect()

    def game_active(self):
        self.node = self.nodes.nodeList[68]
        self.rect.centerx = self.setPosition().x
        self.rect.centery = self.setPosition().y

        self.center = float(self.rect.centerx)
        self.top = self.rect.centery

        self.current = self.node
        # self.target = self.nodes.nodeList[14]
        self.prevdeltax = 1000
        self.prevdeltay = 1000

        self.images = self.frames('right')
        self.timer = Timer(self.images, wait=200)
        self.image = self.images[self.timer.frame_index()]

        self.rect = self.image.get_rect()

    def setPosition(self):
        position = self.node.position.copy()
        return position

    def frames(self, op_path):
        images = []
        path = 'images/Clyde/' + op_path
        for file_name in os.listdir(path):
            ghost = pygame.image.load(path + os.sep + file_name)
            images.append(ghost)
        return images

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if not self.in_danger:
            self.image = self.images[self.timer.frame_index()]
            if self.node is not None:
                self.prev = self.node
                # if self.node is not self.target:
                #  self.move_to_target()
                # self.node = self.current
                self.rect.centerx = self.setPosition().x
                self.rect.centery = self.setPosition().y
            else:
                # self.node = self.prev
                self.node = self.node
        else:
            self.image = self.images[self.timer.frame_index()]

    '''''
    def move_to_target(self):
        deltax = self.target.position.x - self.current.position.x
        deltay = self.target.position.y - self.current.position.y
        if deltax < self.prevdeltax and deltay < self.prevdeltay:
            self.prev = self.current
            self.current = self.node.neighbors[self.nodes.settings.up]
            if deltax < 0:
                deltax *= -1
            if deltay < 0:
                deltax*= -1
            self.prevdeltax = deltax
            self.prevdeltay = deltay
        else:
            self.current = self.prev
'''''

    def danger(self):
        self.images_blue = self.frames('blue-dead')
        self.images_white = self.frames('danger-white')
        self.images = self.images_blue + self.images_white
        self.timer = TimerDual(self.images_blue, self.images_white)

    def retreat(self):
        self.in_danger = False
        self.images = self.frames('retreat')
        self.timer = Timer(self.images)
        self.node = self.nodes.nodeList[70]