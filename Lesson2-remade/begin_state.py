import pygame
from Env import *
font_name=pygame.font.match_font('arial')
class Begin_state():
    def __init__(self,surface):
        self.surf = surface
        self.gamestate="begin"
        pass
    def keyhandle(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            self.gamestate = "start"

    def updateState(self):
        return self.gamestate

    def draw_text(self,surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def show(self):
        self.draw_text(self.surf , "SHMUP!", 64, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.surf , "Arrow keys to move,Space to fire", 22,
                       WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.surf , "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
