import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('../get-data/match-data.csv')

df['blueTeamWardRetentionRatio'] = (df.blueTeamWardsPlaced - df.redTeamWardsDestroyed)/df.blueTeamWardsPlaced
df['blueTeamNetKills'] = (df.blueTeamKills - df.redTeamKills)
df['blueTeamJungleMinionsKilledDiff'] = (df.blueTeamTotalJungleMinionsKilled - df.redTeamTotalJungleMinionsKilled)
df['blueTeamMinionsKilledDiff'] = (df.blueTeamTotalMinionsKilled - df.redTeamTotalMinionsKilled)
df['blueTeamAvgLevelDiff'] = (df.blueTeamAvgLevel - df.redTeamAvgLevel)
df['blueTeamCsPerMinuteDiff'] = (df.blueTeamCsPerMinute - df.redTeamCsPerMinute)
df['blueTeamGoldPerMinuteDiff'] = (df.blueTeamGoldPerMinute - df.redTeamGoldPerMinute)

# remove the columns that are not needed
df = df[['winningTeam', 'blueTeamWardRetentionRatio', 'blueTeamNetKills', 'blueTeamJungleMinionsKilledDiff', 'blueTeamMinionsKilledDiff', 'blueTeamAvgLevelDiff', 'blueTeamCsPerMinuteDiff', 'blueTeamGoldPerMinuteDiff']]

# normalise the data
df = (df - df.mean()) / df.std()

# seaborn plot
plt.figure(figsize=(12, 10))
sns.heatmap(df.corr(), annot=True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
