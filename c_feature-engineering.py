import pandas as pd

df = pd.read_feather('data-final/c_data.feather')
df2 = pd.DataFrame()

df2['blueTeamWardRetentionRatio'] = (df.blueTeamWardsPlaced - df.redTeamWardsDestroyed)/df.blueTeamWardsPlaced
df2['blueTeamNetKills'] = (df.blueTeamKills - df.redTeamKills)
df2['blueTeamJungleMinionsKilledDiff'] = (df.blueTeamTotalJungleMonsterKilled - df.redTeamTotalJungleMonsterKilled)
df2['blueTeamMinionsKilledDiff'] = (df.blueTeamTotalMinionsKilled - df.redTeamTotalMinionsKilled)
df2['blueTeamAvgLevelDiff'] = (df.blueTeamAvgLevel - df.redTeamAvgLevel)
df2['blueTeamCsPerMinuteDiff'] = (df.blueTeamCsPerMinute - df.redTeamCsPerMinute)
df2['blueTeamGoldPerMinuteDiff'] = (df.blueTeamGoldPerMinute - df.redTeamGoldPerMinute)
df2['blueTeamTowerDestroyedDiff'] = (df.blueTeamTowerDestroyed - df.redTeamTowerDestroyed)
df2['blueTeamDragonsKilledDiff'] = (df.blueTeamDragonsKilled - df.redTeamDragonsKilled)
df2['blueTeamHeraldsKilledDiff'] = (df.blueTeamHeraldsKilled - df.redTeamHeraldsKilled)
df2['blueTeamWin'] = df.blueTeamWin

df2.to_csv('data-final/c_data.csv', index=False)

df_train = df2.sample(frac=0.85, random_state=123)
df_test = df2.drop(df_train.index)

df_train.to_csv('data-final/c_data_train.csv', index=False)
df_test.to_csv('data-final/c_data_test.csv', index=False)