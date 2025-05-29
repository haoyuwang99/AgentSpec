import numpy as np
import pandas as pd 

from fractions import Fraction

# learning dtmc from data via Laplace Smoothing
def learn_dtmc(sequences, K, alpha=1.0):
    C = np.zeros((K, K), dtype=int)

    for seq in sequences: 
        for x, y in zip(seq[:-1], seq[1:]):
            C[x, y] += 1
    row_tot = C.sum(axis=1, keepdims=True)
    P_frac = np.empty((K, K), dtype=object)  # store rational strings
    
    # instead of storing the float number, we store the rational number string to ensure the sum of P is 1
    for i in range(K):
        for j in range(K):
            numerator = C[i, j] + alpha
            denominator = row_tot[i, 0] + alpha * K
            prob = Fraction(numerator).limit_denominator() / Fraction(denominator).limit_denominator()
            P_frac[i, j] = str(prob)  # store as string, e.g., "1/3"

    return C, P_frac

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