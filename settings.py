from vector import Vector


class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (0, 0, 0)

        self.node_width = 13
        self.node_height = 13
        self.up = Vector(0, -1, 0)
        self.down = Vector(0, 1, 0)
        self.left = Vector(-1, 0, 0)
        self.right = Vector(1, 0, 0)

        self.pacman_speed = 1
        self.ghost_speed = 1
        self.star_score = 10
        self.super_star_score = 50

        self.ghost_score = 100
