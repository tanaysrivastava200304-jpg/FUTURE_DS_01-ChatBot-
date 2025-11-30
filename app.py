# -----------------------------------------------------
# Streamlit Customer Support Chatbot (FutureInterns Task-3)
# -----------------------------------------------------

import streamlit as st
import joblib

# Load ML model and vectorizer
model = joblib.load("intent_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Response mapping (same as Step-5)
response_map = {
    "Refund/Returns": 
        "Sure! I can help with refund and return issues. Please share your Order ID.",
    
    "Shipping/Order Tracking": 
        "I can help track your order. Please provide your tracking number or order ID.",
    
    "Account Help": 
        "I can help with account login or password issues. What problem are you facing?",
    
    "Product Issue": 
        "Sorry for the inconvenience! Please describe the product issue you are facing.",
    
    "Complaint": 
        "I'm really sorry for the trouble. Please share more details so I can assist you.",
    
    "General Query": 
        "Sure! How can I help you today?",
    
    "Positive Feedback": 
        "Thank you so much! We appreciate your feedback ❤️",
    
    "Greetings": 
        "Hello! How can I assist you today?"
}

# -----------------------------------------------------
# Chatbot Logic
# -----------------------------------------------------

def predict_intent(message):
    clean = message.lower()
    vectorized = vectorizer.transform([clean])
    intent = model.predict(vectorized)[0]
    return intent

def get_response(message):
    intent = predict_intent(message)

    if intent in response_map:
        return response_map[intent]
    else:
        return "I'm not sure I understood. Could you please rephrase?"

# -----------------------------------------------------
# STREAMLIT UI
# -----------------------------------------------------

st.set_page_config(page_title="Customer Support Chatbot", page_icon="💬")

st.title("💬 Customer Support Chatbot (FutureInterns Task-3)")
st.write("Ask me anything related to refunds, orders, account issues, product problems, or general queries.")

# Chat history (so messages stay on screen)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

# User input box
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)

    # Generate bot response
    bot_reply = get_response(user_input)

    # Add bot message to history
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    
    with st.chat_message("assistant"):
        st.write(bot_reply)
