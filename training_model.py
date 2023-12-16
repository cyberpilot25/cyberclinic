import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import dgl
from dgl.nn import GraphConv
import torch
import torch.nn as nn
import torch.optim as optim

# Load your dataset
file_path = os.path.join('H:', 'College', 'Fall 23-24', 'Cyber clinic', 'Model dataset', 'HI-Small_Trans.csv')
df = pd.read_csv(file_path, low_memory=False)

# Assuming your target variable is named 'Is Laundering'
columns_to_drop = ['Timestamp', 'Sender bank code', 'Sender a/c number', 'Receiver bank code', 'Receiver a/c number', 'Amount transacted', 'Payment Currency', 'Payment Format']
X = df.drop(columns=columns_to_drop, axis=1)  # Features
y = df['Is Laundering']  # Target variable

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert the data to DGLGraph
graph_train = dgl.DGLGraph(X_train)
graph_test = dgl.DGLGraph(X_test)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define the GNN model
class GNNModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(GNNModel, self).__init__()
        self.conv1 = GraphConv(input_size, hidden_size)
        self.conv2 = GraphConv(hidden_size, output_size)

    def forward(self, g, features):
        x = torch.relu(self.conv1(g, features))
        x = torch.relu(self.conv2(g, x))
        return x

# Instantiate the model
model = GNNModel(input_size=X_train.shape[1], hidden_size=64, output_size=1)

# Define loss function and optimizer
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train the GNN model
for epoch in range(10):  # Adjust the number of epochs as needed
    model.train()
    logits = model(graph_train, torch.FloatTensor(X_train))
    loss = criterion(logits, torch.FloatTensor(y_train.values.reshape(-1, 1)))

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# Evaluate on the testing set
model.eval()
with torch.no_grad():
    logits_test = model(graph_test, torch.FloatTensor(X_test))
    y_pred = (logits_test.numpy() > 0).astype(int)

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