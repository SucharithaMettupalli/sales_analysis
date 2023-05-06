import streamlit as st
import pandas as pd
import altair as alt
import base64


st.title("Sales Analysis")

# Load the dataset
df = pd.read_csv("customer_shopping_data.csv")


# Add a sidebar to filter the data by shopping mall, category, and payment method
shopping_mall = st.sidebar.selectbox("Select a Shopping Mall", df["shopping_mall"].unique())
category = st.sidebar.selectbox("Select a Category", df["category"].unique())
payment_methods = st.sidebar.multiselect("Select Payment Methods", df["payment_method"].unique())

# Filter the data based on the sidebar selections
filtered_data = df[(df["shopping_mall"] == shopping_mall) & (df["category"] == category) & (df["payment_method"].isin(payment_methods))]

# Display a summary of the filtered data
st.write(f"Showing data for {shopping_mall} shopping mall, {category} category, and {len(payment_methods)} payment method(s): {', '.join(payment_methods)}")
st.write(f"Number of transactions: {len(filtered_data)}")
st.write(f"Total sales: {filtered_data['price'].sum()}")

# Add a slider to filter the data by age range
age_range = st.slider("Select an age range", min_value=18, max_value=80, value=(18, 80))
filtered_data = filtered_data[(filtered_data["age"] >= age_range[0]) & (filtered_data["age"] <= age_range[1])]

# Add a checkbox to toggle the display of the filtered data table
show_table = st.checkbox("Show filtered data table")

# Add a filter to allow the user to select which graphs to display
display_scatter_plot = st.checkbox("Display Age vs. Price Scatter Plot")
display_payment_method_chart = st.checkbox("Display Payment Method Bar Chart")

# Define the color scheme for the charts
colors = alt.Scale(domain=["Female", "Male"], range=["#E15759", "#5DA5DA"])

# Display the scatter plot if the checkbox is checked
if display_scatter_plot:
    scatter_plot = alt.Chart(filtered_data).mark_circle().encode(
        x="age",
        y="price",
        color=alt.Color("gender", scale=colors),
        size="quantity",
        tooltip=["age", "price"]
    ).interactive()

    st.altair_chart(scatter_plot, use_container_width=True)

# Display the payment method chart if the checkbox is checked
if display_payment_method_chart:
    payment_method_chart = alt.Chart(filtered_data).mark_bar().encode(
        x=alt.X("payment_method", sort=alt.EncodingSortField(field="price", op="sum", order="descending")),
        y=alt.Y("sum(price)", axis=alt.Axis(title="Total Sales")),
        color=alt.Color("payment_method", scale=alt.Scale(scheme="set1")),
        tooltip=["payment_method", "sum(price)"]
    ).interactive()

    st.altair_chart(payment_method_chart, use_container_width=True)

# Display the filtered data table if the checkbox is checked
if show_table:
    st.write("Filtered Data")
    st.write(filtered_data)
