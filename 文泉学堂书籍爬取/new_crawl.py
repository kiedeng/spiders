import json
import shutil

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
thread_count = 7

title_name = ""


# 计算书籍总页码
def count_book():
    global title_name, book_uid
    # count_url = "https://lib-nuanxin.wqxuetang.com/v1/read/initread?bid=" + book_uid
    # text = requests.get(count_url).text
    # # print(text)
    # js = json.loads(text)
    with open("书籍信息json.txt", "r", encoding="utf_8") as f:
        data = f.read()
    da = json.loads(data)
    book_uid = str(da["data"]["bid"])
    title_name = da["data"]["name"]
    count = da["data"]["pages"]
    print("书籍id：："+book_uid+"---"+"书籍名称："+title_name+"---"+"页数:"+count)
    return int(count)


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
            while 1:
                try:
                    content = requests.get(url).content
                    break
                except Exception:
                    print("访问出错。。重新访问")
                    time.sleep(1)

            f.write(content)

        time.sleep(0.1)


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
    id = str(book_uid)
    init(id)
    # print(getcmd)
    down_load()
    to_pdf()


    # f = open("in.txt")
    # line = f.readline()
    # while line:
    #     print(line.strip("\n"))
    #
    #     print("书籍号："+line + "下载中，，，，")
    #     id = line
    #     init(id)
    #     # print(getcmd)
    #     down_load()
    #     to_pdf()
    #     line = f.readline()