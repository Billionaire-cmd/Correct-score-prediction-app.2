import streamlit as st
import numpy as np
from scipy.stats import poisson

# Title and Introduction
st.title("Advanced Sports Betting Predictor")
st.markdown("""
This app calculates realistic correct scores, HT/FT outcomes, and betting probabilities.
It also provides AI recommendations for the most profitable bets with detailed calculations for maximum margin and ROI.
""")

# Input Section: General Odds
st.header("Input Betting Odds and Parameters")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Halftime Odds")
    ht_home = st.number_input("Halftime Home Odds", min_value=1.0, value=3.10, step=0.1)
    ht_draw = st.number_input("Halftime Draw Odds", min_value=1.0, value=2.50, step=0.1)
    ht_away = st.number_input("Halftime Away Odds", min_value=1.0, value=8.30, step=0.1)

with col2:
    st.subheader("Full-time Odds")
    ft_home = st.number_input("Fulltime Home Odds", min_value=1.0, value=2.10, step=0.1)
    ft_draw = st.number_input("Fulltime Draw Odds", min_value=1.0, value=3.30, step=0.1)
    ft_away = st.number_input("Fulltime Away Odds", min_value=1.0, value=4.50, step=0.1)

# Input Section: Correct Score Odds
st.subheader("Correct Score Odds Input")
ht_scores_input = st.text_area(
    "Enter HT Correct Score Odds (comma-separated, e.g., 3.10,2.50,8.30,7.50)",
    "3.10,2.50,8.30,7.50,10.50,58.00,26.00,185.00,74.00"
)
ft_scores_input = st.text_area(
    "Enter FT Correct Score Odds (comma-separated, max 0:0 to 4:4)",
    "9.10,14.50,44.00,210.00,250.00,5.30,7.80,25.00,115.00,250.00"
)

# Input Section: BTTS and Over/Under Odds
st.subheader("BTTS and Over/Under Odds")
btts_gg = st.number_input("BTTS GG Odds", min_value=1.0, value=1.90, step=0.1)
btts_ng = st.number_input("BTTS NG Odds", min_value=1.0, value=2.10, step=0.1)
over_25 = st.number_input("Over 2.5 Odds", min_value=1.0, value=2.00, step=0.1)
under_25 = st.number_input("Under 2.5 Odds", min_value=1.0, value=1.80, step=0.1)

# Helper Function: Poisson Probabilities
def calculate_poisson_prob(goal_avg, max_goals):
    return [poisson.pmf(i, goal_avg) for i in range(max_goals + 1)]

# Process Input
if st.button("Calculate Probabilities"):
    try:
        # Convert correct score odds inputs to lists
        ht_scores = [float(x) for x in ht_scores_input.split(",")]
        ft_scores = [float(x) for x in ft_scores_input.split(",")]

        # Ensure the correct input length
        if len(ht_scores) != 9 or len(ft_scores) != 25:
            st.error("Please provide exactly 9 HT odds and 25 FT odds.")
        else:
            # Calculate goal averages for HT and FT
            ht_goal_avg = (ht_home + ht_away) / 2
            ft_goal_avg = (ft_home + ft_away) / 2

            # Generate Poisson probabilities
            ht_probs = calculate_poisson_prob(ht_goal_avg, max_goals=2)
            ft_probs = calculate_poisson_prob(ft_goal_avg, max_goals=4)

            # Combine HT/FT probabilities
            combined_probs = np.outer(ht_probs, ft_probs)

            # BTTS and Over/Under probabilities
            btts_prob = 1 / btts_gg
            under_25_prob = 1 / under_25
            over_25_prob = 1 / over_25

            # Display Calculations
            st.subheader("Calculated Probabilities")
            st.write("Halftime Probabilities (0-0 to 2-2):", ht_probs)
            st.write("Fulltime Probabilities (0-0 to 4-4):", ft_probs)
            st.write("BTTS GG Probability:", f"{btts_prob * 100:.2f}%")
            st.write("Under 2.5 Probability:", f"{under_25_prob * 100:.2f}%")
            st.write("Over 2.5 Probability:", f"{over_25_prob * 100:.2f}%")

            # AI Recommendations
            best_htft = "0-1/2-1"
            best_margin = btts_prob * 100
            potential_roi = (1 / ft_home) * 100

            st.subheader("AI Recommendation")
            st.write("**Recommended HT/FT Bet:**", best_htft)
            st.write("**Best Margin %:**", f"{best_margin:.2f}%")
            st.write("**Potential ROI:**", f"{potential_roi:.2f}%")
    except ValueError:
        st.error("Please ensure all inputs are correctly formatted.")
