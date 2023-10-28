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
    ("Sun", 1, 0, 0, 0, "yellow", 0, 0),
    ("Jupiter", 11.862615, 5.202, 0.05, 5.2026, "orange", 0, 0),
    ("Saturn", 29.447498, 9.576, 0.06, 9.5549, "brown", 0, 0),
    ("Uranus", 84.016846, 19.293, 0.05, 19.2184, "lightblue", 0, 0),
    ("Neptune", 164.79132, 30.246, 0.01, 30.11, "blue", 0, 0),
    ("Pluto", 248.00, 39.509, 0.25, 39.48, "grey", 0, 0),
]
def generate_graph(sol_sys_option, fixed_planet):

    if sol_sys_option == "inner":
        solar_system = solar_system_inner
    elif sol_sys_option == "outer":
        solar_system = solar_system_outer[:5]
    elif sol_sys_option ==  "outer_pluto":
        solar_system = solar_system_outer


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
    # print(solar_system)

    fixed_planet = solar_system[fixed_planet]

    # bokeh plot
    p = figure( title="Solar System", x_axis_label="x / (AU)", y_axis_label="y / (AU)")

    # change title color
    p.title.text_color = "white"

    # plot colors
    p.background_fill_color = "black"
    p.border_fill_color = "black"

    # change outline color
    p.outline_line_color = "white"

    # change axis line colors
    p.axis.axis_line_color = "white"

    # change tick colors
    p.axis.major_tick_line_color = "white"
    p.axis.minor_tick_line_color = "white"

    # change tick labels color
    p.xaxis.major_label_text_color = "white"
    p.yaxis.major_label_text_color = "white"

    # change axis label color
    p.xaxis.axis_label_text_color = "white"
    p.yaxis.axis_label_text_color = "white"
    

    time = 0

    for row in solar_system:
        # initialize the arrays
        x_array = np.array([])
        y_array = np.array([])

        # print(row["radius"], row["name"])

        if row == fixed_planet:
            continue
        time_skew = row["period"] / fixed_planet["period"]
        for j in range(0, 36000+1, 1):
            # calculate the angle
            i = j / 10 /4

            # convert i from degrees to radians
            i = i * np.pi / 180

            # radius of the planet
            radius = (row["semi_major_axis"] * AU * (1-row["eccentricity"]**2)) / (1 + row["eccentricity"] * np.cos((2 * np.pi/ time_skew) * i))
            
            # radius of the fixed planet
            radius_fixed = (fixed_planet["semi_major_axis"]* AU * (1-fixed_planet["eccentricity"]**2)) / (1 + fixed_planet["eccentricity"] * np.cos((2 * np.pi) * i)) / AU
            
            # sun's position relative to the fixed planet
            sun_x = radius_fixed * np.cos((2 * np.pi) * i)
            sun_y = radius_fixed * np.sin((2 * np.pi) * i)
            
            # convert to AU
            radius = -radius / AU 
            
            # (2 * np.pi/ time_skew) * i
            # sun_x_position = 
            if row["name"] == "Sun":
                x = sun_x
                y = sun_y
                # print(x,y)
            else:
                # position of the planet relative to the sun
                x = radius * np.cos((2 * np.pi/ time_skew) * i) - sun_x 
                y = radius * np.sin((2 * np.pi/ time_skew) * i) - sun_y 
            
            # add the position to the array
            x_array = np.append(x_array, x)
            y_array = np.append(y_array, y)
            
        # plot the orbit 
        p.line(x_array, y_array, line_width=1, color=row["color"], legend_label=row["name"])

    # plot the planet
    p.circle(0, 0, radius=0.03, color=fixed_planet["color"], legend_label=fixed_planet["name"])
        
        
    
        
    # my name in the bottom right corner bokeh
    # p.text(0.9, 0.1, "Created by:The Solar System by @AMuh2020", color="white", text_font_size="10pt", text_align="center")
    html = file_html(p, title="Solar system relative orbits")
    # show(p)
    return html

# create_orbit()