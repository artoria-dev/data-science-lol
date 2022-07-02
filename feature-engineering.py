import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_feather('data-final/data.feather')

# split
df_train = df.sample(frac=0.85, random_state=0)  # len 59745
df_test = df.drop(df_train.index)  # len 10543

df_train['blueTeamWardRetentionRatio'] = (df_train.blueTeamWardsPlaced - df_train.redTeamWardsDestroyed)/df_train.blueTeamWardsPlaced
df_train['blueTeamNetKills'] = (df_train.blueTeamKills - df_train.redTeamKills)
df_train['blueTeamJungleMinionsKilledDiff'] = (df_train.blueTeamTotalJungleMonsterKilled - df_train.redTeamTotalJungleMonsterKilled)
df_train['blueTeamMinionsKilledDiff'] = (df_train.blueTeamTotalMinionsKilled - df_train.redTeamTotalMinionsKilled)
df_train['blueTeamAvgLevelDiff'] = (df_train.blueTeamAvgLevel - df_train.redTeamAvgLevel)
df_train['blueTeamCsPerMinuteDiff'] = (df_train.blueTeamCsPerMinute - df_train.redTeamCsPerMinute)
df_train['blueTeamGoldPerMinuteDiff'] = (df_train.blueTeamGoldPerMinute - df_train.redTeamGoldPerMinute)

print(df_train.head())
