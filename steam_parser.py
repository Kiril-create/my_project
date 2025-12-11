from random import uniform
from time import sleep

from bs4 import BeautifulSoup
from fake_headers import Headers
import requests


def get_html(url):
    counter = 0
    while True:
        headers = Headers(headers=True).generate()
        print('Отправляю запрос...')
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print('ok!')
            write_html(response.text)
            return response.text
        sleep(uniform(0.5, 1.5))
        counter += 1
        if counter >= 30:
            print('Превышен лимит запросов!')
            return False


def get_wishlist(url):
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        panels = soup.find_all('div', class_='Panel')
        # первые 6 панелей нам не нужны
        all_games = []
        counter = 0
        for panel in panels[8::2]:
            name_url = panel.find('div', class_='pMrnNJp5sDA-').find('a')
            name = name_url.text
            url = name_url['href']
            divs = panel.find_all('div')
            price = -1
            actual_price = -1
            discount = 0
            for div in divs:
                text = div.text.strip()
                if text.endswith(' руб'):
                    price = text
                    if '%' not in price:
                        price = int(price.split()[0])
                        actual_price = price
                    else:
                        parts = price.split('%')
                        discount = parts[0] + '%'
                        # -30%880 руб616 руб
                        price, actual_price = parts[1].split('руб')[:2]
                        price = int(price.strip())
                        actual_price = int(actual_price.strip())
            print(name, price, actual_price, discount)
            game_info = {}
            game_info['name'] = name
            game_info['url'] = url
            game_info['price'] = price
            game_info['actual_price'] = actual_price
            game_info['discount'] = discount
            all_games.append(game_info)
            counter += 1
            if counter >= 5:
                break
        return all_games
    return False


def write_html(html):
    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(html)


if __name__ == '__main__':
    get_wishlist('https://store.steampowered.com/wishlist/id/ssylo4ka_v_opisanii/')
