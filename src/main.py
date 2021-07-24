import numpy as np
import matplotlib.pyplot as plt

"""

based on equations from:
    http://airfoiltools.com/airfoil/naca4digit

"""

class GenerateNacaProfile():
    def __init__(self):
        self.typeNACA='2412'
        self.Minit = int(typeNACA[0])
        self.Pinit = int(typeNACA[2])
        self.Tinit = int(typeNACA[-2:])

        self.gridPts = 50
        a0 = 0.2969
        a1 = -0.1260
        a2 = -0.3516
        a3 = 0.2843
        a4 = -0.1015    # Closed trailing edge
        # a4 = -0.1036  # Closed trailing edge

        self.M = self.Minit/100.
        self.P = self.Pinit/10.
        self.T = self.Tinit/100.

        # equally spaced on x-axis
        # x = np.linspace(0,1,gridPts)

        # better spacing at leading Edge:
        self.beta = np.linspace(0, np.pi, self.gridPts)
        self.x = (1 - np.cos(self.beta))/2.

    def get_xc_yc(self):
        self.yc = [0]*self.gridPts
        self.dyc_dx = [0]*self.gridPts

        x = self.x
        yc = self.yc

        for i in range(0,self.gridPts-1):
            if (x[i] >= 0 and x[i] < P):
                self.yc[i] = M/P/P*(2*P*x[i] - x[i]*x[i])
                dyc_dx[i] = (2*M)/(P*P)*(P - x[i])
            elif (x[i] >= P and x[i] <= 1):
                self.yc[i] = M / (1-P)**2 * (1 - 2*P + 2*P*x[i] - x[i] * x[i])
                dyc_dx[i] = (2*M)/(1 - P)**2 * (P - x[i])
        return xc, yc


    def get_xu_yu(self):
        # upper surface points
        xu = self.x - self.yt * np.sin(self.theta)
        yu = self.yc + self.yt * np.cos(self.theta)
        return xu, yu



        self.theta = np.arctan(dyc_dx)

        yt = 5.* T * (a0*np.sqrt(x) \
                  + a1 * x \
                  + a2 * x * x \
                  + a3 * x * x * x \
                  + a4 * x * x * x * x)


        # lower surface points
        xl = x + yt * np.sin(theta)
        yl = yc - yt * np.cos(theta)


    # Plot
    # fig, ax = plt.subplots()
    # ax.grid()
    # ax.axis('equal')
    # ax.set_title('NACA: ' + typeNACA)
    # ax.set_xlim(0,1)
    # ax.plot(x, yc, '--', color='grey', linewidth=1)
    # ax.plot(xu, yu, 'r-', marker='|', markersize=5)
    # ax.plot(xl, yl, 'k-', marker='|', markersize=5)
    # plt.show()

# TK-GUI
import matplotlib
import tkinter as tk
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class mainWindow():
    def __init__(self, masterframe, size):

        (w,h) = size
        self.figure = Figure(size)
        self.axes = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=masterframe)
        self.canvas.get_tk_widget().pack()
        self.axes.text(0.8, 0.95, eqString)

    def plotxy(self, x,y):
        self.axes.plot(x,y)
        self.canvas.draw()

    def clearplot(self):
        self.axes.cla()
        self.canvas.draw()

def plotdata():
    x,y=datgen.getxy()
    pw.plotxy(x,y)

def clear():
    pw.clearplot()
    print("Clear")



if __name__ == "__main__":

    # (xu,yu,xl,yl) = get_nacaProfile()
    (xu,yu,xl,yl) = get_nacaProfile()

    root = tk.Tk()
    mf = tk.Frame()
    pw = mainWindow(mf, (10, 5))
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
