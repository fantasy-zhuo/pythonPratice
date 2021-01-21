# 爬取漫画

import urllib.parse, urllib.request, urllib.error
from bs4 import BeautifulSoup
import re, os
import time, json, requests, threadpool
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor

# 获取目录数据


def getListData():
    try:
        baseUrl = "https://www.mh1234.com/comic/9683.html"
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
        }
        # 构建请求对象
        req = urllib.request.Request(url=baseUrl, headers=header)
        # 发起请求获取网页内容
        res = urllib.request.urlopen(req, timeout=6)

        print("获取漫画目录信息", "*" * 20, "成功获取返回数据")

        pageUrlList = []  # 视频页地址列表

        # 正则匹配规则
        findPageUrl = re.compile(r'href="(.*?)".*第73\d.*')

        # 解析网页数据
        bs = BeautifulSoup(res, "html.parser")

        catalogueList = bs.findAll('a', attrs={'href': re.compile(r'/comic/9683/(.*?)')})

        for content in catalogueList:
            pageUrl = re.findall(findPageUrl, str(content))
            if len(pageUrl) == 0:
                continue
            pageUrlList.append(pageUrl[0])

        print("*" * 20, "解析完成", "*" * 20)

        return pageUrlList

    except urllib.error.HTTPError as e:
        print(e)


# 获取章节数据
def getCartoonData(pageUrl):
    # print("*" * 20, "开始请求", "*" * 20)
    reRequest = True
    while reRequest:
        try:
            baseUrl = "https://www.mh1234.com" + pageUrl

            print(baseUrl)
            html = getHtml(baseUrl, True, 20)

            # 存放图片名字及地址
            imageUrlList = []

            # 正则匹配规则
            findPageNum = re.compile(r'value="(.*?)"')
            filterTitle = re.compile(r".*斗罗大陆\b")
            findImageUrl = re.compile(r'src="(.*?)"')
            findImageIndex = re.compile(r'data-index="(.*?)"')

            # 解析网页数据
            bs = BeautifulSoup(html, "html.parser")

            pageNumList = re.findall(findPageNum, str(bs.findAll('option')))

            if len(pageNumList) == 0:
                print('pageNumList is null')
                reRequest = False
                break

            title = str(re.findall(filterTitle, bs.title.string)[0])

            for page in pageNumList:
                singlePageUrl = "https://www.mh1234.com" + pageUrl + '?p=' + page
                singlePageHtml = getHtml(singlePageUrl, True, 5)
                pageBs = BeautifulSoup(singlePageHtml, "html.parser")
                imageUrlHtmlList = pageBs.findAll('div', attrs={'id': 'images'})

                if len(imageUrlHtmlList) == 0:
                    print("div list is null")
                    continue

                imageUrlHtml = str(imageUrlHtmlList[0])

                if len(re.findall(findImageUrl, str(imageUrlHtml))) == 0:
                    print("imageUrl list is null")
                    continue

                imageUrl = re.findall(findImageUrl, str(imageUrlHtml))[0]
                fileName = str(re.findall(findImageIndex, imageUrlHtml)[0]) + '.jpg'
                imageUrlMap = {'name': fileName, 'url': imageUrl}
                imageUrlList.append(imageUrlMap)

            print('len(imageUrlList)', '*' * 20, len(imageUrlList))
            # 保存图片
            downloadCartoonImage(title, imageUrlList)

            reRequest = False

        except Exception as e:
            print("请求超时，尝试重新请求")
            time.sleep(3)
            print('getCartoonData=', e)


# 获取动态加载后的网页
def getHtml(url, loadmore=False, waittime=5):
    # 隐藏浏览器
    chrome_opts = webdriver.ChromeOptions()
    chrome_opts.add_argument("--headless")
    browser = webdriver.Chrome('chromedriver', options=chrome_opts)
    browser.get(url)
    time.sleep(waittime)
    html = browser.page_source
    browser.quit()
    return html


# 保存数据
def downloadCartoonImage(dirName, imageUrlList):
    try:
        print("*" * 20, dirName + " 开始保存数据", "*" * 20)

        # 判断文件夹是否存在
        path = os.getcwd() + '\\斗罗大陆\\' + dirName

        if not os.path.exists(path):
            os.mkdir(path)

        for imageContent in imageUrlList:
            fileName = imageContent["name"]
            url = imageContent['url']
            r = requests.get(url, stream=True)  # 请求图片地址，注意”r“
            with open(path + '/' + fileName, 'wb') as fd:
                for chunk in r.iter_content():
                    fd.write(chunk)

        print("*" * 20, "保存完成", "*" * 20)

    except Exception as result:
        print("写错误:", result)
    finally:
        fd.close()


def main():
    # 获取章节地址信息
    pageUrlList = getListData()

    print(len(pageUrlList))

    pool = threadpool.ThreadPool(3)  # 线程池设置

    # makeRequests构造线程task请求,第一个参数是线程函数,第二个是参数数组
    tasks = threadpool.makeRequests(getCartoonData, pageUrlList)
    [pool.putRequest(task) for task in tasks]
    # 列表推导式,putRequest向线程池里加task,让pool自己去调度task
    pool.wait()  # 等所有任务结束

    print("*" * 20, "爬取完成", "*" * 20)


if __name__ == '__main__':
    main()
