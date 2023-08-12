import pandas as pd
import numpy as np

# 0 for Republican
# 1 for Democratic

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
    print(percent_from_half())