import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/ask" 

st.set_page_config(page_title="Customer Support Duo", page_icon="🤖", layout="centered")

st.title("💬 Customer Support Assistant (Sales + Tech)")

st.markdown(
    """
    This assistant connects you with a **Sales Agent** or **Tech Expert** depending on your query type.
    - 💼 Sales questions are answered immediately.
    - 🛠️ Technical issues are handled by the Tech Expert.
    """
)

# --- User Input ---
user_query = st.text_input("Enter your question:", placeholder="e.g., What are your pricing plans?")

if st.button("Send Query"):
    if user_query.strip():
        with st.spinner("Processing your concern..."):
            try:
                response = requests.post(
                    BACKEND_URL,
                    json={"query": user_query},
                    timeout=300
                )

                if response.status_code == 200:
                    data = response.json()
                    st.markdown("### 🧠 Assistant Response:")
                    st.success(data.get("response", "No response received."))

                    if "agent" in data:
                        st.caption(f"Handled by: **{data['agent']}**")

                else:
                    st.error(f"❌ Backend error: {response.status_code}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
    else:
        st.warning("Please enter a question before sending.")
