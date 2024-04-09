# DNS Shop Parser

## Описание
Данный скрипт предназначен для автоматизированного сбора информации о товарах с веб-сайта интернет-магазина DNS Shop. Использует библиотеки Selenium и BeautifulSoup для парсинга страниц и извлечения данных о товарах. Результаты сбора данных сохраняются в формате CSV.

## Зависимости
Прежде чем запускать скрипт, убедитесь, что установлены следующие зависимости:
- Selenium
- BeautifulSoup4
- undetected_chromedriver
- lxml

Установите необходимые пакеты, используя команду:
```bash
pip install selenium beautifulsoup4 undetected-chromedriver lxml
```
## Функции
init_driver(): Инициализация веб-драйвера. </br>
restart_driver(driver): Перезапуск драйвера. </br>
wait_for_element_with_refresh(driver, locator, timeout=30, refresh_rate=5): Ожидание элемента с возможностью обновления страницы. </br>
get_catalog_url(driver, url): Возвращает список URL всех страниц каталога. </br>
get_all_product_page_urls(driver, catalog_url): Сбор URL всех продуктов на странице каталога. </br>
parse_characteristics_page(driver, url): Парсинг страницы продукта и извлечение данных. </br>
main(): Основная функция скрипта. </br>
## Запуск
Для запуска скрипта выполните в терминале:</br>
  Для парсинга данных в .txt файл
```bash
python3 main.py
```
  Для парсинга данных в .csv файл
```bash
python3 output_to_csv.py
```
