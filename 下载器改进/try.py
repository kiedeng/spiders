import requests
import time
while 1:
    try:
        content = requests.get("www.cc.com").content
        break
    except Exception:
        print("访问出错。。重新访问")
        time.sleep(1)