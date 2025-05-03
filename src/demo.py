import numpy as np
import pandas as pd 

def learn_dtmc(sequences, K, alpha=1.0):
    C = np.zeros((K, K), dtype=int)

    for seq in sequences:
        print(seq)
        for x, y in zip(seq[:-1], seq[1:]):
            C[x, y] += 1
    row_tot = C.sum(axis=1, keepdims=True)
    P = (C + alpha) / (row_tot + alpha * K)
    return C, P

# # Example trajectories over 3 states (0,1,2)
# sequences = [
#     [0, 1, 2, 0, 2, 2],   # 0->1->2->0->2->2
#     [1, 0, 1, 2],         # 1->0->1->2
#     [2, 2, 1, 0, 1],      # 2->2->1->0->1
#     [0, 0, 1, 1, 2]       # 0->0->1->1->2
# ]

# K = 3
# alpha = 1.0

# counts, P_hat = learn_dtmc(sequences, K, alpha)

# Display counts and smoothed transition matrix
# df_counts = pd.DataFrame(counts, index=[f's{i}' for i in range(K)],
#                          columns=[f's{j}' for j in range(K)])
# df_P = pd.DataFrame(P_hat, index=[f's{i}' for i in range(K)],
#                     columns=[f's{j}' for j in range(K)])

# print("\nRaw transition counts:")
# print(df_counts.to_string())

# print("\nSmoothed transition probabilities (α = 1):")
# print(df_P.round(3).to_string())