from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import time

from parsers.utils_str import price_to_float


def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        print('Сайт недоступен!')
        return False
    return response.text


# def get_last_page_number():
#     url = 'https://igm.gg/catalog?page=1'
#     html = get_html(url)
#     if html:
#         soup = BeautifulSoup(html, 'html.parser')
#         paginator = soup.find_all('a', class_='Paginator_link__aaR1G')
#         print(paginator)
#         if paginator:
#             return int(paginator[-1].text)
#     return False


def parse_html():
    all_games = []
    for i in tqdm(range(1, 10)):
        time.sleep(2)
        url = f'https://igm.gg/catalog?page={i}'
        html = get_html(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('div', class_='CardList_list__MuwWR')
            if not table:
                break
            cards = table.find_all('div', class_='Content_content__Uh3QE')
            urls = table.find_all('a')

            for card, url in zip(cards[:25], urls[:25]):
                title = card.find('div', class_='Content_content__name-container__plUNF').text
                actual_price = card.find('div', class_='Price_price__dk_c2').find('p').text
                # original_price = card.find('div', class_='PriceDiscount_price-discount__Ty9aC').find('span').text
                # discount = card.find('p', 'Notification_notification__UAnq9 Notification_notification_type-sale-subscription__TXTSl').find('span').text
                url = 'https://igm.gg' + url['href']
                # original_price = original_price.replace(chr(8239), ' ').replace('₽', '')
                # original_price = float(original_price.replace(',', '.'))
                actual_price = price_to_float(actual_price)
                game_info = {}
                game_info['title'] = title
                game_info['url'] = url
                # game_info['original_price'] = original_price
                game_info['actual_price'] = actual_price
                # game_info['discount'] = discount
                all_games.append(game_info)
    return all_games


def write_html(html):
    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(html)


if __name__ == '__main__':
    parse_html()
