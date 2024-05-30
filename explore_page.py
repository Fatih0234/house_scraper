import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
import seaborn as sns

def show_explore_page():
    st.title("Explore Los Angeles House Rent Market")

    # Load the dataset
    df = pd.read_csv("houses.csv")

    # Calculate average price, square footage, bathrooms, and bedrooms
    avg_price = df['price'].mean()
    avg_ft = df['ft'].mean()
    avg_bathrooms = df['bath_rooms'].mean()
    avg_bedrooms = df['bed_rooms'].mean()

    # Display statistics with bold and larger text
    st.markdown("<h2 style='text-align: center; color: black;'><b>Some Statistics</b></h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: blue;'><b>Average Price:</b> ${avg_price:.2f}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: blue;'><b>Average Square Footage:</b> {avg_ft:.2f} sqft</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: blue;'><b>Average Bathrooms:</b> {avg_bathrooms:.2f}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: blue;'><b>Average Bedrooms:</b> {avg_bedrooms:.2f}</h3>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: black;'><b>Top 10 Most Expensive Cities</b></h2>", unsafe_allow_html=True)
    # Group by city and calculate the average housing price
    city_avg_price = df.groupby('city')['price'].mean().reset_index()

    # Sort cities by average price in descending order
    top_10_expensive = city_avg_price.sort_values(by='price', ascending=False).head(10)

    # Create a bar chart to visualize the top 10 most expensive cities
    plt.figure(figsize=(10, 6))
    plt.barh(top_10_expensive['city'], top_10_expensive['price'], color='skyblue')
    plt.xlabel('Average Housing Price')
    # plt.title('Top 10 Most Expensive Cities')
    plt.gca().invert_yaxis()  # Invert y-axis to display the highest price at the top
    
    # Display the bar chart
    st.pyplot(plt)

    st.markdown("<h2 style='text-align: center; color: black;'><b>Correlation Matrix</b></h2>", unsafe_allow_html=True)
    df_num = df[["price", "bed_rooms", "bath_rooms", "ft", "total_rooms", "price/sqft", "latitude", "longitude"]]
    # Compute the correlation matrix
    corr_matrix = df_num.corr()

    # Set up the matplotlib figure
    plt.figure(figsize=(10, 8))

    # Create a heatmap using Seaborn
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")

    # Add a title
    # plt.title('Correlation Matrix')

    # Display the plot
    st.pyplot(plt)

