import pygame


class Portal:
    NUM_FRAMES = 10

    def __init__(self, settings, screen, x, y, color, wait=10):
        self.screen = screen
        self.settings = settings
        self.x, self.y = x, y
        self.color = color
        self.opensize = Portal.NUM_FRAMES

        self.frames(color)

        self.rect = pygame.Rect(x, y, self.opensize, self.opensize)
        self.isopen = False
        self.isclosed = False
        self.portal_opening = pygame.mixer.Sound("music/portal_open.wav")
        self.portal_closing = pygame.mixer.Sound("music/portal_close.wav")

    def frames(self, color):
        self.image = pygame.image.load('images/portal/portal_' + color + '.png')
        self.image_rect = self.image.get_rect()

    def open(self, game):
        other = game.portals[0] if self == game.portals[1] else game.portals[0]
        if self.isopen:    # close open portal of same color and reopen it here
            self.close()
        if self.rect.colliderect(other.rect):   # if opening it will overlap other portal, close other too
            other.close()

        pman = game
        pman.velocity = 1
        s = pygame.Rect(pman.rect.left, pman.rect.top, pman.rect.width, pman.rect.height)
        self.x, self.y = s.x, s.y
        self.rect.x, self.rect.y = self.x, self.y
        pygame.mixer.Sound.play(self.portal_opening)
        self.isopen = True
        self.isclosed = False

    def close(self):
        if self.isclosed: return

        pygame.mixer.Sound.play(self.portal_closing)
        self.isopen = False
        self.isclosed = True

    def collide_with(self, rect):
        k = 4    # force tiny overlap
        ssmaller = self.rect.inflate(rect.width/k, rect.height/k)
        rsmaller = rect.inflate(rect.width/k, rect.height/k)
        return ssmaller.colliderect(rsmaller)

    @staticmethod
    def attempt_transport(character, game):
        if not (game.portals[0].isopen and game.portals[1].isopen): return False
        char = character
        ocollide = game.portals[0].collide_with(char.rect)
        bcollide = game.portals[1].collide_with(char.rect)
        if (not ocollide and not bcollide): return False

        other = game.portals[1] if ocollide else game.portals[0]
        char.rect.x, char.rect.y = other.rect.x, other.rect.y
        other.close()
        return True

    def blitme(self):
        if not self.isopen and not self.isclosed:
            return
        self.screen.blit(self.image, self.image_rect)
