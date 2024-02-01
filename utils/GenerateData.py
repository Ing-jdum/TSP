import numpy as np
import pandas as pd


def generate_data(n=15, connection_density=0.7):
    while True:
        distance_matrix = np.random.randint(1, 11, size=(n, n))

        # Apply the connection density
        mask = np.random.rand(n, n) > connection_density
        distance_matrix[mask] = -1

        # Ensure the matrix is symmetric
        for i in range(n):
            for j in range(i + 1, n):
                distance_matrix[j][i] = distance_matrix[i][j]

        # No self loops
        np.fill_diagonal(distance_matrix, -1)

        # Check if any row (or column) contains all -1 values
        if not np.any(np.all(distance_matrix == -1, axis=1)):
            break

    # Convert the numpy array to a DataFrame
    distance_df = pd.DataFrame(distance_matrix, columns=[f'l{i + 1}' for i in range(n)],
                               index=[f'l{i + 1}' for i in range(n)])

    # Save the DataFrame to a CSV file
    csv_file_path = '../distance_matrix.csv'
    distance_df.to_csv(csv_file_path)
