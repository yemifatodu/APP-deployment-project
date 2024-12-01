import streamlit as st
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder

# Function to load the model and encoders
def load_model():
    # Define the correct file path for the model
    file_path = r'C:\Users\HP\OneDrive\Documents\Projects\ML app\saved_steps.pkl'

    try:
        # Open the model file from the specified path
        with open(file_path, "rb") as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        # Handle file not found error
        st.error(f"Model file not found at {file_path}. Please ensure it's in the correct location.")
        return None
    except Exception as e:
        # Handle other exceptions
        st.error(f"An error occurred while loading the model: {e}")
        return None

# Load the model and necessary data
data = load_model()

# Check if data is loaded successfully
if data:
    regressor = data["model"]
    le_country = data["le_country"]
    le_education = data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    # Country options
    countries = (
        "United States", "India", "United Kingdom", "Germany", "Canada",
        "Brazil", "France", "Spain", "Australia", "Netherlands", "Poland",
        "Italy", "Russian Federation", "Sweden"
    )

    # Education options
    education = (
        "Post grad", "Master’s degree", "Bachelor’s degree", "Less than a Bachelors"
    )

    # Input fields
    country = st.selectbox("Country", countries)
    education_level = st.selectbox("Education Level", education)
    experience = st.slider("Years of Experience", 0, 50, 3)

    # Prediction
    ok = st.button("Calculate Salary")
    if ok:
        if data:  # Check if the model data is loaded correctly
            try:
                # Prepare input for the model
                X = np.array([[country, education_level, experience]])

                # Encode the categorical values using LabelEncoder
                # Ensure we handle unseen categories by using the transformation methods
                # Encoding country
                try:
                    X[:, 0] = le_country.transform([country])[0]  # Apply label encoding to country
                except ValueError:
                    X[:, 0] = le_country.transform([le_country.classes_[0]])[0]  # Default encoding for unseen country

                # Encoding education level
                try:
                    X[:, 1] = le_education.transform([education_level])[0]  # Apply label encoding to education
                except ValueError:
                    X[:, 1] = le_education.transform([le_education.classes_[0]])[0]  # Default encoding for unseen education level

                # Convert the encoded array to float for prediction
                X = X.astype(float)

                # Ensure X is a 2D array for prediction (it should be, but we enforce it)
                X = X.reshape(1, -1)

                # Predict salary
                salary = regressor.predict(X)
                st.subheader(f"The estimated salary is ${salary[0]:.2f}")
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")
        else:
            st.error("Model not loaded. Please check the configuration.")
