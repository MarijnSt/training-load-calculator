import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Training Load Calculator")
st.write("")
st.write("Please add drills to the table below to calculate the training load for this session.")
st.write("")

# Init training df
training_df = pd.DataFrame(columns=["Drill", "Duration", "RPE"])

# Allow user to input data
edited_df = st.data_editor(
    training_df,
    column_config={
        "Drill": st.column_config.TextColumn(
            "Drill",
            help="Name of the drill to be performed"
        ),
        "Duration": st.column_config.NumberColumn(
            "Duration",
            help="The duration of the drill in minutes",
            min_value=0,
            step=1,
        ),
        "RPE": st.column_config.NumberColumn(
            "RPE",
            help="Rate of Perceived Exertion (1-10)",
            min_value=1,
            max_value=10,
            step=1,
        ),
    },
    hide_index=True,
    num_rows="dynamic",
)