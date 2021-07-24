import tkinter as tk

def say_hi():
    print("Hello - !")

root = tk.Tk()

frame1 = tk.Frame(root)
frame2 = tk.Frame(root)

root.title("tkinter frame")

label = tk.Label(frame1, text="Label", justify=tk.LEFT)
label.pack(side=tk.LEFT)

hi_there = tk.Button(frame2, text="say hi ~", command=say_hi)
hi_there.pack()

frame1.pack(padx=1, pady=1)
frame2.pack(padx=10, pady=10)

for fm in ['blue', 'red', 'blue', 'red', 'blue', 'red']:
    tk.Frame(height=20, width=640, bg=fm).pack()
root.mainloop()
