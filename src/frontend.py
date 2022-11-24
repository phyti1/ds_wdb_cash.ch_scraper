
import os
import time
import json
import traceback
import random
import datetime
import backend

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# Adds chromedriver binary to path
import chromedriver_binary

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd


def init_selenium(timeout):
  
  driver = webdriver.Chrome()
  time.sleep(timeout)
  return driver


def scrape_cash_ch():
  buffer_timeout_s = 1
  page_load_timeout_s = 2
  max_fails = 3
  fails = 0

  # initialize service
  driver = init_selenium(buffer_timeout_s)

  # scrape data
  df_ins = pd.DataFrame()
  i_elem = df_ins.shape[0]
  url = ""

  for i_page in range(3, 2000, 1):
    try:
      url = f"https://www.cash.ch/news/alle?page={i_page}"
      driver.get(url)
      
      # get all news blocks
      main_title_tag = '_3Hxc6z3q'
      _ = WebDriverWait(driver, page_load_timeout_s).until(EC.presence_of_element_located((By.CLASS_NAME, main_title_tag)))
      time.sleep(0.1)

      # get hrefs and text of articles
      news = driver.find_elements(By.CLASS_NAME, main_title_tag)
      if(len(news) == 0):
          raise Exception("no news articles found")

      for i, news_article in enumerate(news):
        df_ins.loc[i_elem, "i_page"] = i_page
        df_ins.loc[i_elem, "href"] = news_article.find_element(By.CLASS_NAME, "_2PHmKV2J").get_attribute("href")
        df_ins.loc[i_elem, "teaser"] = news_article.find_element(By.CLASS_NAME, "_2TpfbHst").get_attribute("innerText")
        df_ins.loc[i_elem, "title"] = news_article.find_element(By.CLASS_NAME, "_1w8f1Lsk").get_attribute("innerText")
        df_ins.loc[i_elem, "date"] = news_article.find_element(By.CLASS_NAME, "_2kyH0Dhp").get_attribute("innerText")
        df_ins.loc[i_elem, "category"] = news_article.find_element(By.CLASS_NAME, "_25SLsqeV").get_attribute("innerText")
        i_elem += 1
      
      # save data


      # reset fails
      fails = 0

    except Exception as e:
      print(e)
      print(f"Scraper failed at <{url}>. Error: {traceback.print_exc()}")

      fails += 1
      if(fails > max_fails):
        break

      



if(__name__ == '__main__'):
  scrape_cash_ch()
