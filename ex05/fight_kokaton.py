import pygame as pg
import sys
import random
import pygame.mixer


class Screen:
    def __init__(self, title, wh, image):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)     # Surface
        self.rct = self.sfc.get_rect()         # Rect
        self.bgi_sfc = pg.image.load(image)    # Surface
        self.bgi_rct = self.bgi_sfc.get_rect() # Rect

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)


class Bird:
    def __init__(self, image: str, size: float, xy):
        self.sfc = pg.image.load(image)    # Surface
        self.sfc = pg.transform.rotozoom(self.sfc, 0, size)  # Surface
        self.rct = self.sfc.get_rect()          # Rect
        self.rct.center = xy

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        key_states = pg.key.get_pressed() # 辞書
        if key_states[pg.K_UP]: 
            self.rct.centery -= 1
        if key_states[pg.K_DOWN]: 
            self.rct.centery += 1
        if key_states[pg.K_LEFT]: 
            self.rct.centerx -= 1
        if key_states[pg.K_RIGHT]: 
            self.rct.centerx += 1
        # # 練習7
        if check_bound(self.rct, scr.rct) != (1, 1): # 領域外だったら
            if key_states[pg.K_UP]: 
                self.rct.centery += 1
            if key_states[pg.K_DOWN]: 
                self.rct.centery -= 1
            if key_states[pg.K_LEFT]: 
                self.rct.centerx += 1
            if key_states[pg.K_RIGHT]: 
                self.rct.centerx -= 1
        self.blit(scr)

    def attack(self):
        return Shot(self)


# class Boss:
#     def __init__(self, image: str, size: float, vxy, scr: Screen):
#         self.sfc = pg.image.load(image)    # Surface
#         self.sfc = pg.transform.rotozoom(self.sfc, 0, size)  # Surface
#         self.rct = self.sfc.get_rect()          # Rect
#         self.rct = self.sfc.get_rect() # Rect
#         self.rct.centerx = random.randint(0, scr.rct.width)
#         self.rct.centery = random.randint(0, scr.rct.height)
#         self.vx, self.vy = vxy
#     def blit(self, scr: Screen):
#         scr.sfc.blit(self.sfc, self.rct)
#     def update(self, scr: Screen):
#         self.rct.move_ip(self.vx, self.vy)
#         yoko, tate = check_bound(self.rct, scr.rct)
#         self.vx *= yoko
#         self.vy *= tate   
#         self.blit(scr)   


class Bomb:
    def __init__(self, color, size, vxy, scr: Screen):
        self.sfc = pg.Surface((2*size, 2*size)) # Surface
        self.sfc.set_colorkey((0, 0, 0)) 
        pg.draw.circle(self.sfc, color, (size, size), size)
        self.rct = self.sfc.get_rect() # Rect
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy # 練習6

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        # 練習6
        self.rct.move_ip(self.vx, self.vy)
        # 練習7
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate   
        # 練習5
        self.blit(scr)          

class Shot:
    def __init__(self, chr: Bird):
        self.sfc = pg.image.load("fig/beam.png")
        self.sfc = pg.transform.rotozoom(self.sfc, 0, 0.1)
        self.rct = self.sfc.get_rect()
        self.rct.midleft = chr.rct.center
        # pg.init()
        # pg.music.load("fig/ビームガンmp3")
        # pg.music.play(1)

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        self.rct.move_ip(+10, 0)
        self.blit(scr)
        if check_bound(self.rct, scr.rct) != (1,1):
            del self
      

def main():
    clock = pg.time.Clock()
    scr = Screen("負けるな！こうかとん", (1400, 700), "fig/地獄.jpg")
    kkt = Bird("fig/6.png", 2.0, (900, 400))
    #boss = Boss("fig/cat_boss_gang.png", 2.0, (1400, 700))
    bkd1 = Bomb((random.randint(0,255),(random.randint(0,255)),(random.randint(0,255))), 10, (+1,+1), scr) #爆弾1
    bkd2 = Bomb((random.randint(0,255),(random.randint(0,255)),(random.randint(0,255))), 10, (+1,+1), scr) #爆弾2
    bkd3 = Bomb((random.randint(0,255),(random.randint(0,255)),(random.randint(0,255))), 10, (+1,+1), scr) #爆弾3

    beam = None

    while True:
        scr.blit()

        # 練習2
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                beam = kkt.attack() #スペースキーでこうかとんが攻撃

        kkt.update(scr)
        bkd1.update(scr)
        bkd2.update(scr)
        bkd3.update(scr)
        if beam:
            beam.update(scr)
        if kkt.rct.colliderect(bkd1.rct): #爆弾1と接触したとき
            return
        if kkt.rct.colliderect(bkd2.rct): #爆弾2と接触したとき
            return
        if kkt.rct.colliderect(bkd3.rct): #爆弾3と接触したとき
            return

        pg.display.update()
        clock.tick(1000)


# 練習7
def check_bound(rct, scr_rct):
    '''
    [1] rct: こうかとん or 爆弾のRect
    [2] scr_rct: スクリーンのRect
    '''
    yoko, tate = +1, +1 # 領域内
    if rct.left < scr_rct.left or scr_rct.right  < rct.right : yoko = -1 # 領域外
    if rct.top  < scr_rct.top  or scr_rct.bottom < rct.bottom: tate = -1 # 領域外
    return yoko, tate


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
