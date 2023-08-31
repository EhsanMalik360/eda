import streamlit as st
import pandas as pd
import ydata_profiling
import streamlit.components.v1 as components  # Import Streamlit
import base64
import os
import time


# Show the Streamlit app in the browser
st.set_page_config(layout="wide")

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href



st.title('AIDeCipher')
uploaded_file = st.file_uploader("Convert your CSVs to interactive reports", type=['csv', 'xlsx'])
st.markdown('<style>.css-16idsys p{font-size: 20px;}.eex3ynb0{visibility: hidden;}.css-1gulkj5{height: 200px;background-color: #2125bae3;}.css-noeb3a{position: absolute;right: 570px;top: 165px;color: white;}.e1ewe7hr10{position: absolute;right: 450px;top: 45%;}.eqdbnj012{position: absolute;right: 425px;top: 28%;color: #ffffff;}.css-9ycgxx{margin-left:500px; color:#ffffff;}.css-1aehpvj{display: none;}</style>', unsafe_allow_html=True)
if uploaded_file is not None:

    filename=uploaded_file.name

    if(filename.endswith("xlsx")):
        st.warning('Only CSV files are allowed. Please upgrade to Premium for other type of files', icon="⚠️")
        exit(1)
    filesize=uploaded_file.size

#condition
    if (filesize>10000000):
        st.warning('File upload limit is 10 mb. Please upgrade to Premium for large files', icon="⚠️")
        exit(1)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)


    # descriptive statistics
    with st.spinner('Please Wait! Generating your report...'):
        prof = ydata_profiling.ProfileReport(dataframe, explorative=True, minimal=True)
        output = prof.to_file('output.html', silent=True)

    if st.button('Download Report'):
        with st.spinner('Please Wait! Generating download link of report...'):
            st.markdown(get_binary_file_downloader_html('output.html', 'HTML Report'), unsafe_allow_html=True)


    #print(output)

    path_to_html = "./output.html"
    with open(path_to_html, 'r') as f:
       html_data = f.read()

    #print(html_data)

    ## Show in webpage
    st.header("View your Report Online")
    st.components.v1.html(html_data, height=1000, scrolling=True)
    # Render the h1 block, contained in a frame of size 200x200.
