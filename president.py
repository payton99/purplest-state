import re
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

# 0 for Republican
# 1 for Democratic

class President:

    pres_url = "https://en.wikipedia.org/wiki/List_of_United_States_presidential_election_results_by_state"

    def __init__(self):
        pass

    def status_code(self):
        try:
            r = requests.head(self.pres_url)
            print(r.status_code)
        except requests.ConnectionError:
            print(f"** FAILURE **: Failed to connect to given url: {self.pres_url}")
    
    def get_table(self):
        site = requests.get(self.pres_url)
        soup = BeautifulSoup(site.text, 'html.parser')
        table = soup.find('table', attrs={'class': 'wikitable'})
        return table



def get_data(url):
    site = requests.get(url)
    soup = BeautifulSoup(site.text, 'html.parser')
    table = soup.find('table', attrs={'class': 'wikitable'})
    years = set()
    date = '\d{4}'
    for x in table.find_all('th'):
        if re.search(date, x.text.strip()):
            years.add(x.text.strip())
    print(years)
    tr = table.find_all('tr')
    vals = []
    # for row in tr:
        # print(row.text.strip())
    #     headers = row.find_all('td')
        # cols = row.find_all('td')
        # print(cols)
    # print(headers)
        # t_row = [row.text for row in cols]
        # print(t_row)
        # vals.append(t_row)
    # return vals

def load_csv():
    df = pd.read_csv("presidential-elections.csv")
    return df

def sum_across():
    df = load_csv()
    df["Total"] = df.sum(axis=1)
    return df

def percent_from_half():
    df = sum_across()
    df["Percent"] = (df["Total"] / 6).replace(np.inf, 0)
    df["Percent"] = df["Percent"].round(2)
    df["Percent From Half"] = (df['Percent'] - 0.5).abs().sort_values()
    df["Rank"] = df["Percent From Half"].rank()
    ranks = df[["State", "Rank"]]
    ranks = ranks.sort_values("Rank")
    ranks["Type"] = "president"
    return ranks


if __name__ == '__main__':
    # print(load_csv())
    # print(sum_across())
    pres = President()
    pres.get_table()