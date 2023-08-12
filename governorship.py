from atexit import register
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_current_United_States_governors'

def get_site(url):
    wiki = requests.get(url)
    soup = BeautifulSoup(wiki.text, 'html.parser')
    table = soup.find('table', attrs={'class': 'sortable'})
    tr = table.find_all('tr')
    vals = []
    for row in tr:
        cols = row.find_all('td')
        t_row = [row.text for row in cols]
        vals.append(t_row)
    return vals


def get_party_values():
    states = get_site(url)
    states = states[2:]
    party = []
    for state in states:
        party.append(state[3].strip())
    return party

def get_state_values():
    vals = get_site(url)
    vals = vals[2:]
    states = []
    for val in vals:
        states.append(val[0].strip())
    return states

def make_dataframe():
    df = pd.DataFrame(data=get_state_values(), columns=["State"])
    df["Governor"] = get_party_values()
    df["Governor"] = df["Governor"].str.replace(r"(note \d|\[|\]|Farmer|Labor)", "", regex = True)
    df["State"] = df["State"].str.replace(r"\(list\)", "", regex = True)
    df["Governor"] = df["Governor"].str.replace(r"[^\w]", "", regex = True)
    print(df)

if __name__ == '__main__':
    # get_site(url)
    # get_party_values()
    # get_state_values()
    make_dataframe()