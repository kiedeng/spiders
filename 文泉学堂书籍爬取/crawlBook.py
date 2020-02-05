import json
import shutil
import random
import img2pdf
import requests
import threading
import os
import time


# 当前路径
getcmd = ""
# 图片存放路径
fold = ""
# 书籍的总页码
sum_book = 0
# 书籍的id
book_uid = 0
# 书籍的总URL
book_url = ""
# 线程数
thread_count = 20

title_name = ""

# 计算书籍总页码
def count_book():
    global title_name
    count_url = "https://lib-nuanxin.wqxuetang.com/v1/read/initread?bid=" + book_uid
    text = requests.get(count_url).text
    # print(text)
    js = json.loads(text)
    count = js['data']['pages']
    title_name = js['data']['name']
    return int(count)


proxies = [{'http': 'http://139.199.15.78:3128',
            'https': 'https://139.199.15.78:3128'},
           {'http': 'http://182.254.175.13:3128',
            'https': 'https://182.254.175.13:3128'},
           {'http': 'http://139.9.220.162:3128',
            'https': 'https://139.9.220.162:3128'}]

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Connection': 'keep-alive',
    'Referer': 'http://www.baidu.com/'
}


# 分批下载图片
def load_img(count):
    # print(threading.current_thread())
    thread_page = int(sum_book/thread_count)
    l = thread_page * count+1
    if count == thread_count - 1:
        r = sum_book
    else:
        r = thread_page * (count+1)

    for page in range(l, r+1):
        url = book_url + str(page) + ".jpeg"
        print("第"+str(page)+"正在下载中。。。")
        local_path = fold + "/" + str(page)+".jpeg"
        with open(local_path, "wb") as f:
            mk = 1
            while mk:
                mk = 0
                try:
                    content = requests.get(url, headers=headers).content
                except Exception:
                    mk = 1
                    print("重新下载一页！")
                    time.sleep(0.2)
            f.write(content)

        # time.sleep(0.03)


def init(book_id):
    global getcmd
    global fold, book_uid, book_url,sum_book
    book_uid = book_id
    getcmd = os.getcwd()
    fold = getcmd+"\\zzuli"
    if os.path.exists(fold):
        shutil.rmtree(fold)
        time.sleep(0.1)
    os.mkdir(fold)
    book_url = "http://img.bookask.com/book/read/" + book_id+"/"
    sum_book = count_book()


def down_load():
    # print(fold)
    threading_list =[]
    for i in range(thread_count):
        t = threading.Thread(target=load_img, args=(i,))
        t.start()
        threading_list.append(t)

    for i in threading_list:
        i.join()


def do_imge_pdf():
    file = getcmd + "\\" + title_name+".pdf"
    with open(file, "wb") as f:
        lst = list()
        for i in range(1, sum_book+1):
            lst.append(fold+"\\"+str(i)+".jpeg")
        # 将有文件目录的列表数据转换为字节数据放入文件
        pdfy = img2pdf.convert(lst)
        print(title_name+" : 已成功转换为pdf")
        f.write(pdfy)


def to_pdf():
    do_imge_pdf()


if __name__ == "__main__":
    print("程序启动。。。")
    f = open("in.txt")
    line = f.readline()
    while line:
        print(line.strip("\n"))

        print("书籍号："+line + "下载中，，，，")
        mark = 1
        while mark:
            mark = 0
            try:
                id = line
                init(id)
                # print(getcmd)
                down_load()
                to_pdf()
                line = f.readline()
            except Exception :
                mark = 1
                time.sleep(10)
    # shutil.rmtree(fold)
