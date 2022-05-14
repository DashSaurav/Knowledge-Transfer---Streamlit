import streamlit as st
import numpy as np
import pandas as pd

def graph():
    df = pd.read_csv("pages/main_data.csv")

    st.subheader("Bar Graph")
    df_bar = df[["Fname","Age"]]
    df_bar = df_bar.set_index("Fname")
    # st.write(df_bar)
    st.bar_chart(df_bar,use_container_width=True)

    st.subheader("Line Graph")
    df_line = df[["Fname","Pets","Children"]]
    df_line = df_line.set_index("Fname")
    st.line_chart(df_line,use_container_width=True)

    st.subheader("Area Chart")
    df_area = df[["Fname","Weight","Property Value"]]
    df_area = df_area.set_index("Fname")
    st.area_chart(df_area,use_container_width=True)
