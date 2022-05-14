import streamlit as st
import numpy as np
import pandas as pd
from pages import utils
# import matplotlib.pyplot as plt
import altair as alt
import os


def bar_graph():
    if 'main_data.csv' not in os.listdir('pages/data'):
            st.markdown("Please upload data through `Upload Data` page!")
    else:
            # df_analysis = pd.read_csv('data/2015.csv')
            df_analysis = pd.read_csv('pages/data/main_data.csv')
            # df_visual = pd.DataFrame(df_analysis)
            df_visual = df_analysis.copy()
            cols = pd.read_csv('pages/data/metadata/column_type_desc.csv')
            Categorical,Numerical,Object = utils.getColumnTypes(cols)
            cat_groups = {}
            unique_Category_val={}

            st.subheader('Showing Bar Graph')
            st.sidebar.subheader("Select Attributes for Bar Graph")
            bar_value = st.sidebar.selectbox('Select an attribute for X-Axis in Bar Graph',df_analysis.columns)
            bar_value1 = st.sidebar.selectbox('Select an attribute for Y-Axis in Bar Graph',df_analysis.columns)
            # Alt bar chart
            chart = (
                alt.Chart(df_analysis)
                .mark_bar()
                .encode(
                    alt.X(bar_value),
                    alt.Y(bar_value1),
                    alt.Color(bar_value),
                    #alt.Size(bar_value1),
                    tooltip = [bar_value, bar_value1],
                ).interactive()
                .properties(
                    width = 600,
                    height = 300
                    )
                #bar.mark_text(color = "black").encode(text = bar_value1)
                )
            st.altair_chart(chart, use_container_width=True)

            #code for line graph
            st.subheader('Showing Line Graph')
            st.sidebar.subheader("Select Attributes for Line Graph")
            line_value = st.sidebar.selectbox('Select an Attribute for X-axis in Line Graph',df_analysis.columns)
            line_value1 = st.sidebar.selectbox('Select an Attribute for Y-axis in Line Graph',df_analysis.columns)
            # Add some matplotlib code !
            chart = alt.Chart(df_analysis).mark_line().encode(
                x=alt.X(line_value),
                y=alt.Y(line_value1),
                tooltip = [line_value, line_value1]
                #alt.Color(line_value)
                ).interactive().properties(title="Altair Line Graph")
            st.altair_chart(chart, use_container_width=True)

            #scatter plot code comes here
            st.subheader('Showing Scatter Plot')
            st.sidebar.subheader("Select Attributes for Scatter Plot")
            stack_bar = st.sidebar.selectbox('Select an attribute for X-Axis in Stacked Bar Graph',df_analysis.columns)
            stack_bar1 = st.sidebar.selectbox('Select an attribute for Y-Axis in Stacked Bar Graph',df_analysis.columns)
            #Stacked chart code goes here!!
            scatter = alt.Chart(df_analysis).mark_point(filled=True).encode(
                alt.X(stack_bar),
                alt.Y(stack_bar1),
                alt.Color(stack_bar),
                alt.Size(stack_bar1),
                alt.OpacityValue(0.8)
                #tooltip = [stack_bar, stack_bar1]
                ).interactive().properties(
                    width = 700,
                    height = 300
                    )
            st.altair_chart(scatter,use_container_width=True)