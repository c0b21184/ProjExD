import tkinter as tk
import tkinter.messagebox as tkm

def button_click(event):
    btn = event.widget
    i = btn["text"]
    tkm.showinfo("",f"{i}のボタンがクリックされました")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("calc")
    #root.geometry("300x500")

    x = 0 #列番号
    y = 0 #行番号

    for i in range(9,-1,-1):
        btn = tk.Button(root,
                        text=i,
                        width=4,
                        height=2,
                        font=("Times New Roman",30)
                        )
        btn.grid(row=y,column=x)
        btn.bind("<1>",button_click)


        x += 1
        if((i-1)%3 == 0):
            y += 1
            x = 0

    root.mainloop()