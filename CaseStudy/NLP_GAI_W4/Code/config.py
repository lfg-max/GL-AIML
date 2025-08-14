# config.py

"""
This file contains all the constant configurations used throughout the RAG LLM application.
It centralizes parameters for file paths, model names, and various hyperparameters,
making them easy to manage and update.
"""
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (for the GEMINI_API_KEY)
load_dotenv()

# --- LLM Provider Configuration ---
# Your API key for Google Gemini. Loaded from the .env file.
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# --- Model Names ---
# Define the default models you want to use for each provider.
DEFAULT_OLLAMA_MODEL = "gemma3n:latest"  # Your last used Ollama model
DEFAULT_OLLAMA_MODEL = 'qwen3:4b-instruct'
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash-latest" # A common and efficient Gemini model

# --> SET YOUR OVERALL DEFAULT MODEL HERE <--
# Change this to DEFAULT_GEMINI_MODEL to use Gemini by default.
DEFAULT_MODEL_NAME = DEFAULT_OLLAMA_MODEL

# --- File Paths ---
# Path to the PDF document for data loading.
APPLE_PDF_PATH = "HBR_How_Apple_Is_Organized_For_Innovation.pdf"
# Directory to persist the Chroma vector database.
VECTOR_DB_DIR = 'vector_db_1024'

# --- Chunking Parameters ---
# The size of each text chunk (in tokens).
CHUNK_SIZE = 1024
# The number of overlapping tokens between consecutive chunks.
CHUNK_OVERLAP = 20
# The encoding name for tiktoken, used for token counting.
ENCODING_NAME = 'cl100k_base'

# --- Embedding Parameters ---
# The name of the Sentence Transformer model used for generating embeddings.
# Note: If you change the embedding model, you must delete the old VECTOR_DB_DIR.
EMBEDDING_MODEL_NAME = 'mixedbread-ai/mxbai-embed-large-v1'

# --- Retriever Parameters ---
# Default number of relevant documents to retrieve from the vector store.
DEFAULT_K_RETRIEVER = 3

# --- LLM Generation Parameters ---
# Default maximum number of tokens for the LLM to generate.
DEFAULT_MAX_TOKENS = 1024 # Increased from 50 to allow for more complete answers
# Default temperature for LLM generation (controls randomness). 0.0 is deterministic.
DEFAULT_TEMPERATURE = 0.1 # A low temperature for more factual, less creative answers
# Default top_p value for nucleus sampling.
DEFAULT_TOP_P = 0.9
# Default top_k value for sampling.
DEFAULT_TOP_K = 40