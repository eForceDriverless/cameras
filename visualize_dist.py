import sys
import numpy as np
import matplotlib.pyplot as plt


RS_DATA = 'cone_dist_realsense.csv'
ZED_DATA = 'cone_dist_zed.csv'
DISTANCES = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

rs_data = np.genfromtxt(RS_DATA, delimiter=',')
zed_data = np.genfromtxt(ZED_DATA, delimiter=',')

zeros = np.zeros((len(DISTANCES), 3))
zeros[:len(rs_data), :] = rs_data
rs_data = zeros

zeros = np.zeros((len(DISTANCES), 3))
zeros[:len(zed_data), :] = zed_data
zed_data = zeros

# print(rs_data)

fig, ax = plt.subplots(figsize=(13, 5))


ax.bar(5*np.arange(len(DISTANCES)), DISTANCES, width=1, label='Ground truth')
ax.bar(5*np.arange(len(DISTANCES)) + 1, np.mean(rs_data, axis=1),
    width=1, yerr=np.std(rs_data, axis=1), capsize=4, label='realsense')
ax.bar(5*np.arange(len(DISTANCES)) + 2.0, np.mean(zed_data, axis=1),
    width=1, yerr=np.std(zed_data, axis=1), capsize=4, label='Zed')

ax.set_xticks(5*np.arange(len(DISTANCES)))
ax.set_xticklabels(DISTANCES)

# def plot_data(ax, data):
#     ax.bar(np.arange(), timing, width=0.55, yerr=std, align='center', ecolor='black', capsize=4)
#     # ax[i, j].set_xticklabels(['gamma'] + list(range(4)))
#     ax[i, k].set_xticks(1.5*np.arange(2))
#     ax[i, k].set_xticklabels(['No \n cutoff', 'Cutoff = \n optimal value'])
#     ax[i, k].set_ylim(0, 25)



# ax[1, 0].set_ylabel('Seconds')
# ax[0, 0].title.set_text('Default config with Presolve & Cuts off')
# ax[0, 1].title.set_text('Decreased tolerance')
# ax[0, 2].title.set_text('Heuristics off')
# ax[0, 3].title.set_text('Barrier')
# ax[0, 4].title.set_text('Barrier + Heuristics off')




# plt.bar(2*np.arange(6), timing)
# plt.bar(2*np.arange(30) + 0.8, timing_reg - training_time)
# plt.bar(2*np.arange(30) + 0.8, training_time, bottom=timing_reg - training_time)

# plt.xticks(2*np.arange(30) + 0.8, fails)
# fig.autofmt_xdate()
ax.legend()
fig.tight_layout()
plt.show()