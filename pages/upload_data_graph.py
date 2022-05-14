import streamlit as st
import numpy as np
import pandas as pd
from pages import utils
# import matplotlib.pyplot as plt
import altair as alt
import os


def upload_data():
    # load csv
    uploaded_file = st.file_uploader('Browse file', type = ['csv', 'xlsx'])
    global df
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # loading the data into a csv file and stroing it for further use.
        if st.button("Load Data"):
            st.dataframe(df)
            df.to_csv('pages/data/main_data.csv', index=False)
            #collect categorical and numerical columns.
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            categorical_cols = list(set(list(df.columns)) - set(numeric_cols))
            columns = []
            columns = utils.genMetaData(df)

            # Save the columns as a dataframe with categories
            # Here column_name is the name of the field and the type is whether it's numerical or categorical
            columns_df = pd.DataFrame(columns, columns = ['column_name', 'type'])
            columns_df.to_csv('pages/data/metadata/column_type_desc.csv', index = False)

            # Display columns 
            st.markdown("**Column Name**-**Type**")
            for i in range(columns_df.shape[0]):
                st.write(f"{i+1}. **{columns_df.iloc[i]['column_name']}** - {columns_df.iloc[i]['type']}")


        
