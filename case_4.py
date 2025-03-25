import os
import sys
import pygame
import requests

server_address = 'https://static-maps.yandex.ru/v1?'
api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'

coord_2 = 55.751462
coord_1 = 37.618790
spn_1 = 0.002
spn_2 = 0.002

min_spn = 0.001
max_spn = 0.1
zoom_step = 0.001
move_step = 0.0005

current_theme = 'light'


def load_map():
    ll_spn = f"ll={coord_1},{coord_2}&spn={spn_1},{spn_2}"
    map_request = f"{server_address}{ll_spn}&theme={current_theme}&apikey={api_key}"
    response = requests.get(map_request)

    if response.status_code != 200:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


pygame.init()
screen = pygame.display.set_mode((600, 450))
pygame.display.set_caption('Press T to change theme (light)')

map_file = load_map()
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                spn_1 = min(spn_1 + zoom_step, max_spn)
                spn_2 = min(spn_2 + zoom_step, max_spn)
            elif event.key == pygame.K_PAGEDOWN:
                spn_1 = max(spn_1 - zoom_step, min_spn)
                spn_2 = max(spn_2 - zoom_step, min_spn)

            elif event.key == pygame.K_UP:
                coord_2 = min(coord_2 + move_step, 90)
            elif event.key == pygame.K_DOWN:
                coord_2 = max(coord_2 - move_step, -90)
            elif event.key == pygame.K_LEFT:
                coord_1 = max(coord_1 - move_step, -180)
            elif event.key == pygame.K_RIGHT:
                coord_1 = min(coord_1 + move_step, 180)

            elif event.key == pygame.K_t:
                current_theme = 'dark' if current_theme == 'light' else 'light'
                pygame.display.set_caption(f'Press T to change theme ({current_theme})')

            map_file = load_map()
            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()

pygame.quit()
os.remove(map_file)
