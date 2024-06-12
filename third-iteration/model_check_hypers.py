import os
import time
import pandas as pd
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


# helper function to convert regulariser class object to string
def get_regulariser_str(reg):
    reg_value = format(reg.l1 if hasattr(reg, 'l1') else reg.l2, '.3f')
    return reg.__class__.__name__ + f'({reg_value})'


# define the model
def run_model(regulariser, amt_layers=1):
    # timing
    m_start = time.time()

    # create the model
    model = Sequential()
    model.add(Input(shape=(X_train.shape[1],)))
    for _ in range(amt_layers):
        model.add(Dense(32, activation='sigmoid', activity_regularizer=regulariser))
    model.add(Dense(1, activation='sigmoid'))

    # compile & train the model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=150, batch_size=20, verbose=0)

    # evaluate by accuracy
    _, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print('Accuracy: %.2f' % (accuracy * 100), f'duration: {round(time.time() - m_start, 2)}s\n')

    # logging to file
    with open('model-results.txt', 'a') as f:
        f.write(
            f'layers: {amt_layers}, regulariser: {get_regulariser_str(regulariser)}, accuracy: {round(accuracy, 4)}, time: {round(time.time() - m_start, 2)}s\n')


# other hyperparameters that werent covered in the grid search
even_more_hypers = {
    'layers': [1, 2, 3],
    'regulariser': [L1(0.001), L1(0.01), L1(0.1), L2(0.001), L2(0.01), L2(0.1)]
}

# running model with different hyperparameters
t_start = time.time()
for layers in even_more_hypers['layers']:
    for reg in even_more_hypers['regulariser']:
        if layers is 1:
            print(f'running model with {layers} layer and {get_regulariser_str(reg)} regulariser')
        else:
            print(f'running model with {layers} layers and {get_regulariser_str(reg)} regulariser')
        run_model(reg, layers)
with open('model-results.txt', 'a') as f:
    f.write(f'total time: {round(time.time() - t_start, 2)}s')
