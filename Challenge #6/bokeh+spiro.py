from bokeh.plotting import figure, show
from bokeh.embed import file_html
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
    ("Venus", 0.62, 1.08E+11, 0.02, "orange", 0, 0),
    ("Earth", 1, 1.50E+11, 0.01, "blue", 0, 0),
    ("Mars", 1.88, 2.28E+11, 0.09, "red", 0, 0),
    ("Jupiter", 11.86, 7.78E+11, 0.05, "orange", 0, 0),
    ("Saturn", 29.46, 1.43E+12, 0.05, "yellow", 0, 0),
    ("Uranus", 84.01, 2.87E+12, 0.05, "lightblue", 0, 0),
    ("Neptune", 164.8, 4.50E+12, 0.01, "blue", 0, 0),
    ("Pluto", 248.6, 5.91E+12, 0.25, "brown", 0, 0),
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
time = 0
def create_spirogram(planet_to_draw,interval):
    planets = []
    for i in range(len(solar_system)):
        if solar_system[i]["name"] in planet_to_draw:
            planets.append(solar_system[i])

    print(planets)
    
    # create a figure and axes bokeh
    p = figure(title=f"Spirogram of {planets[0]['name']} and {planets[1]['name']}", x_axis_label="x / (AU)", y_axis_label="y / (AU)")
    p.background_fill_color = "black"

    

    
    # for each planet, create a circle in the correct position with the correct radius
    for planet in planets:
        # create the orbit
        x_array = np.array([])
        y_array = np.array([])
        for j in range(0, 360*100+1, int(0.36*100)):
            i = j / 100
            radius = (planet["semi_major_axis"] * (1-planet["eccentricity"]**2)) / (1 + planet["eccentricity"] * np.cos(i * np.pi / 180))
            radius = -radius / AU # convert to AU
            
            x = radius * np.cos(i * np.pi / 180)
            y = radius * np.sin(i * np.pi / 180)
            x_array = np.append(x_array, x)
            y_array = np.append(y_array, y)

        # plot the orbit bokeh
        p.line(x_array, y_array, line_width=1, line_color="white")
        
        # print(start_pos_x, start_pos_y)
        # create the circle for the planet
        # planet_patch = p.circle((start_pos_x, start_pos_y), 0.00, color=row["color"],label=row["name"])
    
        # add the name
        # ax.annotate(row["name"], (start_pos_x, start_pos_y), ha="center", va="center", fontsize=7, color='white')



    outermost_planet_period = planets[-1]["period"]



    # number of orbits to animate
    N = 5

    # time_interval = N * 2 * outermost_planet_period / (1234)

    # function that updates the title and positions of the planets
    def run(niter):
        x_line = []
        y_line = []

        for planet in planets:
            # calculate the position of the planet
            t = niter / (planet["period"] * 1/outermost_planet_period )
            
            radius = (planet["semi_major_axis"] * (1-planet["eccentricity"]**2)) / (1 + planet["eccentricity"] * np.cos(t * np.pi / 180))
            radius = -radius / AU
            
            x = radius * np.cos((t) * np.pi / 180)
            y = radius * np.sin((t) * np.pi / 180)
            # update the planet's position plot
            # print(index, planet["name"], x, y)
            
            x_line.append(x)
            y_line.append(y)
            # print(i,planet["name"], x, y)
            # return the artists set
        
        global time
        # each frame is 1 ms
        time += 1
        
        # every time_interval ms, plot line
        if time % interval == 0:
            # bokeh line plot
            p.line(x_line, y_line, line_width=1, line_color="white")

    # name in bottom right corner brokeh
    # p.text(2, -2, "Created by: @AMuh2020", color="white", fontsize=8, ha="center", va="center")


    f=360*N
    # create the animation

    for i in range(f):
        run(i)
        

    html = file_html(p, title="Solar system relative orbits")
    return html

# create_spirogram(["Earth","Venus"], 3)