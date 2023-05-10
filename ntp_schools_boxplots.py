import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

work_dir = Path.home() / 'Programming/Python/data-visualization/'
data_dir = work_dir / 'national-tuition-programme/ntp_2022-23/data/'
data_file = data_dir / 'ntp_delivery_data_2023-04-12.csv'

ntp_df = pd.read_csv(data_file, na_values='-')
regions = list(ntp_df['region_name'][ntp_df['region_name'].notnull()].unique())

# data lists
region_list = []
for reg in regions:
    regional = (ntp_df['time_period'] == 2023) & \
               (ntp_df['time_identifier'] == 'January') & \
               (ntp_df['region_name'] == reg) & \
               (ntp_df['geographic_level'] == 'Local authority') & \
               (ntp_df['school_phase'] == 'All') & \
               (ntp_df['total_type'] == 'Total in academic year')
    data = ntp_df[regional][['region_name', 'la_name',
                             'percentage_schools_participating']]
    region_list.append(data)

# colormap
color_list = ['navy', 'blue', 'royalblue', 'deepskyblue',
              'limegreen', 'yellowgreen', 'gold', 'darkorange',
              'red', 'crimson', 'darkviolet', 'indigo',]
cmap = mpl.colors.ListedColormap(color_list)
colors = cmap.colors

# boxplot
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(9, 7))
for dt, col, ax, color in zip(region_list, regions, axes.flatten(), colors):
    bplot = ax.boxplot(dt['percentage_schools_participating'], widths=0.25,
                       patch_artist=True)
    ax.set_xticks([])
    ax.set_xlabel(col.title(), fontsize=11)
    ax.set_ylabel('Percentage (%)', fontsize=11)
    ax.grid(linestyle=':')
    for tick in ax.get_yticklabels():
        tick.set_rotation(90)
        tick.set_verticalalignment('center')
    for patch in bplot['boxes']:
        patch.set_facecolor(color)
        patch.set_edgecolor('0.2')
        patch.set_linewidth(1.5)
        patch.set_alpha(0.8)
    for whisker in bplot['whiskers']:
        whisker.set_color('0.2')
        whisker.set_linewidth(1.5)
        whisker.set_linestyle(':')
    for fliers in bplot['fliers']:
        fliers.set_markerfacecolor('1.0')
        fliers.set_markeredgecolor('0.0')
    for median in bplot['medians']:
        median.set_color('0.2')
        median.set_linewidth(2.5)
    for caps in bplot['caps']:
        caps.set_color('0.2')
        caps.set_linewidth(1.5)
fig.suptitle('Percentage of local authorities schools in the NTP, '
             'grouped by regions of England', fontsize=13)
fig.tight_layout()
fig.savefig('ntp_schools_boxplot.png', dpi=288,
            bbox_inches='tight')
