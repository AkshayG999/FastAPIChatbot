import streamlit as st
from openai import OpenAI

st.title("SambaNova Fast API Chatbot")
st.write("Ask any questions to our chatbot to help you accelerate your development with SamabaNova")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(base_url=st.secrets["BASE_URL"], api_key=st.secrets["API_KEY"])

# Set a default model
if "model" not in st.session_state:
    st.session_state["model"] = "Meta-Llama-3.1-70B-Instruct"

# Initialize chat history
if "messages" not in st.session_state:
    with open("fast_api_docs.txt", "r") as f:
        doc_content = f.read()
    st.session_state.messages = [{"role": "system", "content": f"You are a chatbot that has access to SambaNova's documentation. Your goal is to help answer user questions in regards to our Fast API offering. Don't answer anything else. Here is the documentation in regards to Fast API:\n\n{doc_content}"}]


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if (message["role"] != "system"):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can I help?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stop=["<|eot_id|>"],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})