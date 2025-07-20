# BonBon Assignment

This repository contains the submission for the BonBon Assignment in the Langchain course. Please focus on the following two key files:

- **`assignment.py`**: This script is the final, fully functional submission for Assignment 1 and 2. Instead of relying on cloud-hosted models like HuggingFace or OpenAI, it runs a local model through Ollama, which requires some initial downloads and setup.

---

## Prerequisites

Ensure the following tools are installed in your environment:

- **WSL**
- **Docker & Docker Compose CLI**

---

## Setup & Run the Chatbot

### 1. Build Docker Images

Run the command below to build the required Docker images and install all dependencies:

```bash
docker compose build
```

> ⚠️ This step may take some time as it downloads and installs necessary packages.

---

### 2. Start All Services

Start the full system with:

```bash
docker compose up
```

This command launches all services including the Ollama server and begins pulling the selected model (default is `phi3`).

> ⚠️ Model downloading may take a while.  
> ⚠️ If the logs hang at the following message:
> ```
> ollama-simple      | verifying sha256 digest
> ollama-simple      | writing manifest
> ollama-simple      | success
> ```
> simply stop the process and run `docker compose up` again.

Wait for these key logs before proceeding:

- `✅ Document indexing complete!`: Indicates successful embedding of `BonBon FAQ.pdf` into ChromaDB.
- `🤖 Chatbot ready! Ask a question (type 'exit' to quit)`: Confirms the chatbot agent has been initialized and is ready.

---

### 3. Attach to the Chatbot Container

In a new terminal window, attach to the chatbot container to begin interaction:

```bash
docker attach bonbon-chat
```

Replace `bonbon-chat` with the actual name of your container if it differs.

---

### 4. Interact with the Chatbot

Once attached, you can start asking questions directly in the terminal.  
When you see:

```
🤖 Bot is thinking...
```

it means the chatbot is generating a response.

To exit the chat, type `exit` or use `Ctrl + C`.  
Alternatively, you can shut down all services from another terminal using:

```bash
docker compose down
```
### 5. Output example:
<img width="1049" height="594" alt="image" src="https://github.com/user-attachments/assets/7c32047b-df64-49dc-a54d-3c2412b515fc" />

---
