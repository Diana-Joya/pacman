import pygame
import os
from pygame.sprite import Sprite, Group
from timer import Timer
from portal import Portal


class Pacman(Sprite):
    def __init__(self, settings, screen, stats, nodes, stars, update_score, red, pink, orange, blue):
        super(Pacman, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.stars = stars
        self.nodes = nodes
        self.update_score = update_score
        self.node = nodes.nodeList[6]

        self.red = red
        self.pink = pink
        self.orange = orange
        self.blue = blue

        self.images = self.frames('right')
        self.timer = Timer(self.images, wait=50)
        self.image = self.images[self.timer.frame_index()]

        self.rect = self.image.get_rect()

        self.eat_star = pygame.mixer.Sound('music/pacman_chomp.wav')
        self.eat_super_star = pygame.mixer.Sound('music/pacman_eatfruit.wav')

        self.open_portal = False
        self.curr_portal = 0
        self.portal_a = Portal(self.settings, self.screen, self.rect.x, self.rect.y, 'orange')
        self.portal_b = Portal(self.settings, self.screen, self.rect.x, self.rect.y, 'blue')
        self.portal_init = False
        self.portals = [self.portal_a, self.portal_b]

    def game_active(self):
        self.images = self.frames('right')
        self.timer = Timer(self.images, wait=50)
        self.image = self.images[self.timer.frame_index()]

        self.node = self.nodes.nodeList[6]
        self.rect.centerx = self.setPosition().x
        self.rect.centery = self.setPosition().y

        self.center = float(self.rect.centerx)
        self.top = self.rect.centery

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.target = self.node
        self.direction = None


    def setPosition(self):
        position = self.node.position.copy()
        return position

    def frames(self, direction):
        images = []
        path = 'images/pacman/' + direction
        for file_name in os.listdir(path):
            pacman = pygame.image.load(path + os.sep + file_name)
            images.append(pacman)
        return images

    def get_portal(self):
        if self.curr_portal == 0:
            portal_color = 'orange'
            self.portal_a = Portal(self.settings, self.screen, self.rect.x, self.rect.y, portal_color)
            self.portals.insert(0, self.portal_a)
            self.portal_a.open(self)
            self.portal_a.blitme()
            self.portal_a.image_rect.centerx = self.rect.centerx + 20
            self.portal_a.image_rect.centery = self.rect.centery
            self.curr_portal += 1
            self.portal_init = True
        else:
            portal_color = 'blue'
            self.portal_b = Portal(self.settings, self.screen, self.rect.x, self.rect.y, portal_color)
            self.portals.insert(1, self.portal_b)
            self.portal_b.open(self)
            self.portal_b.blitme()
            self.portal_b.image_rect.centerx = self.rect.centerx + 20
            self.portal_b.image_rect.centery = self.rect.centery
            self.curr_portal = 0
            self.portal_init = True

    def update(self):
        if self.open_portal:
            self.get_portal()

        if self.stats.lost_life:
            if self.image == self.last_frame:
                self.stats.lost_life = False
                self.images = self.frames('right')
                self.timer = Timer(self.images, wait=50)
                self.game_active()
                self.blue.pacman_hit = False
                self.blue.game_active()
            self.rect.centerx = self.lastx

        self.image = self.images[self.timer.frame_index()]
        self.prev = self.node
        if self.node is not None and not self.stats.lost_life:
            if self.portal_init:
                self.portal()
            if self.moving_right and self.node.column < self.nodes.num_columns:
                self.node = self.nodes.get_path_node(self.nodes.settings.right, self.node.row, self.node.column + 1,
                                                     self.nodes.nodeList)
                self.direction = self.settings.right
                self.moving_right = False
                self.images = self.frames('right')
            if self.moving_left and self.node.column > 0:
                self.node = self.nodes.get_path_node(self.nodes.settings.left, self.node.row, self.node.column - 1,
                                                     self.nodes.nodeList)
                self.direction = self.settings.left
                self.moving_left = False
                self.images = self.frames('left')
            if self.moving_up and self.node.row > 0:
                self.node = self.nodes.get_path_node(self.nodes.settings.up, self.node.row - 1, self.node.column,
                                                     self.nodes.nodeList)
                self.direction = self.settings.up
                self.moving_up = False
                self.images = self.frames('up')
            if self.moving_down and self.node.row < self.nodes.num_rows:
                self.node = self.nodes.get_path_node(self.nodes.settings.down, self.node.row + 1, self.node.column,
                                                     self.nodes.nodeList)
                self.direction = self.settings.down
                self.moving_down = False
                self.images = self.frames('down')

            if self.node is None:
                self.node = self.prev

            self.rect.centerx = self.setPosition().x
            self.rect.centery = self.setPosition().y

            self.check_pacman_ghost_collisions()
            self.check_pacman_pill_collisions()

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def check_pacman_pill_collisions(self):
        self_group = Group()
        self_group.add(self)
        collisions = pygame.sprite.groupcollide(self_group, self.stars.star_group, False, True)
        if collisions:
            for star in collisions.values():
                self.stats.score += self.settings.star_score
                self.update_score.prep_score_title()
                pygame.mixer.Sound.play(self.eat_star)
            self.update_score.check_high_score()
        super_collisions = pygame.sprite.groupcollide(self_group, self.stars.ss_group, False, True)
        if super_collisions:
            for super_star in super_collisions.values():
                self.stats.score += self.settings.super_star_score
                self.update_score.prep_score_title()
                pygame.mixer.Sound.stop(self.eat_star)
                pygame.mixer.Sound.play(self.eat_super_star)
                self.blue.in_danger = True
                self.blue.danger()
                self.pink.in_danger = True
                self.pink.danger()
                self.red.in_danger = True
                self.red.danger()
                self.orange.in_danger = True
                self.orange.danger()

            self.update_score.check_high_score()

    def check_pacman_ghost_collisions(self):
        blue_col = pygame.sprite.collide_rect(self, self.blue)
        if blue_col:
            if self.blue.in_danger:
                self.blue.retreat()
                self.settings.ghost_score *= 2
                self.stats.score += self.settings.ghost_score
                self.update_score.prep_score_title()
                pygame.mixer.Sound.stop(self.eat_star)
                eat_ghost = pygame.mixer.Sound('music/pacman_eatghost.wav')
                pygame.mixer.Sound.play(eat_ghost)
            else:
                self.images = self.frames('death')
                self.last_frame = self.images[len(self.images)-1]
                self.timer = Timer(self.images, wait=30)
                self.lastx = self.rect.centerx
                self.stats.lives_left -= 1
                self.stats.lost_life = True
                pygame.mixer.Sound.stop(self.eat_star)
                die = pygame.mixer.Sound('music/pacman_death.wav')
                pygame.mixer.Sound.play(die)
                self.update_score.prep_lives()
        pink_col = pygame.sprite.collide_rect(self, self.pink)
        if pink_col:
            if self.pink.in_danger:
                self.pink.retreat()
                self.settings.ghost_score *= 2
                self.stats.score += self.settings.ghost_score
                self.update_score.prep_score_title()
                pygame.mixer.Sound.stop(self.eat_star)
                eat_ghost = pygame.mixer.Sound('music/pacman_eatghost.wav')
                pygame.mixer.Sound.play(eat_ghost)
            else:
                self.images = self.frames('death')
                self.last_frame = self.images[len(self.images) - 1]
                self.timer = Timer(self.images, wait=30)
                self.lastx = self.rect.centerx
                self.stats.lives_left -= 1
                self.stats.lost_life = True
                pygame.mixer.Sound.stop(self.eat_star)
                die = pygame.mixer.Sound('music/pacman_death.wav')
                pygame.mixer.Sound.play(die)
                self.update_score.prep_lives()
        self.update_score.check_high_score()
        red_col = pygame.sprite.collide_rect(self, self.red)
        if red_col:
            if self.red.in_danger:
                self.red.retreat()
                self.settings.ghost_score *= 2
                self.stats.score += self.settings.ghost_score
                self.update_score.prep_score_title()
                pygame.mixer.Sound.stop(self.eat_star)
                eat_ghost = pygame.mixer.Sound('music/pacman_eatghost.wav')
                pygame.mixer.Sound.play(eat_ghost)
            else:
                self.images = self.frames('death')
                self.last_frame = self.images[len(self.images) - 1]
                self.timer = Timer(self.images, wait=30)
                self.lastx = self.rect.centerx
                self.stats.lives_left -= 1
                self.stats.lost_life = True
                pygame.mixer.Sound.stop(self.eat_star)
                die = pygame.mixer.Sound('music/pacman_death.wav')
                pygame.mixer.Sound.play(die)
                self.update_score.prep_lives()
        orange_col = pygame.sprite.collide_rect(self, self.orange)
        if orange_col:
            if self.orange.in_danger:
                self.orange.retreat()
                self.settings.ghost_score *= 2
                self.stats.score += self.settings.ghost_score
                self.update_score.prep_score_title()
                pygame.mixer.Sound.stop(self.eat_star)
                eat_ghost = pygame.mixer.Sound('music/pacman_eatghost.wav')
                pygame.mixer.Sound.play(eat_ghost)
            else:
                self.images = self.frames('death')
                self.last_frame = self.images[len(self.images) - 1]
                self.timer = Timer(self.images, wait=30)
                self.lastx = self.rect.centerx
                self.stats.lives_left -= 1
                self.stats.lost_life = True
                pygame.mixer.Sound.stop(self.eat_star)
                die = pygame.mixer.Sound('music/pacman_death.wav')
                pygame.mixer.Sound.play(die)
                self.update_score.prep_lives()
        self.update_score.check_high_score()
        if self.stats.lives_left < 0:
            self.stats.game_over = True
            self.update_score.check_high_score()
            self.game_active()
            self.blue.game_active()
            self.pink.game_active()
            self.orange.game_active()
            self.stats.game_active = False
            self.stats.reset_stats()
            pygame.mouse.set_visible(True)

    def portal(self):
        self.portal_a.attempt_transport(self, self)
        self.portal_b.attempt_transport(self, self)
