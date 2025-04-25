import folium
import json


from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.http import HttpResponse
from django.utils import timezone



MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def get_image_url(request, image):
    return request.build_absolute_uri(image.url) if image else DEFAULT_IMAGE_URL


def show_all_pokemons(request):
    pokemons_on_page = []
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    now = timezone.localtime()
    pokemon_entities = PokemonEntity.objects.filter(
        disappeared_at__gte=now,
        appeared_at__lt=now
    )

    for pokemon_entity in pokemon_entities:
        image_url = get_image_url(request, pokemon_entity.pokemon.image)

        add_pokemon(
            folium_map, 
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            image_url
        )


    for pokemon in Pokemon.objects.all():
        image_url = get_image_url(request, pokemon.image)

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': image_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon_info = {
        'pokemons': [
        ]
    }

    now = timezone.localtime()
    pokemon_entities = PokemonEntity.objects.filter(
        disappeared_at__gte=now,
        appeared_at__lt=now
    )

    for pokemon_entity in pokemon_entities:
        pokemon_image_url = get_image_url(request, pokemon_entity.pokemon.image)

        if pokemon_entity.pokemon.previous_evolution:
            previous_evolution_title = pokemon_entity.pokemon.previous_evolution.title
            previous_evolution_id = pokemon_entity.pokemon.previous_evolution.id
            previous_evolution_img_url = get_image_url(request, pokemon_entity.pokemon.previous_evolution.image)
        else:
            previous_evolution_title = None
            previous_evolution_id = None
            previous_evolution_img_url = None

        pokemon_info['pokemons'].append({
                "pokemon_id": pokemon_entity.pokemon.id,
                "title_ru": pokemon_entity.pokemon.title,
                "title_en": pokemon_entity.pokemon.title_en,
                "title_jp": pokemon_entity.pokemon.title_jp,
                "description": pokemon_entity.pokemon.description,
                "img_url": pokemon_image_url,
                "entities": [
                    {
                        "lat": pokemon_entity.latitude,
                        "lon": pokemon_entity.longitude
                    }
                ],
                "previous_evolution": {
                    "title_ru": previous_evolution_title,
                    "pokemon_id": previous_evolution_id,
                    "img_url": previous_evolution_img_url
                }
            })

        if previous_evolution_title == None:
            for pokemon in pokemon_info['pokemons']:
                del pokemon['previous_evolution']

    for pokemon in pokemon_info['pokemons']:
        if pokemon['pokemon_id'] == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon['entities']:
        add_pokemon(
            folium_map, pokemon_entity['lat'],
            pokemon_entity['lon'],
            pokemon['img_url']
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
