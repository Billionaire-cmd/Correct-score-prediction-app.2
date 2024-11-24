import numpy as np
import pandas as pd
from math import factorial
from scipy.stats import poisson
import streamlit as st

# Streamlit Application Title
st.title("⚽ Halftime Realistic Correct Score Outcome Predictor")
st.markdown("""
Predict **halftime outcomes** based on:
- Expected Goals (XG)
- Attack and Defense Strengths
- Odds Analysis
- Correct Score Probabilities
""")

# Sidebar for Input Parameters
st.sidebar.header("Input Parameters")

# Team Input
home_team = st.sidebar.text_input("Home Team", "Team A")
away_team = st.sidebar.text_input("Away Team", "Team B")

# Expected Goals (XG)
xg_home = st.sidebar.number_input("Expected Goals (Home, HT)", min_value=0.1, value=0.8, step=0.1)
xg_away = st.sidebar.number_input("Expected Goals (Away, HT)", min_value=0.1, value=0.6, step=0.1)

# Odds Input
st.sidebar.write("Halftime Odds")
home_win_odds = st.sidebar.number_input("Odds: Home Win (HT)", value=2.50, step=0.01)
draw_odds = st.sidebar.number_input("Odds: Draw (HT)", value=2.80, step=0.01)
away_win_odds = st.sidebar.number_input("Odds: Away Win (HT)", value=3.10, step=0.01)
over_1_5_odds = st.sidebar.number_input("Odds: Over 1.5 Goals (HT)", value=3.50, step=0.01)
under_1_5_odds = st.sidebar.number_input("Odds: Under 1.5 Goals (HT)", value=1.90, step=0.01)

# Attack and Defense Strengths
st.sidebar.write("Team Strengths")
home_attack_strength = st.sidebar.number_input("Home Attack Strength", min_value=0.1, value=1.2, step=0.1)
home_defense_strength = st.sidebar.number_input("Home Defense Strength", min_value=0.1, value=1.0, step=0.1)
away_attack_strength = st.sidebar.number_input("Away Attack Strength", min_value=0.1, value=1.1, step=0.1)
away_defense_strength = st.sidebar.number_input("Away Defense Strength", min_value=0.1, value=1.0, step=0.1)

# Correct Score Odds
st.sidebar.write("Correct Score Odds (HT)")
correct_score_odds = {}
scores = ["1-0", "0-0", "0-1", "2-0", "1-1", "0-2", "2-1", "2-2", "1-2"]
for score in scores:
    correct_score_odds[score] = st.sidebar.number_input(f"Odds for {score} (HT)", value=10.0, step=0.01)

# Submit Button
submit_button = st.sidebar.button("Submit Prediction")

# Functions
def poisson_prob(mean, goal):
    """Calculate Poisson probability mass function."""
    return (np.exp(-mean) * mean**goal) / factorial(goal)

def calculate_correct_score_probs(home_xg, away_xg, scores):
    """Calculate halftime correct score probabilities."""
    correct_score_probs = {}
    for score in scores:
        home_goals, away_goals = map(int, score.split('-'))
        prob = poisson_prob(home_xg, home_goals) * poisson_prob(away_xg, away_goals)
        correct_score_probs[score] = prob
    return correct_score_probs

def calculate_margin_difference(pred_prob, odds):
    """Calculate the margin difference for identifying value bets."""
    implied_prob = 1 / odds  # Implied probability from odds
    margin = (pred_prob - implied_prob) * 100  # Margin in percentage points
    return margin

# Main Prediction Logic
if submit_button:
    st.write(f"### Match: {home_team} vs {away_team} (HT Prediction)")

    # Adjust XG with attack/defense strengths
    adjusted_home_xg = xg_home * home_attack_strength / away_defense_strength
    adjusted_away_xg = xg_away * away_attack_strength / home_defense_strength

    # Display adjusted XG
    st.write(f"**Adjusted XG (Home):** {adjusted_home_xg:.2f}")
    st.write(f"**Adjusted XG (Away):** {adjusted_away_xg:.2f}")

    # Calculate Correct Score Probabilities
    correct_score_probs = calculate_correct_score_probs(adjusted_home_xg, adjusted_away_xg, scores)

    # Display Correct Score Probabilities and Margins
    st.write("\n### Correct Score Probabilities (HT):")
    best_score = None
    best_margin = -float("inf")

    for score, prob in correct_score_probs.items():
        odds = correct_score_odds[score]
        margin = calculate_margin_difference(prob, odds)
        st.write(f"Score {score}: Probability: {prob * 100:.2f}% | Margin: {margin:.2f}%")
        if margin > best_margin:
            best_margin = margin
            best_score = score

    # Highlight Best Correct Score Prediction
    if best_score:
        st.write(f"\n💡 **Best Correct Score Bet:** {best_score} with margin {best_margin:.2f}%")

    # Halftime Total Goals Prediction
    over_1_5_prob = sum(prob for score, prob in correct_score_probs.items() if sum(map(int, score.split('-'))) > 1)
    under_1_5_prob = 1 - over_1_5_prob
    st.write("\n### Halftime Total Goals Probabilities:")
    st.write(f"**Over 1.5 Goals (HT):** {over_1_5_prob * 100:.2f}%")
    st.write(f"**Under 1.5 Goals (HT):** {under_1_5_prob * 100:.2f}%")

    # Highlight Value Bets for Total Goals
    over_margin = calculate_margin_difference(over_1_5_prob, over_1_5_odds)
    under_margin = calculate_margin_difference(under_1_5_prob, under_1_5_odds)
    if over_margin > 5.0:
        st.write(f"🔥 **Over 1.5 Goals (HT) is a Value Bet!** Margin: {over_margin:.2f}%")
    if under_margin > 5.0:
        st.write(f"🔥 **Under 1.5 Goals (HT) is a Value Bet!** Margin: {under_margin:.2f}%")
