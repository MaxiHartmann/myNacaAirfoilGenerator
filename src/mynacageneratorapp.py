import tkinter as tk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calc_coordinates(naca, points):
    typeNACA=naca
    gridPts=points

    Minit = int(typeNACA[0])
    Pinit = int(typeNACA[2])
    Tinit = int(typeNACA[-2:])

    a0 = 0.2969
    a1 = -0.1260
    a2 = -0.3516
    a3 = 0.2843
    a4 = -0.1015    # Closed trailing edge
    # a4 = -0.1036  # Closed trailing edge

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

    yc = np.array(yc)
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

    return x, yc, xl, yl, xu, yu

# transform coordinates with angle of attack
def rotate(x,y,phi):
    x_new = x*np.cos(phi) - y*np.sin(phi)
    y_new = x*np.sin(phi) + y*np.cos(phi) 
    return x_new, y_new

class MyNacaGeneratorApp:
    def __init__(self, root):

        # build ui
        self.root = root
        self.root.title("4-Digits NACA Airfoil Generator")
        self.input_frame = tk.Frame(self.root)

        self.typeNACA = '2412'
        self.aoa = 0.0
        self.gridPts = 50

        (x, yc, xl, yl, xu, yu) = calc_coordinates(self.typeNACA, self.gridPts)
        (xl, yl) = rotate(xl, yl, self.aoa)
        (xu, yu) = rotate(xu, yu, self.aoa)
        (x, yc) = rotate(x, yc, self.aoa)

        self.x = x
        self.yc = yc
        self.xl = xl
        self.yl = yl
        self.xu = xu
        self.yu = yu

        # Input: NACA digits
        self.lbl_naca = tk.Label(self.input_frame)
        self.lbl_naca.configure(takefocus=False, text='NACA:')
        self.lbl_naca.grid(column='0', row='0')
        self.ent_naca = tk.Entry(self.input_frame)
        self.typeNACA = tk.StringVar(value='2412')
        self.ent_naca.configure(textvariable=self.typeNACA)
        self.ent_naca.grid(column='1', row='0')

        # Input: Angle of attack
        self.lbl_aoa = tk.Label(self.input_frame)
        self.lbl_aoa.configure(text='Angle of Attack:')
        self.lbl_aoa.grid(column='0', row='1')
        self.ent_aoa = tk.Entry(self.input_frame)
        self.aoa = tk.DoubleVar(value=0.0)
        self.ent_aoa.configure(textvariable=self.aoa)
        self.ent_aoa.grid(column='1', row='1')

        # Input: Number of Points
        self.lbl_nbpts = tk.Label(self.input_frame)
        self.lbl_nbpts.configure(text='Number of points:')
        self.lbl_nbpts.grid(column='0', row='2')
        self.ent_nbpts = tk.Entry(self.input_frame)
        self.gridPts = tk.IntVar(value=100)
        self.ent_nbpts.configure(textvariable=self.gridPts)
        self.ent_nbpts.grid(column='1', row='2')

        # update-button
        self.btn_update = tk.Button(self.input_frame)
        self.btn_update.configure(text='Update')
        self.btn_update.grid(column='0', row='3')
        self.btn_update.configure(command=self.update)
        self.root.bind("<Return>", self.update)

        # save-button
        self.btn_save = tk.Button(self.input_frame)
        self.btn_save.configure(text='Save')
        self.btn_save.grid(column='1', row='3')
        self.btn_save.configure(command=self.save)

        self.input_frame.configure(height='200', padx='10', pady='10', width='200')
        self.input_frame.pack(side='left')
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.configure(background='#ffffff', borderwidth='4', height='400', padx='10')
        self.plot_frame.configure(pady='10', relief='sunken', width='400')
        self.plot_frame.pack(side='right')


        # Main widget
        self.mainwindow = self.root
        self.update()

    def update(self, event=None):
        self.typeNACA = self.ent_naca.get()
        self.aoa = float(self.ent_aoa.get())*np.pi/180.
        self.gridPts = int(self.ent_nbpts.get())

        self.plot_values()

        return None
    

    def plot_values(self, event=None):
        (x, yc, xl, yl, xu, yu) = calc_coordinates(self.typeNACA, self.gridPts)

        aoa = self.aoa

        (xl, yl) = rotate(xl, yl, aoa)
        (xu, yu) = rotate(xu, yu, aoa)
        (x, yc) = rotate(x, yc, aoa)

        # Plotting
        fig, ax = plt.subplots()
        ax.grid()
        ax.axis('equal')
        ax.set_xlim(0,1)
        ax.plot(x, yc, '--', color='grey', linewidth=1)
        ax.plot(xu, yu, 'r-', marker='|', markersize=5)
        ax.plot(xl, yl, 'k-', marker='|', markersize=5)
        ax.set_title("NACA " + self.typeNACA)

        chart = FigureCanvasTkAgg(fig, self.plot_frame)
        chart.get_tk_widget().grid(row=0, column=0)

        return None

    def save(self):
        textoutput = pd.DataFrame({'x': self.x, 'yc': self.yc, 'xl': self.xl, 'yl': self.yl, 'xu': self.xu, 'yu': self.yu})
        textoutput.to_csv("coordinates_NACA_"+self.typeNACA+".csv", sep='\t', index=False, float_format='%.8f')

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = MyNacaGeneratorApp(root)
    app.run()
