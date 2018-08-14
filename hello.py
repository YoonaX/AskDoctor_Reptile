# coding: utf-8
import urllib.request
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import json
Count = 0


# import sys

# type = sys.getfilesystemencoding()

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.pFlag = False
        self.pText = []

    def handle_starttag(self, tag, attrs):
        """

        :param tag:
        :param attrs:
        :return:
        """
        print("Encountered a start tag:", tag)
        if tag == 'p':
            self.pFlag = True

    def handle_endtag(self, tag):
        """

        :param tag:
        :return:
        """
        print("Encountered an end tag:", tag)
        if tag == 'p':
            self.pFlag = False

    def handle_data(self, data):
        """

        :param data:
        :return:
        """
        print("Encountered some data :", data)
        if self.pFlag is True:
            print("AAAAAAAAAAA")
            self.pText.append(data)

    def handle_startendtag(self, tag, attrs):
        """

        :param tag:
        :param attrs:
        :return:
        """
        print("Encountered startendtag :", tag)

    def handle_comment(self, data):
        """

        :param data:
        :return:
        """
        print("Encountered comment:", data)


def GetInformatino(url, Count):
    qUrl = url.find('a', class_='q-quename')
    print(qUrl.get('href'))

    reqList = urllib.request.Request(url=qUrl.get('href'), headers=headersList)
    pageList = urllib.request.urlopen(reqList)
    HtmlCodeList = pageList.read().decode('UTF-8')
    sListSoup = BeautifulSoup(HtmlCodeList, "html.parser")

    tag = sListSoup.find('div', class_='b_askcont')
    des = tag.findAll('p')

    blankDes = des[0].contents[2]
    Des = ''
    for i in range(len(blankDes)):
        if blankDes[i] != ' ' and i != '\n':
            Des += blankDes[i]
        if (i == len(blankDes) - 1):
            Des = des[0].contents[1].get_text() + Des
    urlArr.append(qUrl)
    print(Des)


parser = MyHTMLParser()

url2 = "http://www.120ask.com/question/73879155.htm"
url1 = "http://www.120ask.com/question/73876372.htm"
url3 = "http://www.120ask.com/question/73876372.htm"
url = "http://www.120ask.com/list/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
req = urllib.request.Request(url=url3, headers=headers)
page = urllib.request.urlopen(req)

HtmlCode = page.read().decode('UTF-8')
soup = BeautifulSoup(HtmlCode, "html.parser")

TitleDetail = soup.find('div', {'class': 'b_askti'})
Title = TitleDetail.find('h1').get_text()
print(Title)

AskerDetail = soup.find('div', {'class': 'b_askab1'})
Asker = AskerDetail.findAll('span')
Sex_Age = Asker[0].get_text()
Ask_time = Asker[1].get_text()
print(Sex_Age)
print(Ask_time)


Des = soup.find(attrs={'name': 'description'})['content']
print(Des)

tag = soup.find('div', class_='b_askcont')
des = tag.findAll('p')
Helper = ''
if len(des) > 0:
    Helper = des[1].contents[0].get_text() + des[1].contents[1]
    print(Helper)

Doctor = soup.findAll('span', {'class': 'b_sp1'})
Doctor_Detail_List = []
Doctor_Url_List = []
for item in Doctor:
    Result = ''
    # Str = item.find('a').get_text()
    Str = item.get_text()
    # print(Str)
    for i in range(len(Str)):
        if Str[i] not in ['\n', ' ', ' ']:
            Result += Str[i]
        if Str[i] == '\n':
            Result += ' '
        if Str[i] == ' ':
            Result += ' '
        if Str[i] == '师':
            break
    print("Result: " + Result)
    Doctor_Detail_List.append(Result)
    print(item.find('a').get('href'))
    Doctor_Url_List.append(item.find('a').get('href'))

