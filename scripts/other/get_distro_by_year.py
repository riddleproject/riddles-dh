import seaborn as sns
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


data = "../../workset/mapping/Complete_Menus.csv"
df = pd.read_csv(data)

df.dropna(subset=['Newspaper Issue Date'], inplace=True)

df['Year'] = df.apply(lambda row: datetime.strptime(str(row['Newspaper Issue Date']), "%B %d, %Y").year, axis=1)

years = df['Year'].tolist()

boop = []
for year in years:
	if year > 1890 and year < 1920:
		boop.append(year)

print(len(boop)/len(years))

sns.distplot(df['Year'], kde=True, )
plt.xlabel('Publication Year')
plt.ylabel('% of riddles released')
plt.title("Distribution of Riddles by Year of Publication")
plt.show()