import pandas as pd
import matplotlib.pyplot as plt
import ast
import numpy as np
import seaborn as sns

""" NORMAL CASES """
# Import df_normal create with BuildBestStrategy().NormalCases() (from build_best_strategy.py)
df_normal = pd.read_csv("best_strategies/df_normal.csv")

# ["A", "T"] -> "A" or "T"
def get_card(cards, position):
    listed_cards = ast.literal_eval(cards)
    return listed_cards[position]

# Add columns "best_strategy", "best_profit", "card1", "card2"
df_normal["best_strategy"] = df_normal.loc[:, ["mean_profit_stand", "mean_profit_hit", "mean_profit_double"]].idxmax(axis=1)
df_normal["max_profit"] = df_normal.loc[:, ["mean_profit_stand", "mean_profit_hit", "mean_profit_double"]].max(axis=1)
df_normal["card1"] = df_normal.player_cards.apply(get_card, position=1)
df_normal["card2"] = df_normal.player_cards.apply(get_card, position=0)


# Loop to plot normal cases
for card in ["A","T","9","8","7","6","5","4","3","2"]:
    
    df_strat = df_normal.loc[df_normal.dealer_cards == card, ["best_strategy", "max_profit", "card1", "card2"]].copy()
    df_strat.reset_index(drop=True, inplace=True)    

    # 1st plot : Y axis
    y = df_strat.card1
    y = y.replace("T", 10)
    y = y.to_numpy()
    y = y.astype("int")
    
    # 1st plot : X axis
    x = df_strat.card2
    x = x.replace("A", 11)
    x = x.replace("T", 10)
    x = x.to_numpy()
    x = x.astype("int")
    
    # 1st plot : best strategy
    strat_list = df_strat.best_strategy
    strat_list = strat_list.replace("mean_profit_stand", 0)
    strat_list = strat_list.replace("mean_profit_hit", 1)
    strat_list = strat_list.replace("mean_profit_double", 2)
    strat_list = strat_list.to_numpy()
    strat_list = strat_list.astype("int")
    
    # 2nd plot : matrix
    hm_matrix = pd.DataFrame(index=["T","9","8","7","6","5","4","3","2"], columns=["A","T","9","8","7","6","5","4","3"])
    for i in range(len(df_strat.max_profit)):
        hm_matrix.loc[df_strat.card1[i],  df_strat.card2[i]] = df_strat.max_profit[i]
    
    # 2nd plot : matrix shaping
    hm_matrix = np.tril(hm_matrix)
    hm_matrix = hm_matrix.astype("float")
    hm_matrix = hm_matrix.round(2)
    hm_matrix = pd.DataFrame(hm_matrix, index=["T","9","8","7","6","5","4","3","2"], columns=["A","T","9","8","7","6","5","4","3"])
    
    # mask to plot half heatmap
    mask = np.zeros_like(hm_matrix)
    mask[np.triu_indices_from(mask, 1)] = True
    
    
    # plot
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(11,5))
    
    im = ax1.scatter(x, y, s=350, c=strat_list, cmap=plt.cm.get_cmap('Paired', 3), marker="s")
    ax1.set_xlim(11.5, 2.5)
    ax1.set_ylim(1.5, 10.5)
    ax1.set(frame_on=False)
    
    def fmt_func(x, loc):
        return ["Stand", "Hit", "Double"][x]
    formatter = plt.FuncFormatter(fmt_func)
    
    fig.colorbar(im, ticks = [0, 1, 2], format=formatter, ax=ax1)
    im.set_clim(-0.5, 2.5)
    ax1.set_xticks([11,10,9,8,7,6,5,4,3])
    ax1.set_xticklabels(labels=["A", "T", 9, 8, 7, 6, 5, 4, 3])
    ax1.set_yticks([2,3,4,5,6,7,8,9,10])
    ax1.set_yticklabels(labels=[2, 3, 4, 5, 6, 7, 8, 9, "T"])
    ax1.set_xlabel("First Player's Card")
    ax1.set_ylabel("Second Player's Card")
    ax1.set_title("Best Blackjack Strategy", pad=20)
    
    im2 = sns.heatmap(hm_matrix, linewidth=1, mask=mask, cmap="bwr", annot=True, vmax=1, vmin=-1, cbar_kws={'label': 'Mean Profit, Initial Bet = 1'}, ax=ax2)
    im2.set_title('Mean Profit with Best Strategy', pad=20)
    im2.set_xlabel("First Player's Card")
    im2.set_ylabel("Second Player's Card")
    
    
    fig.suptitle("Dealer's Card : {}".format(card), fontsize=20, y=0.98, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.85])
    
    fig.savefig("best_strategies/BS_dealer_{}.pdf".format(card))
    plt.show()
    
    

