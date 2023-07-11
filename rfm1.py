import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# Load the customer data
@st.cache_data
def load_data():
    data = pd.read_csv('data.csv', encoding='unicode_escape')  # Replace 'customer_data.csv' with your own dataset
    return data


# Perform RFM analysis and customer segmentation
def perform_segmentation(data):
    # Perform RFM analysis (Recency, Frequency, Monetary Value)
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    rfm_data = data.groupby('CustomerID').agg({'InvoiceDate': lambda x: (data['InvoiceDate'].max() - x.max()).days,
                                               'InvoiceNo': 'count',
                                               'TotalPrice': 'sum'}).reset_index()
    rfm_data.rename(columns={'InvoiceDate': 'Recency',
                             'InvoiceNo': 'Frequency',
                             'TotalPrice': 'MonetaryValue'}, inplace=True)

    # Normalize the RFM data
    rfm_norm = pd.DataFrame()
    rfm_norm['Recency'] = (rfm_data['Recency'] - rfm_data['Recency'].min()) / (
            rfm_data['Recency'].max() - rfm_data['Recency'].min())
    rfm_norm['Frequency'] = (rfm_data['Frequency'] - rfm_data['Frequency'].min()) / (
            rfm_data['Frequency'].max() - rfm_data['Frequency'].min())
    rfm_norm['MonetaryValue'] = (rfm_data['MonetaryValue'] - rfm_data['MonetaryValue'].min()) / (
            rfm_data['MonetaryValue'].max() - rfm_data['MonetaryValue'].min())

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=5, random_state=42)
    kmeans.fit(rfm_norm)
    rfm_data['Segment'] = kmeans.labels_

    return rfm_data


# Visualize the segmented customers
def visualize_segmentation(data):
    segments = data['Segment'].unique()
    for segment in segments:
        segment_data = data[data['Segment'] == segment]

        st.subheader(f"Segment {segment + 1} Data")
        st.write(segment_data)


# Main function
def main():
    st.title('Customer Segmentation using RFM Analysis')

    # Load the data
    data = load_data()

    # Perform customer segmentation
    rfm_data = perform_segmentation(data)

    # Visualize the segmented customers
    visualize_segmentation(rfm_data)


main()
