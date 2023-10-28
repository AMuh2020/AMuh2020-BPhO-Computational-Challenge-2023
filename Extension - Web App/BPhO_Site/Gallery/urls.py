# urlsfrom django.urls import path, include


from django.urls import path
from . import views

urlpatterns = [
    path('challenge/<int:challenge>/', views.challenge, name='challenge'),
    path('', views.index, name='index'),
    path('acknowledgements/', views.acknowledgements, name='acknowledgements'),
]