Doctor_Skilled = soup.findAll('span', {'class': 'b_sp2'})
Doctor_Skilled_List = []
for item in Doctor_Skilled:
    if Doctor_Skilled.index(item) % 2 == 0:
        print(item.get_text())
        Doctor_Skilled_List.append(item.get_text())

relay = soup.findAll('div', {'class': 'b_anscont_cont'})
Doctor_Relay_List = []
# print(len(relay))
for item in relay:
    Result = ''
    # print(item.find('p').get_text())
    for s in item.find('p').get_text():
        if s != ' ':
            Result += s
    print(Result)
    Doctor_Relay_List.append(Result)

time = soup.findAll('span', {'class': 'b_anscont_time'})
Doctor_Relay_Time_List = []
for item in time:
    Result = ''
    # print(item.get_text())
    Str = item.get_text()
    for i in range(len(Str)):
        if Str[i] in ['0', '1', '2', '3', '4', '5', '6','7', '8', '9', '-', ':'] or (Str[i] == ' ' and i < len(Str) and
                                                                                     Str[i + 1] in ['0', '1', '2', '3',
                                                                                                    '4', '5', '6','7',
                                                                                                    '8', '9', '-', ':']):
            Result += Str[i]
    print(Result)
    Doctor_Relay_Time_List.append(Result)

Ask_Relay = []
for i in range(len(Doctor_Relay_Time_List)):
    data = {
        "Doctor_Relay_Time": Doctor_Relay_Time_List[i],
        "Doctor_Detail": Doctor_Detail_List[i],
        "Doctor_Url": Doctor_Url_List[i],
        "Doctor_Skilled": Doctor_Skilled_List[i],
        "Doctor_Relay": Doctor_Relay_List[i]
    }
    Ask_Relay.append(data)

for i in range(len(Ask_Relay)):
    print(Ask_Relay[i])

File = open("F:\\AskDoctor_Information\\1.json", "w")

data = {
    "Title": Title,
    "Sex_Age": Sex_Age,
    "Ask_Time": Ask_time,
    "Description": Des,
    "Helper:": Helper,
    "Ask_Reply": Ask_Relay
}
dataJson = json.dump(data, File, ensure_ascii=False, indent=4)
File.close()

F = open("F:\\AskDoctor_Information\\1.json")
D = json.load(F)
print(D['Ask_Reply'][0]['Doctor_Relay_Time'])


url4 = "http://www.120ask.com/list/waike/"
AskUrl = ["http://www.120ask.com/list/waike/",
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

AskUrl1 = ["http://www.120ask.com/list/waike/"]

headersList = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
# for Url in AskUrl1:
#     reqList = urllib.request.Request(url=Url, headers=headersList)
#     pageList = urllib.request.urlopen(reqList)
#     HtmlCodeList = pageList.read().decode('UTF-8')
#     sListSoup1 = BeautifulSoup(HtmlCodeList, "html.parser")
#     Ul = sListSoup1.find('ul', class_='clears h-ul3')
#     UrlList = Ul.findAll('div', class_='fl h-left-p')
#
#     while Count < 200:
#         urlArr = []
#         for item in UrlList:
#             GetInformatino(item, Count)
#
#         if Count != 200:
#             Count += 1
#             NextPage = sListSoup1.find('div', class_='clears h-page')
#             # print(NextPage)
#             NextPageAllUrl = NextPage.findAll('span')
#             NextPageUrl = NextPageAllUrl[7].find('a').get('href')
#             print(NextPageUrl[2:])
#             Str = "https://" + NextPageUrl[2:]
#             print(Str)
#             reqList = urllib.request.Request(url=Str, headers=headersList)
#             pageList = urllib.request.urlopen(reqList)
#             HtmlCodeList = pageList.read().decode('UTF-8')
#             sListSoup1 = BeautifulSoup(HtmlCodeList, "html.parser")
#             Ul = sListSoup1.find('ul', class_='clears h-ul3')
#             UrlList = Ul.findAll('div', class_='fl h-left-p')
#
#     Count = 0
