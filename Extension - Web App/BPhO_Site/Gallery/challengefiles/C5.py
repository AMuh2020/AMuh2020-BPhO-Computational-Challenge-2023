# orbit angle vs time
import numpy as np
# bokeh
from bokeh.plotting import figure, show
from bokeh.embed import file_html

# name, orbital period (years), eccentricity, theta0, color
solar_system = [
    ("Sun", 0, 0, 0, "yellow"),
    ("Mercury", 0.241, 0.21, 0, "brown"),
    ("Venus", 0.615, 0.02, 0, "orange"),
    ("Earth", 1, 0.01, 0, "blue"),
    ("Mars", 1.881, 0.09, 0, "red"),
    ("Jupiter", 11.861, 0.05, 0, "orange"),
    ("Saturn", 29.628, 0.05, 0, "yellow"),
    ("Uranus", 84.747, 0.05, 0, "lightblue"),
    ("Neptune", 166.344, 0.01, 0, "blue"),
    ("Pluto", 248.348, 0.25, 0, "brown"),
]

# convert to numpy array for easier manipulation
solar_system = np.array(solar_system, dtype=[
    ("name", "U10"),
    ("period", "f8"),
    ("eccentricity", "f8"),
    ("theta0", "f8"),
    ("color", "U10"),
])
def generate_graph(planet, years):
    for i in range(len(solar_system)):
        if solar_system[i]["name"].lower() == planet.lower():
            planet = solar_system[i]
            break
    years = int(years)
    def angle_vs_time(t, P, ecc, theta0):
        dtheta = 1/1000

        # number of orbits
        N = int(round(t[-1]/P, 0))
        # print(N)
        # array of polar angles
        theta = np.arange(theta0, (2*np.pi*N + theta0), dtheta)

        # evaluate integrand of time integral
        integrand = 1/((1-ecc*np.cos(theta))**2)

        # simpson's rule coefficients
        a = np.ones(len(integrand))
        a[1::2] = 4
        a[2::2] = 2
        a[-1] = 1

        # calculate array of time
        time = P*((1-ecc**2)**(3/2))*(1/(2*np.pi))*dtheta*(1/3)*np.cumsum(a*integrand)
        
        # interpolate polar angles for each time
        theta = np.interp(t, time, theta)

        return theta

    # creat plot bokeh
    p = figure(title=f"Orbit angle vs time for {planet['name']}", x_axis_label="Time / (years)", y_axis_label="Orbit angle / (radians)")

    p.y_range.start = 0
    p.x_range.start = 0
    # time array
    t = np.linspace(0, years, 1000)

    # angle vs time for eccentric orbit
    theta = angle_vs_time(t, planet['period'], planet['eccentricity'], planet['theta0'])
    p.line(t, theta, legend_label="Eccentric orbit", line_color="green")

    # angle vs time for circular orbit
    theta = angle_vs_time(t, planet['period'], 0, planet['theta0'])
    p.line(t, theta, legend_label="Circular orbit", line_color="blue")

    p.legend.location = "top_left"

    # my name in the bottom right corner
    # plt.gcf().text(0.8, 0.02, "Created by: @AMuh2020", fontsize=10,ha="center", va="center", color="black")

    html = file_html(p, title=f"Orbit angle vs time for {planet['name']}")

    return html