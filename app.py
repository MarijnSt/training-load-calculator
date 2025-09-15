import streamlit as st

from src.components.session_table import create_session_table
from src.components.training_chart import create_training_chart

st.title("Training Load Tool")
st.write("")
st.write("Gelieve drills toe te voegen aan de tabel hieronder om de training load voor deze sessie te berekenen.")
st.write("")

# Session table
session_df = create_session_table()

# Only proceed if there's data
if not session_df.empty:
    create_training_chart(session_df)