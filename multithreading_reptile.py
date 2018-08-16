import threading
import json
import urllib.request
import os
from bs4 import BeautifulSoup
from queue import Queue
import time
import sys
import io


def get_doctor_reply(reply_list, soup, div_class):
    doctor_all_information = soup.findAll("div", {"class": div_class})
    for doc_item in doctor_all_information:
        r_list = []
        reply_all = doc_item.findAll('div', {'class': 'crazy_new'})
        time_all = soup.findAll('span', {'class': 'b_anscont_time'})

        for i in range(len(reply_all)):
            reply_result = reply_all[i].find('p').get_text()
            reply = ''
            # get reply
            for r_str in reply_result:
                if r_str != ' ':
                    reply += r_str
            time_result = time_all[i].get_text()
            time_standard = ''
            for j in range(len(time_result)):
                # get standard time
                if time_result[j] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ':'] or (
                        time_result[j] == ' ' and j
                        < len(time_result) and
                        time_result[j + 1] in [
                            '0', '1', '2', '3',
                            '4', '5', '6', '7',
                            '8', '9', '-', ':']):
                    time_standard += time_result[j]
            r_list.append(reply + " | " + time_standard)
        reply_list.append(r_list)


def get_all_detail(html_code, prefix):
    file_prefix = prefix
    soup = BeautifulSoup(html_code, "html.parser")

    family = soup.find('div', {'class': 'b_route'})
    family_url = family.findAll('a')
    family_title = []

    # get family of a question
    for i in range(1, len(family_url)):
        family_title.append(family_url[i].get_text())

    # get title of a question
    title_detail = soup.find('div', {'class': 'b_askti'})
    title = title_detail.find('h1').get_text()

    ask_detail = soup.find('div', {'class': 'b_askab1'})
    ask = ask_detail.findAll('span')

    # get sex and age of people asking
    sex_age = ask[0].get_text()

    # get time and age of people asking
    ask_time = ask[1].get_text()

    reply_list = []

    # get accepted reply of a question
    get_doctor_reply(reply_list, soup, "b_acceptcont clears")

    # get other reply of a question
    get_doctor_reply(reply_list, soup, "b_answercont clears")

    # get description of a question
    des = soup.find(attrs={'name': 'description'})['content']

    # get helps wanted by patients
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
        # get doctor's detail
        doctor_detail_list.append(result)
        try:
            # if existing, get doctor's url
            doctor_url_list.append(item.find('a').get('href'))
        except AttributeError:
            # if not existing, get None
            doctor_url_list.append("None")

    doctor_skilled = soup.findAll('span', {'class': 'b_sp2'})
    doctor_skilled_list = []

    for item in doctor_skilled:
        # get doctor's speciality
        if doctor_skilled.index(item) % 2 == 0 and '擅长' in item.get_text():
            doctor_skilled_list.append(item.get_text())

    ask_relay = []
    if len(doctor_skilled_list) < len(doctor_url_list):
        # if we can't find some doctors' speciality in this page, these doctor's specialities are none
        for i in range(len(doctor_url_list) - len(doctor_skilled_list)):
            doctor_skilled_list.append("无")

    # write doctor's information to data
    for i in range(len(doctor_detail_list)):
        data = {
            "doctor_detail": doctor_detail_list[i],
            "doctor_url": doctor_url_list[i],
            "doctor_skilled": doctor_skilled_list[i],
            "doctor_reply": reply_list[i]
        }
        ask_relay.append(data)

    # write all information to corresponding catalogue according to the family of a question
    if len(family_title) == 1:
        path = "F:\\Ask_Information\\" + family_title[0] + "\\其它"
        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)
        file = open(path + "\\" + file_prefix + ".json", "w")
    elif len(family_title) == 2:
        path = "F:\\Ask_Information\\" + family_title[0] + "\\" + family_title[1] + "\\其它"

        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)
        file = open(path + "\\" + file_prefix + ".json", "w", encoding="utf-8")
    else:
        path = "F:\\Ask_Information\\" + family_title[0] + "\\" + family_title[1] + "\\" + family_title[2]
        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)
        file = open(path + "\\" + file_prefix + ".json", "w", encoding="utf-8")

    question_data = {
        "title": title,
        "sex_age": sex_age,
        "ask_time": ask_time,
        "description": des,
        "helper:": helps,
        "ask_reply": ask_relay
    }

    # write data to json
    json.dump(question_data, file, ensure_ascii=False, indent=4)
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
                req = urllib.request.Request(url=url, headers=self.headers)
                open_page = urllib.request.urlopen(req, timeout=10)
                html_code = open_page.read().decode('UTF-8')
                html_code = html_code.replace(u'\xa0', u' ')
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
                    get_all_detail(html, prefix)

            except Exception as e:
                print(e)


