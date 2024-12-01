import streamlit as st
import numpy as np
from scipy.stats import poisson

# Function to calculate score probabilities using Poisson distribution
def calculate_score_probabilities(avg_goals_scored_A, avg_goals_conceded_B, avg_goals_scored_B, avg_goals_conceded_A):
    lambda_A = avg_goals_scored_A * avg_goals_conceded_B
    lambda_B = avg_goals_scored_B * avg_goals_conceded_A
    
    score_probabilities = {}
    for goals_A in range(6):  # Up to 5 goals for Team A
        for goals_B in range(6):  # Up to 5 goals for Team B
            prob = poisson.pmf(goals_A, lambda_A) * poisson.pmf(goals_B, lambda_B)
            score_probabilities[(goals_A, goals_B)] = prob
    return score_probabilities

# Function to display the most likely scorelines
def display_top_scores(score_probabilities, top_n=5):
    sorted_scores = sorted(score_probabilities.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores[:top_n]

# Streamlit app
st.title("Football Correct Score Predictor")

st.sidebar.header("Input Team Statistics")

# Inputs for Team A
st.sidebar.subheader("Team A")
avg_goals_scored_A = st.sidebar.number_input("Avg. Goals Scored (Team A)", value=0.53, min_value=0.0, step=0.01)
avg_goals_conceded_A = st.sidebar.number_input("Avg. Goals Conceded (Team A)", value=1.60, min_value=0.0, step=0.01)
over_2_5_A = st.sidebar.slider("Over 2.5 Goals (%) (Team A)", value=33.33, min_value=0.0, max_value=100.0, step=0.01)
under_2_5_A = st.sidebar.slider("Under 2.5 Goals (%) (Team A)", value=66.67, min_value=0.0, max_value=100.0, step=0.01)

# Inputs for Team B
st.sidebar.subheader("Team B")
avg_goals_scored_B = st.sidebar.number_input("Avg. Goals Scored (Team B)", value=1.47, min_value=0.0, step=0.01)
avg_goals_conceded_B = st.sidebar.number_input("Avg. Goals Conceded (Team B)", value=0.80, min_value=0.0, step=0.01)
over_2_5_B = st.sidebar.slider("Over 2.5 Goals (%) (Team B)", value=33.33, min_value=0.0, max_value=100.0, step=0.01)
under_2_5_B = st.sidebar.slider("Under 2.5 Goals (%) (Team B)", value=66.67, min_value=0.0, max_value=100.0, step=0.01)

# Calculate probabilities
st.header("Predicted Correct Scores")
score_probabilities = calculate_score_probabilities(avg_goals_scored_A, avg_goals_conceded_B, avg_goals_scored_B, avg_goals_conceded_A)
top_scores = display_top_scores(score_probabilities)

# Display top scorelines
st.subheader("Top Predicted Scorelines")
for score, prob in top_scores:
    st.write(f"Score: {score[0]} - {score[1]} | Probability: {prob:.2%}")
