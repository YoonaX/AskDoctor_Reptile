# coding: utf-8
import urllib.request
from bs4 import BeautifulSoup
import json
import os


def get_all_information():
    ask_url_list = ["http://www.120ask.com/list/waike/",
                    "http://www.120ask.com/list/neike/",
                    "http://www.120ask.com/list/fuchanke/",
                    "http://www.120ask.com/list/erke/",
                    "http://www.120ask.com/list/pfxbk/",
                    "http://www.120ask.com/list/zhongyike/",
                    "http://www.120ask.com/list/wuguanke/",
                    "https://www.120ask.com/list/chuanranke/",
                    "https://www.120ask.com/list/xljkk/",
                    "https://www.120ask.com/list/zxmrk/",
                    "https://www.120ask.com/list/zhongliuke/",
                    "https://www.120ask.com/list/fzjck/",
                    "https://www.120ask.com/list/ydss/",
                    "https://www.120ask.com/list/bjys/",
                    "https://www.120ask.com/list/znjy/",
                    "https://www.120ask.com/list/jjhj/",
                    "https://www.120ask.com/list/yaopin/",
                    "https://www.120ask.com/list/kfyxk/",
                    "https://www.120ask.com/list/yybjk/",
                    "https://www.120ask.com/list/yichuan",
                    "https://www.120ask.com/list/tijianke",
                    "https://www.120ask.com/list/qtks"]

    ask_url1 = ["http://www.120ask.com/list/waike/"]
    headers_list = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    Count = 0
    for url in ask_url1:
        reqList = urllib.request.Request(url=url, headers=headers_list)
        pageList = urllib.request.urlopen(reqList, timeout=10)
        HtmlCodeList = pageList.read().decode('UTF-8')
        soup = BeautifulSoup(HtmlCodeList, "html.parser")
        question_page = soup.find('ul', class_='clears h-ul3')
        question_page_url_div = question_page.findAll('div', class_='fl h-left-p')

        while Count < 200:
            urlArr = []
            for item in question_page_url_div:
                page_url = item.find('a', {'class': 'q-quename'}).get('href')
                print(page_url)
                get_detail(page_url)

            if Count != 200:
                Count += 1
                next_page = soup.find('div', class_='clears h-page')
                print(next_page)
                next_page_all_url = next_page.findAll('span')
                next_page_url = ''
                for page_index in next_page_all_url:
                    if page_index.find('a').get_text() == '下一页':
                        next_page_url = page_index.find('a').get('href')
                # print(next_page_url[2:])
                next_page_str = "https://" + next_page_url[2:]
                print(next_page_str)
                reqList = urllib.request.Request(url=next_page_str, headers=headers_list)
                pageList = urllib.request.urlopen(reqList, timeout=10)
                HtmlCodeList = pageList.read().decode('UTF-8')
                soup = BeautifulSoup(HtmlCodeList, "html.parser")
                question_page = soup.find('ul', class_='clears h-ul3')
                question_page_url_div = question_page.findAll('div', class_='fl h-left-p')

        Count = 0


def get_detail(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    page = urllib.request.urlopen(req, timeout=10)
    file_prefix = ''
    for i in url:
        if i == ':':
            file_prefix += '_'
        elif i == '/':
            file_prefix += '$'
        else:
            file_prefix += i
    # print(file_prefix)

    html_code = page.read().decode('UTF-8')
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
            if doctor_str[i] == '师':
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
        if doctor_skilled.index(item) % 2 == 0:
            # print(item.get_text())
            doctor_skilled_list.append(item.get_text())

    # relay = soup.findAll('div', {'class': 'b_anscont_cont'})
    # doctor_relay_list = []
    # for item in relay:
    #     result = ''
    #     for s in item.find('p').get_text():
    #         if s != ' ':
    #             result += s
    #     # print(result)
    #     doctor_relay_list.append(result)

    # time = soup.findAll('span', {'class': 'b_anscont_time'})
    # doctor_relay_time_list = []
    # for item in time:
    #     result = ''
    #     time_str = item.get_text()
    #     for i in range(len(time_str)):
    #         if time_str[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ':'] or (time_str[i] == ' ' and i
    #                                                                                            < len(time_str) and time_str[i + 1] in [
    #                                                                                               '0', '1', '2', '3',
    #                                                                                               '4', '5', '6', '7',
    #                                                                                               '8', '9', '-', ':']):
    #             result += time_str[i]
    #     # print(result)
    #     doctor_relay_time_list.append(result)

    ask_relay = []
    # print(doctor_detail_list)
    # print(doctor_url_list)
    # print(doctor_skilled_list)
    for i in range(len(doctor_detail_list)):
        data = {
            "doctor_detail": doctor_detail_list[i],
            "doctor_url": doctor_url_list[i],
            "doctor_skilled": doctor_skilled_list[i],
            "doctor_reply": reply_list[i]
        }
        ask_relay.append(data)

    if len(family_title) == 1:
        path = "F:\\AskDoctor_Information\\" + family_title[0] + "\\其它"
        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)
        file = open(path + "\\" + file_prefix + ".json", "w")
        # print(path + "\\" + file_prefix + ".json", encoding="utf-8")

    elif len(family_title) == 2:
        # print("family:")
        # print(family_title)
        path = "F:\\AskDoctor_Information\\" + family_title[0] + "\\" + family_title[1] + "\\其它"

        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)
        file = open(path + "\\" + file_prefix + ".json", "w", encoding="utf-8")
        # print(path + file_prefix + ".json")

    else:
        path = "F:\\AskDoctor_Information\\" + family_title[0] + "\\" + family_title[1] + "\\" + family_title[2]
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


url = "http://www.120ask.com/question/73876372.htm"
url11 = "http://www.120ask.com/question/73912918.htm"
url22 = "http://www.120ask.com/question/73913765.htm"
u = "http://www.120ask.com/question/73913720.htm"
a = "http://www.120ask.com/question/73916324.htm"
b = "http://www.120ask.com/question/64750169.htm"
# get_detail(b)
get_all_information()
