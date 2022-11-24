# save pandas dataframe as csv function
def save_df_as_csv(df):
    """
    Save pandas dataframe as csv

    :param df: pandas dataframe

    :return: None
    """

    df.to_csv('data/cash_news.csv', index=False)
    
# save a pandas data
def save_df_as_feather(df):
    """
    Save pandas dataframe as feather

    :param df: pandas dataframe
    
    :return: None
    """

    df.to_feather('data/cash_news.feather')