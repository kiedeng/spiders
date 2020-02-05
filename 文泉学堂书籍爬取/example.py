import requests

html = requests.get("http://img.bookask.com/book/read/2175744/1.jpeg")

with open("1.jpeg", "wb") as f:
    f.write(html.content)