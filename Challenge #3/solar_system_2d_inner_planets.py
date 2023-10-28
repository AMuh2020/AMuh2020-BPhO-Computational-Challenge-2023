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
    ("Mercury", 0.24, 5.77E+10, 0.21, "brown", 0, 0),
    ("Venus", 0.62, 1.09E+11, 0.02, "orange", 0, 0),
    ("Earth", 1, 1.50E+11, 0.01, "blue", 0, 0),
    ("Mars", 1.88, 2.28E+11, 0.09, "red", 0, 0),
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
fig, ax = plt.subplots(figsize=(10, 10))
fig.set_facecolor("black")
ax.set_facecolor("black")

# set the x and y limits of the plot
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

# change ticks color
ax.tick_params(axis="x", colors="white")
ax.tick_params(axis="y", colors="white")

# grid
ax.grid(True, color="white", alpha=0.5)

# set the title

# set the labels for the axes
ax.set_xlabel("x / (AU)", color="white", fontsize=14)
ax.set_ylabel("y / (AU)", color="white", fontsize=14)

# color of the axes
ax.spines["bottom"].set_color("white")
ax.spines["top"].set_color("white") 
ax.spines["left"].set_color("white")
ax.spines["right"].set_color("white")

# set aspect ratio to 1
ax.set_aspect("equal")
time = 0

# create a circle for the sun
ax.add_patch(plt.Circle((0, 0), 0.1, color=solar_system[0]["color"]))

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
        
        
        x = -radius * np.cos((i) * np.pi / 180)
        y = radius * np.sin(i * np.pi / 180)
        x_array = np.append(x_array, x)
        y_array = np.append(y_array, y)

    ax.plot(x_array, y_array, ".", color=row["color"], ms=1)
    # print(start_pos_x, start_pos_y)
    # create the circle for the planet
    ax.add_patch(plt.Circle((start_pos_x, start_pos_y), 0.02, color=row["color"]))
   
    # add the name
    # ax.annotate(row["name"], (start_pos_x, start_pos_y), ha="center", va="center", fontsize=7, color='white')
    
# my name in the bottom right corner


# for i in range(1, len(solar_system)):

# create a legend for the planets
ax.legend(handles=ax.patches, labels=list(solar_system["name"]), loc="upper right", fontsize=8, facecolor="black", edgecolor="white", labelcolor="white")


# function that updates the title and positions of the planets
def update_animation(frame):
    if frame == 0:
        global time
        time = 0
    for i in range(1, len(solar_system)):
        planet = solar_system[i]
        t = frame / planet["period"]
        radius = (planet["semi_major_axis"] * (1-planet["eccentricity"]**2)) / (1 + planet["eccentricity"] * np.cos(t * np.pi / 180))
        radius = -radius / AU
        x = radius * np.cos(t * np.pi / 180)
        y = radius * np.sin(t * np.pi / 180)
        # update the planet's position plot
        # print(index, planet["name"], x, y)

        ax.patches[i].center = (x, y)
        # print(i,planet["name"], x, y)
        # return the artists set
    
    time += 1
    year = round(time / 360,3)
    return ax.patches + [ax.text(0,1.75 ,f"Solar System: t = {year} years", color="white", fontsize=18, ha="center", va="center")]

f=720
# create the animation
animation = FuncAnimation(fig, update_animation,frames=f, interval=10, blit=True, repeat=False)

plt.gcf().text(0.8, 0.02, "Created by: @AMuh2020", fontsize=10,ha="center", va="center", color="black")
# show the animation
plt.show()

# save the animation
# animation.save("solar_system.gif", writer="Pillow", fps=30)