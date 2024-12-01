import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import poisson

# Function to calculate probabilities for a Poisson distribution
def poisson_prob(lambda1, lambda2, max_goals=5):
    prob_matrix = np.zeros((max_goals + 1, max_goals + 1))
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            prob_matrix[i, j] = poisson.pmf(i, lambda1) * poisson.pmf(j, lambda2)
    return prob_matrix

# Streamlit App Title
st.title("Football Score Prediction (Halftime & Full-Time)")

# Sidebar Inputs
st.sidebar.header("Team A Statistics")
avg_goals_scored_a = st.sidebar.number_input("Avg. Goals Scored (Team A)", value=0.53, step=0.01)
avg_goals_conceded_a = st.sidebar.number_input("Avg. Goals Conceded (Team A)", value=1.60, step=0.01)

st.sidebar.header("Team B Statistics")
avg_goals_scored_b = st.sidebar.number_input("Avg. Goals Scored (Team B)", value=1.47, step=0.01)
avg_goals_conceded_b = st.sidebar.number_input("Avg. Goals Conceded (Team B)", value=0.80, step=0.01)

st.sidebar.header("Over/Under 2.5 Goals Probabilities")
over_2_5 = st.sidebar.slider("Over 2.5 Goals (%)", min_value=0, max_value=100, value=33, step=1)
under_2_5 = st.sidebar.slider("Under 2.5 Goals (%)", min_value=0, max_value=100, value=67, step=1)

# Calculate expected goals
lambda_a_ft = (avg_goals_scored_a + avg_goals_conceded_b) / 2
lambda_b_ft = (avg_goals_scored_b + avg_goals_conceded_a) / 2
lambda_a_ht = lambda_a_ft * 0.45  # Halftime expected goals
lambda_b_ht = lambda_b_ft * 0.45

# Generate probabilities for halftime and full-time scores
max_goals = 3  # Maximum goals to consider for calculation
ht_prob_matrix = poisson_prob(lambda_a_ht, lambda_b_ht, max_goals)
ft_prob_matrix = poisson_prob(lambda_a_ft, lambda_b_ft, max_goals)

# Adjust probabilities based on Over/Under 2.5%
over_weight = over_2_5 / 100
under_weight = under_2_5 / 100

# Halftime adjustments
ht_adjusted_matrix = ht_prob_matrix * under_weight  # Halftime tends to have fewer goals
ht_adjusted_matrix /= ht_adjusted_matrix.sum()  # Normalize probabilities

# Full-time adjustments
ft_adjusted_matrix = ft_prob_matrix.copy()
for i in range(max_goals + 1):
    for j in range(max_goals + 1):
        if i + j > 2:  # Scores greater than 2.5 goals
            ft_adjusted_matrix[i, j] *= over_weight
        else:  # Scores 2.5 goals or less
            ft_adjusted_matrix[i, j] *= under_weight
ft_adjusted_matrix /= ft_adjusted_matrix.sum()  # Normalize probabilities

# Create DataFrames for halftime and full-time probabilities
ht_scores = []
for i in range(max_goals + 1):
    for j in range(max_goals + 1):
        ht_scores.append({
            "Score (A:B)": f"{i}:{j}",
            "Probability": f"{ht_adjusted_matrix[i, j] * 100:.2f}%"
        })
ht_df = pd.DataFrame(ht_scores).sort_values(by="Probability", ascending=False)

ft_scores = []
for i in range(max_goals + 1):
    for j in range(max_goals + 1):
        ft_scores.append({
            "Score (A:B)": f"{i}:{j}",
            "Probability": f"{ft_adjusted_matrix[i, j] * 100:.2f}%"
        })
ft_df = pd.DataFrame(ft_scores).sort_values(by="Probability", ascending=False)

# Display Results
st.header("Prediction Results")
st.subheader("Halftime Score Probabilities")
st.dataframe(ht_df)

st.subheader("Full-Time Score Probabilities")
st.dataframe(ft_df)

# Focused Probabilities
ht_focused = ht_df[ht_df["Score (A:B)"] == "0:0"]
ft_focused = ft_df[ft_df["Score (A:B)"] == "1:1"]

st.subheader("Focused Predictions")
st.write(f"### Halftime Focused Score (0:0):\n{ht_focused.iloc[0]['Probability']} probability")
st.write(f"### Full-Time Focused Score (1:1):\n{ft_focused.iloc[0]['Probability']} probability")
