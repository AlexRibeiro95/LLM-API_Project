import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set the API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate product recommendations
def generate_product_recommendations(user_preferences, temperature=0.7, max_tokens=100):
    prompt = f"Based on the following preferences, recommend some products: {user_preferences}."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        recommendations = response['choices'][0]['message']['content'].strip()
        return recommendations
    except openai.error.RateLimitError:
        return "Rate limit exceeded. Please try again later."

# Streamlit app interface
def main():
    st.title("AI-Powered Product and Services Recommendation Tool")
    
    # Session state to manage the form reset
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    # Collect user input
    st.subheader("Enter your preferences:")
    if not st.session_state.submitted:
        activity = st.text_input("What type of activities do you enjoy? (e.g., outdoor activities, cooking, reading):")
        interests = st.text_input("What are your specific interests? (e.g., hiking, technology, mystery novels):")
        needs = st.text_input("What specific item are you looking for? (e.g., backpack, kitchen gadget, book):")
    else:
        st.text("Form submitted. Click Restart to input new preferences.")

    # Buttons to submit and restart
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Get Recommendations"):
            if not st.session_state.submitted and activity and interests and needs:
                user_preferences = f"I enjoy {activity}, specifically {interests}, and I'm looking for a new {needs}."
                recommendations = generate_product_recommendations(user_preferences)
                st.session_state.submitted = True
                st.subheader("Product Recommendations:")
                st.write(recommendations)
            elif not st.session_state.submitted:
                st.warning("Please fill in all the fields to get recommendations.")
    
    with col2:
        if st.button("Restart"):
            for key in st.session_state.keys():
                del st.session_state[key] # Simulates a rerun by setting query params

if __name__ == "__main__":
    main()