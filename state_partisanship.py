from fileinput import close
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

urls = [
    'https://en.wikipedia.org/wiki/List_of_United_States_state_legislatures',
    'https://www.stateside.com/state-resource/legislative-partisan-splits'
]


def get_site_title(url):
    wiki = requests.get(url)
    soup = BeautifulSoup(wiki.text, 'html.parser')
    print(soup.title)



def get_col_headers(url):
    wiki = requests.get(url)
    soup = BeautifulSoup(wiki.text, 'html.parser')

    heads = []
    table = soup.find('table')
    header = table.find_all('th')
    for head in header:
        heads.append(head.text)
    return heads





def get_state_legislatures(url):
    wiki = requests.get(url)
    soup = BeautifulSoup(wiki.text, 'html.parser')

    vals = []
    table = soup.find('table')
    table_rows = table.find_all('tr')
    for row in table_rows:
        cols = row.find_all('td')
        tr = [row.text for row in cols]
        vals.append(tr)
    return vals



def make_and_clean_dataframe():
    df = pd.DataFrame(data = get_state_legislatures(urls[1]), columns=get_col_headers(urls[1]))
    df.drop(['Independent', 'Vacant', 'Other'], axis = 1, inplace=True)
    df = df.iloc[1:, :]
    df["Democrat"] = df["Democrat"].str.replace(r"[^\w]", "", regex = True)
    # Setting Nebraska's values manually (D = 17, R = 32)
    df.iat[52, 3] = 17
    df.iat[52, 4] = 32
    
    df = df.astype({"Democrat": int, "Republican": int, "Total Seats": int})
    df["Percent Democrat"] = round(df["Democrat"]/df["Total Seats"], 2)
    df["Percent Republican"] = round(df["Republican"]/df["Total Seats"], 2)
    return df




def closest_to_half():
    df = make_and_clean_dataframe()
    # df = df.iloc[(df['Percent Democrat'] - 0.5).abs().argsort(),:]
    df["Democrat From Half"] = (df['Percent Democrat'] - 0.5).abs().sort_values()
    df["Rank"] = df["Democrat From Half"].rank()
    return df
    # df[['State', 'Rank']].groupby("State")["Rank"].sum()/2)
    # print(df[df["State"] == "Georgia"])



def rank_ranks():
    df = closest_to_half()
    rank_df = df.groupby("State")["Rank"].sum().to_frame().reset_index()
    rank_df["Rank"] = rank_df["Rank"].div(2).round(2)
    rank_df = rank_df.sort_values(["Rank"])
    rank_df["Type"] = "state"
    return rank_df



if __name__ == '__main__':
    # print(make_and_clean_dataframe())
    # make_and_clean_dataframe()
    # closest_to_half()
    print(rank_ranks())