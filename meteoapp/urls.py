from django.urls import path
from .views import home,show_map,show_news,nasa_satellite_info

urlpatterns = [
    path('', home, name='home'),
    path('map/', show_map, name='show_map'),
    path('news/', show_news, name='show_news'),
    path('satellite_info/', nasa_satellite_info, name='nasa_satellite_info'),
]