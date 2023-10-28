from django.shortcuts import render
from django.http import FileResponse
from .challengefiles import C1, C2, C5, C6, C7

challenge_titles = {
        1: "Kepler III correlation",
        2: "Elliptical orbits of the planets",
        3: "2D animation of the solar system orbits",
        4: "3D animation of the solar system orbits",
        5: "Orbit angle vs time",
        6: "Solar system spirograph",
        7: "Orbits relative to a planet",
    }

# Create your views here.
def challenge(request, challenge):
    if request.method == 'POST':
        
        if challenge == 1:
            graph_html = C1.create_graph()
        elif challenge == 2:
            inner_outer = request.POST['inner_outer']
            graph_html = C2.create_graph(inner_outer)
        elif challenge == 3:
            inner_outer = request.POST['inner_outer']
            path_to_vid = f"Challenge_3_{inner_outer}.mp4"
            return render(request, 'Gallery.html', {'challenge_num': challenge,'challenge_title':challenge_titles[challenge], 'path_to_vid': path_to_vid})
        elif challenge == 4:
            inner_outer = request.POST['inner_outer']
            path_to_vid = f"Challenge_4_{inner_outer}.mp4"
            return render(request, 'Gallery.html', {'challenge_num': challenge,'challenge_title':challenge_titles[challenge], 'path_to_vid': path_to_vid})
        elif challenge == 5:
            planet = request.POST['planet']
            years = request.POST['years']
            graph_html = C5.generate_graph(planet,years)
        elif challenge == 6:
            planet1 = request.POST['planet1']
            planet2 = request.POST['planet2']
            interval = request.POST['interval']
            graph_html = C6.create_spirogram([planet1, planet2],interval=float(interval))
        elif challenge == 7:
            inner_outer = request.POST['inner_outer']
            if inner_outer == "inner":
                fixed_planet = request.POST['planet_inner']
            elif inner_outer == "outer":
                fixed_planet = request.POST['planet_outer']
            elif inner_outer == "outer_pluto":
                fixed_planet = request.POST['planet_outer']
            graph_html = C7.generate_graph(inner_outer, fixed_planet=int(fixed_planet))
        
        if graph_html == None:
            return render(request, 'Gallery.html', {'challenge_num': challenge,'challenge_title':challenge_titles[challenge]})
        return render(request, 'Gallery.html', {'challenge_num': challenge, 'graph_html': graph_html,'challenge_title':challenge_titles[challenge]})
    else:
        return render(request, 'Gallery.html', {'challenge_num': challenge,'challenge_title':challenge_titles[challenge]})



def index(request):
    return render(request, 'index.html', {'challenges': challenge_titles})

def acknowledgements(request):
    return render(request, 'acknowledgements.html')