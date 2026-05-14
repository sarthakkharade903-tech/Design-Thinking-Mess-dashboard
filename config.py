# ══════════════════════════════════════════════════════════════════
# CENTRAL DASHBOARD CONFIGURATION
# ══════════════════════════════════════════════════════════════════
# 👇 ONLY CHANGE THIS LINE when you download a new CSV from Google Sheets
DATA_FILE = "RAW DATA PVGCOET Mess Feedback.csv"
# ══════════════════════════════════════════════════════════════════

import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """
    Single shared data loader used by ALL pages.
    Uses flexible column matching so it works regardless of minor
    differences in Google Form export column names (spaces, newlines, etc.)
    """
    df = pd.read_csv(DATA_FILE)

    # ── Flexible rename: matches column by keyword, not exact string ──────────
    col_map = {}
    for col in df.columns:
        col_clean = col.strip().replace("\n", " ")
        if "MEAL TYPE" in col_clean.upper():
            col_map[col] = "Meal"
        elif col_clean == "Food Temperature":
            col_map[col] = "Temperature"
        elif col_clean == "Your Experience":
            col_map[col] = "Experience"
        elif col_clean.strip() == "Taste" or col_clean.strip() == "Taste  ":
            col_map[col] = "Taste"

    df.rename(columns=col_map, inplace=True)

    # Drop Timestamp if present
    if "Timestamp" in df.columns:
        df.drop(columns=["Timestamp"], inplace=True)

    return df
