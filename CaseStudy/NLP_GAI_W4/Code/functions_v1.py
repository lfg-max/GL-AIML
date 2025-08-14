# functions.py - Version 1.0

import os
import tiktoken
import pandas as pd
from ollama import Client
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Import constants and prompt templates
from config import (
    APPLE_PDF_PATH, VECTOR_DB_DIR, OLLAMA_MODEL_NAME,
    CHUNK_SIZE, CHUNK_OVERLAP, ENCODING_NAME,
    EMBEDDING_MODEL_NAME, DEFAULT_K_RETRIEVER,
    DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE, DEFAULT_TOP_P, DEFAULT_TOP_K
)
from prompt_templates import (
    QNA_SYSTEM_MESSAGE, QNA_USER_MESSAGE_TEMPLATE,
    GROUNDEDNESS_RATER_SYSTEM_MESSAGE, RELEVANCE_RATER_SYSTEM_MESSAGE,
    EVAL_USER_MESSAGE_TEMPLATE
)

class RAG_LLM:
    """
    A class to encapsulate the Retrieval-Augmented Generation (RAG) LLM workflow.
    This includes data loading, chunking, embedding, vector database management,
    document retrieval, LLM response generation, and evaluation functionalities.
    """

    def __init__(self):
        """
        Initializes the RAG_LLM by setting up the Ollama client and preparing
        placeholders for document chunks, embedding model, and vector store.
        """
        self.client = Client()  # Initialize the Ollama client
        self.document_chunks = None
        self.embedding_model = None
        self.vectorstore = None
        self.retriever = None
        print("RAG_LLM initialized.")

    def load_data(self, pdf_path: str = APPLE_PDF_PATH):
        """
        Loads the PDF document from the specified path.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            list: A list of loaded Document objects.
        """
        print(f"Loading data from: {pdf_path}")
        try:
            pdf_loader = PyMuPDFLoader(pdf_path)
            self.documents = pdf_loader.load()
            print(f"Successfully loaded {len(self.documents)} pages.")
            return self.documents
        except Exception as e:
            print(f"Error loading PDF data: {e}")
            return None

    def chunk_data(self, documents: list,
                   chunk_size: int = CHUNK_SIZE,
                   chunk_overlap: int = CHUNK_OVERLAP,
                   encoding_name: str = ENCODING_NAME):
        """
        Chunks the loaded documents into smaller, manageable pieces.

        Args:
            documents (list): A list of Document objects to chunk.
            chunk_size (int): The maximum size of each chunk.
            chunk_overlap (int): The overlap between consecutive chunks.
            encoding_name (str): The encoding to use for token counting.

        Returns:
            list: A list of chunked Document objects.
        """
        if not documents:
            print("No documents provided for chunking.")
            return None

        print(f"Chunking data with chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")
        try:
            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                encoding_name=encoding_name,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            self.document_chunks = text_splitter.split_documents(documents)
            print(f"Created {len(self.document_chunks)} chunks.")
            return self.document_chunks
        except Exception as e:
            print(f"Error chunking data: {e}")
            return None

    def create_embeddings(self, model_name: str = EMBEDDING_MODEL_NAME):
        """
        Initializes the sentence transformer embedding model.

        Args:
            model_name (str): The name of the sentence transformer model.
        """
        print(f"Initializing embedding model: {model_name}")
        try:
            self.embedding_model = HuggingFaceEmbeddings(model_name=model_name)
            print("Embedding model initialized successfully.")
        except Exception as e:
            print(f"Error initializing embedding model: {e}")

    def setup_vector_database(self, document_chunks: list = None, persist_directory: str = VECTOR_DB_DIR):
        """
        Sets up the Chroma vector database from document chunks and embedding model.
        If chunks are not provided, it attempts to use pre-existing chunks.
        If the database directory already exists, it loads the existing vectorstore.

        Args:
            document_chunks (list, optional): The list of chunked documents.
                                             Defaults to None, using self.document_chunks.
            persist_directory (str): The directory to persist the vector database.
        """
        if not self.embedding_model:
            print("Embedding model not initialized. Please call create_embeddings() first.")
            return

        if not document_chunks and not self.document_chunks:
            print("No document chunks provided or available to set up vector database.")
            return

        chunks_to_use = document_chunks if document_chunks is not None else self.document_chunks

        print(f"Setting up vector database in: {persist_directory}")
        try:
            if not os.path.exists(persist_directory) or not os.listdir(persist_directory):
                # Create directory if it doesn't exist
                os.makedirs(persist_directory, exist_ok=True)
                self.vectorstore = Chroma.from_documents(
                    chunks_to_use,
                    self.embedding_model,
                    persist_directory=persist_directory
                )
                print("Vector database created and persisted.")
            else:
                self.vectorstore = Chroma(
                    persist_directory=persist_directory,
                    embedding_function=self.embedding_model
                )
                print("Vector database loaded from existing directory.")
            self.retriever = self.vectorstore.as_retriever(
                search_type='similarity',
                search_kwargs={'k': DEFAULT_K_RETRIEVER}
            )
            print("Retriever initialized.")
        except Exception as e:
            print(f"Error setting up vector database: {e}")

    def get_context(self, user_input: str, k: int = DEFAULT_K_RETRIEVER):
        """
        Retrieves relevant document chunks based on a user query.

        Args:
            user_input (str): The user's question or query.
            k (int): The number of relevant documents to retrieve.

        Returns:
            str: A concatenated string of relevant document content.
        """
        if not self.retriever:
            print("Retriever not initialized. Please set up the vector database first.")
            return ""

        print(f"Retrieving {k} relevant documents for the query.")
        try:
            relevant_document_chunks = self.retriever.invoke(user_input)
            context_list = [d.page_content for d in relevant_document_chunks]
            return ". ".join(context_list)
        except Exception as e:
            print(f"Error getting context: {e}")
            return ""

    def create_rag_prompt(self, question: str, k: int = DEFAULT_K_RETRIEVER):
        """
        Creates a RAG-enhanced prompt for the LLM by combining the system message,
        retrieved context, and user question.

        Args:
            question (str): The user's question.
            k (int): The number of relevant documents to retrieve for context.

        Returns:
            list: A list of message dictionaries formatted for the Ollama chat API.
        """
        context_for_query = self.get_context(question, k=k)
        if not context_for_query:
            print("Could not retrieve context for the prompt.")
            return [{"role": "user", "content": question}] # Fallback to normal prompt

        user_message = QNA_USER_MESSAGE_TEMPLATE.replace('{context}', context_for_query)
        user_message = user_message.replace('{question}', question)

        prompt = [
            {"role": "system", "content": QNA_SYSTEM_MESSAGE},
            {"role": "user", "content": user_message}
        ]
        print("RAG prompt created.")
        return prompt

    def generate_llm_response(self, prompt: list,
                              model: str = OLLAMA_MODEL_NAME,
                              max_tokens: int = DEFAULT_MAX_TOKENS,
                              temperature: float = DEFAULT_TEMPERATURE,
                              top_p: float = DEFAULT_TOP_P,
                              top_k: int = DEFAULT_TOP_K):
        """
        Generates a response from the Ollama language model using the chat completion API.

        Args:
            prompt (list[dict]): A list of message dictionaries in the format
                                 [{"role": "system", "content": "..."},
                                  {"role": "user", "content": "..."}].
            model (str): The name of the Ollama model to use.
            max_tokens (int): The maximum number of tokens to generate.
            temperature (float): Controls the randomness of the output.
            top_p (float): Nucleus sampling parameter.
            top_k (int): Limits sampling to top_k tokens.

        Returns:
            str: The generated response content from the LLM, or an error message.
        """
        print(f"Generating LLM response using model: {model}")
        try:
            llm_response = self.client.chat(
                model=model,
                messages=prompt,
                options={
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k,
                    "max_tokens": max_tokens,
                }
            )
            message = llm_response['message']['content']
            print("LLM response generated.")
            return message
        except Exception as e:
            response = f'Sorry, I encountered the following error while generating LLM response: \n {e}'
            print(response)
            return response

    def get_answer(self, user_input: str, k: int = DEFAULT_K_RETRIEVER, **llm_kwargs):
        """
        Combines context retrieval and LLM response generation to answer a user question.

        Args:
            user_input (str): The user's question.
            k (int): The number of relevant documents to retrieve.
            **llm_kwargs: Additional keyword arguments to pass to generate_llm_response.

        Returns:
            str: The generated answer from the RAG system.
        """
        rag_prompt = self.create_rag_prompt(user_input, k=k)
        if not rag_prompt: # Fallback if context retrieval failed
            print("Failed to create RAG prompt. Attempting to answer without context.")
            return self.generate_llm_response([{"role": "user", "content": user_input}], **llm_kwargs)
        return self.generate_llm_response(rag_prompt, **llm_kwargs)

    def create_groundedness_prompt(self, question: str, answer: str, k: int = DEFAULT_K_RETRIEVER):
        """
        Creates a prompt for the LLM to evaluate the groundedness of an answer.

        Args:
            question (str): The original user question.
            answer (str): The AI-generated answer to be evaluated.
            k (int): The number of relevant documents used as context.

        Returns:
            list: A list of message dictionaries for the Ollama chat API.
        """
        context_for_query = self.get_context(question, k=k)
        if not context_for_query:
            print("Could not retrieve context for groundedness evaluation.")
            return None

        user_message = EVAL_USER_MESSAGE_TEMPLATE.replace('{context}', context_for_query)
        user_message = user_message.replace('{question}', question)
        user_message = user_message.replace('{answer}', answer)

        prompt = [
            {"role": "system", "content": GROUNDEDNESS_RATER_SYSTEM_MESSAGE},
            {"role": "user", "content": user_message}
        ]
        return prompt

    def create_relevance_prompt(self, question: str, answer: str, k: int = DEFAULT_K_RETRIEVER):
        """
        Creates a prompt for the LLM to evaluate the relevance of an answer.

        Args:
            question (str): The original user question.
            answer (str): The AI-generated answer to be evaluated.
            k (int): The number of relevant documents used as context.

        Returns:
            list: A list of message dictionaries for the Ollama chat API.
        """
        context_for_query = self.get_context(question, k=k)
        if not context_for_query:
            print("Could not retrieve context for relevance evaluation.")
            return None

        user_message = EVAL_USER_MESSAGE_TEMPLATE.replace('{context}', context_for_query)
        user_message = user_message.replace('{question}', question)
        user_message = user_message.replace('{answer}', answer)

        prompt = [
            {"role": "system", "content": RELEVANCE_RATER_SYSTEM_MESSAGE},
            {"role": "user", "content": user_message}
        ]
        return prompt

    def rate_groundedness(self, question: str, answer: str, k: int = DEFAULT_K_RETRIEVER):
        """
        Rates the groundedness of an answer using the LLM as a judge.

        Args:
            question (str): The original user question.
            answer (str): The AI-generated answer to be evaluated.
            k (int): The number of relevant documents used as context.

        Returns:
            str: The LLM's groundedness rating.
        """
        print("Rating groundedness...")
        prompt = self.create_groundedness_prompt(question, answer, k=k)
        if not prompt:
            return "Groundedness evaluation failed: context not found."
        response = self.generate_llm_response(prompt, max_tokens=200, temperature=0.1) # Use higher max_tokens for evaluation output
        return response

    def rate_relevance(self, question: str, answer: str, k: int = DEFAULT_K_RETRIEVER):
        """
        Rates the relevance of an answer using the LLM as a judge.

        Args:
            question (str): The original user question.
            answer (str): The AI-generated answer to be evaluated.
            k (int): The number of relevant documents used as context.

        Returns:
            str: The LLM's relevance rating.
        """
        print("Rating relevance...")
        prompt = self.create_relevance_prompt(question, answer, k=k)
        if not prompt:
            return "Relevance evaluation failed: context not found."
        response = self.generate_llm_response(prompt, max_tokens=200, temperature=0.1) # Use higher max_tokens for evaluation output
        return response

    def rate_answer(self, question: str, answer: str, k: int = DEFAULT_K_RETRIEVER):
        """
        Rates both groundedness and relevance of an answer.

        Args:
            question (str): The original user question.
            answer (str): The AI-generated answer to be evaluated.
            k (int): The number of relevant documents used as context.

        Returns:
            dict: A dictionary containing groundedness and relevance ratings.
        """
        print("Rating overall answer quality (groundedness and relevance)...")
        groundedness_response = self.rate_groundedness(question, answer, k=k)
        relevance_response = self.rate_relevance(question, answer, k=k)

        return {
            "groundedness": groundedness_response,
            "relevance": relevance_response
        }

    def calculate_rating(self, question: str, k: int = DEFAULT_K_RETRIEVER, **llm_kwargs):
        """
        Generates an answer for a question and then rates its groundedness and relevance.

        Args:
            question (str): The user's question.
            k (int): The number of relevant documents to retrieve.
            **llm_kwargs: Additional keyword arguments to pass to generate_llm_response.
        """
        print(f"\n--- Calculating Ratings for Question: '{question}' ---")
        answer = self.get_answer(question, k=k, **llm_kwargs)
        rating = self.rate_answer(question, answer, k=k)

        print("\n--- Results ---")
        print("Question: \n", question)
        print("\nAnswer: \n", answer)
        print("\nGroundedness Rating: \n", rating['groundedness'])
        print("\nRelevance Rating: \n", rating['relevance'])
        print("--------------------------------------------------")

