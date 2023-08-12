from typing import final
import pandas as pd
import numpy as np
from federal_legislatures import rank_both_chambers
from state_partisanship import rank_ranks
from president import percent_from_half


def purplest_state():
    federal = rank_both_chambers()
    state = rank_ranks()
    # print(type(state))
    executive = percent_from_half()
    frames = [federal, state, executive]
    df = pd.concat(frames)
    final_rank = df.groupby("State")["Rank"].sum().to_frame().reset_index()
    final_rank["Final Rank"] = final_rank["Rank"].rank()
    final_rank = final_rank.sort_values(["Final Rank"])
    return final_rank

if __name__ == "__main__":
    print(purplest_state())