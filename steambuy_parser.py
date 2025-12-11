from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys



def get_driver():
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    return driver


def get_html(url):
    driver = get_driver()
    print('запускаю chrome...')
    driver.get(url)
    print('открыл страницу, ждем 5 секунд...')
    # search_field = driver.find_element(By.XPATH, "//input[@class='search__control']")
    # search_field.click()
    # sleep(3)
    # search_field.send_keys('fallout')
    # sleep(3)
    # search_field.send_keys(Keys.RETURN)
    sleep(5)
    return driver.page_source


def parse_html(url):
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.find('div', class_='product-list').find_all('div', class_='product-item product-item_red')
        # перебрать все карточки на странице
        # собрать 4 значения (типизация, очистка и тп)
        # url, title, price, discount
        # + пересчитать начальнцую цену, зная скидку и текущую цену


        for card in cards:
            name = card.find('div', class_='product-item__title').find('a', class_='product-item__title-link').text
            skid = card.find('div', class_='product-item__price').find('div', class_='product-item__discount').text
            price = card.find('div', class_='product-item__price').find('div', class_='product-item__cost').text
            url = card.find('div', class_='product-item__img').find('a')['href']
            price = price.split()
            price = price[0]
            price = int(price)
            skid = skid.split('%')
            skid = skid[0]
            skid = int(skid)
            price_n = price / skid * 100
            print(name, round(price_n, 2), price, skid, url)
            print('\n')
            print('=' * 40)
            print('\n')



if __name__ == '__main__':
    parse_html('https://steambuy.com/catalog/?page=1')
