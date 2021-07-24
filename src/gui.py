import matplotlib
import tkinter as tk
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class PlotWindow():
    def __init__(self, masterframe, size):

        (w,h) = size
        self.figure = Figure(size)
        self.axes = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=masterframe)
        self.canvas.get_tk_widget().pack()
        eqString=r'sin(4x) exp(-nx/10)'
        self.axes.text(0.8, 0.95, eqString)

    def plotxy(self, x,y):
        self.axes.plot(x,y)
        self.canvas.draw()

    def clearplot(self):
        self.axes.cla()
        self.canvas.draw()

class GenerateTestData():
    def __init__(self):
        self.index=0
        self.xmin=0.0
        self.xmax=10.0
        self.nbvalues=500
        
    def getxy(self):
        n=self.index
        n=int(user_input.get())
    
        x=np.linspace(self.xmin, self.xmax, self.nbvalues)
        y=np.sin(4*x)*np.exp(-n*x/10)
        self.index+=1
        return x,y


def plotdata():
    x,y=datgen.getxy()
    pw.plotxy(x,y)

def clear():
    pw.clearplot()
    print("Clear")

if __name__ == "__main__":

    datgen = GenerateTestData()

    root = tk.Tk()
    mf = tk.Frame()
    pw = PlotWindow(mf, (10, 5))
    mf.grid(row=0)

    user_input = tk.StringVar(root)

    bf = tk.Frame()
    b1 = tk.Button(bf, text="Plot", command=plotdata)
    b1.grid(row=1, column=0)
    b2 = tk.Button(bf, text="Clear", command=clear)
    b2.grid(row=1, column=1)
    l1 = tk.Label(bf, text="n = ")
    l1.grid(row=2, column=0)
    entry = tk.Entry(bf, textvariable=user_input)
    entry.grid(row=2, column=1)
    entry.insert(tk.END, "0")
    bf.grid(row=3, column=0)

    root.mainloop()
