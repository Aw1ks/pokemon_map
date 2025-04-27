import folium
import json


from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
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
            # 𝘞𝘢𝘳𝘯𝘪𝘯𝘨! `𝘵𝘰𝘰𝘭𝘵𝘪𝘱` 𝘢𝘵𝘵𝘳𝘪𝘣𝘶𝘵𝘦 𝘪𝘴 𝘥𝘪𝘴𝘢𝘣𝘭𝘦𝘥 𝘪𝘯𝘵𝘦𝘯𝘵𝘪𝘰𝘯𝘢𝘭𝘭𝘺
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
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)

    now = timezone.localtime()
    pokemon_entities = PokemonEntity.objects.filter(
        disappeared_at__gte=now,
        appeared_at__lt=now,
        pokemon=pokemon
    )

    previous_pokemon_evolution = None
    next_pokemon_evolution = None

    previous_evolution = pokemon.previous_evolution
    next_evolution = pokemon.next_evolutions.first()


    pokemon_image_url = get_image_url(request, pokemon.image)

    if previous_evolution:
        previous_evolution_image = get_image_url(request, previous_evolution.image)
        previous_pokemon_evolution = {
                "title_ru": previous_evolution.title,
                "pokemon_id": previous_evolution.id,
                "img_url": previous_evolution_image
            }

    if next_evolution:
        next_evolution_image = get_image_url(request, next_evolution.image)
        next_pokemon_evolution = {
                "title_ru": next_evolution.title,
                "pokemon_id": next_evolution.id,
                "img_url": next_evolution_image
            }

    pokemon_info = {
            "pokemon_id": pokemon.id,
            "title_ru": pokemon.title,
            "title_en": pokemon.title_en,
            "title_jp": pokemon.title_jp,
            "description": pokemon.description,
            "img_url": pokemon_image_url,
            "entities": [],
            "previous_evolution": previous_pokemon_evolution, 
            "next_evolution": next_pokemon_evolution
        }
    
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        pokemon_info['entities'].append({
            'lat': pokemon_entity.latitude,
            'lon': pokemon_entity.longitude
        })

        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            pokemon_info['img_url']
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_info
    })
