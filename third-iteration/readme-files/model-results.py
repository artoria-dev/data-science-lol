import matplotlib.pyplot as plt

d = [  # layers, regulariser, accuracy, time
    [1, "L1(0.001)", 0.7355, 1717.41],
    [1, "L1(0.010)", 0.735, 1743.46],
    [1, "L1(0.100)", 0.7353, 1691.97],
    [1, "L2(0.001)", 0.7352, 1651.81],
    [1, "L2(0.010)", 0.7354, 1614.85],
    [1, "L2(0.100)", 0.7356, 1612.95],
    [2, "L1(0.001)", 0.7355, 1767.34],
    # [2, "L1(0.010)", 0.5057, 1774.88],
    # [2, "L1(0.100)", 0.4943, 1803.4],
    [2, "L2(0.001)", 0.7354, 1753.43],
    [2, "L2(0.010)", 0.7353, 1701.47],
    [2, "L2(0.100)", 0.7348, 1702.68],
    [3, "L1(0.001)", 0.7356, 1910.78],
    # [3, "L1(0.010)", 0.4943, 1858.15],
    # [3, "L1(0.100)", 0.4943, 1887.93],
    [3, "L2(0.001)", 0.735, 1858.11],
    [3, "L2(0.010)", 0.7354, 1829.26],
    # [3, "L2(0.100)", 0.5057, 1836.38]
    ]

# sort by duration
d_sorted = sorted(d, key=lambda x: x[3])

# get values for plotting
layers = [item[0] for item in d_sorted]
regularisers = [item[1] for item in d_sorted]
accuracies = [item[2] for item in d_sorted]
times = [item[3] for item in d_sorted]

# coloring
colors = {1: 'b', 2: 'g', 3: 'r'}
bar_colors = [colors[layer] for layer in layers]

# bar the chart
plt.figure(figsize=(12, 6))
bars = plt.bar(range(len(d_sorted)), accuracies, color=bar_colors, edgecolor='black')

# ylim to show differences
plt.ylim(0.7345, 0.736)

# add labels for accuracy
for i, bar in enumerate(bars):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{accuracies[i]:.4f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# put the rest as x labels
plt.xticks(range(len(d_sorted)), [f'{regularisers[i]}\n({times[i]}s)' for i in range(len(d_sorted))])

# legend for layers
legend = [plt.Rectangle((0, 0), 1, 1, fc=colors[layer]) for layer in colors]
plt.legend(legend, colors.keys(), title='Layers')

# display
plt.tight_layout()
plt.show()