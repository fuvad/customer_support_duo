import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8080/ask" 

st.set_page_config(page_title="Customer Support Duo", page_icon="🤖", layout="centered")

st.title("💬 Customer Support Assistant (Sales + Tech)")

st.markdown(
    """
    This assistant connects you with a **Sales Agent** or **Tech Expert** depending on your query type.
    - 💼 Sales questions are answered immediately.
    - 🛠️ Technical issues are handled by the Tech Expert.
    """
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Display previous messages like a real chat ---
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])
            if "agent" in msg:
                st.caption(f"🧩 Handled by: **{msg['agent']}**")

# --- User Input ---
if user_input := st.chat_input("Type your question..."):
    # Save user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Show it immediately
    with st.chat_message("user"):
        st.markdown(user_input)


    # Prepare the context (last 2 user+assistant pairs)
    recent_context = []
    for m in reversed(st.session_state["messages"]):
        recent_context.append(m)
        if len(recent_context) >= 4:  # last 2 interactions (user+bot)
            break
    recent_context.reverse()

    # --- Send to FastAPI backend ---
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    BACKEND_URL,
                    json={"query": user_input,
                          "history": recent_context
                    },
                    timeout=300
                )

                if response.status_code == 200:
                    data = response.json()
                    assistant_response = data.get("response", "No response received.")
                    agent = data.get("agent", "Unknown")

                    st.markdown(assistant_response)
                    st.caption(f"🧩 Handled by: **{agent}**")

                # Save assistant message
                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": assistant_response,
                        "agent": agent
                    })

                else:
                    st.error(f"❌ Backend error: {response.status_code}")

            except Exception as e:
                st.error(f"⚠️ Failed to connect to backend: {e}")
