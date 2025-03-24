import streamlit as st
import fitz  # PyMuPDF for PDF extraction
from groq import Groq

# Set up Streamlit app
st.set_page_config(page_title="🤖 Elariz's Chatbot", layout="wide")
st.title("🤖 Elariz's Chatbot")

# Initialize Groq client
client = Groq(api_key="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")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_content" not in st.session_state:
    st.session_state.file_content = ""
if "file_context_added" not in st.session_state:
    st.session_state.file_context_added = False

# File uploader widget
uploaded_file = st.file_uploader("Upload a file to add context", type=["txt", "pdf", "docx"])
if uploaded_file is not None:
    file_text = ""

    try:
        if uploaded_file.type == "text/plain":
            # Handle plain text files
            file_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            # Handle PDFs using PyMuPDF
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            file_text = "\n".join([page.get_text("text") for page in doc])
        else:
            st.error("Unsupported file type. Only TXT and PDF are supported.")
    
    except Exception as e:
        st.error(f"Error reading file: {e}")
        file_text = ""

    if file_text:
        # Save the file content in session state
        st.session_state.file_content = file_text
        
        # Add the file content as context via a system message (only once)
        if not st.session_state.file_context_added:
            st.session_state.messages.insert(0, {
                "role": "system",
                "content": f"File context: {file_text}"
            })
            st.session_state.file_context_added = True
        
        st.success("File uploaded successfully! It will be used for context.")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input field for chatting
user_input = st.chat_input("Ask me anything...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # API call to Groq with the conversation history (including file context, if provided)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages,
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    bot_reply = ""
    for chunk in completion:
        bot_reply += chunk.choices[0].delta.content or ""
    
    # Store and display bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
