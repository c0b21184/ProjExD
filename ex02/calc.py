import tkinter as tk
import tkinter.messagebox as tkm

def button_click(event): #ボタンが押されたとき
    btn = event.widget
    num = btn["text"]
    #tkm.showinfo("",f"{i}のボタンがクリックされました")
    if (num == "="): #＝が押されたとき
        eqn = entry.get()
        res = eval(eqn)
        entry.delete(0,tk.END)
        entry.insert(tk.END,res)
    
    elif (num == "AC"): #ACが押されたとき
        entry.delete(0,tk.END)
    
    elif (num == "%"): #％が押されたとき
        eqn = entry.get()
        res = eval(eqn)
        res = res * 0.01
        entry.delete(0,tk.END)
        entry.insert(tk.END,res)
    
    elif(num == "+/-"): #+/-が押されたとき
        eqn = entry.get()
        res = eval(eqn)
        res = res * (-1)
        entry.delete(0,tk.END)
        entry.insert(tk.END,res)
    
    else:
        entry.insert(tk.END,num)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("calc")
    #root.geometry("300x500")

    x = 0 #列番号
    y = 1 #行番号

    entry = tk.Entry(root, justify="right", width=14, font=(("Times New Roman", 40)))
    entry.grid(row = 0, column = 0, columnspan = 4)

    for i, num in enumerate(["AC","+/-","%","/",7, 8, 9,"*", 4, 5, 6,"-", 1, 2, 3,"+" ,0, ".", "="]): #ボタン生成
        btn = tk.Button(root,
                        text=f"{num}",
                        width=4,
                        height=2,
                        font=("Times New Roman",30)
                        )
        btn.grid(row=y,column=x)
        btn.bind("<1>",button_click)

        x += 1
        if((i+1)%4 == 0): #ボタンが4つ並んだら改行
            y += 1
            x = 0

    root.mainloop()