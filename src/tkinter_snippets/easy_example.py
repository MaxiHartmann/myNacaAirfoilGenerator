import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np


root = tkinter.Tk()
root.wm_title("Embedding in Tk")


fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def _plot_graph(a1, a2, a3):

    t = np.arange(0, 3, .1)
    ax.plot(t, a1*t**2 + a2 * t * a3, 'r.')
    
    canvas.draw()
    
    # toolbar = NavigationToolbar2Tk(canvas, root)
    # toolbar.update()
    # canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


# def on_key_press(event):
#     print("you pressed {}".format(event.key))
#     key_press_handler(event, canvas, toolbar)
# 
# 
# canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def _update():
    a1 = float(entry_a1.get())
    a2 = float(entry_a2.get())
    a3 = float(entry_a3.get())
    _plot_graph(a1,a2, a3)

def _clear():
    ax.cla()
    canvas.draw()

button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)
button_update = tkinter.Button(master=root, text="Update", command=_update)
button_update.pack(side=tkinter.BOTTOM)
button_clear = tkinter.Button(master=root, text="Clear", command=_clear)
button_clear.pack(side=tkinter.BOTTOM)
entry_a1 = tkinter.Entry(master=root)
entry_a1.pack(side=tkinter.BOTTOM)
entry_a2 = tkinter.Entry(master=root)
entry_a2.pack(side=tkinter.BOTTOM)
entry_a3 = tkinter.Entry(master=root)
entry_a3.pack(side=tkinter.BOTTOM)


tkinter.mainloop()
