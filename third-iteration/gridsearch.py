import logging
import os
import time
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input
from scikeras.wrappers import KerasClassifier
from sklearn.model_selection import GridSearchCV


os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # suppress onednn

# set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
fh = logging.FileHandler('grid_search_log.txt')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

logging.info('loading data...')
df = pd.read_csv('get-data/match-data.csv')

# feature engineering
logging.info('getting features...')
df['blueTeamWardRetentionRatio'] = (df.blueTeamWardsPlaced - df.redTeamWardsDestroyed)
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
logging.info('normalising data...')
df.iloc[:, 1:] = (df.iloc[:, 1:] - df.iloc[:, 1:].mean()) / df.iloc[:, 1:].std()

# splitting
logging.info('splitting data into training and testing sets...')
X = df.drop('winningTeam', axis=1)
y = df['winningTeam']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=0)


# define the model
def create_model(optimizer='adam', activation='relu', neurons=32):
    logging.info(f'creating model with optimizer={optimizer}, activation={activation}, neurons={neurons}')
    model = Sequential()
    model.add(Input(shape=(X_train.shape[1],)))
    model.add(Dense(neurons, activation=activation))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    return model


# get keras classifier, early stopping
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
model = KerasClassifier(model=create_model, optimizer='adam', activation='relu', neurons=32, callbacks=[early_stopping], verbose=0)

# randomized search parameters
param_grid = {
    'optimizer': ['adam', 'rmsprop'],
    'activation': ['relu', 'tanh', 'sigmoid'],
    'neurons': [16, 32, 64, 128],
    'batch_size': [10, 20, 50],
    'epochs': [50, 100, 150]
}

# randomized search
logging.info('starting randomised search...')
start = time.time()
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=4, cv=3, verbose=3)
search_result = grid_search.fit(X_train, y_train)
end = time.time()
logging.info(f'randomised search completed in {round(end - start, 2)} seconds')

# summarise
logging.info('summarising results...')
best_score = search_result.best_score_
best_params = search_result.best_params_
means = search_result.cv_results_['mean_test_score']
stds = search_result.cv_results_['std_test_score']
params = search_result.cv_results_['params']

with open('grid_search_results3.txt', 'w') as f:
    f.write(f'best: {best_score} using {best_params}\n')
    for mean, std, param in zip(means, stds, params):
        f.write(f'mean: {mean}, std: {std}, params: {param}\n')
    f.write(f'took: {round(end - start, 2)} seconds\n')

print(f'\nbest: {best_score} using {best_params}')