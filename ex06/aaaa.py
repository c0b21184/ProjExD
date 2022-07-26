import tkinter
import math
import tkinter.messagebox as tkm
import pygame as pg

NUM_H_BLOCK = 10  # ブロッックの数（横方向)
NUM_V_BLOCK = 5  # ブロックの数（縦方向）
WIDTH_BLOCK = 40  # ブロックの幅
HEIGHT_BLOCK = 20  # ブロックの高さ
COLOR_BLOCK = "blue"  # ブロックの色

HEIGHT_SPACE = 300  # 縦方向の空きスペース

WIDTH_PADDLE = 280  # パドルの幅
HEIGHT_PADDLE = 20  # パドルの高さ
Y_PADDLE = 50  # パドルの下方向からの位置
COLOR_PADDLE = "green"  # パドルの色

RADIUS_BALL = 10  # ボールの半径
COLOR_BALL = "red"  # ボールの色
NUM_BALL = 15  # ボールの数

UPDATE_TIME = 20  # 更新間隔（ms）
count = 0 # 得点

music_wavs=["sound/game.wav","sound/gameover.wav","sound/gameclear.wav"]  #音データ


class Ball:
    def __init__(self, x, y, radius, x_min, y_min, x_max, y_max):
        '''ボール作成'''

        # 位置と半径と移動可能範囲を設定
        self.x = x
        self.y = y
        self.r = radius
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        # 一度に移動する距離（px）
        self.speed = 10

        # 移動方向を設定
        self.angle = math.radians(30)
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)

    def getCoords(self):
        '''左上の座標と右下の座標の取得'''

        return (self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)

    def move(self):
        '''移動'''

        # 移動方向に移動
        self.x += self.dx
        self.y += self.dy

        if self.x < self.x_min:
            # 左の壁とぶつかった

            # 横方向に反射
            self.reflectH()
            self.x = self.x_min

        elif self.x > self.x_max:
            # 右の壁とぶつかった

            # 横方向に反射
            self.reflectH()
            self.x = self.x_max


    def turn(self, angle):
        '''移動方向をangleに応じて設定'''

        self.angle = angle
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)

    def reflectH(self):
        '''横方向に対して反射'''

        self.turn(math.atan2(self.dy, -self.dx))

    def reflectV(self):
        '''縦方向に対して反射'''

        self.turn(math.atan2(-self.dy, self.dx))

    def getCollisionCoords(self, object):
        '''objectと当たった領域の座標の取得'''

        # 各オブジェクトの座標を取得
        ball_x1, ball_y1, ball_x2, ball_y2 = self.getCoords()
        object_x1, object_y1, object_x2, object_y2 = object.getCoords()

        # 新たな矩形の座標を取得
        x1 = max(ball_x1, object_x1)
        y1 = max(ball_y1, object_y1)
        x2 = min(ball_x2, object_x2)
        y2 = min(ball_y2, object_y2)

        if x1 < x2 and y1 < y2:
            # 始点が終点よりも左上にある

            # 当たった領域の左上座標と右上座標を返却
            return (x1, y1, x2, y2)
        else:

            # 当たっていないならNoneを返却
            return None

    def reflect(self, object): # 宮﨑作成
        '''当たった方向に応じて反射'''

        # 各オブジェクトの座標を取得
        object_x1, object_y1, object_x2, object_y2 = object.getCoords()

        # 重なった領域の座標を取得
        x1, y1, x2, y2 = self.getCollisionCoords(object)

        is_collideV = False
        is_collideH = False

        # どの方向からボールが当たったかを判断
        if self.dx < 0:
            # ボールが左方向に移動中
            if x2 == object_x2:
                # objectの左側と当たった
                is_collideH = True
        else:
            # ボールが右方向に移動中
            if x1 == object_x1:
                # objectの右側と当たった
                is_collideH = True

        if self.dy < 0:
            # ボールが上方向に移動中
            if y2 == object_y2:
                # objectの下側と当たった
                is_collideV = True
        else:
            # ボールが下方向に移動中
            if y1 == object_y1:
                # objectの上側と当たった
                is_collideV = True

        if is_collideV and is_collideH:
            # 横方向と縦方向両方から当たった場合
            if x2 - x1 > y2 - y1:
                # 横方向の方が重なりが大きいので横方向に反射
                self.reflectV()
            elif x2 - x1 < y2 - y1:
                # 縦方向の方が重なりが大きいので縦方向に反射
                self.reflectH()
            else:
                # 両方同じなので両方向に反射
                self.reflectH()
                self.reflectV()

        elif is_collideV:
            # 縦方向のみ当たったので縦方向に反射
            self.reflectV()

        elif is_collideH:
            # 横方向のみ当たったので横方向に反射
            self.reflectH()
    #川畑
    def exists1(self):
        '''画面内に残っているかどうかの確認'''
        return False if 0 > self.y else True 
    #川畑
    def exists2(self):
        return True if self.y < self.y_max else False


