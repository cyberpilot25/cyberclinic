import pandas as pd
import os
from sklearn.utils import validation
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from tensorflow import keras
from tensorflow.keras import layers

# Load your dataset
file_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'HI-Small_Trans.csv')  # Replace with the actual file path
df = pd.read_csv(file_path,low_memory=False)

# Assuming your target variable is named 'is_laundered'
columns_to_drop = ['Timestamp', 'Sender bank code', 'Sender a/c number','Receiver bank code','Receiver a/c number','Receiving Currency','Amount transacted','Payment Currency','Payment Format','Is Laundering']
X = df.drop(columns=columns_to_drop, axis=1)  # Features
y = df['Is Laundering']  # Target variable


# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
X_train = scaler.fit_transform(X_train)

# Build the DNN model

# Compile the model

# Train the model

# Predictions on the testing set

# Calculate performance metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print(classification_report(y_test, y_pred))
print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")
print("Confusion Matrix:")
print(conf_matrix)