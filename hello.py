# coding: utf-8
import urllib.request
from bs4 import BeautifulSoup
import json
import os

# def get_information(url):
#     qUrl = url.find('a', class_='q-quename')
#     print(qUrl.get('href'))
#
#     reqList = urllib.request.Request(url=qUrl.get('href'), headers=headersList)
#     pageList = urllib.request.urlopen(reqList)
#     HtmlCodeList = pageList.read().decode('UTF-8')
#     sListSoup = BeautifulSoup(HtmlCodeList, "html.parser")
#
#     tag = sListSoup.find('div', class_='b_askcont')
#     des = tag.findAll('p')
#
#     blankDes = des[0].contents[2]
#     Des = ''
#     for i in range(len(blankDes)):
#         if blankDes[i] != ' ' and i != '\n':
#             Des += blankDes[i]
#         if (i == len(blankDes) - 1):
#             Des = des[0].contents[1].get_text() + Des
#     urlArr.append(qUrl)
#     print(Des)


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

    des = soup.find(attrs={'name': 'description'})['content']
    # print(des)
    helps = soup.find(attrs={'name': 'keywords'})['content']
    # print(helps)
    # tag = soup.find('div', class_='b_askcont')
    # p_help = tag.findAll('p')
    # help_detail = ''
    # print(p_help)
    # print("aaaaaa")
    # if len(p_help) == 2:
    #     help_detail = p_help[1].contents[0].get_text() + p_help[1].contents[1]
    #     print(help_detail)

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
        # print(item.find('a').get('href'))
        doctor_url_list.append(item.find('a').get('href'))

    doctor_skilled = soup.findAll('span', {'class': 'b_sp2'})
    doctor_skilled_list = []
    for item in doctor_skilled:
        if doctor_skilled.index(item) % 2 == 0:
            # print(item.get_text())
            doctor_skilled_list.append(item.get_text())

    relay = soup.findAll('div', {'class': 'b_anscont_cont'})
    doctor_relay_list = []
    for item in relay:
        result = ''
        for s in item.find('p').get_text():
            if s != ' ':
                result += s
        # print(result)
        doctor_relay_list.append(result)

    time = soup.findAll('span', {'class': 'b_anscont_time'})
    doctor_relay_time_list = []
    for item in time:
        result = ''
        time_str = item.get_text()
        for i in range(len(time_str)):
            if time_str[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ':'] or (time_str[i] == ' ' and i
                                                                                               < len(time_str) and time_str[i + 1] in [
                                                                                                  '0', '1', '2', '3',
                                                                                                  '4', '5', '6', '7',
                                                                                                  '8', '9', '-', ':']):
                result += time_str[i]
        # print(result)
        doctor_relay_time_list.append(result)

    ask_relay = []
    for i in range(len(doctor_relay_time_list)):
        data = {
            "doctor_relay_time": doctor_relay_time_list[i],
            "doctor_detail": doctor_detail_list[i],
            "doctor_url": doctor_url_list[i],
            "doctor_skilled": doctor_skilled_list[i],
            "doctor_relay": doctor_relay_list[i]
        }
        ask_relay.append(data)

    # for i in range(len(ask_relay)):
        # print(ask_relay[i])

    if len(family_title) == 1:
        path = "F:\\AskDoctor_Information\\" + family_title[0] + "\\其它"
        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)
        file = open(path + "\\" + file_prefix + ".json", "w")
        # print(path + "\\" + file_prefix + ".json")

    elif len(family_title) == 2:
        # print("family:")
        # print(family_title)
        path = "F:\\AskDoctor_Information\\" + family_title[0] + "\\" + family_title[1] + "\\其它"

        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)
        file = open(path + "\\" + file_prefix + ".json", "w")
        # print(path + file_prefix + ".json")

    else:
        path = "F:\\AskDoctor_Information\\" + family_title[0] + "\\" + family_title[1] + "\\" + family_title[2]
        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)
        file = open(path + "\\" + file_prefix + ".json", "w")

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

    # file_test = open("F:\\AskDoctor_Information\\1.json")
    # test = json.load(file_test)
    # print(test['ask_reply'][0]['doctor_relay_time'])


url = "http://www.120ask.com/question/73876372.htm"
# get_detail(url)

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
            NextPage = sListSoup1.find('div', class_='clears h-page')
            # print(NextPage)
            NextPageAllUrl = NextPage.findAll('span')
            NextPageUrl = NextPageAllUrl[7].find('a').get('href')
            print(NextPageUrl[2:])
            Str = "https://" + NextPageUrl[2:]
            print(Str)
            reqList = urllib.request.Request(url=Str, headers=headers_list)
            pageList = urllib.request.urlopen(reqList, timeout=10)
            HtmlCodeList = pageList.read().decode('UTF-8')
            sListSoup1 = BeautifulSoup(HtmlCodeList, "html.parser")
            Ul = sListSoup1.find('ul', class_='clears h-ul3')
            UrlList = Ul.findAll('div', class_='fl h-left-p')

    Count = 0
