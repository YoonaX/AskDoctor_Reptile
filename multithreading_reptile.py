import threading
import json
# import time
import urllib.request
import os
from bs4 import BeautifulSoup
from queue import Queue
import time
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8') #改变标准输出的默认编码

def get_detail(html_code, prefix):
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    # req = urllib.request.Request(url=url, headers=headers)
    # page = urllib.request.urlopen(req, timeout=10)
    file_prefix = prefix
    # for i in url:
    #     if i == ':':
    #         file_prefix += '_'
    #     elif i == '/':
    #         file_prefix += '$'
    #     else:
    #         file_prefix += i
    # print(file_prefix)
    #
    # html_code = page.read().decode('UTF-8')
    soup = BeautifulSoup(html_code, "html.parser")

    family = soup.find('div', {'class': 'b_route'})
    family_url = family.findAll('a')
    family_title = []
    for i in range(1, len(family_url)):
        # print(family_url[i].get_text())
        family_title.append(family_url[i].get_text())

    title_detail = soup.find('div', {'class': 'b_askti'})
    title = title_detail.find('h1').get_text()
    # print(title)

    ask_detail = soup.find('div', {'class': 'b_askab1'})
    ask = ask_detail.findAll('span')
    sex_age = ask[0].get_text()
    ask_time = ask[1].get_text()
    # print(sex_age)
    # print(ask_time)

    accpte_doctor_all_information = soup.findAll("div", {"class": "b_acceptcont clears"})
    # print(len(accpte_doctor_all_information))
    reply_list = []
    for doc_item in accpte_doctor_all_information:
        r_list = []
        reply_all = doc_item.findAll('div', {'class': 'crazy_new'})
        time_all = soup.findAll('span', {'class': 'b_anscont_time'})

        for i in range(len(reply_all)):
            # print("Reply:")
            reply_result = reply_all[i].find('p').get_text()
            reply = ''
            for r_str in reply_result:
                if r_str != ' ':
                    reply += r_str
            # print(reply)
            # print("Time:")
            time_result = time_all[i].get_text()
            time_standard = ''
            for j in range(len(time_result)):
                if time_result[j] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ':'] or (time_result[j] == ' ' and j
                                                                                                   < len(time_result) and
                                                                                                   time_result[j + 1] in [
                                                                                                       '0', '1', '2', '3',
                                                                                                       '4', '5', '6', '7',
                                                                                                       '8', '9', '-', ':']):
                    time_standard += time_result[j]
            # print(time_standard)
            # print(reply + " | " + time_standard)
            r_list.append(reply + " | " + time_standard)
        reply_list.append(r_list)
        # print(reply_list)

    doctor_all_information = soup.findAll("div", {"class": "b_answercont clears"})
    # print(len(doctor_all_information))
    for doc_item in doctor_all_information:
        r_list = []
        reply_all = doc_item.findAll('div', {'class': 'crazy_new'})
        time_all = soup.findAll('span', {'class': 'b_anscont_time'})

        for i in range(len(reply_all)):
            # print("Reply:")
            reply_result = reply_all[i].find('p').get_text()
            reply = ''
            for r_str in reply_result:
                if r_str != ' ':
                    reply += r_str
            # print(reply)
            # print("Time:")
            time_result = time_all[i].get_text()
            time_standard = ''
            for j in range(len(time_result)):
                if time_result[j] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ':'] or (time_result[j] == ' ' and j
                                                                                                   < len(time_result) and
                                                                                                   time_result[j + 1] in [
                                                                                                       '0', '1', '2', '3',
                                                                                                       '4', '5', '6', '7',
                                                                                                       '8', '9', '-', ':']):
                    time_standard += time_result[j]
            # print(time_standard)
            # print(reply + " | " + time_standard)
            r_list.append(reply + " | " + time_standard)
        reply_list.append(r_list)
        # print(reply_list)

    # print(len(reply_list))
    des = soup.find(attrs={'name': 'description'})['content']
    # print(des)
    helps = soup.find(attrs={'name': 'keywords'})['content']

    doctor_detail = soup.findAll('span', {'class': 'b_sp1'})
    doctor_detail_list = []
    doctor_url_list = []
    for item in doctor_detail:
        result = ''
        doctor_str = item.get_text()
        for i in range(len(doctor_str)):
            if doctor_str[i] not in ['\n', ' ', ' ']:
                result += doctor_str[i]
            if doctor_str[i] == '\n':
                result += ' '
            if doctor_str[i] == ' ':
                result += ' '
            if doctor_str[i] == '师'or doctor_str[i] == '员' or doctor_str[i] == '他':
                break
        # print("Result: " + result)
        doctor_detail_list.append(result)
        # print(item)
        try:
            # print(item.find('a').get('href'))
            doctor_url_list.append(item.find('a').get('href'))
        except AttributeError:
            doctor_url_list.append("None")

    doctor_skilled = soup.findAll('span', {'class': 'b_sp2'})
    doctor_skilled_list = []

    for item in doctor_skilled:
        if doctor_skilled.index(item) % 2 == 0 and '擅长' in item.get_text():
            # print("item: ")
            # print(item.get_text())
            doctor_skilled_list.append(item.get_text())

    ask_relay = []
    if len(doctor_skilled_list) < len(doctor_url_list):
        for i in range(len(doctor_url_list) - len(doctor_skilled_list)):
            doctor_skilled_list.append("无")

    for i in range(len(doctor_detail_list)):
        data = {
            "doctor_detail": doctor_detail_list[i],
            "doctor_url": doctor_url_list[i],
            "doctor_skilled": doctor_skilled_list[i],
            "doctor_reply": reply_list[i]
        }
        ask_relay.append(data)

    if len(family_title) == 1:
        path = "F:\\Ask_Information\\" + family_title[0] + "\\其它"
        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)
        file = open(path + "\\" + file_prefix + ".json", "w")
        # print(path + "\\" + file_prefix + ".json", encoding="utf-8")

    elif len(family_title) == 2:
        # print("family:")
        # print(family_title)
        path = "F:\\Ask_Information\\" + family_title[0] + "\\" + family_title[1] + "\\其它"

        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)
        file = open(path + "\\" + file_prefix + ".json", "w", encoding="utf-8")
        # print(path + file_prefix + ".json")

    else:
        path = "F:\\Ask_Information\\" + family_title[0] + "\\" + family_title[1] + "\\" + family_title[2]
        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)
        file = open(path + "\\" + file_prefix + ".json", "w", encoding="utf-8")

    data = {
        "title": title,
        "sex_age": sex_age,
        "ask_time": ask_time,
        "description": des,
        "helper:": helps,
        "ask_reply": ask_relay
    }
    json.dump(data, file, ensure_ascii=False, indent=4)
    file.close()


