import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses SambaNovaCloud to generate responses. "
    "To use this app, you need to provide Samba Nova API key, which you can get [here](https://cloud.sambanova.ai/apis). "
)

samba_nova_api_key = st.text_input("SambaNova API Key", type="password")
if not samba_nova_api_key:
    st.info("Please add your SambaNova API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(
            base_url="https://api.sambanova.ai/v1",
            api_key=samba_nova_api_key
        )

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        stream = client.chat.completions.create(
            model="Meta-Llama-3.1-8B-Instruct",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
