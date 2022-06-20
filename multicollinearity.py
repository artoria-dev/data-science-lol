import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_feather('data-final/data.feather')

df = df.sample(frac=0.01, random_state=0)
df = df.sample(frac=0.1, random_state=0)
df = df.loc[(df['blueTeamWin'] == 1)]
df = df[df['blueTeamFirstBlood'] == 1]

goldPerMinute = [x/10 for x in list(df.blueTeamGoldPerMinute)]
totalMinionsKilled = list(df.blueTeamTotalMinionsKilled)

yAxis = [x for x in range(len(goldPerMinute))]

plt.plot(yAxis, goldPerMinute, label='Gold Per Minute')
plt.plot(yAxis, totalMinionsKilled, label='Total Minions Killed')

plt.legend()
plt.show()