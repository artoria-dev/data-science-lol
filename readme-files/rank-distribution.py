import matplotlib.pyplot as plt

tiers = ['Challenger', 'Grandmaster', 'Master', 'Diamond', 'Platinum', 'Gold', 'Silver', 'Bronze', 'Iron']
percentage = [0.014, 0.033, 0.17, 1.7, 9.4, 23, 34, 26, 4.8]

fig = plt.figure(figsize=(10, 5))
plt.bar(tiers, percentage)
for i in range(len(percentage)):
    plt.annotate(str(percentage[i]), xy=(tiers[i], percentage[i]), ha='center', va='bottom')
plt.xlabel("Tiers")
plt.ylabel("Percentage")
plt.title('Rank Distribution In League Of Legends')
plt.show()