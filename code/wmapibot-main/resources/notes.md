# wmAPIbot
## Overview

This project integrates Chainlit with LangChain to create an interactive conversational bot. The bot fetches API data, displays it, and allows users to ask questions about the fetched data. Below are the functionalities, core concepts, and technical details of the implementation.

## Functionalities

1. **Fetch API Data**: The bot fetches a list of available APIs from a specified endpoint and stores the API names and their corresponding IDs.
2. **Display API Data**: The bot fetches and displays the Swagger documentation for the APIs using the stored API IDs.
3. **Ask Questions**: After processing the API data, users can ask questions, and the bot responds based on the fetched and processed API data.

## Core Concepts

### Conversational Retrieval Chain

- **ConversationalRetrievalChain**: This is a key component of LangChain used to manage the conversation flow and retrieve relevant information based on user queries. It integrates the following elements:
  - **ChatFireworks**: A conversational model that generates responses based on user input.
  - **Chroma Vector Store**: Stores text chunks and their embeddings, allowing for efficient retrieval.
  - **Memory**: Maintains the context of the conversation to provide coherent and contextually relevant responses.

### Text Splitting and Embedding

- **RecursiveCharacterTextSplitter**: Splits large text documents into smaller, manageable chunks. This is important for creating embeddings and storing them in a vector store.
- **HuggingFaceEmbeddings**: Generates embeddings for the text chunks. These embeddings are used to create a vector store, enabling semantic search and retrieval.

### Chainlit Integration

- **Chainlit**: Provides the chat interface and handles user interactions. It manages the state of the conversation and integrates with LangChain to provide real-time responses.

## Technical Details

### Event Handling

#### `on_chat_start`

This event handler initializes the chat session. It presents the user with options to fetch APIs, display fetched APIs, or ask questions. Based on user selection, it performs the appropriate action:

- **Fetching APIs**: Makes an HTTP GET request to retrieve the list of available APIs and stores their names and IDs.
- **Displaying APIs**: Fetches the Swagger documentation for each API and stores it for further processing.
- **Processing API Data**: Splits the Swagger documentation into text chunks, generates embeddings, and stores them in a Chroma vector store. Initializes the conversational retrieval chain.

### Message Handling

#### `on_message`

This event handler processes user messages. It retrieves the conversational retrieval chain from the session, generates a response using the chain, and sends the response back to the user. If there are any source documents used in generating the response, they are included as references.

## Language Model and Fireworks API Integration

### Language Model: LLaMA-7b-Chat

The conversational bot leverages the **LLaMA-7b-Chat** model to generate human-like responses. This model is designed to handle a wide range of conversational contexts and provides robust natural language understanding and generation capabilities.

### Fireworks API for Model Loading

To integrate the LLaMA-7b-Chat model into the script, the Fireworks API is used. This API facilitates the loading and configuration of the model, ensuring it is ready to generate responses as part of the conversational retrieval chain.

### Key Steps for Model Integration

1. **Model Initialization**: The Fireworks API is used to initialize the LLaMA-7b-Chat model with specific parameters such as temperature, max tokens, and top-p settings.
2. **Embedding Creation**: The model generates embeddings for text chunks, which are then stored in the Chroma vector store for efficient retrieval.
3. **Conversational Model Configuration**: The Fireworks API configures the LLaMA-7b-Chat model to work seamlessly within the LangChain framework, enabling it to provide contextually relevant responses based on user queries.

## Developer Portal API

The project interacts with a Dev Portal to fetch and display API data. This integration enables the conversational bot to retrieve a list of available APIs, fetch detailed Swagger documentation for each API, and use this information to answer user queries. The following sections describe the key APIs used and how they are integrated into the code.

### Key APIs Used

1. **Fetch All APIs**: Retrieves a list of all available APIs from the Dev Portal.
2. **Export API Documentation**: Fetches the Swagger documentation for a specific API based on its ID.

### API Endpoints

1. **Fetch All APIs Endpoint**

    - **URL**: `https://env675177.devportal-aw-us.webmethods.io/portal/rest/v1/apis/`
    - **Method**: `GET`
    - **Response**: A JSON object containing the list of APIs, each with its name and ID.

2. **Export API Documentation Endpoint**

    - **URL**: `https://env675177.devportal-aw-us.webmethods.io/portal/rest/v1/apis/{api_id}/export`
    - **Method**: `GET`
    - **Response**: A JSON object containing the Swagger documentation for the specified API.
