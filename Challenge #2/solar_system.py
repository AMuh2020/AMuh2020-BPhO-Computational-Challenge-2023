import numpy as np
import matplotlib.pyplot as plt

# constants
AU = 1.495978707e11 # astronomical unit


# name, orbital period (years), semi-major axis (m), eccentricity, color
solar_system = [
    ("Sun", 0, 0, 0, "yellow"),
    ("Mercury", 0.24, 5.77E+10, 0.21, "brown"),
    ("Venus", 0.62, 1.08E+11, 0.02, "orange"),
    ("Earth", 1, 1.50E+11, 0.01, "blue"),
    ("Mars", 1.88, 2.28E+11, 0.09, "red"),
    ("Jupiter", 11.86, 7.78E+11, 0.05, "orange"),
    ("Saturn", 29.46, 1.43E+12, 0.05, "yellow"),
    ("Uranus", 84.01, 2.87E+12, 0.05, "lightblue"),
    ("Neptune", 164.8, 4.50E+12, 0.01, "blue"),
    ("Pluto", 248.6, 5.91E+12, 0.25, "brown"),
]

# convert to numpy array for easier manipulation
solar_system = np.array(solar_system, dtype=[
    ("name", "U10"),
    ("period", "f8"),
    ("semi_major_axis", "f8"),
    ("eccentricity", "f8"),
    ("color", "U10"),
])
print(solar_system)
# create a figure and axes
fig, ax = plt.subplots(figsize=(10, 10))

# background color of the plot
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

plt.show()