import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
# 2d solar system model using matplotlib

# constants
AU = 1.495978707e11 # astronomical unit
JUPITER_YEAR = 11.86 # earth years for one orbit
# data for the solar system
# name, orbital period (jupiter years), semi-major axis (m), eccentricity, color, x, y
solar_system = [
    ("Sun", 0, 0, 0, "yellow", 0, 0),
    ("Jupiter", 11.86, 7.78E+11, 0.05, "orange", 0, 0),
    ("Saturn", 29.63, 1.43E+12, 0.06, "yellow", 0, 0),
    ("Uranus", 84.75, 2.88E+12, 0.05, "lightblue", 0, 0),
    ("Neptune", 166.34, 4.52E+12, 0.01, "blue", 0, 0),
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

# background color of the plot
fig.set_facecolor("black")
ax.set_facecolor("black")

# set the x and y limits of the plot
ax.set_xlim(-50, 50)
ax.set_ylim(-50, 50)

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
ax.add_patch(plt.Circle((0, 0), 1.5, color=solar_system[0]["color"]))

# for each planet, create a circle in the correct position with the correct radius
for row in solar_system[1:]:
    # create the orbit
    x_array = np.array([])
    y_array = np.array([])
    for j in range(0, 360*100+1, int(0.36*100)):
        i = j / 100
        radius = (row["semi_major_axis"] * (1-row["eccentricity"]**2)) / (1 + row["eccentricity"] * np.cos(i * np.pi / 180))
        radius = -radius / AU 
        if j == 0:
            start_pos_x = radius * np.cos(i * np.pi / 180)
            start_pos_y = radius * np.sin(i * np.pi / 180)
        
        # calculate the x and y coordinates of the orbit
        x = radius * np.cos((i) * np.pi / 180)
        y = radius * np.sin(i * np.pi / 180)
        x_array = np.append(x_array, x)
        y_array = np.append(y_array, y)
    
    # plot the orbit
    ax.plot(x_array, y_array, ".", color=row["color"], ms=1)
    # print(start_pos_x, start_pos_y)
    # create the circle for the planet
    ax.add_patch(plt.Circle((start_pos_x, start_pos_y), 0.7, color=row["color"]))
   
    # add the name
    # ax.annotate(row["name"], (start_pos_x, start_pos_y), ha="center", va="center", fontsize=7, color='white')
    
# my name in the bottom right corner
plt.gcf().text(0.8, 0.02, "Created by: @AMuh2020", fontsize=10,ha="center", va="center", color="black")


# create a legend for the planets
ax.legend(handles=ax.patches, labels=list(solar_system["name"]), loc="upper right", fontsize=8, facecolor="black", edgecolor="white", labelcolor="white")


# function that updates the title and positions of the planets
def update_animation(frame):
    if frame == 0:
        global time
        time = 0
    for i in range(1, len(solar_system)):
        planet = solar_system[i]
        t = frame *4 / (planet["period"]*(1/JUPITER_YEAR))
        radius = (planet["semi_major_axis"] * (1-planet["eccentricity"]**2)) / (1 + planet["eccentricity"] * np.cos(t * np.pi / 180))
        radius = -radius / AU
        x = radius * np.cos(t * np.pi / 180)
        y = radius * np.sin(t * np.pi / 180)
        # update the planet's position plot
        # print(index, planet["name"], x, y)

        ax.patches[i].center = (x, y)
        
    
    time += 1
    year = round(time * 4 / 360 * JUPITER_YEAR,3)
    # return the artists set
    return ax.patches + [ax.text(0,40 ,f"Solar System: t = {year} years", color="white", fontsize=18, ha="center", va="center")]

f=1440

# create the animation
animation = FuncAnimation(fig, update_animation,frames=f, interval=10, blit=True, repeat=False)

# show the animation
plt.show()

# save the animation
# animation.save("solar_system_outer.gif", writer="imagemagick", fps=30)
