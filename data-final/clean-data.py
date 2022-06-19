import pandas as pd

df = pd.read_feather('raw-data.feather')

df = df[df.blueTeamWin != 2]  # 70474 left
df = df.drop_duplicates()  # 70419 left
df = df[df.gameDuration < 6000]  # get rid of all games longer than 100 minutes # 70363 left
df = df[df.blueTeamGoldPerMinute != 0]  # 70314 left
df = df[df.redTeamGoldPerMinute != 0]  # 70314 left
df = df.loc[(df.blueTeamKills != 0) & (df.blueTeamKills != 0)]  # 70288 left # to fix first blood issue for red team
df.loc[df.blueTeamFirstBlood == 0, 'redTeamFirstBlood'] = 1  # fixed an issue i made in the code
df = df.reset_index(drop=True)  # resets index, argument is to prevent pandas to create another index column

df.to_feather('data.feather')
