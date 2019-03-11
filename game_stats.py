class GameStats:
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()

        self.game_active = False
        self.sb_active = False
        self.game_over = False
        self.lost_life = False
        self.check_end_score = 0

        self.high_score = self.get_high_score()

    def reset_stats(self):
        self.lives_left = 2
        self.score = 0

    def get_high_score(self):
        first = 0
        high_score = 0
        read = open("scores.txt", 'r')
        for line in read:
            if int(line) > first:
                high_score = int(line)
            break
        return high_score
