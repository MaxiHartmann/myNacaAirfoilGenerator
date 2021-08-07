import numpy as np
import matplotlib.pyplot as plt

"""

based on equations from:
    http://airfoiltools.com/airfoil/naca4digit

"""

typeNACA='2412'
aoa = -5 * np.pi/180

Minit = int(typeNACA[0])
Pinit = int(typeNACA[2])
Tinit = int(typeNACA[-2:])

gridPts = 50
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

# transform coordinates with angle of attack
def rotate(x,y,phi):
    x_new = x*np.cos(phi) - y*np.sin(phi)
    y_new = x*np.sin(phi) + y*np.cos(phi)
    return x_new, y_new

(xl, yl) = rotate(xl, yl, aoa)
(xu, yu) = rotate(xu, yu, aoa)
(x, yc) = rotate(x, yc, aoa)

# Plot
fig, ax = plt.subplots()
# ax.grid()
ax.axis('equal')
# ax.set_title('NACA: ' + typeNACA)
ax.set_xlim(0,1)
ax.plot(x, yc, '--', color='grey', linewidth=1)
ax.plot(xu, yu, 'r-', marker='|', markersize=5)
ax.plot(xl, yl, 'k-', marker='|', markersize=5)
# ax.fill_between(xu, yu, color='grey')
# ax.fill_between(xl, yl, alpha=0.5, color='grey')
ax.fill_between(x, yu, yl, color='green')
plt.show()
