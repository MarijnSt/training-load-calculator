import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# from io import BytesIO

from src.styling.colors import colors
from src.styling.fonts import fonts
from src.styling.typography import typo

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

    # Merge summary data with totals row
    summary_data = pd.concat([summary_data, totals_row], ignore_index=True)
    
    # Pandas formatting
    formatted_df = summary_data.copy()
    formatted_df = formatted_df.round({'Duur': 0, 'RPE': 0, 'sRPE': 0})

    # Calculate dynamic figure size
    num_rows = len(formatted_df)
    fig_height = max(8, 6 + (num_rows * 0.5))

    # Init plt styling
    plt.rcParams.update({
        'font.family': fonts['light'].get_name(),
        'font.size': typo['sizes']['p'],
        'text.color': colors['primary'],
        'axes.labelcolor': colors['primary'],
        'axes.edgecolor': colors['primary'],
        'xtick.color': colors['primary'],
        'ytick.color': colors['primary'],
        'grid.color': colors['primary'],
        'figure.facecolor': colors['white'],
        'axes.facecolor': colors['white'],
    })

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
    table.set_fontsize(typo['sizes']['p'])
    table.scale(1, 2)
    
    # Style header
    for i in range(4):
        table[(0, i)].set_facecolor(colors['light'])
        table[(0, i)].set_text_props(fontproperties=fonts['medium_italic'])
    
    # Style totals row
    for i in range(4):
        table[(len(formatted_df), i)].set_facecolor(colors['light'])
        table[(len(formatted_df), i)].set_text_props(fontproperties=fonts['medium_italic'])
    
    # Game reference text
    ax.text(0.15, 0.15, "Wedstrijd referentie", fontproperties=fonts['medium_italic'])
    ax.text(0.15, 0.1, f"{match_duration} x {match_rpe} = {match_srpe} AU")
    ax.text(0.15, 0.07, "(duur x RPE)", fontsize=typo['sizes']['label'])

    # Training load text
    ax.text(0.44, 0.15, "Training load", fontproperties=fonts['medium_italic'])
    ax.text(0.44, 0.1, "Absoluut:")
    ax.text(0.51, 0.1, f"{total_srpe:.0f} AU", fontproperties=fonts['medium_italic'])
    ax.text(0.44, 0.07, "(totale sRPE)", fontsize=typo['sizes']['label'])
    ax.text(0.44, 0.025, "Relatief:")
    ax.text(0.51, 0.025, f"{relative_load:.0f}%", fontproperties=fonts['medium_italic'])

    # Training intensity text
    ax.text(0.7, 0.15, "Trainingsintensiteit", fontproperties=fonts['medium_italic'])
    ax.text(0.7, 0.1, "Absoluut:")
    ax.text(0.77, 0.1, f"{session_rpe:.1f} RPE", fontproperties=fonts['medium_italic'])
    ax.text(0.7, 0.07, "(totale sRPE / totale duur)", fontsize=typo['sizes']['label'])
    ax.text(0.7, 0.025, "Relatief:")
    ax.text(0.77, 0.025, f"{relative_intensity:.0f}%", fontproperties=fonts['medium_italic'])

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