import numpy as np
from bokeh.plotting import figure
from bokeh.embed import file_html
def create_graph():
    AU = 1.495978707e11 # astronomical unit
    # data for the solar system
    # name, orbital period (years), semi-major axis (m), color
    solar_system = [
        ("Sun", 0, 0,  "yellow"),
        ("Mercury", 0.24, 5.77E+10, "brown"),
        ("Venus", 0.62, 1.08E+11, "orange"),
        ("Earth", 1, 1.50E+11, "blue"),
        ("Mars", 1.88, 2.28E+11, "red"),
        ("Jupiter", 11.86, 7.78E+11, "orange"),
        ("Saturn", 29.46, 1.43E+12, "yellow"),
        ("Uranus", 84.01, 2.87E+12, "lightblue"),
        ("Neptune", 164.8, 4.50E+12, "blue"),
    ]

    solar_system = np.array(solar_system, dtype=[
        ("name", "U10"),
        ("period", "f8"),
        ("semi_major_axis", "f8"),
        ("color", "U10"),
    ])
    p = figure(title="Solar System", x_axis_label="(a / AU)^(3/2)", y_axis_label="T / years")
   
    #  empty numpy array for x and y
    x = np.array([])
    y = np.array([])
    
    # plot the planets
    for i in range(1,len(solar_system)):
        semi_major = (solar_system[i]["semi_major_axis"]/ AU)**(3/2)
        p.circle(semi_major, solar_system[i]["period"], radius=3, color=solar_system[i]["color"], legend_label=solar_system[i]["name"])
        x = np.append(x, semi_major)
        y = np.append(y, solar_system[i]["period"])
    
    p.line(x, y, color="white", legend_label="Kepler's 3rd Law")
    p.legend.location = "top_left"
    p.legend.click_policy="hide"
    
    
    p.y_range.start = 0
    p.x_range.start = 0
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
    
    html = file_html(p,title="my plot")

    return html