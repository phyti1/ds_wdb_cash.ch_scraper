
import time
import backend
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import logging
import logging.config

# Adds chromedriver binary to path
import chromedriver_binary
from console_progressbar import ProgressBar



def init_selenium(timeout):
  """
  Initialize Selenium driver

  :param timeout: timeout in seconds to wait for the driver to start the browser

  :return: driver instance
  """

  driver = webdriver.Chrome()

  # wait for the driver to start the browser
  time.sleep(timeout)

  logging.info("Driver initialized")

  return driver


def read_data_from_url(driver, url, i_page, page_load_timeout_s = 2):
  
  """
  Read all news articles from a page

  :param driver: selenium driver instance
  :param url: url to scrape
  :param i_page: page number
  :param page_load_timeout_s: timeout in seconds to wait for the page to load

  :return: pandas dataframe with all news articles from the page
  """

  #  create empty dataframe
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
    if len(news) == 0:
        logging.warning(f"No news found on page {i_page}")
        return

    # iterate through the news articles and extract the data
    for i_article, news_article in enumerate(news):
      
      # fill the dataframe with the data
      df_page.loc[i_article, "i_page"] = i_page
      df_page.loc[i_article, "href"] = news_article.find_element(By.CLASS_NAME, "_2PHmKV2J").get_attribute("href")
      df_page.loc[i_article, "title"] = news_article.find_element(By.CLASS_NAME, "_1w8f1Lsk").get_attribute("innerText")
      df_page.loc[i_article, "date"] = news_article.find_element(By.CLASS_NAME, "_2kyH0Dhp").get_attribute("innerText")
      df_page.loc[i_article, "category"] = news_article.find_element(By.CLASS_NAME, "_25SLsqeV").get_attribute("innerText")

      #  check if the article has a teaser and extract it, else set to empty string (not all articles have a teaser)
      if news_article.find_element(By.CLASS_NAME, "_2TpfbHst") and news_article.find_element(By.CLASS_NAME, "_2TpfbHst").get_attribute("innerText"):
        df_page.loc[i_article, "teaser"] = news_article.find_element(By.CLASS_NAME, "_2TpfbHst").get_attribute("innerText")
      else:
        df_page.loc[i_article, "teaser"] = ""
        logging.warning(f"<{url}>, article <{i_article}>. No Teaser present.")
    
    return df_page

  except Exception as e:
    logging.error(f"<{url}>, article <{i_article}>. Error: {e}")
    raise e
    

def scrape_cash_ch(buffer_timeout_s = 1, max_fails = 3, max_pages = 12350):
  """
  Scrapes cash.ch for news articles and saves them to a csv file
  Stops when max number of pages is reached or if there are more than max fails in a row

  :param buffer_timeout_s: timeout in seconds to wait for the driver to start the browser
  :param max_fails: maximum number of fails in a row before stopping
  :param max_pages: maximum number of pages to scrape
  """

  # set fails to 0 
  fails = 0

  # initialize service
  driver = init_selenium(buffer_timeout_s)

  # initial setup
  df = backend.load_df_from_csv()
  pb = ProgressBar(total=100, decimals=3, length=50)

  # find next page id to scrape  
  max_page = 1
  if(df.shape[0] > 0):
    max_page = int(df['i_page'].max() + 1)

  # iterate through the pages
  for i_page in range(max_page, max_pages):
    url = f"https://www.cash.ch/news/alle?page={i_page}"

    # catch if a page fails
    try:
      # set fails to 0 if page is scraped successfully
      fails = 0

      df_page = read_data_from_url(driver, url, i_page)
      df = pd.concat([df, df_page], axis=0)

      # print a progress bar to the console
      pb.print_progress_bar(i_page / max_pages * 100)

      # save the dataframe after every page, so that we don't lose data if the program crashes
      backend.save_df_as_csv(df)
      logging.info(f"Page {i_page} scraped successfully.")
    except:
      logging.warning(f"Failed to scrape page {i_page}")

      # count fails and break if max fails reached in a row
      fails += 1
      if fails > max_fails:
        logging.warning("Max fails reached. Stopping.")
        return

  logging.info("Finished scraping")

if __name__ == '__main__':

  # set logging config (see https://docs.python.org/3/howto/logging.html for more info)
  logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True, 
  })
  logging.basicConfig(filename='scrape.log', encoding='utf-8', level=logging.INFO)

  scrape_cash_ch()

