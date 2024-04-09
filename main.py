import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import itertools

def get_catalog_url(driver, url): #возвращает списком url всех страниц категории
    driver.get(url)
    sleep(4)
    url_all_pages = []
    soup = BeautifulSoup(driver.page_source, "lxml")
    items_count = soup.find('span', class_='products-count')
    pages_count = int(items_count.text[0:-7])//18+1
    for i in range(pages_count):
        update_url = url + f'?p={i+1}'
        url_all_pages.append(update_url)

    return url_all_pages
def get_all_product_page_urls(driver, catalog_url):
    """Извлекает и возвращает список URL страниц товаров из каталога."""
    driver.get(catalog_url)
    sleep(4)  # Пауза для загрузки страницы

    soup = BeautifulSoup(driver.page_source, 'lxml')
    product_links = soup.find_all('a',
                                  class_="catalog-product__name ui-link ui-link_black")

    urls = ['https://www.dns-shop.ru' + link['href'] for link in product_links]
    return urls


def parse_characteristics_page(driver, url):
    """Вытаскивает название, цену и хар-ки и преобразует в строку."""

    driver.get(url)
    sleep(4) #Параметр нужно менять в зависимости от скорости соедиенения, если интернет медленный (либо сайт перегружен), то время выставляется выше

    soup = BeautifulSoup(driver.page_source, 'lxml')
    name = soup.find('div', class_='product-card-top__name')
    price = soup.find('div', class_='product-buy__price')
    characteristics = soup.find_all('div', class_='product-characteristics__spec-value')
    characteristics_title = soup.find_all('div', class_='product-characteristics__spec-title')

    info = (f'{name.text}\n{" ".join(price.text.split()[0:2])} руб.\n')

    for (i, j) in zip(characteristics_title, characteristics):
        info += (i.text + ' - ' + j.text + '\n')

    return (info)


def main():
    driver = uc.Chrome()
    urls = [
        'https://www.dns-shop.ru/catalog/17a8df6816404e77/lazernye-mfu/',
        'https://www.dns-shop.ru/catalog/17a8df9d16404e77/strujnye-mfu/',
        'https://www.dns-shop.ru/catalog/17a8e00716404e77/lazernye-printery/',
        'https://www.dns-shop.ru/catalog/17a8e07216404e77/strujnye-printery/',
        'https://www.dns-shop.ru/catalog/17a8e0a516404e77/shirokoformatnye-printery/',
        'https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/',
        'https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/',
        'https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/',
        'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/',
        'https://www.dns-shop.ru/catalog/17a89a3916404e77/operativnaya-pamyat-dimm/',
        'https://www.dns-shop.ru/catalog/17a89c2216404e77/bloki-pitaniya/',
        'https://www.dns-shop.ru/catalog/8a9ddfba20724e77/ssd-nakopiteli/',
        'https://www.dns-shop.ru/catalog/dd58148920724e77/ssd-m2-nakopiteli/',
        'https://www.dns-shop.ru/catalog/1023687c7ba7a69d/servernye-ssd/',
        'https://www.dns-shop.ru/catalog/2b911f3c621a36eb/servernye-ssd-m2/',
        'https://www.dns-shop.ru/catalog/17a8914916404e77/zhestkie-diski-35/',
        'https://www.dns-shop.ru/catalog/f09d15560cdd4e77/zhestkie-diski-25/',
        'https://www.dns-shop.ru/catalog/17aa4e3216404e77/servernye-hdd/'
    ]

    filename = f"product_price{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    for url in urls:
        catalog_url = get_catalog_url(driver, url)
        with open(filename, 'a', encoding='utf-8') as file:
            for url in catalog_url:
                product_urls = get_all_product_page_urls(driver, url)
                for link in product_urls:
                    file.write("\n" + parse_characteristics_page(driver, link + "characteristics/"))

    driver.quit()

if __name__ == '__main__':
    main()
