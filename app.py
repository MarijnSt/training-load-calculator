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

# Only proceed if there's data
if not edited_df.empty and edited_df["Drill"].notna().any():
    # Remove rows with empty drills
    df_clean = edited_df.dropna(subset=["Drill"]).copy()
    
    if not df_clean.empty:
        # Calculate sRPE for each drill
        df_clean["sRPE"] = df_clean["Duration"] * df_clean["RPE"]
        
        # Calculate totals
        total_duration = df_clean["Duration"].sum()
        total_srpe = df_clean["sRPE"].sum()
        session_rpe = total_srpe / total_duration if total_duration > 0 else 0
        
        # Match reference values (you can make these configurable)
        match_duration = 80
        match_rpe = 7
        match_srpe = match_duration * match_rpe
        
        # Calculate relative values
        relative_load = (total_srpe / match_srpe) * 100 if match_srpe > 0 else 0
        relative_intensity = (session_rpe / match_rpe) * 100 if match_rpe > 0 else 0
        
        # Create the summary dataframe with totals
        summary_data = df_clean.copy()
        totals_row = pd.DataFrame({
            "Drill": ["Sessie"],
            "Duration": [total_duration],
            "RPE": [round(session_rpe, 2)],
            "sRPE": [total_srpe]
        })
        summary_data = pd.concat([summary_data, totals_row], ignore_index=True)
        
        # Create table
        table_data = []
        for _, row in summary_data.iterrows():
            table_data.append([
                str(row["Drill"]),
                f"{row['Duration']:.0f}" if pd.notna(row['Duration']) else "",
                f"{row['RPE']:.2f}" if pd.notna(row['RPE']) else "",
                f"{row['sRPE']:.0f}" if pd.notna(row['sRPE']) else ""
            ])

        # Calculate dynamic figure size
        num_rows = len(table_data)
        fig_height = max(8, 6 + (num_rows * 0.5))

        # Create figure
        fig, ax = plt.subplots(figsize=(12, fig_height))
        ax.axis('off')
        
        
        # Position table dynamically
        table_bottom = 0.25  # Fixed space for summary
        table_height = 0.7   # Fixed table height

        table = ax.table(
            cellText=table_data,
            colLabels=["Drill", "Duur (min)", "RPE", "sRPE"],
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
            table[(len(table_data), i)].set_facecolor('#f2f4ee')
            table[(len(table_data), i)].set_text_props(weight='bold')
        
        # Game reference text
        ax.text(
            0.2,
            0.15,
            "Wedstrijd referentie",
            fontweight='bold',
        )
        ax.text(
            0.2,
            0.1,
            f"{match_duration} x {match_rpe} = {match_srpe} AU",
            fontsize=10,
        )

        # Training load text
        ax.text(
            0.4,
            0.15,
            "Training load",
            fontweight='bold',
        )
        ax.text(
            0.4,
            0.1,
            f"Absoluut:",
            fontsize=10,
        )
        ax.text(
            0.465,
            0.1,
            f"{total_srpe:.0f} AU",
            fontsize=10,
            fontweight='bold',
        )
        ax.text(
            0.4,
            0.05,
            f"Relatief: {total_srpe:.0f} / {match_srpe} =",
            fontsize=10,
        )
        ax.text(
            0.535,
            0.05,
            f"{relative_load:.0f}%",
            fontsize=10,
            fontweight='bold',
        )

        # Training intensity text
        ax.text(
            0.6,
            0.15,
            "Trainingsintensiteit",
            fontweight='bold',
        )
        ax.text(
            0.6,
            0.1,
            f"Absoluut: {total_srpe:.0f} / {total_duration:.0f} =",
            fontsize=10,
        )
        ax.text(
            0.735,
            0.1,
            f"{session_rpe:.1f} RPE",
            fontsize=10,
            fontweight='bold',
        )
        ax.text(
            0.6,
            0.05,
            f"Relatief: {session_rpe:.1f} / {match_rpe} =",
            fontsize=10,
        )
        ax.text(
            0.715,
            0.05,
            f"{relative_intensity:.0f}%",
            fontsize=10,
            fontweight='bold',
        )

        plt.tight_layout()
        
        # Display the figure
        st.pyplot(fig)
        
        # Download button
        from io import BytesIO
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
        buf.seek(0)
        
        st.download_button(
            label="Download Training Load Summary",
            data=buf.getvalue(),
            file_name="training_load_summary.png",
            mime="image/png"
        )