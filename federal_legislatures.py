import pandas as pd


def load_csv_house():
    df_house = pd.read_csv("us-house.csv")
    return df_house

def load_csv_senate():
    df_senate = pd.read_csv("us-senate.csv")
    return df_senate


def percent_house():
    df_house = load_csv_house()
    df_house["Percent Democratic"] = round(df_house["Democratic"] / df_house["Total"], 2)
    return df_house

def house_closest_to_half():
    df_house = percent_house()
    df_house["Democratic From Half"] = (df_house['Percent Democratic'] - 0.5).abs()
    df_house["Rank"] = df_house["Democratic From Half"].rank()
    df_house = df_house.sort_values("Rank")
    return df_house

def percent_senate():
    df_senate = load_csv_senate()
    df_senate["Percent Democratic"] = round(df_senate["Democratic"] / (df_senate["Democratic"] + df_senate["Republican"]), 2)
    return df_senate

def senate_closest_to_half():
    df_senate = percent_senate()
    df_senate["Democratic From Half"] = (df_senate['Percent Democratic'] - 0.5).abs()
    df_senate["Rank"] = df_senate["Democratic From Half"].rank()
    df_senate = df_senate.sort_values("Rank")
    return df_senate


def rank_both_chambers():
    combined = pd.concat([house_closest_to_half(), senate_closest_to_half()], axis=0)
    sum_ranks = combined.groupby("State")["Rank"].sum().to_frame().reset_index()
    sum_ranks = sum_ranks.sort_values(["Rank"])
    sum_ranks["Type"] = "federal"
    return sum_ranks


# def federal_and_state():
#     pass


if __name__ == '__main__':
    # load_csv_senate()
    # percent_house()
    # print(house_closest_to_half())
    # print(percent_senate())
    # print(senate_closest_to_half())
    print(rank_both_chambers())
