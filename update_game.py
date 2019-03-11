import sys
import pygame

from start_screen import Start


class UpdateGame:
    def __init__(self, settings, screen, stats, nodes, stars, maze, pacman, ghost, redenemy, pinkenemy, orangeenemy,
                 score_board, update_score, start_screen):
        self.screen = screen
        self.settings = settings
        self.stats = stats
        self.nodes = nodes
        self.stars = stars
        self.maze = maze
        self.score_board = score_board
        self.update_score = update_score
        self.pacman = pacman
        self.ghost = ghost
        self.redenemy = redenemy
        self.pinkenemy = pinkenemy
        self.orangeenemy = orangeenemy
        self.start_screen = start_screen

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)

        if self.stats.game_active:
            self.maze.blit()
            # self.nodes.render()
            self.stars.render()
            self.pacman.blitme()
            self.ghost.blitme()
            self.redenemy.blitme()
            self.pinkenemy.blitme()
            self.orangeenemy.blitme()
            self.update_score.show_score()
        if not self.stats.game_active:
            self.start_screen.draw_start_screen()
            self.start_screen.animate()
        if self.stats.sb_active:
            self.score_board.draw_scoreboard_screen()

        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            self.event = event
            if self.event.type == pygame.QUIT:
                sys.exit()
            elif self.event.type == pygame.KEYDOWN:
                self.check_keydown_events()
            elif self.event.type == pygame.KEYUP:
                self.check_keyup_events()
            elif self.event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                if self.stats.sb_active:
                    self.stats.sb_active = False
                    self.start_screen.start_animation()
                self.check_button()

    def check_keydown_events(self):
        if self.event.key == pygame.K_RIGHT:
            self.pacman.moving_right = True
        elif self.event.key == pygame.K_LEFT:
            self.pacman.moving_left = True
        elif self.event.key == pygame.K_UP:
            self.pacman.moving_up = True
        elif self.event.key == pygame.K_DOWN:
            self.pacman.moving_down = True
        elif self.event.key == pygame.K_SPACE:
            self.pacman.open_portal = True
        elif self.event.key == pygame.K_q or self.event.key == pygame.K_ESCAPE:
            sys.exit()

    def check_keyup_events(self):
        if self.event.key == pygame.K_RIGHT:
            self.pacman.moving_right = False
        elif self.event.key == pygame.K_LEFT:
            self.pacman.moving_left = False
        elif self.event.key == pygame.K_UP:
            self.pacman.moving_up = False
        elif self.event.key == pygame.K_DOWN:
            self.pacman.moving_down = False
        elif self.event.key == pygame.K_SPACE:
            self.pacman.open_portal = False

    def check_button(self):
        play_button = self.start_screen.play.rect.collidepoint(self.mouse_x, self.mouse_y)
        if play_button:
            self.check_play_button()
        score_button = self.start_screen.score_button.rect.collidepoint(self.mouse_x, self.mouse_y)
        if score_button:
            self.check_scores()

    def check_play_button(self):
        if not self.stats.game_active:
            self.start_screen.intro_music(4)
            self.pacman.game_active()
            self.ghost.game_active()
            pygame.mouse.set_visible(False)
            self.stats.game_active = True
            self.play_music()

    def check_scores(self):
        self.stats.sb_active = True

    def play_music(self):
        pygame.init()
        pygame.mixer.init()

        self.music = 'music/pacman_beginning.wav'
        self.loop = 0

        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(self.loop)
