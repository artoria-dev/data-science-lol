import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# fit models
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
# scoring funcs
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

df = pd.read_feather('data-final/data.feather')

df_train = df.sample(frac=0.85, random_state=99)  # len 59745
df_test = df.drop(df_train.index)  # len 10543

# BUILDING THE MODEL
df_train['blueTeamWardRetentionRatio'] = (
                                                 df_train.blueTeamWardsPlaced - df_train.redTeamWardsDestroyed) / df_train.blueTeamWardsPlaced
df_train['blueTeamNetKills'] = (df_train.blueTeamKills - df_train.redTeamKills)
df_train['blueTeamJungleMinionsKilledDiff'] = (
        df_train.blueTeamTotalJungleMonsterKilled - df_train.redTeamTotalJungleMonsterKilled)
df_train['blueTeamMinionsKilledDiff'] = (df_train.blueTeamTotalMinionsKilled - df_train.redTeamTotalMinionsKilled)
df_train['blueTeamAvgLevelDiff'] = (df_train.blueTeamAvgLevel - df_train.redTeamAvgLevel)
df_train['blueTeamCsPerMinuteDiff'] = (df_train.blueTeamCsPerMinute - df_train.redTeamCsPerMinute)
df_train['blueTeamGoldPerMinuteDiff'] = (df_train.blueTeamGoldPerMinute - df_train.redTeamGoldPerMinute)

continuousVars = ['blueTeamNetKills', 'blueTeamAssists', 'blueTeamAvgLevelDiff', 'blueTeamGoldPerMinuteDiff',
                   'blueTeamCsPerMinuteDiff', 'blueTeamJungleMinionsKilledDiff', 'blueTeamMinionsKilledDiff',
                   'blueTeamWardRetentionRatio']
categoricalVars = ['blueTeamFirstBlood', 'blueTeamDragonsKilled', 'blueTeamHeraldsKilled', 'blueTeamTowerDestroyed']

df_train = df_train[['blueTeamWin'] + continuousVars + categoricalVars]

df_train.loc[df_train.blueTeamFirstBlood == 0, 'blueTeamFirstBlood'] = -1
df_train.loc[df_train.blueTeamDragonsKilled == 0, 'blueTeamDragonsKilled'] = -1
df_train.loc[df_train.blueTeamHeraldsKilled == 0, 'blueTeamHeraldsKilled'] = -1
df_train.loc[df_train.blueTeamTowerDestroyed == 0, 'blueTeamTowerDestroyed'] = -1

minVec = df_train[continuousVars].min().copy()
maxVec = df_train[continuousVars].max().copy()
df_train[continuousVars] = (df_train[continuousVars] - minVec) / (maxVec - minVec)