class ThreadCrawl(threading.Thread):
    def __init__(self, thread_name, page_queue, data_queue, file_prefix_queue):
        super(ThreadCrawl, self).__init__()  # 调用父类初始化方法
        self.thread_name = thread_name  # 线程名
        self.page_queue = page_queue  # 页码队列
        self.data_queue = data_queue  # 数据队列
        self.file_prefix_queue = file_prefix_queue
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


    def run(self):
        print("启动" + self.thread_name)
        while not self.page_queue.empty():  # 如果pageQueue为空，采集线程退出循环 Queue.empty() 判断队列是否为空
            try:
                # 取出一个数字，先进先出
                # 可选参数block，默认值为True
                # 1. 如果对列为空，block为True的话，不会结束，会进入阻塞状态，直到队列有新的数据
                # 2. 如果队列为空，block为False的话，就弹出一个Queue.empty()异常，
                page = self.page_queue.get(False)
                url = "https://www.120ask.com/question/" + str(page) + ".htm"
                print(url)
                # print("AAAAAAAAAAAAAAAAAAABBB")
                req = urllib.request.Request(url=url, headers=self.headers)
                # print("BBBBBBBBBBBBBBBBBBBBBB")
                open_page = urllib.request.urlopen(req, timeout=10)
                html_code = open_page.read().decode('UTF-8')
                html_code = html_code.replace(u'\xa0', u' ')
                # print("AAAAAAAAAAAAAAAAAAAAAA")
                # print(html_code)
                prefix = ''
                for i in url:
                    if i == ':':
                        prefix += '_'
                    elif i == '/':
                        prefix += '$'
                    else:
                        prefix += i
                self.file_prefix_queue.put(prefix)
                time.sleep(1)  # 等待1s等他全部下完
                self.data_queue.put(html_code)
            except Exception as e:
                pass
        print("结束" + self.thread_name)


class ThreadParse(threading.Thread):
    def __init__(self, threadName, dataQueue, lock, file_prefix_queue):
        super(ThreadParse, self).__init__()
        self.threadName = threadName
        self.dataQueue = dataQueue
        self.lock = lock  # 文件读写锁
        self.file_prefix_queue = file_prefix_queue
        self.headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}

    def run(self):
        print("启动" + self.threadName)
        while not self.dataQueue.empty():  # 如果pageQueue为空，采集线程退出循环
            try:
                html = self.dataQueue.get()  # 解析为HTML DOM
                prefix = self.file_prefix_queue.get()
                with self.lock:
                    print("解析：" + prefix)
                    get_detail(html, prefix)

            except Exception as e:
                print(e)


