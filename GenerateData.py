import numpy as np
import pandas as pd

# Define the size of the matrix and the percentage of connections
n = 15  # Size of the matrix
connection_density = 0.7  # Percentage of connected nodes, e.g., 0.7 means 70% connected

# Generate a random n x n distance matrix with integers from 1 to 10
distance_matrix = np.random.randint(1, 11, size=(n, n))

# Apply the connection density
mask = np.random.rand(n, n) > connection_density
distance_matrix[mask] = -1

# Ensure the matrix is symmetric and there are no self-loops
for i in range(n):
    for j in range(i+1, n):
        distance_matrix[j][i] = distance_matrix[i][j]
np.fill_diagonal(distance_matrix, -1)

# Convert the numpy array to a DataFrame, just for visual inspection here
distance_df = pd.DataFrame(distance_matrix, columns=[f'l{i+1}' for i in range(n)], index=[f'l{i+1}' for i in range(n)])

# Save the DataFrame to a CSV file
csv_file_path = 'random_distance_matrix.csv'
distance_df.to_csv(csv_file_path)

