import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Construct the full file path
file_path = os.path.join(r'H:\College\Fall 23-24\Cyber clinic\Model dataset', 'test_dataset.csv')

# Load your dataset
df = pd.read_csv(file_path)

# Display the first few rows of the dataset
print(df.head())
print("Column names:", df.columns)

# Bar chart for payment currency distribution with rotated x-axis labels
plt.figure(figsize=(10, 6))
sns.countplot(x='Payment Currency', data=df, palette='viridis')  # You can choose a palette that suits your preference
plt.title('Payment Currency Distribution', fontsize=16)
plt.xticks(rotation=45, ha='right', fontsize=7)  # Rotate x-axis labels for better readability
plt.xlabel('Payment Currency', fontsize=7)
plt.ylabel('Count', fontsize=14)
plt.show()

# Pie chart for payment format distribution with decreased font size
plt.figure(figsize=(8, 8))
df['Payment Format'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, textprops={'fontsize': 5.8})
plt.title('Payment Format Distribution', fontsize=14)
plt.ylabel('')  # Remove y-axis label for better clarity
plt.show()

# Box plot for transacted amount
plt.figure(figsize=(10, 6))
sns.boxplot(x='Is laundering', y='Transacted Amount', data=df, palette='Set3')  # You can choose a palette that suits your preference
plt.title('Boxplot of Transacted Amount (Laundered vs Non-Laundered)', fontsize=16)
plt.xlabel('Is Laundering', fontsize=14)
plt.ylabel('Transacted Amount', fontsize=14)
plt.show()

# Scatter plot for transacted amount by payment format
plt.figure(figsize=(10, 6))
sns.swarmplot(x='Payment Format', y='Transacted Amount', hue='Is laundering', data=df, palette='coolwarm')  # You can choose a palette that suits your preference
plt.title('Categorical Scatter Plot of Transacted Amount by Payment Format', fontsize=16)
plt.xlabel('Payment Format', fontsize=14)
plt.ylabel('Transacted Amount', fontsize=14)
plt.legend(title='Is Laundering', fontsize=12)
plt.show()