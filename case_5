import os
import sys
import pygame
import requests

server_address = 'https://static-maps.yandex.ru/v1?'
geocode_address = 'https://geocode-maps.yandex.ru/1.x/?'
api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
coord_2 = 55.751462
coord_1 = 37.618790
spn_1 = 0.002
spn_2 = 0.002

min_spn = 0.001
max_spn = 0.1
zoom_step = 0.001

move_step = 0.0005

current_map_type = 'map'


def load_map():
    ll_spn = f"ll={coord_1},{coord_2}&spn={spn_1},{spn_2}&l={current_map_type}"
    map_request = f"{server_address}{ll_spn}&apikey={api_key}"
    response = requests.get(map_request)

    if response.status_code != 200:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    return map_file


def search_object(query):
    geocode_request = f"{geocode_address}?apikey={api_key}&geocode={query}&format=json"
    response = requests.get(geocode_request)

    if response.status_code != 200:
        print("Ошибка выполнения запроса геокодирования:")
        print(geocode_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return None

    json_response = response.json()
    try:
        coords = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        lon, lat = map(float, coords.split())
        return lat, lon
    except (IndexError, KeyError):
        print("Объект не найден.")
        return None


pygame.init()
screen = pygame.display.set_mode((600, 450))
font = pygame.font.Font(None, 36)

map_file = load_map()
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()

input_box = pygame.Rect(10, 10, 300, 40)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
text = ''
active = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    result = search_object(text)
                    if result:
                        coord_2, coord_1 = result
                        map_file = load_map()
                        screen.blit(pygame.image.load(map_file), (0, 0))
