import requests
import random

proxies = [{'http': 'http://139.199.15.78:3128',
            'https': 'https://139.199.15.78:3128'},

           {'http': 'http://182.254.175.13:3128',
            'https': 'https://182.254.175.13:3128'},

           {'http': 'http://139.9.220.162:3128',
            'https': 'https://139.9.220.162:3128'}]


def run(px):
    try:
        response = requests.get('http://httpbin.org/get', proxies=proxies[px])
        print(response.text)
    except requests.exceptions.ConnectionError as e:
        print('错误:', e.args)


for i in range(10):
    ans = random.randint(0, 2)
    run(ans)
    print(ans)
