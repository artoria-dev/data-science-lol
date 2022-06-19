import matplotlib.pyplot as plt

tiers = ['Challenger', 'Grandmaster', 'Master', 'Diamond', 'Platinum', 'Gold', 'Silver', 'Bronze', 'Iron']
percentage = [800, 800, 800, 1400, 6500, 16600, 23600, 17900, 3600]

fig = plt.figure(figsize=(10, 5))
plt.bar(tiers, percentage)
for i in range(len(percentage)):
    plt.annotate(str(percentage[i]), xy=(tiers[i], percentage[i]), ha='center', va='bottom')
plt.xlabel('Elo')
plt.ylabel('Amount Of Games')
plt.title('Games Tracked Per Elo')
plt.show()