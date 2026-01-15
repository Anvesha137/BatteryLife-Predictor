import streamlit as st
import pandas as pd
import requests
import io
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="EV Battery RUL Dashboard", layout="wide")
st.title("EV Battery RUL + Mode Prediction")

st.markdown("""
Upload a CSV with **battery data**. The API will compute features, predict Remaining Useful Life (RUL), 
and detect battery mode (charging / discharging / idle). Visualizations show trends and mode coloring.
""")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    try:
        # Send to API
        files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
        response = requests.post("http://127.0.0.1:8000/predict/", files=files)

        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)

            st.subheader("Predictions Table")
            st.dataframe(df)

            # Map mode to color
            mode_colors = {"charging": "green", "discharging": "red", "idle": "gray"}
            df["color"] = df["mode"].map(mode_colors)

            # -------------------------
            # Matplotlib/Seaborn Plots
            # -------------------------

            st.subheader("Voltage & Current Over Time")
            fig, ax1 = plt.subplots(figsize=(12, 4))
            ax2 = ax1.twinx()

            sns.lineplot(x=df.index, y=df["Voltage_measured"], ax=ax1, label="Voltage (V)", color="blue")
            sns.lineplot(x=df.index, y=df["Current_measured"], ax=ax2, label="Current (A)", color="orange")

            ax1.set_xlabel("Time Steps")
            ax1.set_ylabel("Voltage (V)")
            ax2.set_ylabel("Current (A)")
            ax1.set_title("Voltage & Current Over Time")
            ax1.legend(loc="upper left")
            ax2.legend(loc="upper right")
            st.pyplot(fig)

            st.subheader("RUL Predicted with Mode Coloring")
            fig2, ax = plt.subplots(figsize=(12, 4))
            for mode in df["mode"].unique():
                subset = df[df["mode"] == mode]
                ax.scatter(subset.index, subset["RUL_predicted"], label=mode, color=mode_colors[mode], s=20)

            ax.set_xlabel("Time Steps")
            ax.set_ylabel("RUL Predicted")
            ax.set_title("RUL Prediction by Battery Mode")
            ax.legend()
            st.pyplot(fig2)

        else:
            st.error(f"API Error {response.status_code}: {response.text}")

    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("""
**Required CSV Columns (raw data)**:  
- Voltage_measured  
- Current_measured  
- Temperature_measured  
- Current_load  
- Voltage_load  
- Time
""")
