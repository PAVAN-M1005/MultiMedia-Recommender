import streamlit as st
import requests

# Import API key securely from config.py
from config import OPENROUTER_API_KEY

# OpenRouter API endpoint
API_URL = "https://openrouter.ai/api/v1/chat/completions"

st.title("📚🎬🎵 MultiMedia Recommender")

query = st.text_input("Enter a book, movie, or music title or keyword:")
category = st.radio("Select category:", ("Books", "Movies", "Music"))

# Model selection
models = ["gpt-4o-mini", "gpt-4o"]
selected_model = st.selectbox("Select model:", models)

def generate_recommendations(prompt, model):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 500,
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    elif response.status_code == 401:
        return "Error 401: Unauthorized - Please check your API key and credentials."
    else:
        return f"Error: {response.status_code} {response.text}"

if query:
    prompt = f"""
    You are a helpful media recommendation engine.
    Suggest 5 {category.lower()} titles similar to "{query}".
    For each, include a short description.
    Format the response as a numbered list.
    """
    st.write("Prompt sent to API:", prompt)
    # Debug partial API key display to verify loading (do not expose fully)
    st.write("Using API Key starts with:", OPENROUTER_API_KEY[:5] + "...")
    with st.spinner("Generating recommendations..."):
        result = generate_recommendations(prompt, selected_model)
        st.markdown("### Recommendations")
        st.markdown(result)
