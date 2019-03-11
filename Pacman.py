import pygame

from settings import Settings
from update_game import UpdateGame
from game_stats import GameStats
from nodes import NodeGroup
from points import StarGroup
from maze import Maze
from playable import Pacman
from scoreboard import ScoreBoard
from update_score import Scores
from ghosts import *
from start_screen import Start


def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Pacman Portal by Diana Joya")

    nodes = NodeGroup(screen, "pacmanportalmaze.txt")
    stars = StarGroup(screen, "pacmanportalmaze.txt")
    maze = Maze(screen, settings, "pacmanportalmaze.txt", "brick", "shield")

    stats = GameStats(settings)
    score_board = ScoreBoard(settings, screen, stats)

    ghost = TesterGhost(settings, screen, nodes)
    redenemy = Red(settings, screen, nodes)
    pinkenemy = Pink(settings, screen, nodes)
    orangeenemy = Orange(settings, screen, nodes)

    update_score = Scores(settings, screen, stats, nodes, stars, score_board, redenemy, pinkenemy, orangeenemy, ghost)
    pacman = Pacman(settings, screen, stats, nodes, stars, update_score, redenemy, pinkenemy, orangeenemy, ghost)

    start_screen = Start(settings, screen, stats, pacman, ghost, redenemy, pinkenemy, orangeenemy)
    update = UpdateGame(settings, screen, stats, nodes, stars, maze, pacman, ghost, redenemy, pinkenemy, orangeenemy,
                        score_board, update_score, start_screen)

    while True:
        if stats.game_active:
            pacman.update()
            ghost.update()
            redenemy.update()
            pinkenemy.update()
            orangeenemy.update()
        if stats.game_over:
            start_screen.reset()
            start_screen.start_animation()
        update.check_events()
        update.update_screen()


run_game()
