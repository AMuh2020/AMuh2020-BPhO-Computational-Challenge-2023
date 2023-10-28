# orbit angle vs time
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

def angle_vs_time(t, P, ecc, theta0):
    dtheta = 1/1000

    # number of orbits
    N = int(round(t[-1]/P, 0))
    # print(N)
    # array of polar angles
    theta = np.arange(theta0, (2*np.pi*N + theta0), dtheta)

    # evaluate integrand of time integral
    integrand = 1/((1-ecc*np.cos(theta))**2)

    # simpson's rule coefficients
    a = np.ones(len(integrand))
    a[1::2] = 4
    a[2::2] = 2
    a[-1] = 1

    # calculate array of time
    time = P*((1-ecc**2)**(3/2))*(1/(2*np.pi))*dtheta*(1/3)*np.cumsum(a*integrand)
    
    # interpolate polar angles for each time
    theta = np.interp(t, time, theta)

    return theta

# creat plot
fig, ax = plt.subplots(1, 1)


# time array
t = np.linspace(0, 800, 1000)

# angle vs time for eccentric orbit
theta = angle_vs_time(t, 248.348, 0.25, 0)
ax.plot(t, theta)

# angle vs time for circular orbit
theta = angle_vs_time(t, 248.348, 0, 0)
ax.plot(t, theta)

# set axis labels
ax.set_xlabel("Time / (years)")
ax.set_ylabel("Orbit angle / (radians)")

# set axis limits
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

# my name in the bottom right corner
plt.gcf().text(0.8, 0.02, "Created by: @AMuh2020", fontsize=10,ha="center", va="center", color="black")

# show plot
plt.show()