from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from random import randint
import time
import datetime

#===================================
# VARIABLES
#===================================

username_credentials = ''
password_credentials = ''
post_id = 'B5FkvNIppAB'
comment_to_spam = ''
spam_interval = 123
spam_limit = 500

#===================================

trackfile = open('trackfile.txt', 'r')
logfile = open('log.txt', 'a')
clickcounter = -1
for line in trackfile:
    clickcounter = int(line)
    print('line: ', line)
    break
print('previous counts: {} '.format(clickcounter))

print('logging in..');
browser = webdriver.Chrome()
browser.set_page_load_timeout(30)
browser.get("https://www.instagram.com/accounts/login/")
delay = 5
try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'coreSpriteLoggedOutWordmark')))
    time.sleep(3)
except TimeoutError:
    print("Loading took too much time!")
assert "Login" in browser.title

user = browser.find_element_by_name("username")
passw = browser.find_element_by_name('password')
login = browser.find_element_by_xpath("//button[@type='submit']")

ActionChains(browser)\
    .move_to_element(user).click()\
    .send_keys(username_credentials)\
    .move_to_element(passw).click()\
    .send_keys(password_credentials)\
    .perform()
login.click()

for i in range(10, 0, -1):
  print('starting spam in {}'.format(i))
  time.sleep(1)
post_url = "https://www.instagram.com/p/{}/".format(post_id)
browser.get(post_url)
delay = 5
try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/p/{}/']".format(post_id))))
    time.sleep(3)
except TimeoutError:
    print("Loading took too much time!")
assert "on Instagram" in browser.title
print('login success! start spam..')
logfile.write('{} - logged in as {}\n'.format(datetime.datetime.now(), username_credentials))
logfile.close()

while True:
    comment = browser.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
    comment.click()
    inputstr = comment_to_spam
    for i in range(len(inputstr)):
        comment = browser.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
        comment.send_keys(inputstr[i])
        time.sleep(0.2)
    post = browser.find_element_by_xpath("//button[@type='submit'][text()='Post']")
    post.click()
    clickcounter += 1
    track = open('trackfile.txt', 'w')
    track.write(str(clickcounter))
    track.close()
    print('{} times clicked.. clicking in {} seconds'.format(clickcounter, spam_interval));
    logfile = open('log.txt', 'a+')
    logfile.write('{} - clicked ({}) times in total\n'.format(datetime.datetime.now(), clickcounter))
    logfile.close()
    if clickcounter >= spam_limit:
        print('clickcounter reached spam_limit ({}), stopping process..'.format(clickcounter))
        break
    time.sleep(spam_interval)
browser.close()