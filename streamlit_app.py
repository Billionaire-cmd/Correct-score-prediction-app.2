import streamlit as st
import numpy as np

# App title
st.title("🤖 Rabiotic Realistic Halftime Predictor")

# Input section
st.header("Input Parameters")

# Home and Away Team
home_team = st.text_input("Home Team", "Team A")
away_team = st.text_input("Away Team", "Team B")

# Expected Goals for Home and Away
home_goals_ht = st.number_input("Expected Goals (Home, HT)", min_value=0.0, value=1.21)
away_goals_ht = st.number_input("Expected Goals (Away, HT)", min_value=0.0, value=1.64)

# Halftime Odds
st.subheader("Halftime Odds")
home_win_odds = st.number_input("Odds: Home Win (HT)", min_value=0.0, value=2.05)
draw_odds = st.number_input("Odds: Draw (HT)", min_value=0.0, value=2.20)
away_win_odds = st.number_input("Odds: Away Win (HT)", min_value=0.0, value=7.25)
over_15_goals_odds = st.number_input("Odds: Over 1.5 Goals (HT)", min_value=0.0, value=3.10)
under_15_goals_odds = st.number_input("Odds: Under 1.5 Goals (HT)", min_value=0.0, value=1.35)

# Team Strengths
st.subheader("Team Strengths")
home_attack_strength = st.number_input("Home Attack Strength", min_value=0.0, value=1.73)
home_defense_strength = st.number_input("Home Defense Strength", min_value=0.0, value=0.91)
away_attack_strength = st.number_input("Away Attack Strength", min_value=0.0, value=1.64)
away_defense_strength = st.number_input("Away Defense Strength", min_value=0.0, value=0.64)

# Correct Score Odds
st.subheader("Correct Score Odds (HT)")
score_1_0_odds = st.number_input("Odds for 1-0 (HT)", min_value=0.0, value=3.10)
score_0_0_odds = st.number_input("Odds for 0-0 (HT)", min_value=0.0, value=2.50)
score_0_1_odds = st.number_input("Odds for 0-1 (HT)", min_value=0.0, value=8.30)
score_2_0_odds = st.number_input("Odds for 2-0 (HT)", min_value=0.0, value=7.50)
score_1_1_odds = st.number_input("Odds for 1-1 (HT)", min_value=0.0, value=10.50)
score_0_2_odds = st.number_input("Odds for 0-2 (HT)", min_value=0.0, value=58.00)
score_2_1_odds = st.number_input("Odds for 2-1 (HT)", min_value=0.0, value=26.00)
score_2_2_odds = st.number_input("Odds for 2-2 (HT)", min_value=0.0, value=185.00)
score_1_2_odds = st.number_input("Odds for 1-2 (HT)", min_value=0.0, value=74.00)

# Add a button to submit the prediction
if st.button('Submit Prediction'):
    # Logic to calculate Halftime Correct Score Recommendation
    # Here we assume the model recommends 1-0 as the most likely correct score
    recommended_score = "1-0"
    recommended_odds = score_1_0_odds

    # Display the recommended score and its odds
    st.subheader(f"Recommended Halftime Score: {recommended_score}")
    st.write(f"The predicted best halftime score is **{recommended_score}** with odds of **{recommended_odds}**.")

    # Additional calculations or recommendations can go here
    st.subheader("Additional Information & Insights")

    # Example calculation: Estimated probability of 1-0 based on odds
    odds_to_probability = lambda odds: 1 / odds
    prob_1_0 = odds_to_probability(score_1_0_odds)

    st.write(f"Estimated Probability of 1-0 (HT) = {prob_1_0:.2%}")

    # Display some additional metrics or insights
    # Example: Home Team Strength + Away Team Defense interaction
    home_defense_efficiency = home_attack_strength * home_defense_strength
    away_attack_efficiency = away_attack_strength * away_defense_strength

    st.write(f"Home Team Defensive Efficiency (HT): {home_defense_efficiency:.2f}")
    st.write(f"Away Team Offensive Efficiency (HT): {away_attack_efficiency:.2f}")

    # Calculate expected halftime score probabilities
    expected_home_score = home_goals_ht * home_attack_strength / away_defense_strength
    expected_away_score = away_goals_ht * away_attack_strength / home_defense_strength

    st.write(f"Expected Home Score (HT): {expected_home_score:.2f}")
    st.write(f"Expected Away Score (HT): {expected_away_score:.2f}")

    # You can add more detailed calculations based on the available inputs and your prediction logic.
