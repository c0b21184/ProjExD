import tkinter as tk
import maze_maker as mm

def key_down(event):
    global key
    key = event.keysym

def key_up(event):
    global key
    key = ""

def main_proc():
    global cx, cy, mx, my
    delta = {
        ""     : [0, 0],
        "Up"   : [0,-1],
        "Down" : [0,+1],
        "Left" : [-1,0],
        "Right": [+1,0],
    }
    try:
        if(maze_bg[my+delta[key][1]][mx+delta[key][0]] == 0): #移動先が床なら
           my, mx = my + delta[key][1], mx + delta[key][0]
        elif(maze_bg[my+delta[key][11]][mx+delta[key][5]] == 0): #移動先がゴールなら
            tk.showinfo("ゴール","ゴール！！！！") #メッセージ表示
    except:
        pass
    
    cx, cy = mx*100+50, my*100+50
    canvas.coords("tori", cx, cy)
    root.after(100,main_proc)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")
    canvas = tk.Canvas(root, width=1300, height=700, bg="black")
    canvas.pack()

    maze_bg = mm.make_maze(13, 7) #1:壁/0:床を表す二次元配列
    mm.show_maze(canvas, maze_bg) #canvasにmaze_bgを描画

    tori = tk.PhotoImage(file="fig/3.png")
    start = tk.PhotoImage(file="fig/text_start.png")
    box = tk.PhotoImage(file="fig/kaizoku_takarabako.png")
    mx, my = 1, 1
    cx, cy = mx*100+50, my*100+50
    sx, sy = 100, 100
    tx, ty = 1150, 550
    canvas.create_image(cx, cy, image=tori, tag="tori") #こうかとんを描画
    canvas.create_image(sx, sy, image=start, tag="start") #スタートを描画
    canvas.create_image(tx, ty,image=box, tag ="box") #宝箱を描画

    key = ""

    root.bind("<KeyPress>",key_down)
    root.bind("<KeyRelease>",key_up)
    
    main_proc()

    root.mainloop()