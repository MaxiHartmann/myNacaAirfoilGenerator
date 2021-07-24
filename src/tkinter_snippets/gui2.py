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

class generate_naca_profile():
    def __init__(self):
        self.typeNACA='2412'
        self.Minit = int(typeNACA[0])
        self.Pinit = int(typeNACA[2])
        self.Tinit = int(typeNACA[-2:])
        self.xmin=0.0
        self.xmax=1.0
        self.gridPts = 50

        a0 = 0.2969
        a1 = -0.1260
        a2 = -0.3516
        a3 = 0.2843
        a4 = -0.1015    # Closed trailing edge
        # a4 = -0.1036  # Closed trailing edge
        
    def getxy(self):
        M = Minit/100.
        P = Pinit/10.
        T = Tinit/100.

        # equally spaced on x-axis
        # x = np.linspace(0,1,gridPts)

        # better spacing at leading Edge:
        beta = np.linspace(0, np.pi/2, gridPts)
        x = (1 - np.cos(beta))

        yc = [0]*gridPts
        dyc_dx = [0]*gridPts

        for i in range(0,gridPts-1):
            if (x[i] >= 0 and x[i] < P):
                yc[i] = M/P/P*(2*P*x[i] - x[i]*x[i])
                dyc_dx[i] = (2*M)/(P*P)*(P - x[i])
            elif (x[i] >= P and x[i] <= 1):
                yc[i] = M / (1-P)**2 * (1 - 2*P + 2*P*x[i] - x[i] * x[i])
                dyc_dx[i] = (2*M)/(1 - P)**2 * (P - x[i])

        theta = np.arctan(dyc_dx)

        yt = 5.* T * (a0*np.sqrt(x) \
                  + a1 * x \
                  + a2 * x * x \
                  + a3 * x * x * x \
                  + a4 * x * x * x * x)

        # upper surface points
        xu = x - yt * np.sin(theta)
        yu = yc + yt * np.cos(theta)

        # lower surface points
        xl = x + yt * np.sin(theta)
        yl = yc - yt * np.cos(theta)
        return xu, yu, xl, yl
                
#     def get_xuyu(self):
#         self.typeNACA=user_input.get()
#     
#         x=np.linspace(self.xmin, self.xmax, self.nbvalues)
#         y=np.sin(4*x)*np.exp(-n*x/10)
#         self.index+=1
#         return xu,yu


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
