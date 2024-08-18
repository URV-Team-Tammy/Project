import pandas as pd 
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

filename = "period_data.csv"
outputname = 'plot_output'

df = pd.read_csv(filename, index_col='zone_code').rename_axis(None)

zonecodelist = df.index

sns.set_style('ticks')
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'

markers = ["o", "H","^"]

fig, ax = plt.subplots(figsize=(7,0.9))
columns = df.columns

# colorlist = ["skyblue", "bisque", "lightgreen", "sandybrown"]
colorlist = ["#7bc8f6", "#9af764","#BABABA"]

for i, col in enumerate(columns[::-1]):
    i = -(i+1)
    plt.scatter(df.index, df[col], label = col,
                c = colorlist[i],
                edgecolors="k",linewidths = 0.8,
                marker = markers[i], s= 70)
    
plt.tick_params(direction='in', color='#000000',grid_alpha=0,bottom=False, left=False)
plt.yticks(np.arange(0,1.3,0.5), fontsize=10)

plt.xticks( rotation=90, fontsize=9)
plt.ylabel("Score",  fontsize=14,x=1)
plt.grid(alpha=0.85)

custom_line = []
for i in range(len(columns)): 
    custom_line.append(Line2D([], [], color="k", marker=markers[i], markerfacecolor=colorlist[i],markeredgewidth=1,  markersize=9))

plt.legend(
    custom_line, columns, handlelength=0, 
    bbox_to_anchor=(0.29,0.86,1,0.2),

    loc="lower left", ncol = len(custom_line), 
    frameon=False, 
    )
# fig.subplots_adjust(left=0, right=1, bottom=0, top=0.8)
plt.ylim([-0.1, 1.2])
plt.xlim([-0.5,24.5])

savename = f"{outputname}"

plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)