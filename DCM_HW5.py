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

chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("__headless")

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
driver.implicitly_wait(10)

driver.get('https://account.mail.ru/login')

elem = driver.find_element(By.XPATH, "//input[@name='username']")
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)

time.sleep(1)
elem = driver.find_element(By.XPATH, "//input[@name='password']")
elem.send_keys('NextPassword172#')
elem.send_keys(Keys.ENTER)


# # ---------
# elem = driver.find_element(By.XPATH, "//a[contains(@href,'/users/')]")
# link = elem.get_attribute('href')
# driver.get(link)
#
# elem = driver.find_element(By.CLASS_NAME, "text-sm")
# link = elem.get_attribute('href')
# driver.get(link)
#
# elem = driver.find_element(By.NAME, "user[time_zone]")
# select = Select(elem)
# select.select_by_value('Athens')
#
# elem.submit()
#
# driver.refresh()
# driver.back()
# driver.forward()
#
# print()
#
# # driver.quit()