def main():
    page_queue = Queue(4000)  # 页码的队列，表示10个页面，不写表示不限制个数
    for i in range(60006001, 60010000):  # 放入1~10的数字，先进先出
        page_queue.put(i)

    data_queue = Queue()  # 采集结果(每页的HTML源码)的数据队列，参数为空表示不限制个数
    file_prefix_queue = Queue()
    crawl_list = [
        "采集线程1号", "采集线程2号", "采集线程3号", "采集线程4号", "采集线程5号",
        "采集线程6号", "采集线程7号", "采集线程8号", "采集线程9号", "采集线程10号",
        "采集线程11号", "采集线程12号", "采集线程13号", "采集线程14号", "采集线程15号",
        "采集线程16号", "采集线程17号", "采集线程18号", "采集线程19号", "采集线程20号",
        "采集线程21号", "采集线程22号", "采集线程23号", "采集线程24号", "采集线程25号",
        "采集线程26号", "采集线程27号", "采集线程28号", "采集线程29号", "采集线程30号",
        "采集线程31号", "采集线程32号", "采集线程33号", "采集线程34号", "采集线程35号",
        "采集线程36号", "采集线程37号", "采集线程38号", "采集线程39号", "采集线程40号",
        "采集线程41号", "采集线程42号", "采集线程43号", "采集线程44号", "采集线程45号",
        "采集线程46号", "采集线程47号", "采集线程48号", "采集线程49号", "采集线程50号",
        "采集线程51号", "采集线程52号", "采集线程53号", "采集线程54号", "采集线程55号",
        "采集线程56号", "采集线程57号", "采集线程58号", "采集线程59号", "采集线程60号",
        "采集线程61号", "采集线程62号", "采集线程63号", "采集线程64号", "采集线程65号",
        "采集线程66号", "采集线程67号", "采集线程68号", "采集线程69号", "采集线程60号",
        "采集线程71号", "采集线程72号", "采集线程73号", "采集线程74号", "采集线程75号",
        "采集线程76号", "采集线程77号", "采集线程78号", "采集线程79号", "采集线程70号",
        "采集线程81号", "采集线程82号", "采集线程83号", "采集线程84号", "采集线程85号",
        "采集线程86号", "采集线程87号", "采集线程88号", "采集线程89号", "采集线程80号",
        "采集线程91号", "采集线程92号", "采集线程93号", "采集线程94号", "采集线程95号",
        "采集线程96号", "采集线程97号", "采集线程98号", "采集线程99号", "采集线程100号"
    ]  # 存储三个采集线程的列表集合，留着后面join（等待所有子进程完成在退出程序）

    thread_crawl = []
    # print("aaaaaaa")
    for thread_name in crawl_list:
        thread = ThreadCrawl(thread_name, page_queue, data_queue, file_prefix_queue)
        thread.start()
        thread_crawl.append(thread)

    for i in thread_crawl:
        i.join()
        print('1')

    lock = threading.Lock()  # 创建锁

    # *** 解析线程一定要在采集线程join（结束）以后写，否则会出现dataQueue.empty()=True（数据队列为空），因为采集线程还没往里面存东西呢 ***
    parse_list = [
        "解析线程1号", "解析线程2号", "解析线程3号", "解析线程4号", "解析线程5号",
        "解析线程6号", "解析线程7号", "解析线程8号", "解析线程9号", "解析线程10号",
        "解析线程11号", "解析线程12号", "解析线程13号", "解析线程14号", "解析线程15号",
        "解析线程16号", "解析线程17号", "解析线程18号", "解析线程19号", "解析线程20号",
        "解析线程21号", "解析线程22号", "解析线程23号", "解析线程24号", "解析线程25号",
        "解析线程26号", "解析线程27号", "解析线程28号", "解析线程29号", "解析线程30号",
        "解析线程31号", "解析线程32号", "解析线程33号", "解析线程34号", "解析线程35号",
        "解析线程36号", "解析线程37号", "解析线程38号", "解析线程39号", "解析线程40号",
        "解析线程41号", "解析线程42号", "解析线程43号", "解析线程44号", "解析线程45号",
        "解析线程46号", "解析线程47号", "解析线程48号", "解析线程49号", "解析线程50号",
        "解析线程51号", "解析线程52号", "解析线程53号", "解析线程54号", "解析线程55号",
        "解析线程56号", "解析线程57号", "解析线程58号", "解析线程59号", "解析线程60号",
        "解析线程61号", "解析线程62号", "解析线程63号", "解析线程64号", "解析线程65号",
        "解析线程66号", "解析线程67号", "解析线程68号", "解析线程69号", "解析线程70号",
        "解析线程71号", "解析线程72号", "解析线程73号", "解析线程74号", "解析线程75号",
        "解析线程76号", "解析线程77号", "解析线程78号", "解析线程79号", "解析线程80号",
        "解析线程81号", "解析线程82号", "解析线程83号", "解析线程84号", "解析线程85号",
        "解析线程86号", "解析线程87号", "解析线程88号", "解析线程89号", "解析线程90号",
        "解析线程91号", "解析线程92号", "解析线程93号", "解析线程94号", "解析线程95号",
        "解析线程96号", "解析线程97号", "解析线程98号", "解析线程99号", "解析线程100号"
    ]  # 三个解析线程的名字
    thread_parse = []  # 存储三个解析线程，留着后面join（等待所有子进程完成在退出程序）
    for threadName in parse_list:
        thread = ThreadParse(threadName, data_queue, lock, file_prefix_queue)
        thread.start()
        thread_parse.append(thread)

    for j in thread_parse:
        j.join()
        print('2')
    print("谢谢使用！")


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("用时：%s" % (end - start))