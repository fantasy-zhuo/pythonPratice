# 爬取小说存进txt

import urllib.parse, urllib.request, urllib.error
from bs4 import BeautifulSoup
import re
import time


# 获取目录数据
def getCatalogueData():
    try:
        baseUrl = "https://www.booktxt.net/7_7296/"
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
            "Cookie": "Hm_lvt_40639e2e855ad00c65304ee021f07859=1610279487; Hm_lpvt_40639e2e855ad00c65304ee021f07859=1610286876"
        }
        # 构建请求对象
        req = urllib.request.Request(url=baseUrl, headers=header)
        # 发起请求获取网页内容
        res = urllib.request.urlopen(req, timeout=6)

        print("获取目录", "*" * 20, "成功获取返回数据")

        # 正则匹配规则
        findSectionUrl = re.compile(r'<dd><a href="(.*?)">')

        # 解析网页数据
        bs = BeautifulSoup(res, "html.parser")
        sectionUrlHtml = str(bs.find("dl"))
        sectionUrlList = re.findall(findSectionUrl, sectionUrlHtml)

        sectionUrlList = sectionUrlList[6:]

        print("*" * 20, "解析完成", "*" * 20)

        return sectionUrlList
    except urllib.error.HTTPError as e:
        print(e)


# 获取章节数据
def getSectionData(sectionUrl):
    print("*" * 20, "开始请求", "*" * 20)
    reRequest = True
    while reRequest:
        try:
            baseUrl = "https://www.booktxt.net/7_7296/" + sectionUrl
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
            }
            # 构建请求对象
            req = urllib.request.Request(url=baseUrl, headers=header)
            # 发起请求获取网页内容
            res = urllib.request.urlopen(req, timeout=6)

            print("获取章节", "*" * 20, "成功获取返回数据")

            # 正则匹配规则
            findTitle = re.compile(r'<h1>(.*?)</h1>')
            findContent = re.compile(r'<div id="content">(.*?)<script>.*m.booktxt.net</div>')

            # 解析网页数据
            bs = BeautifulSoup(res, "html.parser")
            titleHtml = str(bs.find("div", class_="bookname"))
            contentHtml = str(bs.find('div', id="content"));

            title = re.findall(findTitle, titleHtml)[0]
            content = re.findall(findContent, contentHtml)[0]

            # 处理换行符
            content = content.replace('<br/>', '\n')

            merge = '　' + title + '\n' + content

            return merge
        except Exception as e:
            print("请求超时，尝试重新请求")
            time.sleep(1)
            print(e)


# 保存数据
def saveData(fileName, content):
    try:
        f = open(fileName, "a+", encoding="utf-8")

        f.write(content)
    except Exception as result:
        print("写错误:", result)
    finally:
        f.close()


def main():
    # 获取章节地址信息
    sectionUrlList = getCatalogueData()

    print(len(sectionUrlList))

    fileName = "test.txt"

    # 获取章节数据
    for url in sectionUrlList:
        index = sectionUrlList.index(url)
        content = getSectionData(url)
        print("*" * 20, "成功获取 ", index + 1, " 章节", "*" * 20)
        # 保存数据
        saveData(fileName, content)
        print("*" * 20, "成功保存 ", index + 1, " 章节", "*" * 20)


    print("*" * 20, "爬取完成", "*" * 20)
    print("*" * 20, "开始保存数据", "*" * 20)

    print("*" * 20, "保存完成", "*" * 20)


if __name__ == '__main__':
    main()
