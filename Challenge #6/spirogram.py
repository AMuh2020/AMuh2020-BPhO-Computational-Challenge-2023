import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
# 2d solar system model using matplotlib

# constants
AU = 1.495978707e11 # astronomical unit

# data for the solar system
# name, orbital period (years), semi-major axis (m), eccentricity, color, x, y
solar_system = [
    ("Sun", 0, 0, 0, "yellow", 0, 0),
    # ("Mercury", 0.24, 5.77E+10, 0.21, "brown", 0, 0),
    ("Venus", 0.62, 1.08E+11, 0.02, "orange", 0, 0),
    ("Earth", 1, 1.50E+11, 0.01, "blue", 0, 0),
    # ("Mars", 1.88, 2.28E+11, 0.09, "red", 0, 0),
    # ("Jupiter", 11.86, 7.78E+11, 0.05, "orange", 0, 0),
    # ("Saturn", 29.46, 1.43E+12, 0.05, "yellow", 0, 0),
    # ("Uranus", 84.01, 2.87E+12, 0.05, "lightblue", 0, 0),
    # ("Neptune", 164.8, 4.50E+12, 0.01, "blue", 0, 0),
    # ("Pluto", 248.6, 5.91E+12, 0.25, "brown", 0, 0),
]

# convert to numpy array for easier manipulation
solar_system = np.array(solar_system, dtype=[
    ("name", "U10"),
    ("period", "f8"),
    ("semi_major_axis", "f8"),
    ("eccentricity", "f8"),
    ("color", "U10"),
    ("x", "f8"),
    ("y", "f8"),
])
print(solar_system)
# create a figure and axes
fig = plt.figure()
ax = plt.axes()

# background color of the plot
fig.set_facecolor("white")
ax.set_facecolor("white")

# remove ticks and tick labels
ax.set_xticks([])
ax.set_yticks([])
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.tick_params(axis="both", which="both", length=0)

# color of the axes
ax.spines["bottom"].set_color("white")
ax.spines["top"].set_color("white") 
ax.spines["left"].set_color("white")
ax.spines["right"].set_color("white")

# set aspect ratio to 1
ax.set_aspect("equal")
time = 1

# legend for the planets

# array for planet patches
planet_patches = []
planet_names = []
# for each planet, create a circle in the correct position with the correct radius
for row in solar_system[1:]:
    # create the orbit
    x_array = np.array([])
    y_array = np.array([])
    for j in range(0, 360*100+1, int(0.36*100)):
        i = j / 100
        radius = (row["semi_major_axis"] * (1-row["eccentricity"]**2)) / (1 + row["eccentricity"] * np.cos(i * np.pi / 180))
        radius = radius / AU 
        if j == 0:
            start_pos_x = -radius * np.cos(i * np.pi / 180)
            start_pos_y = radius * np.sin(i * np.pi / 180)
        
        
        x = -radius * np.cos(i * np.pi / 180)
        y = radius * np.sin(i * np.pi / 180)
        x_array = np.append(x_array, x)
        y_array = np.append(y_array, y)

    ax.plot(x_array, y_array, ".", color=row["color"], ms=1)
    # print(start_pos_x, start_pos_y)
    # create the circle for the planet
    planet_patch = plt.Circle((start_pos_x, start_pos_y), 0.00, color=row["color"])
    ax.add_patch(planet_patch)
    planet_patches.append(planet_patch)

    planet_names.append(row["name"])
   
    # add the name
    # ax.annotate(row["name"], (start_pos_x, start_pos_y), ha="center", va="center", fontsize=7, color='white')


plt.gcf().text(0.5, 0.9, f"{planet_names[0]} and {planet_names[1]}", fontsize=10,ha="center", va="center", color="black")

# my name in the bottom right corner
plt.gcf().text(0.8, 0.02, "Created by: @AMuh2020", fontsize=10,ha="center", va="center", color="black")


outermost_planet_period = solar_system[-1]["period"]



# number of orbits to animate
N = 10

time_interval = N * 2 * outermost_planet_period / (1234)
while int(time_interval * 100) > 10:
    time_interval = time_interval / 10


if int(time_interval * 100) <= 1:
    time_interval = time_interval + 0.01
print(time_interval)
print(int(time_interval * 100))
# function that updates the title and positions of the planets
def update_animation(frame):
    x_line = []
    y_line = []

    for i in range(1, len(solar_system)):
        planet = solar_system[i]
        t = frame / (planet["period"] * 1/outermost_planet_period )
        
        radius = (planet["semi_major_axis"] * (1-planet["eccentricity"]**2)) / (1 + planet["eccentricity"] * np.cos(t * np.pi / 180))
        radius = -radius / AU
        
        x = radius * np.cos((t) * np.pi / 180)
        y = radius * np.sin((t) * np.pi / 180)
        # update the planet's position plot
        # print(index, planet["name"], x, y)
        
        planet_patches[i-1].center = (x, y)
        x_line.append(x)
        y_line.append(y)
        # print(i,planet["name"], x, y)
        # return the artists set
    
    global time
    # each frame is 1 ms
    time += 1
    
    # every time_interval ms, plot line
    if time % int(time_interval * 100) == 0:
        ax.plot(x_line, y_line, color="black", linewidth=0.5)

    return ax.lines

f=360*N
# create the animation
animation = FuncAnimation(fig, update_animation,frames=f, interval=10, blit=True, repeat=False)
# print(ax.lines)
# for i in ax.lines:
#     print(i)

# show the animation
plt.show()

# save the animation
# animation.save("solar_system.gif", writer="Pillow", fps=30)

# save figure
# fig1.savefig(f"{planet_names[0]}_{planet_names[1]}_spirograph.png", dpi=300, bbox_inches="tight")
