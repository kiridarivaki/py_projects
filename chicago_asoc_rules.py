import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('Chicago_Data.csv')

data['Date'] = pd.to_datetime(data['Date'])
data['Hour'] = data['Date'].dt.hour
data['Month'] = data['Date'].dt.month

def group_hours(hour): #groupping to times of the day according to police conventions
    if 7 <= hour <= 17:
        return 'Daytime'
    elif 18 <= hour <= 20:
        return 'Evening'
    elif 21 <= hour <= 23:
        return 'Night'
    else:
        return 'Midnight'

data['Time_Range'] = data['Hour'].apply(group_hours)

def group_months(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

data['Season'] = data['Month'].apply(group_months)

columns_to_encode = ['Primary_Type', 'Time_Range', 'Season']
encoded_data = pd.get_dummies(data[columns_to_encode], columns=columns_to_encode)

frequent_itemsets = apriori(encoded_data, min_support=0.05, use_colnames=True)

rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)

rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))

with pd.ExcelWriter("rules2.xlsx", engine='openpyxl') as writer:
    rules.to_excel(writer, index=False, sheet_name='Crimes_Data')

df_sorted = rules.sort_values(by='confidence', ascending=False)

pivot = df_sorted.pivot(index='antecedents', columns='consequents', values='confidence')

plt.figure(figsize=(10, 8)) #seaborn plot to visualize confidence between pairs
sns.heatmap(pivot, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Heatmap of Confidence for Association Rules')
plt.xlabel('Consequents')
plt.ylabel('Antecedents')
plt.show()

print(df_sorted[['antecedents', 'consequents', 'confidence']])