class Paddle:
    def __init__(self, x, y, width, height, x_min, y_min, x_max, y_max):
        '''パドル作成'''

        # 中心座標と半径と移動可能範囲を設定
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def getCoords(self):
        '''左上の座標と右下の座標の取得'''

        return (self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2)

    def move(self, mouse_x, mouse_y):
        '''(mouse_x, mouse_y) に移動'''

        # 移動可能範囲で移動
        self.x = min(max(mouse_x, self.x_min), self.x_max)
        self.y = min(max(mouse_y, self.y_min), self.y_max)


class Block:

    def __init__(self, x, y, width, height):
        '''ブロック作成'''

        # 中心座標とサイズを設定
        self.x = x
        self.y = y
        self.w = width
        self.h = height

    def getCoords(self):
        '''左上の座標と右下の座標の取得'''

        return (self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2)


class Breakout:

    def __init__(self, master):
        '''ブロック崩しゲーム起動'''
        self.master = master

        # サイズを設定
        self.width = NUM_H_BLOCK * WIDTH_BLOCK
        self.height = NUM_V_BLOCK * HEIGHT_BLOCK + HEIGHT_SPACE

        # ゲーム開始フラグを設定
        self.is_playing = False

        self.createWidgets()
        self.createObjects()
        self.drawFigures()
        self.setEvents()
    
    #川畑
    def count_time(self): #得点と生存時間を表示する関数
        time = pg.time.get_ticks()
        time = time / 1000
        times = time *10
        score = int(count * 100 - times)
        tkm.showinfo("score",f"あなたの得点は{score}点です")
        tkm.showinfo("time",f"生存時間は{time}秒です")

    #芹澤
    def sound(self,n):    #音データから引数のデータを取り出し音を流す関数
        pg.mixer.init(frequency = 44100)
        pg.mixer.music.load(music_wavs[n])
        pg.mixer.music.play(-1)


    def start(self, event):
        global count
        '''ゲーム開始'''
        self.sound(0)    #ゲームが始まったらbgmを流す
        
        if len(self.blocks) == 0 or len(self.balls) == 0:
            # ゲームクリア or ゲームオーバー時は最初からやり直し

            # キャンバスの図形を全て削除
            self.canvas.delete("all")

            # 全オブジェクトの作り直しと図形描画
            self.createObjects()
            self.drawFigures()
            count = 0

        # ゲーム開始していない場合はゲーム開始
        if not self.is_playing:
            self.is_playing = True
            self.loop()
        else:
            self.is_playing = False

    def loop(self):
        '''ゲームのメインループ'''
        global count

        if not self.is_playing:
            # ゲーム開始していないなら何もしない
            return

        # loopをUPDATE_TIME ms後に再度実行
        self.master.after(UPDATE_TIME, self.loop)

        # 全ボールを移動する
        for ball in self.balls:
            ball.move()

        # ボールが画面外に出たかどうかをチェック
        delete_balls = []
        delete_balls2 = []
        for ball in self.balls:
            if not ball.exists1():
                # 外に出たボールは削除対象リストに入れる(上側)
                delete_balls.append(ball)
            elif not ball.exists2():
                #（下側）
                delete_balls2.append(ball)
                count += 1
        

        for ball in delete_balls:
            # 削除対象リストのボールを削除(上側)
            self.delete(ball)
            self.canvas.create_text(
                self.width // 2, self.height // 2,
                text="GAME OVER",
                font=("", 40),
                fill="red"
            )
            self.is_playing = False
            self.sound(1)
            self.count_time()
        
        
        for ball in delete_balls2:
            #(下側)
            self.delete(ball)

        self.collision()
        self.updateFigures()
        self.result()

    def motion(self, event):
        '''パドルの移動'''

        self.paddle.move(event.x, event.y)

    def delete(self, target):
        '''targetのオブジェクトと図形を削除'''

        # 図形IDを取得してキャンバスから削除
        figure = self.figs.pop(target)
        self.canvas.delete(figure)

        # targetを管理リストから削除
        if isinstance(target, Ball):
            self.balls.remove(target)
        elif isinstance(target, Block):
            self.blocks.remove(target)

    def collision(self):
        '''当たり判定と当たった時の処理'''

        for ball in self.balls:

            collided_block = None  # 一番大きく当たったブロック
            max_area = 0  # 一番大きな当たった領域

            for block in self.blocks:

                # ballとblockとの当たった領域の座標を取得
                collision_rect = ball.getCollisionCoords(block)
                if collision_rect is not None:
                    # 当たった場合

                    # 当たった領域の面積を計算
                    x1, y1, x2, y2 = collision_rect
                    area = (x2 - x1) * (y2 - y1)

                    # 一番大きく当たっているかどうかを判断
                    if area > max_area:
                        # 一番大きく当たった領域の座標を覚えておく
                        max_area = area

                        # 一番大きく当たったブロックを覚えておく
                        collided_block = block

            if collided_block is not None:

                # 一番大きく当たったブロックに対してボールを反射
                ball.reflect(collided_block)

                # 一番大きく当たったブロックを削除
                self.delete(collided_block)

            for another_ball in self.balls:
                if another_ball is ball:
                    # 同じボールの場合はスキップ
                    continue

                # ballとanother_ballとの当たり判定
                if ball.getCollisionCoords(another_ball) is not None:

                    # 当たってたらballを反射
                    ball.reflect(another_ball)

            # ballとself.paddleとの当たり判定
            if ball.getCollisionCoords(self.paddle) is not None:

                # 当たってたらballを反射
                ball.reflect(self.paddle)
    
    #川畑
    def result(self):
        '''ゲームの結果を表示する'''


        if len(self.balls) == 0:
            self.canvas.create_text(
                self.width // 2, self.height // 2,
                text="GAME CLEAR",
                font=("", 40),
                fill="red"
            )
            self.sound(2)
            self.is_playing = False
            self.count_time()

    def setEvents(self):
        '''イベント受付設定'''

        self.canvas.bind("<ButtonPress>", self.start)
        self.canvas.bind("<Motion>", self.motion)

    def createWidgets(self):
        '''必要なウィジェットを作成'''

        # キャンバスを作成
        self.canvas = tkinter.Canvas(
            self.master,
            width=self.width,
            height=self.height,
            highlightthickness=0,
            bg="gray"
        )
        self.canvas.pack(padx=10, pady=10)

    def createObjects(self):
        '''ゲームに登場するオブジェクトを作成'''

        # ボールを作成
        self.balls = []
        for i in range(NUM_BALL):
            x = self.width / NUM_BALL * i + self.width / NUM_BALL / 2
            ball = Ball(
                x, self.height // 2,
                RADIUS_BALL,
                RADIUS_BALL, RADIUS_BALL,
                self.width - RADIUS_BALL, self.height - RADIUS_BALL
            )
            self.balls.append(ball)

        # パドルを作成 宮﨑作成
        self.paddle = Paddle(
            self.width // 2, self.height - Y_PADDLE,
            WIDTH_PADDLE, HEIGHT_PADDLE,
            WIDTH_PADDLE // 2, self.height - Y_PADDLE,
            self.width - WIDTH_PADDLE // 2, self.height - Y_PADDLE
        )

        # ブロックを作成
        self.blocks = []
        for v in range(NUM_V_BLOCK):
            for h in range(NUM_H_BLOCK):
                block = Block(
                    h * WIDTH_BLOCK + WIDTH_BLOCK // 2,
                    v * HEIGHT_BLOCK + HEIGHT_BLOCK // 2,
                    WIDTH_BLOCK,
                    HEIGHT_BLOCK
                )
                self.blocks.append(block)

    def drawFigures(self):
        '''各オブジェクト毎に図形を描画'''

        # オブジェクト図形を関連づける辞書
        self.figs = {}

        # ボールを描画
        for ball in self.balls:
            x1, y1, x2, y2 = ball.getCoords()
            figure = self.canvas.create_oval(
                x1, y1, x2, y2,
                fill=COLOR_BALL
            )
            self.figs[ball] = figure

        # パドルを描画
        x1, y1, x2, y2 = self.paddle.getCoords()
        figure = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=COLOR_PADDLE
        )
        self.figs[self.paddle] = figure

        # ブロックを描画
        for block in self.blocks:
            x1, y1, x2, y2 = block.getCoords() 
            figure = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=COLOR_BLOCK
            )
            self.figs[block] = figure

    def updateFigures(self):
        '''新しい座標に図形を移動'''

        # ボールの座標を変更
        for ball in self.balls:
            x1, y1, x2, y2 = ball.getCoords()
            figure = self.figs[ball]
            self.canvas.coords(figure, x1, y1, x2, y2)

        # パドルの座標を変更
        x1, y1, x2, y2 = self.paddle.getCoords()
        figure = self.figs[self.paddle]
        self.canvas.coords(figure, x1, y1, x2, y2)


app = tkinter.Tk()
Breakout(app)
pg.init()
app.mainloop()