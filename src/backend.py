import pandas as pd
import os

############################################################################################################
#############################################  Saving  ####################################################
############################################################################################################

def save_df_as_csv(df):
    """
    Save pandas dataframe as csv

    :param df: pandas dataframe

    :return: None
    """

    df.to_csv('src/data/cash_news.csv', index=False)
    
def save_df_as_feather(df):
    """
    Save pandas dataframe as feather

    :param df: pandas dataframe
    
    :return: None
    """

    df.to_feather('src/data/cash_news.feather')

############################################################################################################
#############################################  Loading  ####################################################
############################################################################################################

def load_df_from_csv():
    """
    Load pandas dataframe from csv

    :return: pandas dataframe
    """
    
    # check if file exists and return empty dataframe otherwise
    if os.path.isfile('src/data/cash_news.csv'):
        return pd.read_csv('src/data/cash_news.csv')
    else:
        return pd.DataFrame()

def load_df_from_feather():
    """
    Load pandas dataframe from feather

    :return: pandas dataframe
    """

    # check if file exists and return empty dataframe otherwise
    if os.path.isfile('src/data/cash_news.feather'):
        return pd.read_feather('src/data/cash_news.feather')
    else:
        return pd.DataFrame()
