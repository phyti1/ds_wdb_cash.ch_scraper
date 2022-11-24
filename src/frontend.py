
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
from console_progressbar import ProgressBar

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd


def init_selenium(timeout):
  """
  Initialize Selenium driver

  :param timeout: timeout in seconds to wait for the driver to start the browser

  :return: driver instance
  """

  driver = webdriver.Chrome()
  time.sleep(timeout)
  return driver


def read_data_from_url(driver, url, i_page):
  page_load_timeout_s = 2
  df_page = pd.DataFrame()
  i_article = -1
  try:
    driver.get(url)
    
    # get all news blocks
    main_title_tag = '_3Hxc6z3q'
    _ = WebDriverWait(driver, page_load_timeout_s).until(EC.presence_of_element_located((By.CLASS_NAME, main_title_tag)))
    time.sleep(0.1)

    # get hrefs and text of articles
    news = driver.find_elements(By.CLASS_NAME, main_title_tag)
    if(len(news) == 0):
        raise Exception("no news articles found")

    for i_article, news_article in enumerate(news):
      df_page.loc[i_article, "i_page"] = i_page
      df_page.loc[i_article, "href"] = news_article.find_element(By.CLASS_NAME, "_2PHmKV2J").get_attribute("href")
      try:
        df_page.loc[i_article, "teaser"] = news_article.find_element(By.CLASS_NAME, "_2TpfbHst").get_attribute("innerText")
      except:
        df_page.loc[i_article, "teaser"] = ""
        print(f"<{url}>, article <{i_article}>. No Teaser present.")
      
      df_page.loc[i_article, "title"] = news_article.find_element(By.CLASS_NAME, "_1w8f1Lsk").get_attribute("innerText")
      df_page.loc[i_article, "date"] = news_article.find_element(By.CLASS_NAME, "_2kyH0Dhp").get_attribute("innerText")
      df_page.loc[i_article, "category"] = news_article.find_element(By.CLASS_NAME, "_25SLsqeV").get_attribute("innerText")
    
    return df_page

  except Exception as e:
    print(e)
    print(f"<{url}>, article <{i_article}>. Error: {traceback.print_exc()}")
    raise e
    

def scrape_cash_ch():
  buffer_timeout_s = 1
  max_fails = 3
  fails = 0
  max_pages = 12350

  # initialize service
  driver = init_selenium(buffer_timeout_s)

  # initial setup
  df = pd.DataFrame()
  pb = ProgressBar(total=100, decimals=3, length=50)

  # scrape data
  for i_page in range(1, max_pages):
    url = f"https://www.cash.ch/news/alle?page={i_page}"
    try:
      df_page = read_data_from_url(driver, url, i_page)
      fails = 0
      df = pd.concat([df, df_page], axis=0)

      # save, overwrite data
      backend.save_df_as_csv(df)
      pb.print_progress_bar(i_page / max_pages * 100)
    except:
      fails += 1
      if(fails > max_fails):
        break


if(__name__ == '__main__'):
  scrape_cash_ch()

