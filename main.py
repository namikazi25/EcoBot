import streamlit as st
import requests

# Title of the product
st.title("Biodiversity Assistant")
st.subheader("A Vision and Language Model-Powered Chatbot for Species Identification")

# Session state to store chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Chat container
st.write("### Chat Window")
chat_container = st.container()

# User input fields
with st.form(key="user_input_form", clear_on_submit=True):
    # Text input
    user_input = st.text_area("Type your message here:", placeholder="Ask a question or describe your image...")
    # File uploader for image
    uploaded_file = st.file_uploader("Attach an image (optional):", type=["jpg", "jpeg", "png"])
    # Submit button
    send_button = st.form_submit_button("Send")

# If the user sends a message
if send_button:
    # Display user's message in the chat history
    user_message = {"role": "user", "content": user_input, "image": uploaded_file}
    st.session_state["messages"].append(user_message)

    # API interaction
    response = ""  # Placeholder for bot response
    try:
        if uploaded_file:
            # If an image is uploaded, send it to the backend
            files = {"file": uploaded_file.getvalue()}
            res = requests.post("http://127.0.0.1:8000/classify_image", files=files)
            if res.status_code == 200:
                response = res.json().get("species", "I couldn't identify this species.")
            else:
                response = "Error: Unable to process the image."
        elif user_input.strip():
            # If only text is sent, interact with the text endpoint
            res = requests.get("http://127.0.0.1:8000/ask_question", params={"query": user_input})
            if res.status_code == 200:
                response = res.json().get("answer", "I couldn't understand your question.")
            else:
                response = "Error: Unable to process your question."
        else:
            response = "Please provide text or an image."
    except Exception as e:
        response = f"Error: {str(e)}"

    # Display bot's response in the chat history
    bot_message = {"role": "bot", "content": response}
    st.session_state["messages"].append(bot_message)

# Display the chat history
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
        if message.get("image"):
            st.image(message["image"], caption="Your image", use_column_width=True)
    else:
        st.write(f"**Bot:** {message['content']}")
