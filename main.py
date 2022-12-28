import os
import requests
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, url):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    long_url = {"long_url": url}
    response = requests.post("https://api-ssl.bitly.com/v4/shorten", headers=headers, json=long_url)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_clicks(token, url):
    headers = {
        'Authorization': f'Bearer {token}',
    }

    parsed_url = urlparse(url)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary', headers=headers,
                            )
    response.raise_for_status()
    clicks = response.json()['total_clicks']
    return clicks


def is_bitlink(url, token):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    parsed_url = urlparse(url)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}', headers=headers)

    return response.ok


def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('-urls', nargs='+', help="Введите ссылку", required=True)
    bitly_token = os.getenv("BITLY_TOKEN")
    urls = parser.parse_args()
    for url in urls.urls:
        try:
            if is_bitlink(url, bitly_token):

                print('your clicks', count_clicks(bitly_token, url))
            else:
                print('Битлинк', shorten_link(bitly_token, url))
        except requests.exceptions.HTTPError as e:
            print(f"error:{e}")


if __name__ == "__main__":
    main()
