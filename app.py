import streamlit as st
import json
import os
import time
from langchain.prompts.chat import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from pinecone import Pinecone, ServerlessSpec
import cloudinary
import cloudinary.uploader
import cloudinary.api
# from IPython.display import Audio

# Initialize embedding model
def initialize_embedding_model(model_name, device="cpu", normalize_embeddings=True):
    model_kwargs = {"device": device}
    encode_kwargs = {"normalize_embeddings": normalize_embeddings}
    return HuggingFaceBgeEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

MODEL_NAME = "intfloat/multilingual-e5-large-instruct"
embedding_bge = initialize_embedding_model(MODEL_NAME)

# Initialize Pinecone
def initialize_pinecone():
    os.environ['PINECONE_API_KEY'] = 'your_pinecone_api_key_here'
    return Pinecone(api_key=os.environ['PINECONE_API_KEY'])

pc = initialize_pinecone()
index_name = "audioscoutmultifinal"

index = pc.Index(index_name)

def query_pinecone(query_text, top_k=3):
    query_embedding = embedding_bge.embed_query(query_text)
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    
    context = [match['metadata']['text'] for match in results["matches"]]
    audio_file_name = results["matches"][0]['metadata'].get("audio_file_name", "") if results["matches"] else ""
    
    return context, audio_file_name

# # Prompt Template
# template = """
# You are given retrieved documents {chunks} to a user question {question}. Generate the response both in Telugu and English based on the context. Ensure it is directly based on the context provided:
#     1) Generate the response in Telugu (avoid repeating points).
#     2) Generate the response in English (avoid repeating points).

# Output format:
# {{
#   "response_te": "Telugu response here",
#   "response_en": "English response here"
# }}
# """

# def build_prompt(chunks: list, question: str) -> str:
#     """
#     Builds the prompt with the extracted chunks and the user’s question.

#     Args:
#         chunks (list): Extracted chunks of text.
#         question (str): The user's question based on the chunks.

#     Returns:
#         str: Constructed prompt for Ollama model.
#     """
#     chunks_str = "\n".join(chunks)
#     return template.format(chunks=chunks_str, question=question)

# # Initialize the LLM
# llm = ChatOllama(
#     model="llama3.2",
#     temperature=0.1,
# )

# # Cloudinary Configuration
# cloudinary.config(
#     cloud_name="dor6f9djm",
#     api_key="913583522522472",
#     api_secret="Dv24O8YWHgt3Hq7HVkeq8pokfeU"
# )

# def search_audio_by_name(filename):
#     response = cloudinary.api.resources(
#         type="upload",
#         resource_type="video",
#         prefix=filename
#     )
#     return response["resources"][0]["secure_url"] if response["resources"] else "No file found."

st.title("AudioScout Chatbot")
question = st.text_input("Ask a question:")
if st.button("Get Answer") and question:
    context, audio_file_name = query_pinecone(question)
    # prompt = build_prompt(context, question)
    # chat_prompt = ChatPromptTemplate.from_messages([
    #     ("system", "You are a helpful assistant trained to generate Telugu and English responses."),
    #     ("human", "{input}"),
    # ])
    # chain = chat_prompt | llm
    # response = chain.invoke({"input": prompt})
    
    # json_content = response.content.replace("\n", "")
    
    # # Audio search
    # audio_file_name, _ = os.path.splitext(audio_file_name)
    # audio_url = search_audio_by_name(audio_file_name)
    
    # if "No file found" not in audio_url:
    #     st.audio(audio_url)
    # else:
    #     st.warning("Audio file not found.")
    
    # try:
    #     response_json = json.loads(json_content)
    #     st.subheader("Telugu Response:")
    #     st.write(response_json["response_te"])
    #     st.subheader("English Response:")
    #     st.write(response_json["response_en"])
    # except json.JSONDecodeError:
    #     st.error("Error parsing response.")
    st.subheader("Telugu Response:")
    st.write(context)
    st.subheader("English Response:")
    st.write(audio_file_name)

