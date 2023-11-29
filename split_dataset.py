import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
import os

# Specify the file path to your CSV file on the desktop
file_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'HI-Small_Trans.csv')

# Load the dataset
df = pd.read_csv(file_path,low_memory=False)

# Reset index if necessary
df = df.reset_index(drop=True)

# Define a dictionary with column names and their corresponding data types
dtype_mapping = {
    'Timestamp': str,
    'From Bank': int,
    'Account': str,
    'To Bank': int,
    'Account': str,
    'Amount Received': float,
    'Receiving Currency': str,
    'Amount Paid': float,
    'Payment Currency': str,
    'Payment Format': str,
    'Is Laundering': int,
    # Add more columns as needed
}

# Split the dataset
test_size = 0.2
train_df, test_df = train_test_split(df, test_size=test_size, random_state=42)

# Specify the file names for the training and testing sets
train_file = os.path.join(os.path.expanduser('~'), 'Desktop', 'train_dataset.csv')
test_file = os.path.join(os.path.expanduser('~'), 'Desktop', 'test_dataset.csv')

# Save the split datasets
train_df.to_csv(train_file, index=False)
test_df.to_csv(test_file, index=False)