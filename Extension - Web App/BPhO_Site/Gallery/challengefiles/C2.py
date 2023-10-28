import numpy as np
from bokeh.plotting import figure, show
from bokeh.embed import file_html

# constants
AU = 1.495978707e11 # astronomical unit


# name, orbital period (years), semi-major axis (m), eccentricity, color

# convert to numpy array for easier manipulation

def create_graph(inner_outer):
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

    solar_system = np.array(solar_system, dtype=[
        ("name", "U10"),
        ("period", "f8"),
        ("semi_major_axis", "f8"),
        ("eccentricity", "f8"),
        ("color", "U10"),
    ])
    p = figure(title="Solar System", x_axis_label="x / (AU)", y_axis_label="y / (AU)")
    if inner_outer == "inner":
        solar_system = solar_system[1:5]
        p.circle(0, 0, radius=0.1, color="yellow")
    elif inner_outer == "outer":
        solar_system = solar_system[5:8]
        p.circle(0, 0, radius=1.5, color="yellow")
    elif inner_outer == "outer_pluto":
        solar_system = solar_system[5:]
        p.circle(0, 0, radius=1.5, color="yellow")
    else:
        solar_system = solar_system[1:]
        p.circle(0, 0, radius=0.1, color="yellow")
    
    
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

    # for each planet, create a circle in the correct position with the correct radius
    for row in solar_system:
        # create the orbit
        x_array = np.array([])
        y_array = np.array([])
        for j in range(0, 360*100+1, int(0.36*100)):
            i = j / 100
            radius = (row["semi_major_axis"] * (1-row["eccentricity"]**2)) / (1 + row["eccentricity"] * np.cos(i * np.pi / 180))
            radius = radius / AU 
            
            x = -radius * np.cos((i) * np.pi / 180)
            y = radius * np.sin(i * np.pi / 180)
            x_array = np.append(x_array, x)
            y_array = np.append(y_array, y)

        p.line(x_array, y_array, color=row["color"], line_width=1, legend_label=row["name"])

    html = file_html(p,title="Solar system")
    return html