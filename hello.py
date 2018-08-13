# coding: utf-8
import re
import urllib.request
from html.parser import HTMLParser
from bs4 import BeautifulSoup

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
print(HtmlCode)
soup = BeautifulSoup(HtmlCode, "html.parser")
description = re.findall('<meta name="description" content=".*"/>', HtmlCode)
print(description)
r = description[0].split(' ')
print(r[2])
for item in description:
    print(parser.feed(item))
    print(parser.pText)



age = re.findall('<span>[女男] |.*岁</span>', HtmlCode)
print(age)
for item in age:
    # parser.feed(item)
    print(item.find('女'))
    print(item[26:32])

Des = soup.find(attrs={'name': 'description'})['content']
print(Des)

# p = re.findall('<p>(?=&nbsp;).*</p>', HtmlCode)
# for item in p:
#     print(item)
# g = re.findall("追问\s*</span>\s*<p>.*</p>", HtmlCode)
# for item in g:
#     print(item)
#
# solve = re.findall(" <p><span>想得到怎样的帮助：</span>.*</p>", HtmlCode)
# print(solve)
# print("solve: ")
# for item in solve:
#     print(parser.feed(item))
#     print(parser.pText)

tag = soup.find('div', class_='b_askcont')
# print("aaaa")
des = tag.findAll('p')
# print(des[1].contents[0].get_text())
# print(des[1].contents[1])
if len(des) > 0:
    Helper = des[1].contents[0].get_text() + des[1].contents[1]
    print(Helper)
word = '<!-- 回复开始 -->'
# .feed(HtmlCode)


list = [i.start() for i in re.finditer('\\\\', 'C:\\Users\\aaa\\computer\\flicker\\01213.jpg')]
list1 = [i.start() for i in re.finditer(u'<!-- 回复开始 -->', HtmlCode)]
print(list1)

Doctor = soup.findAll('span', {'class': 'b_sp1'})
for item in Doctor:
    print(item.get_text())
    print(item.find('a').get('href'))
    # print(item.find('a').get_text())
    # print(item)

DoctorDetail = soup.findAll('span', {'class': 'b_sp2'})
for item in DoctorDetail:
    if DoctorDetail.index(item) % 2 == 0:
        # print(item.find('a').get('href'))
        # print(item.find('a').get_text())
        # print(item.get_text())
        print(item.get_text())

# description = soup.find(attrs={"name": "description"})['content']
# keywords = soup.find(attrs={"name": "keywords"})['content']
# print(description)
# print(keywords)
# print("SSSSS")



# print(des[0].contents[1].get_text())
# print(des[0].contents[2])

# blankDes = des[0].contents[2]
# Des = ''
#
# for i in range(len(blankDes)):
#     if blankDes[i] != ' ' and i != '\n':
#         Des += blankDes[i]
#     if (i == len(blankDes) - 1):
#         Des = des[0].contents[1].get_text() + Des
#
# print(Des)

soup1 = BeautifulSoup(HtmlCode[16211:20017], 'html.parser')
relay = soup1.find('div', class_='crazy_new')
relayp = relay.findAll('p')
for item in relayp:
    print(item.get_text())
# print(relay)
# re_ask_ans = soup1.find('div', class_='b_ansaddbox')
# re_ask_ans_det = re_ask_ans.find_all('div', attrs = {class: 'b_ansaddli'})

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
