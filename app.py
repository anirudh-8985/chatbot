# import asyncio

# import streamlit as st
# import json
# import os
# import time
# from langchain.prompts.chat import ChatPromptTemplate
# from langchain_ollama import ChatOllama
# # from langchain_community.embeddings import HuggingFaceBgeEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings

# from pinecone import Pinecone, ServerlessSpec
# import cloudinary
# import cloudinary.uploader
# import cloudinary.api
# from IPython.display import Audio

# # Initialize embedding model
# def initialize_embedding_model(model_name, device="cpu", normalize_embeddings=True):
#     model_kwargs = {"device": device}
#     encode_kwargs = {"normalize_embeddings": normalize_embeddings}
#     return HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

# MODEL_NAME = "intfloat/multilingual-e5-large-instruct"
# embedding_bge = initialize_embedding_model(MODEL_NAME)

# # Initialize Pinecone
# def initialize_pinecone():
#     # os.environ['PINECONE_API_KEY'] = 'pcsk_3CQZqt_M3GaEapEbngsNymUEnyGagoVWgg6EhwN8nfSMoWSTbbiipW7tjJZhV3UwpKccTZ'
#     return Pinecone(api_key='pcsk_3CQZqt_M3GaEapEbngsNymUEnyGagoVWgg6EhwN8nfSMoWSTbbiipW7tjJZhV3UwpKccTZ')

# pc = initialize_pinecone()
# index_name = "audioscoutmultifinal"

# # existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
# # if index_name not in existing_indexes:
# #     pc.create_index(
# #         name=index_name,
# #         dimension=896,
# #         metric="cosine",
# #         spec=ServerlessSpec(cloud="aws", region="us-east-1"),
# #     )
# #     while not pc.describe_index(index_name).status["ready"]:
# #         time.sleep(1)

# index = pc.Index(index_name)

# def query_pinecone(query_text, top_k=3):
#     query_embedding = embedding_bge.embed_query(query_text)
#     results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    
#     context = [match['metadata']['text'] for match in results["matches"]]
#     audio_file_name = ""
#     if results["matches"]:
#         audio_file_name = results["matches"][0]['metadata'].get("audio_file_name", "")

#     # audio_file_name = results["matches"][0]['metadata'].get("audio_file_name", "") if results["matches"] else ""
    
#     return context, audio_file_name

# st.title("AudioScout Chatbot")
# question = st.text_input("Ask a question:")
# if st.button("Get Answer") and question:
#     # context, audio_file_name = query_pinecone(question)

#     st.subheader("Chunks:")
#     # st.write(context)
#     st.subheader("Audio name")
#     # st.write(audio_file_name)
import streamlit as st

# Initialize session state for sum if not already present
if "total" not in st.session_state:
    st.session_state.total = 0

st.title("Simple Addition App")

# User input for a number
num = st.number_input("Enter a number:", value=0, step=1)

# Add button
if st.button("Add to Total"):
    st.session_state.total += num

# Display the total sum
st.subheader(f"Running Total: {st.session_state.total}")
