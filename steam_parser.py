# from random import uniform
from time import sleep

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
# from fake_headers import Headers
# import requests

from parsers.utils_str import get_driver, price_to_float


# def get_html(url):
#     counter = 0
#     while True:
#         headers = Headers(headers=True).generate()
#         print('Отправляю запрос...', end=' ')
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             print('ok!')
#             write_html(response.text)
#             return response.text
#         sleep(uniform(2, 5))
#         print(response.status_code)
#         counter += 1
#         if counter >= 50:
#             print('Превышен лимит запросов!')
#             return False


def get_html(url):
    driver = get_driver()
    print('запускаю chrome...')
    driver.get(url)
    print('открыл страницу, ждем ...')
    sleep(10)
    return driver.page_source


def get_wishlist(url):
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        panels = soup.find_all('div', class_='Panel')
        # первые 6 панелей нам не нужны
        all_games = []
        for panel in panels[8::2]:
            title_url = panel.find('div', class_='-irQN7ogs-M-').find('a')
            title = title_url.text
            url = title_url['href']
            divs = panel.find_all('div')
            original_price = -1
            actual_price = -1
            discount = 0
            for div in divs:
                text = div.text.strip()
                if text.endswith(' руб'):
                    original_price = text
                    if '%' not in original_price:
                        original_price = price_to_float(original_price.split()[0])
                        actual_price = original_price
                    else:
                        parts = original_price.split('%')
                        discount = float(parts[0].lstrip('-')) / 100
                        actual_price = parts[1].split('руб')[1]
                        actual_price = price_to_float(actual_price)
                        original_price = round(actual_price / discount, 2)
            game_info = {}
            game_info['title'] = title
            game_info['url'] = url
            game_info['original_price'] = original_price
            game_info['actual_price'] = actual_price
            game_info['discount'] = discount
            all_games.append(game_info)
        return all_games
    return False


def write_html(html):
    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(html)


if __name__ == '__main__':
    get_wishlist('https://steamcommunity.com/profiles/76561198125406999/wishlist/')

