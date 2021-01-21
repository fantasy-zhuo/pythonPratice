#
from selenium import webdriver
import time

url = 'http://192.168.1.66:9081/index.html#/'

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_opts = webdriver.ChromeOptions()
# chrome_opts.add_argument("--headless")
browser = webdriver.Chrome('chromedriver' , options=options)
browser.maximize_window()
browser.get(url)
time.sleep(3)
html = browser.page_source

# 登录
browser.find_element_by_id('username').send_keys('Ladmin2')
browser.find_element_by_id('password').send_keys('123456')
browser.find_element_by_id('submitFun').click()

time.sleep(5)

# 点击校园应用
browser.find_element_by_xpath('//*[@id="mainMenu"]/li[2]').click()

currentHandle = browser.current_window_handle

time.sleep(5)

# 点击学校用户画像
browser.find_element_by_xpath('//*[@id="app"]/section/section/main/div/div[2]/section/main/section/main/div[1]/div/div[20]').click()

time.sleep(5)

browser.switch_to.window(currentHandle)

time.sleep(5)

browser.quit()

