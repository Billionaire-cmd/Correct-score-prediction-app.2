import numpy as np
from scipy.stats import poisson
import pandas as pd

# Function to calculate probabilities for a Poisson distribution
def poisson_prob(lambda1, lambda2, max_goals=5):
    prob_matrix = np.zeros((max_goals + 1, max_goals + 1))
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            prob_matrix[i, j] = poisson.pmf(i, lambda1) * poisson.pmf(j, lambda2)
    return prob_matrix

# Inputs for Team A and Team B
avg_goals_scored_a = 0.53
avg_goals_conceded_a = 1.60
avg_goals_scored_b = 1.47
avg_goals_conceded_b = 0.80

# Calculate expected goals
lambda_a_ft = (avg_goals_scored_a + avg_goals_conceded_b) / 2
lambda_b_ft = (avg_goals_scored_b + avg_goals_conceded_a) / 2
lambda_a_ht = lambda_a_ft * 0.45  # Halftime expected goals
lambda_b_ht = lambda_b_ft * 0.45

# Generate probabilities for halftime and full-time scores
max_goals = 3  # Maximum goals to consider for calculation
ht_prob_matrix = poisson_prob(lambda_a_ht, lambda_b_ht, max_goals)
ft_prob_matrix = poisson_prob(lambda_a_ft, lambda_b_ft, max_goals)

# Create a DataFrame for halftime probabilities
ht_scores = []
for i in range(max_goals + 1):
    for j in range(max_goals + 1):
        ht_scores.append({
            "Score (A:B)": f"{i}:{j}",
            "Probability": f"{ht_prob_matrix[i, j] * 100:.2f}%"
        })
ht_df = pd.DataFrame(ht_scores).sort_values(by="Probability", ascending=False)

# Create a DataFrame for full-time probabilities
ft_scores = []
for i in range(max_goals + 1):
    for j in range(max_goals + 1):
        ft_scores.append({
            "Score (A:B)": f"{i}:{j}",
            "Probability": f"{ft_prob_matrix[i, j] * 100:.2f}%"
        })
ft_df = pd.DataFrame(ft_scores).sort_values(by="Probability", ascending=False)

# Focused probabilities
ht_focused = ht_df[ht_df["Score (A:B)"] == "0:0"]
ft_focused = ft_df[ft_df["Score (A:B)"] == "1:1"]

# Display results
print("### Halftime Score Probabilities")
print(ht_df.head(5))  # Top 5 halftime probabilities
print("\nFocused Halftime Score (0:0):")
print(ht_focused)

print("\n### Full-Time Score Probabilities")
print(ft_df.head(5))  # Top 5 full-time probabilities
print("\nFocused Full-Time Score (1:1):")
print(ft_focused)
