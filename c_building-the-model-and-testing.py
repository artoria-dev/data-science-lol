# nn keras attempt
from keras.regularizers import l1
from matplotlib import pyplot as plt
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense, Normalization
from sklearn.metrics import roc_curve, roc_auc_score


dataset = loadtxt('data-final/c_data.csv', delimiter=',')
dataset_values = dataset[:, 0:10]
dataset_win = dataset[:, 10]


# normalize
norm_layer = Normalization()
norm_layer.adapt(dataset_values)

# define the keras model
model = Sequential()
model.add(norm_layer)
model.add(Dense(7, input_shape=(7,), activation='sigmoid'))
model.add(Dense(6, activation='sigmoid', activity_regularizer=l1(0.001)))
model.add(Dense(6, activation='sigmoid', activity_regularizer=l1(0.001)))
model.add(Dense(6, activation='sigmoid', activity_regularizer=l1(0.001)))
model.add(Dense(1, activation='sigmoid', activity_regularizer=l1(0.001)))

# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the keras model on the dataset
model.fit(dataset_values, dataset_win, epochs=500, batch_size=1000, workers=4, use_multiprocessing=True)

# evaluate the keras model
_, accuracy = model.evaluate(dataset_values, dataset_win)
print('Accuracy: %.2f' % (accuracy * 100))

# make class predictions with the model
predictions = (model.predict(dataset_values))  # numpy.ndarray

# roc curve
fpr, tpr, thresholds = roc_curve(dataset_win, predictions)
aucScore = roc_auc_score(dataset_win, predictions)

plt.plot(fpr, tpr, label='AUC-Score: ' + str(round(aucScore, 2)))
plt.plot([0, 1], [0, 1], 'k--', label='Random: 0.5')
plt.axis([0, 1, 0, 1])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc='best')
plt.show()
