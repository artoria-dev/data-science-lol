import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.regularizers import L1, L2

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # suppress onednn

df = pd.read_csv('get-data/match-data.csv')

# feature engineering
df['blueTeamWardRetentionRatio'] = (df.blueTeamWardsPlaced - df.redTeamWardsDestroyed) / df.blueTeamWardsPlaced
df['blueTeamNetKills'] = (df.blueTeamKills - df.redTeamKills)
df['blueTeamJungleMinionsKilledDiff'] = (df.blueTeamTotalJungleMinionsKilled - df.redTeamTotalJungleMinionsKilled)
df['blueTeamMinionsKilledDiff'] = (df.blueTeamTotalMinionsKilled - df.redTeamTotalMinionsKilled)
df['blueTeamAvgLevelDiff'] = (df.blueTeamAvgLevel - df.redTeamAvgLevel)
df['blueTeamCsPerMinuteDiff'] = (df.blueTeamCsPerMinute - df.redTeamCsPerMinute)
df['blueTeamGoldPerMinuteDiff'] = (df.blueTeamGoldPerMinute - df.redTeamGoldPerMinute)

# remove the columns that are not needed
df = df[['winningTeam', 'blueTeamWardRetentionRatio', 'blueTeamNetKills', 'blueTeamJungleMinionsKilledDiff',
         'blueTeamMinionsKilledDiff', 'blueTeamAvgLevelDiff', 'blueTeamCsPerMinuteDiff', 'blueTeamGoldPerMinuteDiff']]

# drop NA
df = df.dropna()

# normalise the data except for the target variable 'winningTeam'
df.iloc[:, 1:] = (df.iloc[:, 1:] - df.iloc[:, 1:].mean()) / df.iloc[:, 1:].std()

# splitting
X = df.drop('winningTeam', axis=1)
y = df['winningTeam']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=0)


# timing
m_start = time.time()

# create the model
model = Sequential()
model.add(Input(shape=(X_train.shape[1],)))
model.add(Dense(32, activation='sigmoid', activity_regularizer=L2(0.1)))
model.add(Dense(1, activation='sigmoid'))

# compile & train the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=150, batch_size=20)

# evaluate by accuracy
_, accuracy = model.evaluate(X_test, y_test, verbose=0)
print('Accuracy: %.2f' % (accuracy * 100), f'duration: {round(time.time() - m_start, 2)}s\n')

# plot the loss after the third iteration
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'])
plt.title('Model loss over epochs')
plt.ylabel('Loss')
plt.xticks([])
plt.xlabel('Epochs')
plt.tight_layout()
plt.show()