# Вариант I
# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и
# сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient
from pprint import pprint

chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("__headless")

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
driver.implicitly_wait(10)

driver.get('https://account.mail.ru/login')

client = MongoClient('127.0.0.1', 27017)
db = client['inbox']
inbox_mail = db.inbox
inbox_mail.drop()

elem = driver.find_element(By.XPATH, "//input[@name='username']")
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)
time.sleep(.1)
elem = driver.find_element(By.XPATH, "//input[@name='password']")
elem.send_keys('NextPassword172#')
elem.send_keys(Keys.ENTER)

msg1 = driver.find_element(By.XPATH, "//div[contains(@class,'ReactVirtualized__Grid__innerScrollContainer')]/a[1]")
link = msg1.get_attribute('href')
driver.get(link)

inbox_all = []

while True:
    inbox = {}
    time.sleep(1)
    sent_from = driver.find_element(By.XPATH, "//div[@class='letter__author']/span[@class='letter-contact']").text
    sent_date = driver.find_element(By.XPATH, "//div[@class='letter__author']/div[@class='letter__date']").text
    subject = driver.find_element(By.XPATH, "//h2[@class='thread-subject']").text
    msg_body_text = ''
    for any in driver.find_elements(By.XPATH, "*//div[@class='letter-body']"):
        msg_body_text += ' '.join(any.text)

    inbox['sent_from'] = sent_from
    inbox['sent_date'] = sent_date
    inbox['subject'] = subject
    inbox['msg_body_text'] = msg_body_text

    inbox_all.append(inbox)
    try:
        inbox_mail.insert_one({
            'sent_from' : sent_from,
            'sent_date' : sent_date,
            'subject' : subject,
            'msg_body_text' : msg_body_text
        })
    except:
        pass

    button = driver.find_element(By.XPATH, "//span[@data-title-shortcut = 'Ctrl+↓']")
    arrow_down = button.get_attribute('disabled')
    print(arrow_down)
    if arrow_down != None:
        break
    button.click()





