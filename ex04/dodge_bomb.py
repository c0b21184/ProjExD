import pygame as pg
import sys
import random
import tkinter as tk

def main():
    clock = pg.time.Clock()

    #練習1
    pg.display.set_caption("逃げろ！こうかとん")
    screen_sfc = pg.display.set_mode((1300, 700)) #Surface
    screen_rct = screen_sfc.get_rect() #Rect
    bgimg_sfc = pg.image.load("fig/地獄.jpg") #Surface
    bgimg_rct = bgimg_sfc.get_rect() #rect
    screen_sfc.blit(bgimg_sfc, bgimg_rct)

    #練習3
    kkimg_sfc = pg.image.load("fig/6.png") #Surface
    kkimg_sfc = pg.transform.rotozoom(kkimg_sfc, 0, 2.0) #Surface
    kkimg_rct = kkimg_sfc.get_rect() #Rect
    kkimg_rct.center = 600, 300 #こうかとんを表示する

    #練習5
    bmimg_sfc1 = pg.image.load("fig/bakudan.png") #Surface
    bmimg_sfc1 = pg.transform.rotozoom(bmimg_sfc1,0, 0.3) #Surface
    bmimg_rct1 = bmimg_sfc1.get_rect() #Rect
    bmimg_rct1.centerx = random.randint(0, screen_rct.width)
    bmimg_rct1.centery = random.randint(0, screen_rct.height) #爆弾1を表示

    bmimg_sfc2 = pg.image.load("fig/bakudan.png")#Surface
    bmimg_sfc2 = pg.transform.rotozoom(bmimg_sfc2,0, 0.3)#Surface
    bmimg_rct2 = bmimg_sfc2.get_rect() #rect
    bmimg_rct2.centerx = random.randint(0, screen_rct.width)
    bmimg_rct2.centery = random.randint(0, screen_rct.height) #爆弾2を表示

    #練習6
    vx1, vy1 = +1, +1
    vx2, vy2 = +1, +1

    while True:
        screen_sfc.blit(bgimg_sfc, bgimg_rct) #Surfaceに貼り付け

        #練習2
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        
        #練習4
        key_states = pg.key.get_pressed()
        if key_states[pg.K_UP]     == True :kkimg_rct.centery -= 1
        if key_states[pg.K_DOWN]   == True :kkimg_rct.centery += 1
        if key_states[pg.K_LEFT]   == True :kkimg_rct.centerx -= 1
        if key_states[pg.K_RIGHT]  == True :kkimg_rct.centerx += 1

        #練習7
        if check_bound(kkimg_rct, screen_rct) != (1, 1):
            if key_states[pg.K_UP]     == True :kkimg_rct.centery += 1
            if key_states[pg.K_DOWN]   == True :kkimg_rct.centery -= 1
            if key_states[pg.K_LEFT]   == True :kkimg_rct.centerx += 1
            if key_states[pg.K_RIGHT]  == True :kkimg_rct.centerx -= 1
        screen_sfc.blit(kkimg_sfc, kkimg_rct)

        #練習6
        bmimg_rct1.move_ip(vx1, vy1)
        bmimg_rct2.move_ip(vx2, vy2)

        #練習5
        screen_sfc.blit(bmimg_sfc1, bmimg_rct1)
        screen_sfc.blit(bmimg_sfc2, bmimg_rct2)

        #練習7
        yoko, tate = check_bound(bmimg_rct1, screen_rct)
        vx1 *= yoko
        vy1 *= tate

        yoko, tate = check_bound(bmimg_rct2, screen_rct)
        vx2 *= yoko
        vy2 *= tate

        #練習8
        if kkimg_rct.colliderect(bmimg_rct1): #衝突判定
            root = tk()
            root.showinfo("ゲームオーバー","ゲームオーバー")
            root.mainloop()
        if kkimg_rct.colliderect(bmimg_rct2):
            root = tk()
            root.showinfo("ゲームオーバー","ゲームオーバー")
            root.mainloop()
            

        pg.display.update() #画面を更新
        clock.tick(1000)

def check_bound(rct, scr_rct):
    yoko, tate = +1, +1
    if rct.left < scr_rct.left or scr_rct.right < rct.right     : yoko = -1
    if rct.top  < scr_rct.top  or scr_rct.bottom < rct.bottom   : tate = -1
    return yoko, tate

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
