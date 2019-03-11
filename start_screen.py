import pygame
import pygame.font
from button import Button
from points import SuperStar
import time


class Start:
    def __init__(self, settings, screen, stats, pacman, ghost, redenemy, pinkenemy, orangeenemy):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.bg_color = self.settings.bg_color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 28)

        self.pacman = pacman
        self.blue = ghost
        self.red = redenemy
        self.pink = pinkenemy
        self.orange = orangeenemy
        self.reset()

        self.play_button = "Play Game"
        self.play_y = 600

        self.scores_button = "High Scores"
        self.scores_y = 680

        self.music_started = False
        self.intro_music(0)

        self.game_title()
        self.start_animation()

    def reset(self):
        self.music_started = False
        self.intro_music(0)
        self.current = 0
        self.current_ghost = (self.red, self.blue, self.pink, self.orange)
        self.current_ghost_name = 'Blinky/Name/name.png'
        self.score_timer = 0
        self.ghost_timer = 0
        self.ghost_left = 4
        self.star = SuperStar(self.screen, 900, 405, 0)
        self.stats.game_over = False

    def intro_music(self, music):
        pygame.init()
        pygame.mixer.init()

        if music == 0:
            self.music = 'music/pacman_beginning.wav'
            self.loop = -1
        elif music == 1:
            self.music = 'music/pacman_eatghost.wav'
            self.loop = 0
        elif music == 2:
            self.music = 'music/pacman_intermission.wav'
            self.loop = -1
        elif music == 3:
            self.music = 'music/pacman_eatfruit.wav'
            self.loop = 0
        elif music == 4:
            pygame.mixer.music.stop()
            return

        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(self.loop)

    def game_title(self):
        self.title = pygame.image.load('images/title.png')
        self.screen_width = self.title.get_width()
        self.title_x = self.screen_width/2 + self.screen_width/2
        self.title_rect = self.title.get_rect(topleft=(self.title_x, 35))
        self.screen.blit(self.title, self.title_rect)

    def render_play_button(self):
        self.play = Button(self.screen, self.play_button, self.play_y)
        self.play.draw_button()

    def render_score_button(self):
        self.score_button = Button(self.screen, self.scores_button, self.scores_y)
        self.score_button.draw_button()

    def draw_start_screen(self):
        self.screen.fill(self.bg_color, self.screen_rect)
        self.game_title()
        self.render_play_button()
        self.render_score_button()

    def start_animation(self):
        self.current = 0
        self.update_path_name('right')
        self.pacman.rect.centerx = -30
        self.pacman.rect.centery = 400
        self.red.rect.centerx = -115
        self.red.rect.centery = 410
        self.blue.rect.centerx = -155
        self.blue.rect.centery = 410
        self.pink.rect.centerx = -195
        self.pink.rect.centery = 410
        self.orange.rect.centerx = -235
        self.orange.rect.centery = 410
        self.star.position.x = 900
        self.star.update()
        self.state = True
        self.intro = False
        self.name = False
        self.eat = False

    def animate(self):
        self.pacman.image = self.pacman.images[self.pacman.timer.frame_index()]
        self.red.image = self.red.images[self.red.timer.frame_index()]
        self.blue.image = self.blue.images[self.blue.timer.frame_index()]
        self.pink.image = self.pink.images[self.pink.timer.frame_index()]
        self.orange.image = self.orange.images[self.orange.timer.frame_index()]

        if self.eat:
            self.settings.pacman_speed = 1.2
        else:
            self.settings.pacman_speed = 1

        if self.pacman.rect.centerx < self.settings.screen_width+100 and self.state:
            self.pacman.rect.centerx += self.settings.pacman_speed
            self.blue.rect.centerx += self.settings.ghost_speed
            self.red.rect.centerx += self.settings.ghost_speed
            self.pink.rect.centerx += self.settings.ghost_speed
            self.orange.rect.centerx += self.settings.ghost_speed
            if self.intro:
                self.update_path_name('right')
                if self.current_ghost[self.current].rect.centerx >= 800:
                    self.name = True
            if self.music_started:
                self.music_started = False
                self.intro_music(0)
        elif self.pacman.rect.centerx >= self.settings.screen_width or self.state is False:
            self.pacman.images = self.pacman.frames('left')
            self.pacman.rect.centerx -= self.settings.pacman_speed
            self.blue.rect.centerx -= self.settings.ghost_speed
            self.red.rect.centerx -= self.settings.ghost_speed
            self.pink.rect.centerx -= self.settings.ghost_speed
            self.orange.rect.centerx -= self.settings.ghost_speed
            self.name = False
            if self.intro:
                self.update_path_name('blue-dead')
                if self.music_started:
                    self.intro_music(2)
                    self.music_started = False

            if self.pacman.rect.centerx == -90:
                self.update_current()
                self.state = True
                self.eat = False
                self.music_started = True

        if self.current < 4:
            if self.name and self.ghost_timer >= 0:
                self.introduce_ghost()
        if self.ghost_timer < 0:
            self.name = False
        if self.current_ghost[self.current].rect.centerx >= self.settings.screen_width+20:
            self.current += 1
            self.update_current()

        if self.score_timer > 0:
            self.show_score()

        self.pacman.blitme()
        self.red.blitme()
        self.blue.blitme()
        self.pink.blitme()
        self.orange.blitme()
        self.star_collision()
        self.check_ghost_pacman_col()

    def check_ghost_pacman_col(self):
        red_col = pygame.sprite.collide_rect(self.pacman, self.red)
        if red_col:
            self.score_timer = 50
            self.score = '200'
            self.prep_score()
            self.score_rect.centerx = self.red.rect.centerx
            self.red.rect.centerx = -3000
            self.intro_music(1)
            time.sleep(0.2)
        blue_col = pygame.sprite.collide_rect(self.pacman, self.blue)
        if blue_col:
            self.score_timer = 50
            self.score = '400'
            self.prep_score()
            self.score_rect.centerx = self.blue.rect.centerx
            self.blue.rect.centerx = -3000
            self.intro_music(1)
            time.sleep(0.2)
        pink_col = pygame.sprite.collide_rect(self.pacman, self.pink)
        if pink_col:
            self.score_timer = 50
            self.score = '800'
            self.prep_score()
            self.score_rect.centerx = self.pink.rect.centerx
            self.pink.rect.centerx = -3000
            self.intro_music(1)
            time.sleep(0.2)
        orange_col = pygame.sprite.collide_rect(self.pacman, self.orange)
        if orange_col:
            self.score_timer = 90
            self.score = '1600'
            self.prep_score()
            self.score_rect.centerx = self.orange.rect.centerx
            self.orange.rect.centerx = -3000
            self.intro_music(1)
            time.sleep(0.4)
            self.music_started = True

    def prep_score(self):
        self.score_image = self.font.render(self.score, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centery = 410

    def show_score(self):
        self.score_timer -= 1
        self.screen.blit(self.score_image, self.score_rect)

    def star_collision(self):
        collisions = pygame.sprite.collide_rect(self.pacman, self.star)
        if collisions:
            self.intro = True
            self.state = False
            self.eat = True
            self.intro_music(3)
            self.star.position.x = 3000
            time.sleep(0.2)


            self.music_started = True
        self.star.update()

    def introduce_ghost(self):
        self.pacman.rect.centerx = -3500
        self.ghost_timer -= 1
        self.current_ghost[self.current].rect.centerx = 800
        self.name = pygame.image.load('images/' + self.current_ghost_name)
        self.name_rect = self.name.get_rect(topleft=(540, 390))
        self.screen.blit(self.name, self.name_rect)

    def update_current(self):
        self.pacman.rect.centerx = -3500
        if self.current == 0:
            self.blue.rect.centerx = -3000
            self.red.rect.centerx = -30
            self.pink.rect.centerx = -3000
            self.orange.rect.centerx = -3000
            self.current_ghost_name = 'Blinky/Name/name.png'
        elif self.current == 1:
            self.blue.rect.centerx = -30
            self.red.rect.centerx = -3000
            self.pink.rect.centerx = -3000
            self.orange.rect.centerx = -3000
            self.current_ghost_name = 'Tester/Name/name.png'
        elif self.current == 2:
            self.blue.rect.centerx = -3000
            self.red.rect.centerx = -3000
            self.pink.rect.centerx = -30
            self.orange.rect.centerx = -3000
            self.current_ghost_name = 'Pinky/Name/name.png'
        elif self.current == 3:
            self.blue.rect.centerx = -3000
            self.red.rect.centerx = -3000
            self.pink.rect.centerx = -3000
            self.orange.rect.centerx = -30
            self.current_ghost_name = 'Clyde/Name/name.png'
            self.pacman.images = self.pacman.frames('right')
        else:
            self.start_animation()
        self.ghost_timer = 200
        self.state = True

    def update_path_name(self, path):
        self.blue.images = self.blue.frames(path)
        self.red.images = self.red.frames(path)
        self.pink.images = self.pink.frames(path)
        self.orange.images = self.orange.frames(path)
