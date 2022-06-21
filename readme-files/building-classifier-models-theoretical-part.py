import matplotlib.pyplot as plt
import numpy as np

# data values
x = np.array([2, 2, 4, 7, 10])
y = np.array([1, 2, 5, 7, 8])

# mean values
avgX = [x[0], x[-1]]
avgY = [y[0], y[-1]]

fig, ax = plt.subplots()

ax.plot(x, y, marker='o', label='data')  # draw data lines
ax.plot(avgX, avgY, linestyle='dotted', label='model')  # draw model
ax.axline((6, 4.5), (6, 1), color='green', label='prediction')  # draw pbox line
ax.axline((1, 4.5), (6, 4.5), color='green')  # draw pbox line

ax.set(xlabel='Amount Of Hours Studied', ylabel='Mark in %',
       title='Sample Data - Mark % Per Hours Studied')
plt.legend()
plt.show()
