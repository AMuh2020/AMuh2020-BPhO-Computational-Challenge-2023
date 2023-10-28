import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
# 2d solar system model using matplotlib

# constants
AU = 1.495978707e11 # astronomical unit

# data for the solar system
# name, orbital period (years), semi-major axis (m), eccentricity, elliptical inclination angle, color, x, y, z
solar_system = [
    ("Sun", 0, 0, 0, 0, "yellow", 0, 0, 0),
    ("Mercury", 0.24, 5.77E+10, 0.21, 7.00, "brown", 0, 0, 0),
    ("Venus", 0.62, 1.09E+11, 0.02, 3.39, "orange", 0, 0, 0),
    ("Earth", 1, 1.50E+11, 0.01, 0.00, "blue", 0, 0, 0),
    ("Mars", 1.88, 2.28E+11, 0.09, 1.85, "red", 0, 0, 0),
]

# convert to numpy array for easier manipulation
solar_system = np.array(solar_system, dtype=[
    ("name", "U10"),
    ("period", "f8"),
    ("semi_major_axis", "f8"),
    ("eccentricity", "f8"),
    ("inclination", "f8"),
    ("color", "U10"),
    ("x", "f8"),
    ("y", "f8"),
    ("z", "f8"),
])
print(solar_system)
# create a figure and axes
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(projection='3d')


# background color of the plot
fig.set_facecolor("black")
ax.set_facecolor("black")

# set the x and y limits of the plot
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-0.5, 0.5)

# change ticks color
ax.tick_params(axis="x", colors="white")
ax.tick_params(axis="y", colors="white")
ax.tick_params(axis="z", colors="white")

# grid
ax.grid(True, color="white", alpha=0.5)

# set the labels for the axes
ax.set_xlabel("x / (AU)", color="white", fontsize=14)
ax.set_ylabel("y / (AU)", color="white", fontsize=14)
ax.set_zlabel("z / (AU)", color="white", fontsize=14)

# color of the axes
ax.spines["bottom"].set_color("white")
ax.spines["top"].set_color("white") 
ax.spines["left"].set_color("white")
ax.spines["right"].set_color("white")

# remove grid lines
# ax.grid(False)

# color of the plot background
ax.xaxis.set_pane_color((0, 0, 0, 0))
ax.yaxis.set_pane_color((0, 0, 0, 0))
ax.zaxis.set_pane_color((0, 0, 0, 0))

# set aspect ratio to 1
ax.set_aspect("equal")
time = 0

# my name in the bottom right corner
ax.text2D(0.8, 0.2, f"Created by: @AMuh2020", fontsize=10,ha="center", va="center", color="white", transform=ax.transAxes)

# create a point for the sun
ax.plot(0, 0, 0, ".", color=solar_system[0]["color"], ms=20)

# for each planet, create a circle in the correct position with the correct radius
planet_objects = []
for planet in solar_system[1:]:
    # create the orbit
    x_array = np.array([])
    y_array = np.array([])
    z_array = np.array([])
    for j in range(0, 360*100+1, int(0.36*100)):
        i = j / 100
        radius = (planet["semi_major_axis"] * (1-planet["eccentricity"]**2)) / (1 + planet["eccentricity"] * np.cos(i * np.pi / 180))
        radius = radius / AU 
        x = radius * np.cos(i * np.pi / 180)
        y = radius * np.sin(i * np.pi / 180)

        
        
        # calculate the x and z coordinates of the orbit
        x_prime = x * np.cos(planet["inclination"] * np.pi / 180)
        z_prime = x * np.sin(planet["inclination"] * np.pi / 180) 

        if j == 0:
            start_pos_x = x_prime
            start_pos_y = y
            start_pos_z = z_prime
        
        x_array = np.append(x_array, x_prime)
        y_array = np.append(y_array, y)
        z_array = np.append(z_array, z_prime)
    # plot the orbit
    ax.plot(x_array, y_array, z_array, ".", color=planet["color"], ms=1)
    # create plot for planet
    planet_plot = ax.plot(start_pos_x,start_pos_y, start_pos_z, ".", color=planet["color"], ms=10)
    planet_objects.append(planet_plot)
    

# create a legend for the planets
# ax.legend(handles=, labels=list(solar_system["name"]), loc="upper right", fontsize=8, facecolor="black", edgecolor="white", labelcolor="white")


# function that updates the title and positions of the planets
def update_animation(frame):
    # intialise time to 0
    if frame == 0:
        global time
        time = 0
    for i in range(1, len(solar_system)):
        # get the planet
        planet = solar_system[i]
        # calculate the time of the planets position relative to its orbital period
        t = frame / planet["period"]
        # calculate the radius of the planet
        radius = (planet["semi_major_axis"] * (1-planet["eccentricity"]**2)) / (1 + planet["eccentricity"] * np.cos(t * np.pi / 180))
        # convert to AU
        radius = radius / AU

        # calculate the x and y
        x = radius * np.cos(t * np.pi / 180)
        y = radius * np.sin(t * np.pi / 180)

        # calculate the x and z coordinates of the orbit
        x_prime = x * np.cos(planet["inclination"] * np.pi / 180)
        z_prime = x * np.sin(planet["inclination"] * np.pi / 180) 
        # get the planets position plot
        planet_plot = planet_objects[i-1][0]

        # update the planet's position
        planet_plot.set_data(x_prime, y)
        planet_plot.set_3d_properties(z_prime)

        
    # update the time
    time += 1
    year = round(time / 360,3)
    # return the artists set and the title
    return [planet_artist[0] for planet_artist in planet_objects] + [ax.text2D(0.5, 0.7, f"Solar System: {year} years", fontsize=10,ha="center", va="center", color="white", transform=ax.transAxes)]

# number of frames to animate, 360 frames is one orbit of earth
f=720
# create the animation
animation = FuncAnimation(fig, update_animation,frames=f, interval=10, blit=True, repeat=False)


# show the animation
plt.show()

# save the animation
# animation.save("solar_system.gif", writer="Pillow", fps=30)