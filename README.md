# YoutubeChatBot
RAG Based Youtube ChatBot application
# 🎥 YouTube RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows users to ask questions about a specific YouTube video and receive answers grounded in the video's transcript.

The project uses **LangChain, Google Gemini, embeddings, FAISS, and Streamlit** to build an end-to-end RAG application.

## 🚀 Features

* 📺 Accepts a YouTube video URL
* 📝 Extracts the video's English transcript
* ✂️ Splits the transcript into smaller chunks
* 🔢 Generates embeddings for transcript chunks
* 🗄️ Stores embeddings in a FAISS vector database
* 🔍 Retrieves the most relevant transcript chunks for a question
* 🤖 Uses Google Gemini to generate answers
* 💬 Provides an interactive Streamlit chat interface
* 🛡️ Answers only from the retrieved transcript context
* ❓ Responds with "I don't know" when the available context is insufficient

## 🧠 How It Works

The application follows a standard RAG pipeline:

```text
YouTube URL
     │
     ▼
Extract Video ID
     │
     ▼
Fetch YouTube Transcript
     │
     ▼
Text Splitting
     │
     ▼
Generate Embeddings
     │
     ▼
FAISS Vector Store
     │
     ▼
User Question
     │
     ▼
Similarity Search
     │
     ▼
Top 4 Relevant Chunks
     │
     ▼
Prompt + Retrieved Context
     │
     ▼
Google Gemini
     │
     ▼
Final Answer
```

## 🛠️ Tech Stack

* **Python** — Core programming language
* **LangChain** — RAG pipeline and LLM orchestration
* **Google Gemini** — LLM and embedding model
* **FAISS** — Vector similarity search
* **YouTube Transcript API** — Transcript extraction
* **Streamlit** — Web interface
* **python-dotenv** — Environment variable management

## 📁 Project Structure

```text
youtube-rag-chatbot/
│
├── app.py
├── rag.py
├── requirements.txt
├── .env
└── .gitignore
```

### `app.py`

Handles the Streamlit application and user interaction.

Responsibilities:

* YouTube URL input
* Video processing button
* Chat interface
* Calling the RAG pipeline
* Displaying responses

### `rag.py`

Contains the core RAG logic.

Responsibilities:

* YouTube transcript extraction
* Text chunking
* Embedding generation
* FAISS vector store creation
* Retriever configuration
* Prompt construction
* Gemini LLM integration
* RAG chain creation

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/youtube-rag-chatbot.git
cd youtube-rag-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
```

Never commit your `.env` file or expose your API key publicly.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 💬 Example

Paste a YouTube video URL:

```text
https://www.youtube.com/watch?v=VIDEO_ID
```

After processing the video, ask questions such as:

```text
What is the main topic of this video?

What are the key points discussed?

Explain the concept mentioned in the video.

What example does the speaker give?
```

The system retrieves relevant transcript chunks and provides an answer based on that context.

## 🔍 RAG Configuration

The current implementation uses:

```text
Chunk Size     → 1000
Chunk Overlap  → 200
Retriever      → Similarity Search
Top K          → 4
Temperature    → 0.2
Vector Store   → FAISS
```

These parameters can be modified to experiment with retrieval quality and answer generation.

## 🧩 Key RAG Components

### 1. Document Processing

The YouTube transcript is divided into smaller chunks using `RecursiveCharacterTextSplitter`.

### 2. Embeddings

Each chunk is converted into a vector representation using Google's embedding model.

### 3. Vector Database

FAISS stores the embeddings and enables efficient similarity search.

### 4. Retrieval

When the user asks a question, the retriever searches for the most relevant transcript chunks.

### 5. Generation

The retrieved context is passed to Google Gemini through a prompt that instructs the model to answer only using the provided transcript.

## 🎯 Learning Goals

This project was built to understand the practical implementation of:

* Retrieval-Augmented Generation
* LangChain RAG pipelines
* Document chunking
* Embeddings
* Vector databases
* Semantic similarity search
* Prompt construction
* LLM integration
* Streamlit application development

## 🔮 Future Improvements

Possible improvements include:

* ⏱️ Displaying transcript timestamps with answers
* 🎬 Linking answers to relevant sections of the YouTube video
* 💾 Persistent vector database storage
* 🧠 Conversational memory
* 📚 Support for multiple videos
* 📊 RAG evaluation and retrieval-quality metrics
* ⚡ Streaming LLM responses
* 🌐 Deployment as a public web application

## ⚠️ Limitations

* Currently focused on videos with available English transcripts.
* Answer quality depends on the quality and availability of the transcript.
* FAISS is currently created during video processing rather than using a persistent vector database.
* The chatbot is designed to answer questions about the processed video rather than general questions.

## 📄 License

This project is available under the MIT License.