def Pipe(df_predict, df_train_Cols, minVec, maxVec):
    df_predict['blueTeamWardRetentionRatio'] = (
                                                       df_predict.blueTeamWardsPlaced - df_predict.redTeamWardsDestroyed) / df_predict.blueTeamWardsPlaced
    df_predict['blueTeamNetKills'] = (df_predict.blueTeamKills - df_predict.redTeamKills)
    df_predict[
        'blueTeamJungleMinionsKilledDiff'] = df_predict.blueTeamTotalJungleMonsterKilled - df_predict.redTeamTotalJungleMonsterKilled
    df_predict[
        'blueTeamMinionsKilledDiff'] = df_predict.blueTeamTotalMinionsKilled - df_predict.redTeamTotalMinionsKilled
    df_predict['blueTeamAvgLevelDiff'] = df_predict.blueTeamAvgLevel - df_predict.redTeamAvgLevel
    df_predict['blueTeamCsPerMinuteDiff'] = df_predict.blueTeamCsPerMinute - df_predict.redTeamCsPerMinute
    df_predict['blueTeamGoldPerMinuteDiff'] = df_predict.redTeamGoldPerMinute - df_predict.redTeamGoldPerMinute

    continuousVars = ['blueTeamNetKills', 'blueTeamAssists', 'blueTeamAvgLevelDiff', 'blueTeamGoldPerMinuteDiff',
                       'blueTeamCsPerMinuteDiff', 'blueTeamJungleMinionsKilledDiff', 'blueTeamMinionsKilledDiff',
                       'blueTeamWardRetentionRatio']
    categoricalVars = ['blueTeamFirstBlood', 'blueTeamDragonsKilled', 'blueTeamHeraldsKilled',
                        'blueTeamTowerDestroyed']

    df_predict = df_predict[['blueTeamWin'] + continuousVars + categoricalVars]
    df_predict.loc[df_predict.blueTeamFirstBlood == 0, 'blueTeamFirstBlood'] = -1
    df_predict.loc[df_predict.blueTeamDragonsKilled == 0, 'blueTeamDragonsKilled'] = -1
    df_predict.loc[df_predict.blueTeamHeraldsKilled == 0, 'blueTeamHeraldsKilled'] = -1
    df_predict.loc[df_predict.blueTeamTowerDestroyed == 0, 'blueTeamTowerDestroyed'] = -1

    lst = list(set(df_train_Cols) - set(df_predict.columns))
    for item in lst:
        df_predict[str(item)] = -1

    df_predict[continuousVars] = (df_predict[continuousVars] - minVec) / (maxVec - minVec)

    df_predict = df_predict[df_train_Cols]
    return df_predict


def best_model(model):
    print(model.best_score_)
    print(model.best_params_)
    print(model.best_estimator_)


def get_auc_scores(y_actual, method, method2):
    auc_score = roc_auc_score(y_actual, method)
    fpr_df, tpr_df, _ = roc_curve(y_actual, method2)
    return auc_score, fpr_df, tpr_df


logReg = LogisticRegression(solver='lbfgs', max_iter=100000)
logReg.fit(df_train.loc[:, df_train.columns != 'blueTeamWin'], df_train.blueTeamWin)

forestReg = RandomForestClassifier(max_depth=9, max_features=9, max_leaf_nodes=None)
forestReg.fit(df_train.loc[:, df_train.columns != 'blueTeamWin'], df_train.blueTeamWin)

XGB = XGBClassifier()
XGB.fit(df_train.loc[:, df_train.columns != 'blueTeamWin'], df_train.blueTeamWin)

print(classification_report(df_train.blueTeamWin, logReg.predict(df_train.loc[:, df_train.columns != 'blueTeamWin'])))
print(classification_report(df_train.blueTeamWin, forestReg.predict(df_train.loc[:, df_train.columns != 'blueTeamWin'])))
print(classification_report(df_train.blueTeamWin, XGB.predict(df_train.loc[:, df_train.columns != 'blueTeamWin'])))

# EVALUATION
df_test = Pipe(df_test, df_train.columns, minVec, maxVec)
df_test = df_test.mask(np.isinf(df_test))
df_test = df_test.dropna()
print(classification_report(df_test.blueTeamWin, XGB.predict(df_test.loc[:, df_test.columns != 'blueTeamWin'])))

# ROC-CURVE
auc_XGB_test, fpr_XGB_test, tpr_XGB_test = get_auc_scores(df_test.blueTeamWin,
                                                          XGB.predict(df_test.loc[:, df_test.columns != 'blueTeamWin']),
                                                          XGB.predict_proba(
                                                              df_test.loc[:, df_test.columns != 'blueTeamWin'])[:, 1])
plt.figure(figsize=(12, 6), linewidth=1)
plt.plot(fpr_XGB_test, tpr_XGB_test, label='XGB score: ' + str(round(auc_XGB_test, 5)))
plt.plot([0, 1], [0, 1], 'k--', label='Random: 0.5')
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('ROC Curve')
plt.legend(loc='best')
plt.show()
