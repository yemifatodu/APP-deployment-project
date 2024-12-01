import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Utility Functions
def shorten_categories(categories, cutoff):
    """Shortens categories by grouping less-represented items into 'Other'."""
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = "Other"
    return categorical_map

def clean_experience(x):
    """Cleans YearsCodePro column."""
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    try:
        return float(x)
    except ValueError:
        return None  # Handle invalid entries

def clean_education(x):
    """Simplifies EdLevel column."""
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree"
    if "Master’s degree" in x:
        return "Master’s degree"
    if "Professional degree" in x or "Other doctoral" in x:
        return "Post grad"
    return "Less than a Bachelors"

@st.cache_data
def load_data():
    """Loads and cleans the dataset."""
    file_path = r"C:\Users\HP\OneDrive\Documents\Projects\ML app\survey_results_public.csv"
    
    if not os.path.exists(file_path):
        st.error(f"File not found at {file_path}. Please check the path.")
        return pd.DataFrame()

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()
    
    # Select and rename relevant columns
    if "ConvertedCompYearly" not in df.columns:
        st.error("'ConvertedCompYearly' column is missing in the dataset.")
        return pd.DataFrame()

    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    
    # Drop rows with missing salary values
    df = df[df["Salary"].notnull()]
    
    # Filter for valid employment types
    df = df[df["Employment"].str.contains("full-time", na=False)]
    df = df.drop("Employment", axis=1)

    # Shorten country categories
    country_map = shorten_categories(df.Country.value_counts(), 50)  # Lower cutoff to 50
    df["Country"] = df["Country"].map(country_map)
    
    # Salary range filtering
    df = df[(df["Salary"] <= 300000) & (df["Salary"] >= 5000)]
    df = df[df["Country"] != "Other"]

    # Clean experience and education columns
    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df = df[df["YearsCodePro"].notnull()]  # Remove invalid experience entries
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    
    return df

# Load the cleaned data
df = load_data()

# Explore page function
def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
        ### Stack Overflow Developer Survey 2020
        Explore the data to understand salary trends by country and experience level.
        """
    )

    # Pie Chart - Top 15 countries
    st.write("#### Number of Data from Top 15 Countries")
    country_data = df["Country"].value_counts()
    top_15_countries = country_data[:15]
    other_countries_count = country_data[15:].sum()
    pie_data = pd.concat([top_15_countries, pd.Series({"Other": other_countries_count})])

    fig1, ax1 = plt.subplots()
    ax1.pie(
        pie_data,
        labels=pie_data.index,
        autopct="%1.1f%%",
        shadow=True,
        startangle=90,
    )
    ax1.axis("equal")  # Ensures the pie chart is a circle
    st.pyplot(fig1)

    # Bar chart - Mean salary by country
    st.write("#### Mean Salary Based on Country")
    country_salary = df.groupby("Country")["Salary"].mean().sort_values(ascending=True)
    if country_salary.empty:
        st.warning("No data available to create the bar chart.")
    else:
        st.bar_chart(country_salary)

    # Line chart - Mean salary by experience
    st.write("#### Mean Salary Based on Experience")
    experience_salary = df.groupby("YearsCodePro")["Salary"].mean().sort_values(ascending=True)
    if experience_salary.empty:
        st.warning("No data available to create the line chart.")
    else:
        st.line_chart(experience_salary)

    # Display columns and first 5 rows at the bottom
    st.write("#### Data Preview")
    st.write("Columns:", df.columns)
    st.write("First 5 rows of the dataset:")
    st.dataframe(df.head())

    # Debugging info (below visuals)
    st.write(f"Initial number of rows: {len(df)}")
    st.write(f"Rows after removing missing salary values: {df['Salary'].notnull().sum()}")
    st.write(f"Rows after filtering for valid employment: {len(df)}")
    st.write(f"Rows after shortening country categories: {len(df)}")
    st.write(f"Rows after filtering salary range: {len(df)}")
    st.write(f"Rows after cleaning 'YearsCodePro': {len(df)}")

