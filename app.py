import streamlit as st

from src.components.session_table import create_session_table
from src.components.training_chart import create_training_chart
from src.components.rpe_info import rpe_info

st.title("Training Load Tool")
st.write("")
st.write("Gelieve drills toe te voegen aan de tabel hieronder om de training load voor deze sessie te berekenen.")
st.write("")

# RPE info
rpe_info()

# Session table
session_df = create_session_table()

# Only proceed if there's data
if not session_df.empty:
    create_training_chart(session_df)