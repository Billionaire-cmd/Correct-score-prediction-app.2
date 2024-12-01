import streamlit as st
import numpy as np
from scipy.stats import poisson

# Function to calculate Poisson probabilities
def poisson_prob(lambda1, lambda2, max_goals=5):
    prob_matrix = np.zeros((max_goals+1, max_goals+1))
    for i in range(max_goals+1):
        for j in range(max_goals+1):
            prob_matrix[i, j] = poisson.pmf(i, lambda1) * poisson.pmf(j, lambda2)
    return prob_matrix

# Streamlit app
def main():
    st.title("Football Match Correct Score Predictor")
    st.sidebar.header("Input Team Statistics")
    
    # Inputs for Team A
    st.sidebar.subheader("Team A")
    avg_goals_scored_a = st.sidebar.number_input("Avg. Goals Scored (Team A)", value=0.53, step=0.01)
    avg_goals_conceded_a = st.sidebar.number_input("Avg. Goals Conceded (Team A)", value=1.60, step=0.01)
    over_2_5_a = st.sidebar.number_input("Over 2.5% (Team A)", value=33.33, step=0.01)
    under_2_5_a = st.sidebar.number_input("Under 2.5% (Team A)", value=66.67, step=0.01)
    
    # Inputs for Team B
    st.sidebar.subheader("Team B")
    avg_goals_scored_b = st.sidebar.number_input("Avg. Goals Scored (Team B)", value=1.47, step=0.01)
    avg_goals_conceded_b = st.sidebar.number_input("Avg. Goals Conceded (Team B)", value=0.80, step=0.01)
    over_2_5_b = st.sidebar.number_input("Over 2.5% (Team B)", value=33.33, step=0.01)
    under_2_5_b = st.sidebar.number_input("Under 2.5% (Team B)", value=66.67, step=0.01)
    
    # Compute expected goals
    lambda_a = (avg_goals_scored_a + avg_goals_conceded_b) / 2
    lambda_b = (avg_goals_scored_b + avg_goals_conceded_a) / 2
    
    st.write(f"### Predicted Goals:")
    st.write(f"Team A Expected Goals: **{lambda_a:.2f}**")
    st.write(f"Team B Expected Goals: **{lambda_b:.2f}**")
    
    # Generate score probabilities
    max_goals = 5  # Maximum goals to consider
    prob_matrix = poisson_prob(lambda_a, lambda_b, max_goals)
    
    # Display probabilities
    st.write("### Correct Score Probabilities")
    st.write("The matrix below shows the probabilities for each scoreline:")
    score_prob_df = {}
    for i in range(max_goals+1):
        score_prob_df[f"Team B {i}"] = [f"{prob_matrix[j, i]*100:.2f}%" for j in range(max_goals+1)]
    score_prob_df = {f"Team A {i}": v for i, v in enumerate(zip(*score_prob_df.values()))}
    st.dataframe(score_prob_df)
    
    # Recommend most likely scores
    flat_probs = prob_matrix.flatten()
    indices = np.argsort(flat_probs)[::-1]
    st.write("### Top Predicted Scores")
    for idx in indices[:5]:  # Display top 5 scorelines
        score_a = idx // (max_goals+1)
        score_b = idx % (max_goals+1)
        st.write(f"Score {score_a}:{score_b} with probability {flat_probs[idx]*100:.2f}%")
    
if __name__ == "__main__":
    main()
