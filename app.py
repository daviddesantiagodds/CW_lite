import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
file_path = "CW Retail Scedule-dds- EXPLODED.xlsm"  # Update this if running locally
df = pd.read_excel(file_path, sheet_name="ALL EXPLODED")

# Melt the DataFrame to have time slots in one column
time_columns = df.columns[6:]
df_melted = df.melt(id_vars=["TIMEofDAY", "OPERATIVE", "ZONE", "TOP TASK", "SUB TASK", "AM SHIFT SEGMENT"], 
                     value_vars=time_columns, 
                     var_name="Time Slot", 
                     value_name="Shift Status")

# Streamlit App
st.title("Site Activity Dashboard")
st.sidebar.header("Filters")

# Filters
selected_task = st.sidebar.multiselect("Select Task Type", df_melted["TOP TASK"].unique(), default=df_melted["TOP TASK"].unique())
selected_zone = st.sidebar.multiselect("Select Zone", df_melted["ZONE"].unique(), default=df_melted["ZONE"].unique())
selected_shift_status = st.sidebar.multiselect("Select Shift Status", df_melted["Shift Status"].unique(), default=["ON SHIFT"])

# Filter data
df_filtered = df_melted[(df_melted["TOP TASK"].isin(selected_task)) & 
                         (df_melted["ZONE"].isin(selected_zone)) &
                         (df_melted["Shift Status"].isin(selected_shift_status))]

# Task Distribution
st.subheader("Task Distribution by Zone")
task_distribution = df_filtered.groupby(["ZONE", "TOP TASK"]).size().reset_index(name="Count")
fig1 = px.bar(task_distribution, x="ZONE", y="Count", color="TOP TASK", title="Task Distribution")
st.plotly_chart(fig1)

# Operatives per Zone
st.subheader("Number of Operatives per Zone")
operative_count = df_filtered.groupby(["ZONE"])['OPERATIVE'].nunique().reset_index(name="Operative Count")
fig2 = px.bar(operative_count, x="ZONE", y="Operative Count", title="Operatives by Zone")
st.plotly_chart(fig2)

# Shift Heatmap
st.subheader("Activity Heatmap")
heatmap_data = df_filtered.pivot_table(index="Time Slot", columns="ZONE", aggfunc="size", fill_value=0)
fig3 = px.imshow(heatmap_data, title="Operative Activity Heatmap", aspect="auto")
st.plotly_chart(fig3)

st.write("This dashboard allows you to explore operative activities dynamically. Use the filters to slice and dice the data!")
