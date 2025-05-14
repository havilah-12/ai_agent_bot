# step 1: setup UI with Streamlit (model provider, model, system prompt, web_search, query)

import streamlit as st
import requests

st.set_page_config(page_title="LangGraph Agent UI", layout="centered")
st.title("AI Chatbot Agents")
st.write("Create and Interact with the AI Agents!")

system_prompt = st.text_area("Define your AI Agent:", height=70, placeholder="Type your system prompt here...")

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

provider = st.radio("Select Provider:", ("Groq", "OpenAI"))

if provider == "Groq":
    selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)

allow_web_search = st.checkbox("Allow Web Search")

user_query = st.text_area("Enter your query:", height=150, placeholder="Ask Anything...")

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent"):

    if user_query.strip():  # avoid empty queries
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                try:
                    response_data = response.json()

                    if response_data is not None and "error" in response_data:
                        st.error(response_data["error"])
                    elif response_data:
                        st.subheader("Agent Response")
                        st.markdown(f"**Final Response:** {response_data}")
                    else:
                        st.warning("Received empty response from the agent.")
                except ValueError:
                    st.error("Failed to decode response JSON.")
            else:
                st.error(f"Request failed with status code {response.status_code}.")
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")
    else:
        st.warning("Please enter a query before asking the agent.")
