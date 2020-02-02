import seaborn as sns
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


data = "../../workset/mapping/Complete_Menus.csv"
df = pd.read_csv(data)

df.dropna(subset=['Newspaper Issue Date'], inplace=True)


df['Year'] = df.apply(lambda row: datetime.strptime(str(row['Newspaper Issue Date']), "%B %d, %Y").weekday(), axis=1)

y = "February 3, 2020"
weekdays = datetime.strptime(y, "%B %d, %Y").weekday()
print(weekdays)
exit()
years = df['Year'].tolist()

boop = []
# for year in years:
# 	if year > 1890 and year < 1895:
# 		boop.append(year)
 


# def ny_and_period(row):
# 	if 'NYS' in row['Archive'] and row['Year'] > 1890 and row['Year'] < 1895:
# 		return 0
# 	if 'NYS' in row['Archive'] and row['Year'] > 1890 and row['Year'] < 1920:
# 		return 1
# 	if 'NYS' in row['Archive']:
# 		return 2

# is_ny = df.apply(lambda row: ny_and_period(row), axis=1)

# n = 0
# m = 0
# o = 0
# for item in is_ny:
# 	if item == 0:
# 		n+=1
# 	if item == 1:
# 		m+=1
# 	else:
# 		o+=1

# print(n/o)
# print(m/o)
# print(n/m)

yrs = df['Year'].tolist()

fig, ax = plt.subplots()
sns.distplot(yrs, kde=False )
plt.xlabel('Publication Day')
plt.ylabel('# of riddle events')
plt.title("Distribution of Riddles by Day of the Week")

labels = ['', 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
ax.set_xticklabels(labels)
plt.xticks(rotation=45)

plt.show()