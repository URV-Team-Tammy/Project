import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
# import os 
# import sys
# import graph_templates
# import regions

def annon(zonecode,x,y,ax,rot=0, flag=False,zorder=99): 
    ax.annotate(zonecode, xy=(x,y),xycoords='data',fontsize=tagfont, rotation=rot,zorder=zorder)

year = 2023
file_path = f'mean_and_cv_{year}.csv'
savetodir = 'plot_output'


tagfont = 6
# boldfont = graph_templates.get_font(2)

stat_df = pd.read_csv(file_path, index_col='zone_code').rename_axis(None)

x = "Average Daily Coefficient of Variation (CV)"
y = r"Average Carbon Intensity (g.CO$_2$eq/kWh)"
stat_df.columns = [y,x]


sns.set()
sns.set_style('ticks')
# plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'



fig, ax = plt.subplots(figsize=(5,4))
xmin = 0
xmax = 0.8
ymin = 0
ymax = 1000
stat_df.plot.scatter(x=x, 
                     y=y,c=y,cmap="RdYlGn_r",
                     ax=ax,
                     s=50,
                      colorbar=False,
                      vmin=ymin,
                      vmax=ymax, 
                      edgecolors='k',
                      linewidth=0.15
                    )



lw = 0.8

global_avg = 368.39
global_cv = 0.12
plt.axhline(global_avg, color = 'grey', linestyle = 'dashdot',linewidth=lw)
plt.axvline(x=global_cv, color = 'grey', linestyle = 'dashdot',linewidth=lw)
intensity_stats = f"Global Avg. Intensity"
cv_stats = f"Global Avg. CV"


ax.annotate(intensity_stats , xy=(0.590,420),xycoords='data', size=8)
ax.annotate(global_avg , xy=(0.728,383),xycoords='data', size=8)
ax.annotate(cv_stats, xy=(0.128,960),xycoords='data', size=8, rotation=0)
ax.annotate(global_cv, xy=(0.128,923),xycoords='data', size=8, rotation=0)

plt.tick_params(direction='out', color='#000000')
# plt.yticks(np.arange(0,1.3,0.5), fontsize=10)
# plt.xticks( rotation=90, fontsize=9)
plt.xlabel(x)
plt.ylabel(y)
plt.ylim([ymin,ymax])
plt.xlim([xmin,xmax])

ax.annotate("BE" , xy=(0.4552, 157), size = 6)
ax.annotate("BG" , xy=(0.1985, 268), size = 6)
ax.annotate("CH" , xy=(0.4332, 33), size = 6)
ax.annotate("CZ" , xy=(0.1548, 309), size = 6)
ax.annotate("DK" , xy=(0.1723, 345), size = 6)
ax.annotate("EE" , xy=(0.2083, 318), size = 6)
ax.annotate("ES" , xy=(0.5542, 205), size = 6)
ax.annotate("FI" , xy=(0.0760, 153), size = 6)
ax.annotate("FR" , xy=(0.5072, 77), size = 6)
ax.annotate("HU" , xy=(0.3906, 201), size = 6)

ax.annotate("IE" , xy=(0.7674, 320), size = 6)
ax.annotate("IT" , xy=(0.4037, 134), size = 6)
ax.annotate("LT" , xy=(0.4171, 404), size = 6)
ax.annotate("LV" , xy=(0.3295, 159), size = 6)
ax.annotate("ME" , xy=(0.2642, 274), size = 6)
ax.annotate("MK" , xy=(0.1280, 255), size = 6)
ax.annotate("NL" , xy=(0.0959, 335), size = 6)
ax.annotate("NO" , xy=(0.0618, 15), size = 6)
ax.annotate("PL" , xy=(0.0618, 554), size = 6)
ax.annotate("PT" , xy=(0.5099, 278), size = 6)

ax.annotate("RO" , xy=(0.1390, 204), size = 6)
ax.annotate("RS" , xy=(0.0481, 300), size = 6)
ax.annotate("SE" , xy=(0.2040, 16), size = 6)
ax.annotate("SI" , xy=(0.2082, 146), size = 6)
ax.annotate("SK" , xy=(0.3493, 125), size = 6)

filename = f"mean_and_cv"

plt.tight_layout(rect=(-0.015, -0.04, 1.015, 1.04))
plt.savefig(filename, dpi=300)
plt.close() 