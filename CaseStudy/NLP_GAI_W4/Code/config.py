# config.py

"""
This file contains all the constant configurations used throughout the RAG LLM application.
It centralizes parameters such as file paths, model names, and various hyperparameters
for chunking, embedding, and LLM generation, making them easy to manage and update.
"""

# --- File Paths ---
# Path to the PDF document for data loading.
APPLE_PDF_PATH = "HBR_How_Apple_Is_Organized_For_Innovation.pdf"
# Directory to persist the Chroma vector database.
VECTOR_DB_DIR = 'vector_db_1024'   # This will have to be changed if the embedding model is changed.

# --- LLM Configuration ---
# Name of the Ollama model to be used for generating responses.
# OLLAMA_MODEL_NAME = "llama3.2"
# OLLAMA_MODEL_NAME = "deepseek-r1"
# OLLAMA_MODEL_NAME = "qwen3:4b"
# OLLAMA_MODEL_NAME = "deepseek-r1:1.5b"
OLLAMA_MODEL_NAME = "gemma3n:latest"
# OLLAMA_MODEL_NAME = "mistral"

# --- Chunking Parameters ---
# The size of each text chunk (in tokens) for RecursiveCharacterTextSplitter.
CHUNK_SIZE = 1024
# The number of overlapping tokens between consecutive chunks.
CHUNK_OVERLAP = 20
# The encoding name for tiktoken, used by RecursiveCharacterTextSplitter.
ENCODING_NAME = 'cl100k_base'

# --- Embedding Parameters ---
# The name of the Sentence Transformer model used for generating embeddings.
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'
EMBEDDING_MODEL_NAME = 'mixedbread-ai/mxbai-embed-large-v1'

# --- Retriever Parameters ---
# Default number of relevant documents to retrieve from the vector store.
DEFAULT_K_RETRIEVER = 3

# --- LLM Generation Parameters ---
# Default maximum number of tokens for the LLM to generate in its response.
DEFAULT_MAX_TOKENS = 50
# Default temperature for LLM generation (controls randomness). 0.0 is deterministic.
DEFAULT_TEMPERATURE = 0.0
# Default top_p value for nucleus sampling.
DEFAULT_TOP_P = 0.9
# Default top_k value for sampling.
DEFAULT_TOP_K = 40
