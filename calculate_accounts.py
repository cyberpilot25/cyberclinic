import pandas as pd

# Load your dataset (replace 'money_laundering_dataset.csv' with the actual file path)
df = pd.read_csv('HI-Small_Trans.csv')

# Specify the column for which you want to identify unique values
column_name = 'Account'  # Replace with the actual column name

# Use the unique() function to get the unique values in the specified column
unique_values = df[column_name].unique()

# Create a DataFrame with serial numbers and unique values
unique_values_df = pd.DataFrame({'Serial Number': range(1, len(unique_values)+1), column_name: unique_values})

# Print and save the DataFrame to a CSV file
print("Unique values in the column '{}':".format(column_name))
print(unique_values_df)

# Save DataFrame to CSV (replace 'output_file.csv' with the desired file name)
output_file = 'unique_accounts.csv'
unique_values_df.to_csv(output_file, index=False)
print("Unique values saved to '{}'.".format(output_file))
