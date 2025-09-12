import streamlit as st
import pandas as pd

def create_session_table():
    """
    Creates and returns a data editor for training session input.
    
    Returns:
        pd.DataFrame: The edited dataframe with training data
    """
    # Init training df
    training_df = pd.DataFrame(columns=["Oefening", "Duur", "RPE"])
    
    # Allow user to input data
    edited_df = st.data_editor(
        training_df,
        column_config={
            "Oefening": st.column_config.TextColumn(
                "Oefening",
                help="Naam van de oefening die uitgevoerd wordt"
            ),
            "Duur": st.column_config.NumberColumn(
                "Duur",
                help="De duur van de oefening in minuten",
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
    
    return edited_df