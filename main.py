import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, url):
    api_url = 'https://api.vk.ru/method/utils.getShortLink'
    payload = {'access_token': token,
               'v': '5.199',
               'url': url,
               'private': '0'}

    response = requests.get(api_url, params=payload)
    response.raise_for_status()

    if 'error' not in response.json():
        short_link = response.json()['response']['short_url']
        return short_link
    else:
        raise requests.exceptions.HTTPError


def count_clicks(token, link):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    url_path = urlparse(link).path.replace('/', '')
    payload = {'access_token': token,
               'v': '5.199',
               'key': url_path,
               'interval': 'forever'}

    response = requests.get(api_url, params=payload)
    response.raise_for_status()

    if 'error' not in response.json():
        clicks_count = response.json()['response']['stats'][0]['views']
        return clicks_count
    else:
        raise requests.exceptions.HTTPError


def is_shorten_link(url):
    return urlparse(url).netloc == 'vk.cc'


def main():
    load_dotenv()
    token = os.environ['VK_ID_ACCESS_TOKEN']

    parser = argparse.ArgumentParser(
        description='Программа сокращает указанную пользователем ссылку. Если ссылка уже сокращена, то выводит количество переходов по ней'
    )
    parser.add_argument('user_url', help='Пользовательская ссылка')
    args = parser.parse_args()
    user_url = args.user_url

    try:
        if not is_shorten_link(user_url):
            short_link = shorten_link(token, user_url)
            print('Сокращённая ссылка:', short_link)
        else:
            clicks_amount = count_clicks(token, user_url)
            print('Число переходов по ссылке:', clicks_amount)
    except requests.exceptions.HTTPError:
        print('Ошибка: неверный формат ссылки')


if __name__ == "__main__":
    main()
