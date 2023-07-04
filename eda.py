import streamlit as st
import pandas as pd
#from io import StringIO
import ydata_profiling
from pathlib import Path


st.title('EDA Tool')
uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])
if uploaded_file is not None:
    # To read file as bytes:
    #bytes_data = uploaded_file.getvalue()
    #st.write(bytes_data)

    # To convert to a string based IO:
    #stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    #st.write(stringio)

    # To read file as string:
    #string_data = stringio.read()
    #st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    #st.write(dataframe)

    # descriptive statistics
    prof = ydata_profiling.ProfileReport(dataframe, explorative=True, minimal=True)
    output = prof.to_file('output.html', silent=False)

    #st.write("check out this [link](%s)" % url)
    #st.markdown("check out this [link](%s)" % url)