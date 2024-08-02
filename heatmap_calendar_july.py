from datetime import datetime, timedelta

import july
import matplotlib.pyplot as plt
import pandas as pd
from july.utils import date_range
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MultipleLocator

# Define start date and data
start_date = "2024-07-01"
data = [2, 12, 0, 0, 2, 8, 7,
        15, 5, 2, 5, 19, 20, 18,
        37, 37, 8, -9, 59, 32, 17,
        22, -8, 10, 30, 61, 45, 33,
        27, 25, 14, -5]

# Calculate the end date based on the length of the data
end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=len(data)-1)).strftime("%Y-%m-%d")
dates = date_range(start_date, end_date)

# Create the heatmap
fig, ax = plt.subplots(figsize=(20, 10))  # Adjust the size of the figure

background_color = '#2e2e2e'
fig.patch.set_facecolor(background_color)  # Set the figure background color
ax.set_facecolor(background_color)  # Set the axes background color

# Define custom colormap with 9 gradients using GitHub's color scheme
colors = ["#ebedf0", "#c6e48b", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
n_bins = 9
cmap_name = 'github_greens'
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

july.heatmap(dates, data, title=f'Money Points {sum(data)}', cmap=cm, ax=ax, month_grid=True)

ax.title.set_color('white')
ax.tick_params(colors='white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.xaxis.set_tick_params(labelcolor='white')
ax.yaxis.set_tick_params(labelcolor='white')

fig.savefig('/home/xged/productivity/Money Points.png', bbox_inches='tight', facecolor=fig.get_facecolor())
plt.show()

# Calculate the 14-day rolling average
data_series = pd.Series(data)
rolling_avg = data_series.rolling(window=14).mean()

# Plot the 14-day rolling average as a bar chart
fig, ax = plt.subplots(figsize=(20, 10))

ax.bar(dates, rolling_avg, color='#40c463', edgecolor='black')  # Light green bars with black edges
ax.set_title(f'14-Day Rolling Average of Money Points - {round(sum(data[-14:])/14)}', color='white')
ax.set_xlabel('Date', color='white')
ax.set_ylabel('14-Day Rolling Average', color='white')

# Customize the background color and font color
fig.patch.set_facecolor(background_color)
ax.set_facecolor(background_color)
ax.tick_params(colors='white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.xaxis.set_tick_params(labelcolor='white')
ax.yaxis.set_tick_params(labelcolor='white')

# Add non-bold y-axis grid lines every 5 units
ax.yaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.grid(True, which='major', color='gray', linestyle='--', linewidth=0.5)

# Set the y-axis limit
ax.set_ylim(0, 40)

ax.title.set_fontsize(20)

fig.savefig('/home/xged/productivity/Rolling_Average_Bar_Chart.png', bbox_inches='tight', facecolor=fig.get_facecolor())
plt.show()
