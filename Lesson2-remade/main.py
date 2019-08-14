import random
from os import path
import pygame
from meteor import Meteor
from player import Player
from begin_state import Begin_state
# TODO Refactor 將參數統一放到另外一個檔案
from Env import*
font_name = pygame.font.match_font('arial')
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(path.join(sound_dir, "bgm.mp3"))
pygame.mixer.music.play(-1)





class Bullet(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(path.join(img_dir, "laser_gun.png"))
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.speedy = 10

    def update(self):
        self.rect.y -= self.speedy
        if self.rect.bottom < 0:
            self.kill()


from explosion import Explosion

class Support(pygame.sprite.Sprite):
    def __init__(self,x,y,type):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load(path.join(img_dir, "shield_gold.png"))
       self.rect = self.image.get_rect()
       self.rect.centerx = x
       self.rect.centery = y
       self.speedy = 8

    def update(self):
       # self.rect.x = self.speedx
       self.rect.y = self.rect.y + self.speedy
       # self.image = pygame.image.load(path.join(img_dir, "shield_gold.png"))





screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.image.load(path.join(img_dir, 'background.png'))
bg_rect = bg.get_rect()
clock = pygame.time.Clock()

meteors = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
supports = pygame.sprite.Group()

last_shot = pygame.time.get_ticks()
now = 0
score = 0
player = Player(WIDTH / 2, HEIGHT - 50)





def newMeteor():
    m = Meteor(meteors, all_sprites)
    meteors.add(m)
    all_sprites.add(m)
for i in range(8):
    newMeteor()

all_sprites.add(bullets)
all_sprites.add(player)
all_sprites.add(meteors)
running = True
sound_pew = pygame.mixer.Sound(path.join(sound_dir, "pew.wav"))


def check_meteor_hit_player():
    global running, meteors
    # TODO 05.修正碰撞偵測的規則
    hits = pygame.sprite.spritecollide(player, meteors, False, pygame.sprite.collide_circle_ratio(0.7))
    if hits:
        for hit in hits:
            hit.kill()
            # print("check_meteor_hit_player")
            newMeteor()
            # TODO 修改死亡的規則，改成扣血扣到0時，遊戲才結束
            player.shield = player.shield-30
            print(player.shield)
            if player.shield <= 0:
                running = False



def check_bullets_hit_meteor():
    global score
    # TODO 05.修正碰撞偵測的規則
    hits = pygame.sprite.groupcollide(meteors, bullets, True, True)
    if hits:
        for hit in hits:
            # TODO 02.修改加分的機制

            score += 1
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(explosion)
            # if random.randint(0,10)>5:
            sup = Support(hit.rect.x,hit.rect.y,1)
            supports.add(sup)
            all_sprites.add(sup)

            hit.kill()
            # print("check_bullets_hit_meteor")
            newMeteor()

            # TODO 04.增加爆炸的動畫

            # TODO 06.擊破隕石會掉出武器或是能量包 武器可以改變攻擊模式 能量包可以回血


def check_support_hit_player():
    hits = pygame.sprite.spritecollide(player, supports, True,pygame.sprite.collide_rect_ratio(0.7))
    for hit in hits:
        player.power += 1

def draw_score():
    font = pygame.font.Font(font_name, 14)
    text_surface = font.render(str(score), True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH / 2, 20)
    screen.blit(text_surface, text_rect)
    pass



def shoot():
    sound_pew.play()
    if player.power > 1:
        bullet1 = Bullet(player.rect.left, player.rect.centery)
        bullets.add(bullet1)
        all_sprites.add(bullet1)
        bullet2 = Bullet(player.rect.right, player.rect.centery)
        bullets.add(bullet2)
        all_sprites.add(bullet2)
    else:
        bullet = Bullet(player.rect.centerx, player.rect.centery)
        bullets.add(bullet)
        all_sprites.add(bullet)




def draw_shield():
    shield_bar = pygame.rect.Rect(10,10,player.shield,30)
    outline_rect = pygame.rect.Rect(10,10,100,30)
    pygame.draw.rect(screen,GREEN,shield_bar)
    pygame.draw.rect(screen, (255,255,255), outline_rect,2)
    pass

gamestate = "begin"
begin_state = Begin_state(screen)
while running:
    # clocks control how fast the loop will execute
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if gamestate == "begin":
        begin_state.keyhandle()
        begin_state.show()
        gamestate = begin_state.updateState()

    elif gamestate == "start":
        # event trigger
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now-last_shot> SHOT_DELAY:
                last_shot = now
                shoot()
        # TODO 新增起始畫面 按下空白鍵才開始遊戲
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #     if event.type == pygame.KEYDOWN:
        #         # TODO 03.修正成子彈可以連發
        #         if event.key == pygame.K_SPACE:
        #

        # update the state of sprites
        check_meteor_hit_player()
        #
        check_bullets_hit_meteor()
        check_support_hit_player()
        all_sprites.update()

        # draw on screen

        # screen.fill(BLACK)
        screen.blit(bg, bg_rect)
        draw_shield()
        draw_score()
        all_sprites.draw(screen)
    # flip to display
    pygame.display.flip()

pygame.quit()
