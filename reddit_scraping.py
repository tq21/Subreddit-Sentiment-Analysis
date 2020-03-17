import requests
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import time

## initiate chrome driver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/Users/Sky/Documents/webdriver/chromedriver", chrome_options = options)

## load all comments, get webpage
driver.get("https://old.reddit.com/r/movies/comments/fafwsf/official_discussion_the_invisible_man_2020/")
more_comments = driver.find_elements_by_class_name("morecomments")
for i in range(len(more_comments)):
    if more_comments[i].is_displayed():
        driver.execute_script("arguments[0].click();", more_comments[i])
        time.sleep(1)

page_source = driver.page_source

## create soup object
page_soup = soup(page_source, 'html.parser')

content = page_soup.findAll('div', {'class': 'content'})[0]
taglines = content.findAll('p', {'class': 'tagline'})
comments = content.findAll('div', {'class': 'md'})

## output to file
filename = "reddit_comments.csv"
f = open(filename, 'w')
headers = "username, comment\n"
f.write(headers)

for i in range(1, len(comments)):
    tagline = taglines[i]

    # grabs all usernames
    user_container = tagline.findAll('a')[1]
    username = user_container.text.replace(",", " ")

    # grabs texts
    comment = comments[i].text.strip().replace(",", " ")

    f.write(username + "," + comment + "\n")

f.close()