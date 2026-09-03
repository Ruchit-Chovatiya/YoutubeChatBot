import streamlit as st

from rag import process_video, create_rag_chain


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="YouTube RAG Chatbot",
    page_icon="🎥",
    layout="centered"
)


# -----------------------------
# Title
# -----------------------------

st.title("🎥 YouTube RAG Chatbot")

st.write(
    "Paste a YouTube video URL and ask questions about its content."
)


# -----------------------------
# Session State
# -----------------------------

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None


# -----------------------------
# YouTube URL
# -----------------------------

youtube_url = st.text_input(
    "YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=..."
)


# -----------------------------
# Process Video
# -----------------------------

if st.button("Process Video"):

    if not youtube_url:
        st.warning("Please enter a YouTube URL.")

    else:

        with st.spinner("Processing video..."):

            try:

                vector_store = process_video(youtube_url)

                st.session_state.rag_chain = create_rag_chain(
                    vector_store
                )

                st.success("Video processed successfully!")

            except Exception as e:

                st.error(f"Error: {e}")


# -----------------------------
# Chat
# -----------------------------

if st.session_state.rag_chain:

    st.divider()

    st.subheader("💬 Ask Questions")

    question = st.chat_input(
        "Ask something about the video..."
    )

    if question:

        # User message
        with st.chat_message("user"):
            st.write(question)

        # Assistant response
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    answer = st.session_state.rag_chain.invoke(
                        question
                    )

                    st.write(answer)

                except Exception as e:

                    st.error(f"Error: {e}")

else:

    st.info("Process a YouTube video to start chatting.")