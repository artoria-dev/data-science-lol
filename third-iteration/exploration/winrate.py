import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('../get-data/match-data.csv')

wt = data['winningTeam']
bw = np.sum(wt == 1)
rw = np.sum(wt == 0)

plt.pie([bw, rw], autopct='%1.1f%%', colors=['lightblue', 'pink'])
plt.legend(['Blue team', 'Red team'], loc='center')
plt.title('Winrate')
plt.tight_layout()

plt.show()