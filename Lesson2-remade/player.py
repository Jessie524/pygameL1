import pygame
from Env import*
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load(path.join(img_dir, "ship.png"))
        self.image = pygame.transform.scale(image, (50, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 8
        self.shield = 100
        self.power =1
        self.power_time=0


    def update(self):
        self.keyEventHandling()
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > 5000:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
            self.power_time=0

    def keyEventHandling(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.move(-self.speedx, 0)
        if keystate[pygame.K_RIGHT]:
           self.move(self.speedx, 0)
        # TODO 01.新增上下移動

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def powerup(self):
        self.power+=1
