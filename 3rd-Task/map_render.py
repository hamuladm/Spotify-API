'''
Laboratorna 2
'''

import folium
from geopy import Nominatim
import pycountry
from spotify_api_render import print_result
from geopy.exc import GeocoderUnavailable


def get_countries(artist: str) -> list:
    '''
    Generates HTML-map
    '''
    countries_alpha_2 = print_result(artist)
    countries_list = [pycountry.countries.get(alpha_2 = country).name for country in countries_alpha_2
                      if pycountry.countries.get(alpha_2 = country)]

    return countries_list


def get_coords(countries: list) -> list:
    '''
    Gets coordinations for countries
    '''
    geolocator = Nominatim(user_agent = "Map_App")
    locations = []
    for location in countries:
        try:
            addr = geolocator.geocode(location)
            if not addr:
                continue
            loc = [addr.latitude, addr.longitude]
            locations.append(loc)
        except GeocoderUnavailable:
            continue

    return locations


def mark_on_map(coords: list) -> 0:
    '''
    Marks on a map
    '''
    map = folium.Map()
    fg_0 = folium.FeatureGroup(name = 'Locations for the top track')

    for elem in coords:
        fg_0.add_child(
            folium.Marker(
                location = elem,
                icon = folium.Icon(color = 'red'))
        )

    map.add_child(fg_0)
    map.add_child(folium.LayerControl())
    map.save('Map.html')

    return 0



if __name__ == '__main__':
    raw_countries = get_countries('Metallica')
    raw_coords = get_coords(raw_countries)
    result = mark_on_map(raw_coords)
    print(result)
