import pygame
import pygame.font
from pygame.sprite import Group

from playable import Pacman


class Scores:
    def __init__(self, settings, screen, stats, nodes, stars, score_board, red, pink, orange, blue):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.nodes = nodes
        self.stars = stars
        self.score_board = score_board

        self.red = red
        self.pink = pink
        self.orange = orange
        self.blue = blue

        self.text_color = (250, 250, 250)
        self.font = pygame.font.SysFont('Broadway', 40)

        self.prep_score_title()
        self.prep_lives()

    def show_score(self):
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.lives_image, self.lives_image_rect)
        self.pacman.draw(self.screen)

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
        if self.stats.game_over:
            self.score_board.update_scores()
            self.stats.game_over = False

    def prep_lives(self):
        lives = "Lives: "
        self.lives_image = self.font.render(lives, True, self.text_color)
        self.lives_image_rect = self.lives_image.get_rect()
        self.lives_image_rect.top = self.score_image_rect.top
        self.lives_image_rect.left = self.score_image_rect.left * 40

        self.pacman = Group()
        for life in range(self.stats.lives_left):
            pacman = Pacman(self.settings, self.screen, self.stats, self.nodes, self.stars, self, self.red, self.pink, self.orange, self.blue)
            pacman.rect.x = (self.score_image_rect.left * 40 + self.lives_image_rect.width) + life * pacman.rect.width
            pacman.rect.y = self.score_image_rect.y
            self.pacman.add(pacman)

    def prep_score_title(self):
        title = "Score: "
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        score_str = str(self.stats.score)
        self.score_image = self.font.render(title + score_str, True, self.text_color)
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.top = self.screen_rect.bottom - 50
        self.score_image_rect.left = self.screen_rect.left + 10