def main():
    page_queue = Queue(30)  # 页码的队列，表示10个页面，不写表示不限制个数
    for i in range(72930001, 72930030):  # 放入1~10的数字，先进先出
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
        "采集线程86号", "采集线程87号", "采集线程88号", "采集线程89号", "采集线程90号",
        "采集线程91号", "采集线程92号", "采集线程93号", "采集线程94号", "采集线程95号",
        "采集线程96号", "采集线程97号", "采集线程98号", "采集线程99号", "采集线程100号",
        "采集线程101号", "采集线程102号", "采集线程103号", "采集线程104号", "采集线程105号",
        "采集线程106号", "采集线程107号", "采集线程108号", "采集线程109号", "采集线程110号",
        "采集线程111号", "采集线程112号", "采集线程113号", "采集线程114号", "采集线程115号",
        "采集线程116号", "采集线程117号", "采集线程118号", "采集线程119号", "采集线程120号",
        "采集线程121号", "采集线程122号", "采集线程123号", "采集线程124号", "采集线程125号",
        "采集线程126号", "采集线程127号", "采集线程128号", "采集线程129号", "采集线程130号",
        "采集线程131号", "采集线程132号", "采集线程133号", "采集线程134号", "采集线程135号",
        "采集线程136号", "采集线程137号", "采集线程138号", "采集线程139号", "采集线程140号",
        "采集线程141号", "采集线程142号", "采集线程143号", "采集线程144号", "采集线程145号",
        "采集线程146号", "采集线程147号", "采集线程148号", "采集线程149号", "采集线程150号",
        "采集线程151号", "采集线程152号", "采集线程153号", "采集线程154号", "采集线程155号",
        "采集线程156号", "采集线程157号", "采集线程158号", "采集线程159号", "采集线程160号",
        "采集线程161号", "采集线程162号", "采集线程163号", "采集线程164号", "采集线程165号",
        "采集线程166号", "采集线程167号", "采集线程168号", "采集线程169号", "采集线程160号",
        "采集线程171号", "采集线程172号", "采集线程173号", "采集线程174号", "采集线程175号",
        "采集线程176号", "采集线程177号", "采集线程178号", "采集线程179号", "采集线程170号",
        "采集线程181号", "采集线程182号", "采集线程183号", "采集线程184号", "采集线程185号",
        "采集线程186号", "采集线程187号", "采集线程188号", "采集线程189号", "采集线程190号",
        "采集线程191号", "采集线程192号", "采集线程193号", "采集线程194号", "采集线程195号",
        "采集线程196号", "采集线程197号", "采集线程198号", "采集线程199号", "采集线程200号"
    ]  # 存储三个采集线程的列表集合，留着后面join（等待所有子进程完成在退出程序）

    thread_crawl = []
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
        "解析线程96号", "解析线程97号", "解析线程98号", "解析线程99号", "解析线程100号",
        "解析线程101号", "解析线程102号", "解析线程103号", "解析线程104号", "解析线程105号",
        "解析线程106号", "解析线程107号", "解析线程108号", "解析线程109号", "解析线程110号",
        "解析线程111号", "解析线程112号", "解析线程113号", "解析线程114号", "解析线程115号",
        "解析线程116号", "解析线程117号", "解析线程118号", "解析线程119号", "解析线程120号",
        "解析线程121号", "解析线程122号", "解析线程123号", "解析线程124号", "解析线程125号",
        "解析线程126号", "解析线程127号", "解析线程128号", "解析线程129号", "解析线程130号",
        "解析线程131号", "解析线程132号", "解析线程133号", "解析线程134号", "解析线程135号",
        "解析线程136号", "解析线程137号", "解析线程138号", "解析线程139号", "解析线程140号",
        "解析线程141号", "解析线程142号", "解析线程143号", "解析线程144号", "解析线程145号",
        "解析线程146号", "解析线程147号", "解析线程148号", "解析线程149号", "解析线程150号",
        "解析线程151号", "解析线程152号", "解析线程153号", "解析线程154号", "解析线程155号",
        "解析线程156号", "解析线程157号", "解析线程158号", "解析线程159号", "解析线程160号",
        "解析线程161号", "解析线程162号", "解析线程163号", "解析线程164号", "解析线程165号",
        "解析线程166号", "解析线程167号", "解析线程168号", "解析线程169号", "解析线程170号",
        "解析线程171号", "解析线程172号", "解析线程173号", "解析线程174号", "解析线程175号",
        "解析线程176号", "解析线程177号", "解析线程178号", "解析线程179号", "解析线程180号",
        "解析线程181号", "解析线程182号", "解析线程183号", "解析线程184号", "解析线程185号",
        "解析线程186号", "解析线程187号", "解析线程188号", "解析线程189号", "解析线程190号",
        "解析线程191号", "解析线程192号", "解析线程193号", "解析线程194号", "解析线程195号",
        "解析线程196号", "解析线程197号", "解析线程198号", "解析线程199号", "解析线程200号"
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
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码
    start = time.time()
    main()
    end = time.time()
    print("用时：%s" % (end - start))
