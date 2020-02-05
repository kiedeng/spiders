import requests
import json


def get_ip():
    url = 'http://proxy.1again.cc:35050/api/v1/proxy/'
    text = requests.get(url).text
    print(text)
    js = json.loads(text)
    return js['data']['proxy']


def get_proxy():
    mark = 1
    while mark:
        mark = 0
        proxy = get_ip()  # 本地代理
        # proxy='username:password@123.58.10.36:8080'
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        try:
            response = requests.get('http://httpbin.org/get', proxies=proxies, timeout=3)
            print(response.text)
        except Exception as e:
            print('错误:', e.args)
            mark = 1
    with open("proxy_pool.txt", "a+") as f:
        f.write(proxy+"\n")

    return proxies


for i in range(10):
    get_proxy()
