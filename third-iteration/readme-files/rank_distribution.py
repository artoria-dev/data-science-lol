import matplotlib.pyplot as plt

tiers = ['Challenger', 'Grandmaster', 'Master', 'Diamond', 'Emerald', 'Platinum', 'Gold', 'Silver', 'Bronze', 'Iron']
percentage = [0.0017, 0.03, 0.27, 4, 9.5, 16, 13, 17, 25, 13]

fig = plt.figure(figsize=(10, 5))
plt.bar(tiers, percentage)
for i in range(len(percentage)):
    plt.annotate(str(percentage[i]), xy=(tiers[i], percentage[i]), ha='center', va='bottom')
plt.xlabel("Tiers")
plt.ylabel("Percentage")
plt.title('Rank Distribution In League Of Legends\nRegion: EUW1 | Date: May 2024')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()