import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.common.exceptions import TimeoutException
import time
import csv


def init_driver():
    return uc.Chrome()


def restart_driver(driver):
    driver.quit()
    return init_driver()


def wait_for_element_with_refresh(driver, locator, timeout=30, refresh_rate=5):
    """
    Пытается найти элемент на странице, обновляя её каждые refresh_rate секунд.
    driver: Экземпляр веб-драйвера.
    locator: Локатор элемента (например, (By.CLASS_NAME, "my-class")).
    timeout: Общее время ожидания в секундах.
    refresh_rate: Интервал обновления страницы в секундах.
    """
    end_time = time.time() + timeout
    while True:
        try:
            return WebDriverWait(driver, refresh_rate).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            current_time = time.time()
            if current_time > end_time:
                raise TimeoutException(f"Элемент {locator} не найден за {timeout} сек.")
            driver.refresh()


def get_catalog_url(driver, url):
    """
        Получает все URL страниц каталога товаров, разбитых на страницы.
        Определяет количество товаров и страниц в каталоге, создает URL каждой страницы каталога.
    """
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.products-count')))
    url_all_pages = []
    soup = BeautifulSoup(driver.page_source, "lxml")
    items_count = soup.find('span', class_='products-count')
    pages_count = int(items_count.text[:-7]) // 18
    if int(items_count.text[:-7]) % 18 != 0:
        pages_count += 1
    for i in range(pages_count):
        update_url = f'{url}?p={i + 1}'
        url_all_pages.append(update_url)
    return url_all_pages


def get_all_product_page_urls(driver, catalog_url):
    """
        Извлекает URL всех страниц продуктов с текущей страницы каталога.
        Ожидает загрузки элементов со ссылками на продукты, а затем собирает и возвращает их URL.
    """
    driver.get(catalog_url)
    wait_for_element_with_refresh(driver, (By.CLASS_NAME, "catalog-product__name"), 30, 5)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    product_links = soup.find_all('a', class_="catalog-product__name ui-link ui-link_black")

    urls = ['https://www.dns-shop.ru' + link['href'] for link in product_links]
    return urls


def parse_characteristics_page(driver, url):
    """
        Получает информацию о продукте и его характеристики со страницы продукта.
        Ожидает появления элемента с ценой продукта, извлекает название, цену и характеристики продукта.
        Возвращает собранную информацию вместе с URL страницы продукта.
    """
    driver.get(url)
    wait_for_element_with_refresh(driver, (By.CLASS_NAME, "product-buy__price"), 30, 5)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    name = soup.find('div', class_='product-card-top__name').text.strip()
    price = soup.find('div', class_='product-buy__price').text.strip().split()[0:2]
    price = int("".join(price))

    characteristics_info = []
    characteristics = soup.find_all('div', class_='product-characteristics__spec-value')
    characteristics_title = soup.find_all('div', class_='product-characteristics__spec-title')

    for title, value in zip(characteristics_title, characteristics):
        characteristics_info.append(f"{title.text.strip()} - {value.text.strip()}")

    return name, price, characteristics_info, url


def main():
    """
        Инициализирует драйвер, проходит по каждой странице каталога, собирает URL продуктов,
        извлекает данные о каждом продукте и записывает их в CSV-файл.
        Перезапускает драйвер после определенного количества итераций для предотвращения перегрузки системы.
    """
    driver = init_driver()
    urls = [
        'https://www.dns-shop.ru/catalog/2b911f3c621a36eb/servernye-ssd-m2/'
    ]
    iterations = 0
    restart_threshold = 20
    filename = f"product_price_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Название продукта', 'Цена, р.', 'Характеристики', 'Ссылка на товар'])

        iterations = 0
        for url in urls:
            catalog_url = get_catalog_url(driver, url)
            for url in catalog_url:
                product_urls = get_all_product_page_urls(driver, url)
                for link in product_urls:
                    name, price, characteristics, url = parse_characteristics_page(driver, link + "characteristics/")
                    csv_writer.writerow([name, price, "  ".join(characteristics), url])
                    iterations += 1
                    if iterations >= restart_threshold:
                        driver = restart_driver(driver)
                        iterations = 0
    driver.quit()


if __name__ == '__main__':
    main()