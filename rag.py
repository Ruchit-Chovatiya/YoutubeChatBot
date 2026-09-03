from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

from urllib.parse import urlparse, parse_qs


def extract_video_id(youtube_url):

    parsed_url = urlparse(youtube_url)

    # Standard URL:
    # https://www.youtube.com/watch?v=VIDEO_ID
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed_url.query).get("v", [None])[0]

    # Short URL:
    # https://youtu.be/VIDEO_ID
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path.strip("/")

    return None

def process_video(youtube_url):

    video_id = extract_video_id(youtube_url)

    try:
        transcript_list = YouTubeTranscriptApi().fetch(video_id, languages = ['en'])

        # flatten it into the plain text
        transcript = " ".join(chunk.text for chunk in transcript_list)
        print(transcript)

    except TranscriptsDisabled:
        print('No caption available for this video')

    # transcript_list
    splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    chunks = splitter.create_documents([transcript])

    # Indexing(Embedding generation and storing in vector store)

    embeddings = GoogleGenerativeAIEmbeddings(model = 'gemini-embedding-2')
    vector_store = FAISS.from_documents(chunks, embeddings)

    return vector_store


# Building a chain

def format_docs(retrieved_docs):
    context_text = '\n\n'.join(doc.page_content for doc in retrieved_docs)
    return context_text

def create_rag_chain(vector_store):

    # Step 1: Retrieval
    retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
    )

    # Step 2: Prompt
    prompt = PromptTemplate(
        template = """
        You are helpful assistant.
        Answer ONLY from provided transcript context.
        If the context is insufficient, just say you don't know.

        {context}
        Question: {question}
        """,
        input_variables = ['context', 'question']
    )

    # Step 3: LLM
    llm = ChatGoogleGenerativeAI(model = 'gemini-3.6-flash', temperature = 0.2)

    # Step 4: Output parser
    parser = StrOutputParser()

    # Step 5: RAG chain
    chain = {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    } | prompt | llm | parser

    return chain