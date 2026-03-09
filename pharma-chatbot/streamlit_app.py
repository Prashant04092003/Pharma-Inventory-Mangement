import streamlit as st
import requests
import uuid

# Backend URL
API_URL = "http://127.0.0.1:8001/chat"

st.set_page_config(page_title="Pharmacy Chatbot", layout="wide")

st.title("💊 Pharmacy Inventory Chatbot")

# Role selection
role = st.selectbox("Select Role", ["SHOP_OPERATOR", "ADMIN"])

# Store input
store_id = None
if role == "SHOP_OPERATOR":
    store_id = st.number_input("Enter Your Store ID", min_value=1, step=1)

# Message input
message = st.text_input("Ask your question")

# Session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if st.button("Send"):
    if not message:
        st.warning("Please enter a message.")
    else:
        payload = {
            "message": message,
            "role": role,
            "store_id": store_id,
            "session_id": st.session_state.session_id
        }

        try:
            response = requests.post(API_URL, json=payload)
            result = response.json()

            if result["success"]:
                data = result["data"]

                if isinstance(data, dict) and "items" in data:
                    st.success(data.get("summary", "Results"))
                    st.write(f"Total Items: {data.get('total_items')}")
                    st.dataframe(data["items"])

                elif isinstance(data, dict) and "response" in data:
                    st.success(data["response"])

                else:
                    st.json(data)

            else:
                st.error(result["error"])

        except Exception as e:
            st.error(f"Backend error: {e}")