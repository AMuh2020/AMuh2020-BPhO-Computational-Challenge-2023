from bokeh.plotting import figure, show
from bokeh.embed import file_html
import numpy as np
from matplotlib.animation import FuncAnimation
# 2d solar system model using matplotlib

# constants
AU = 1.495978707e11 # astronomical unit

# data for the solar system
# name, orbital period (years), semi-major axis (AU), eccentricity, radius of epicycle(AU), color, x, y
solar_system_inner = [
    ("Sun", 1, 0, 0, 0, "yellow", 0, 0),
    ("Mercury", 0.2408467, 0.387, 0.21, 0.387098, "grey", 0, 0),
    ("Venus", 0.61519726, 0.723, 0.01, 0.723332, "orange", 0, 0),
    ("Earth", 1, 1, 0.02, 1, "blue", 0, 0),
    ("Mars", 1.8808158, 1.523, 0.09, 1.523679, "red", 0, 0),
]
solar_system_outer = [
    ("Sun", 1, 0, 0, 0, "green", 0, 0),
    ("Jupiter", 11.862615, 5.202, 0.05, 5.2026, "orange", 0, 0),
    ("Saturn", 29.447498, 9.576, 0.06, 9.5549, "yellow", 0, 0),
    ("Uranus", 84.016846, 19.293, 0.05, 19.2184, "lightblue", 0, 0),
    ("Neptune", 164.79132, 30.246, 0.01, 30.11, "blue", 0, 0),
    ("Pluto", 248.00, 39.509, 0.25, 39.48, "grey", 0, 0),
]
def create_orbit():
    solar_system = solar_system_inner


    # convert to numpy array for easier manipulation
    solar_system = np.array(solar_system, dtype=[
        ("name", "U10"),
        ("period", "f8"),
        ("semi_major_axis", "f8"),
        ("eccentricity", "f8"),
        ("radius", "f8"),
        ("color", "U10"),
        ("x", "f8"),
        ("y", "f8"),
    ])
    print(solar_system)

    fixed_planet = solar_system[3]

    # bokeh plot
    p = figure( title="Solar System", x_axis_label="x / (AU)", y_axis_label="y / (AU)")


    # # set the x and y limits of the plot
    # if solar_system[1]["name"] == "Mercury":
    #     ax.set_xlim(-3, 3)
    #     ax.set_ylim(-3, 3)
    #     ax.add_patch(plt.Circle((0, 0), 0.02, color=fixed_planet["color"]))
    # elif solar_system[1]["name"] == "Jupiter":
    #     ax.set_xlim(-40, 40)
    #     ax.set_ylim(-40, 40)
    #     ax.add_patch(plt.Circle((0, 0), 0.5 , color=fixed_planet["color"]))

    # change ticks color

    # grid



    # set the labels for the axes

    # color of the axes
    

    # set aspect ratio to 1


    time = 0

    # title
    # ax.set_title(f"Inner Solar System relative to {fixed_planet['name']}", color="white", fontsize=16)

    for row in solar_system:
        # create the orbit
        x_array = np.array([])
        y_array = np.array([])

        print(row["radius"], row["name"])

        if row == fixed_planet:
            continue
        time_skew = row["period"] / fixed_planet["period"]
        for j in range(0, 36000+1, 1):
            i = j / 10 /4
            # print(i)
            # convert i from degrees to radians
            i = i * np.pi / 180
            # print(i,int(0.36*100))
            radius = (row["semi_major_axis"] * AU * (1-row["eccentricity"]**2)) / (1 + row["eccentricity"] * np.cos((2 * np.pi/ time_skew) * i))
            # radius = row["radius"]
            radius_fixed = (fixed_planet["semi_major_axis"]* AU * (1-fixed_planet["eccentricity"]**2)) / (1 + fixed_planet["eccentricity"] * np.cos((2 * np.pi) * i)) / AU
            # print(radius_fixed)
            sun_x = radius_fixed * np.cos((2 * np.pi) * i)
            sun_y = radius_fixed * np.sin((2 * np.pi) * i)
            
            radius = -radius / AU 
            
            # (2 * np.pi/ time_skew) * i
            # sun_x_position = 
            if row["name"] == "Sun":
                x = sun_x
                y = sun_y
                # print(x,y)
            else:
                x = radius * np.cos((2 * np.pi/ time_skew) * i) - sun_x 
                y = radius * np.sin((2 * np.pi/ time_skew) * i) - sun_y 
            x_array = np.append(x_array, x)
            y_array = np.append(y_array, y)
            

        p.line(x_array, y_array, line_width=1, color=row["color"], legend_label=row["name"])

        # plot the planet bokeh
        p.circle(0, 0, radius=0.03, color=fixed_planet["color"], legend_label=fixed_planet["name"])
        
        
    
        
    # my name in the bottom right corner bokeh
    # p.text(0.9, 0.1, "Created by: \n\n\n The Solar System\ by @AMuh2020", color="white", text_font_size="10pt", text_align="center")
    html = file_html(p, title="Solar system relative orbits")
    show(p)
    return html

create_orbit()