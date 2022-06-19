import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def winRate():
    labels = 'Blue Wins', 'Red Wins'
    sizes = [df.blueTeamWin[df['blueTeamWin'] == 1].count(), df.redTeamWin[df['redTeamWin'] == 1].count()]
    fig1, ax1 = plt.subplots(figsize=(7, 7))
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['b', 'r'])
    ax1.axis('equal')
    plt.title("Winrate", size=15)
    plt.show()


def winRatePerFirstBlood():
    n = 2
    winsWithFirstBlood = ((df.blueTeamWin[df['blueTeamFirstBlood'] == 1].count()/(len(df)/100)), (df.redTeamWin[df['redTeamFirstBlood'] == 1].count())/(len(df)/100))
    winsWithoutFirstBlood = ((df.blueTeamWin[df['blueTeamFirstBlood'] == 0].count()/(len(df)/100)), (df.redTeamWin[df['redTeamFirstBlood'] == 0].count())/(len(df)/100))
    print(winsWithFirstBlood, winsWithoutFirstBlood)
    ind = np.arange(n)
    plt.figure(figsize=(7, 5))
    width = 0.2
    plt.bar(ind, winsWithFirstBlood, width, label='With First Blood')
    plt.bar(ind + width, winsWithoutFirstBlood, width, label='Without First Blood')
    plt.xlabel('Teams')
    plt.ylabel('Win Rate')
    plt.title('Win Rate Per Team Per First Blood')
    plt.xticks(ind + width / 2, ('Blue Team', 'Red Team'))
    plt.legend(loc='best')
    plt.show()


def avgLevelByCs():
    df2 = df.loc[(df['blueTeamWin'] == 1) & (df['gameDuration'] > 2500)]
    goldPerMinute = [x/10 for x in list(df2.blueTeamGoldPerMinute)]
    csPerMinute = list(df2.blueTeamCsPerMinute)
    xAxis = [x for x in range(len(goldPerMinute))]
    levelCs = {'Gold Per Minute': goldPerMinute, 'Cs Per Minute': csPerMinute}

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.stackplot(xAxis, levelCs.values(),
                 labels=levelCs.keys(), alpha=0.9)
    ax.legend(loc='upper left')
    ax.set_title('CsPM & GPM Correlation')
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    df = pd.read_feather('data-final/data.feather')
    # winRate()
    # winRatePerFirstBlood()
    # avgLevelByCs()
