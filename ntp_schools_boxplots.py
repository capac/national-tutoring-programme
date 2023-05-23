import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

plt.style.use('boxplot-style.mplstyle')

# data directory
main_data_dir = Path.home() / 'Programming/data/'
data_dir = main_data_dir / 'national-tutoring-programme_22-23/data/'
data_file = data_dir / 'ntp_delivery_data_2023-04-12.csv'

main_work_dir = Path.home() / 'Programming/Python/data-visualization/'
work_dir = main_work_dir / 'national-tutoring-programme_22-23'

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
color_list = ['#A6CEE3', '#1F78B4', '#B2DF8A', '#33A02C',
              '#FB9A99', '#E31A1C', '#FDBF6F', '#FF7F00',
              '#CAB2D6', '#6A3D9A', '#FFD700', '#B15928']
cmap = mpl.colors.ListedColormap(color_list)
colors = cmap.colors

# boxplot
fig, axes = plt.subplots(nrows=3, ncols=3)
for dt, col, color, ax in zip(region_list, regions, colors, axes.flatten()):
    bplot = ax.boxplot(dt['percentage_schools_participating'],
                       widths=0.25, patch_artist=True)
    ax.set_xticks([])
    ax.set_xlabel(col.title())
    ax.set_ylabel('Percentage (%)')
    for patch in bplot['boxes']:
        patch.set_facecolor(color)
        patch.set_edgecolor('0.2')
        patch.set_alpha(0.95)

# set source text
ax.text(x=0.08, y=0.01,
        s='''Source: "National Tutoring Programme 2022/23 Academic year" '''
        '''via the UK Department for Education (DfE). ''',
        transform=fig.transFigure,
        ha='left', fontsize=11, alpha=0.7)

fig.suptitle('Percentage of local authorities schools in the NTP, '
             'grouped by regions of England', fontsize=20, fontweight='bold',)

fig.subplots_adjust(top=0.92)
fig.savefig(work_dir / 'plots/ntp_schools_boxplot.png')
