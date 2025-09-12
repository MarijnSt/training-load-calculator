import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# from io import BytesIO

def create_training_chart(session_df):
    """
    Creates and displays a training load chart with table and summary statistics.
    
    Parameters:
    ----------
    session_df: pd.DataFrame
        DataFrame with session data
    """

    # Calculate sRPE for each drill
    session_df["sRPE"] = session_df["Duur"] * session_df["RPE"]
    
    # Calculate totals
    total_duration = session_df["Duur"].sum()
    total_srpe = session_df["sRPE"].sum()
    session_rpe = total_srpe / total_duration if total_duration > 0 else 0

    # Match reference values
    match_duration = 80
    match_rpe = 7
    match_srpe = match_duration * match_rpe

    # Calculate relative values
    relative_load = (total_srpe / match_srpe) * 100 if match_srpe > 0 else 0
    relative_intensity = (session_rpe / match_rpe) * 100 if match_rpe > 0 else 0

    # Create the summary dataframe with totals
    summary_data = session_df.copy()
    totals_row = pd.DataFrame({
        "Oefening": ["Sessie"],
        "Duur": [total_duration],
        "RPE": [round(session_rpe, 2)],
        "sRPE": [total_srpe]
    })
    summary_data = pd.concat([summary_data, totals_row], ignore_index=True)
    
    # Pandas formatting
    formatted_df = summary_data.copy()
    formatted_df = formatted_df.round({'Duur': 0, 'RPE': 0, 'sRPE': 0})

    # Calculate dynamic figure size
    num_rows = len(formatted_df)
    fig_height = max(8, 6 + (num_rows * 0.5))

    # Create figure
    fig, ax = plt.subplots(figsize=(12, fig_height))
    ax.axis('off')
    
    # Position table dynamically
    table_bottom = 0.25  # Fixed space for summary
    table_height = 0.7   # Fixed table height

    table = ax.table(
        cellText=formatted_df.values,
        colLabels=["Oefening", "Duur (min)", "RPE", "sRPE"],
        cellLoc='center',
        loc='upper center',
        bbox=[0.1, table_bottom, 0.8, table_height]
    )
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style header
    for i in range(4):
        table[(0, i)].set_facecolor('#f2f4ee')
        table[(0, i)].set_text_props(weight='bold')
    
    # Style totals row
    for i in range(4):
        table[(len(formatted_df), i)].set_facecolor('#f2f4ee')
        table[(len(formatted_df), i)].set_text_props(weight='bold')
    
    # Game reference text
    ax.text(0.2, 0.15, "Wedstrijd referentie", fontweight='bold')
    ax.text(0.2, 0.1, f"{match_duration} x {match_rpe} = {match_srpe} AU", fontsize=10)

    # Training load text
    ax.text(0.4, 0.15, "Training load", fontweight='bold')
    ax.text(0.4, 0.1, f"Absoluut:", fontsize=10)
    ax.text(0.465, 0.1, f"{total_srpe:.0f} AU", fontsize=10, fontweight='bold')
    ax.text(0.4, 0.05, f"Relatief: {total_srpe:.0f} / {match_srpe} =", fontsize=10)
    ax.text(0.535, 0.05, f"{relative_load:.0f}%", fontsize=10, fontweight='bold')

    # Training intensity text
    ax.text(0.6, 0.15, "Trainingsintensiteit", fontweight='bold')
    ax.text(0.6, 0.1, f"Absoluut: {total_srpe:.0f} / {total_duration:.0f} =", fontsize=10)
    ax.text(0.735, 0.1, f"{session_rpe:.1f} RPE", fontsize=10, fontweight='bold')
    ax.text(0.6, 0.05, f"Relatief: {session_rpe:.1f} / {match_rpe} =", fontsize=10)
    ax.text(0.715, 0.05, f"{relative_intensity:.0f}%", fontsize=10, fontweight='bold')

    plt.tight_layout()
    
    # Display the figure
    st.pyplot(fig)
    
    # # Download button
    # buf = BytesIO()
    # fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    # buf.seek(0)
    
    # st.download_button(
    #     label="Download Training Load Samenvatting",
    #     data=buf.getvalue(),
    #     file_name="training_load_samenvatting.png",
    #     mime="image/png"
    # )