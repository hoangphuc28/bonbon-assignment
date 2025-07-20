# 🤖 BonBon Assignment

This repo is created as a submission for BonBon Assignment of Langchain course. You should focus on 2 assignment file:
- `assignment.ipynb`: This file is the original one which contains submission for assignment 1 and 2. However, because of the expired of the free-trial token of HuggingFace (an open-source AI provider), we can not interact with the chatbot in this submission anymore. So I created the `assignment.py` below.
- `assignment.py`: This file is the final submission for assignment 1 and 2. Which requires you to wait for some set-up download steps because this will run an Ollama model behind the screen instead of using a cloud hosted model (like OpenAI or HuggingFace).

---

# Prerequisites

- `WSL`
- `Docker and Docker compose CLI`

---

# Setup & Run the Chatbot

### 1. 🧱 Build the Docker images

```bash
docker compose build
```
This installs all dependencies and prepares the environment for python app (require time to install).  
⚠️ Be aware that this step requires time to install.

### 2. 🚀 Start all services

```bash
docker compose up
```
This will start all services, including `Ollama` server on the background and pull your chosen model (in this case `phi3`).  
You could change to another agent supported model if needed (change in `assignment.py` and `docker-compose.yml`).  
⚠️ Be aware that this step requires time to pull the model.  
⚠️ If you freeze at this message log from `Ollama` like below, please exit then `docker compose up` again:
```
ollama-simple      | verifying sha256 digest
ollama-simple      | writing manifest
ollama-simple      | success
```

Wait for these messages showed up, then you can continue to next step:
- `✅ Document indexing complete!`: Indicates that BonBon FAQ.pdf has already embedded into ChromaDB.
- `🤖 Chatbot ready! Ask a question (type 'exit' to quit)`: The python code has create agent instance successfully.

### 3. Attach to the chatbot container

Open a new terminal and run:
```bash
docker attach bonbon-chat
```

The chatbot running in container `bonbon-chat` waits for user input in an interactive CLI, so we need to attach to it
to enable I/O interaction.
Replace `bonbon-chat` with the actual name of your chatbot container (if different).

### 4. Start chat and exit

After attach to the `bonbon-chat` container, you could start typing any question then enter.  
Message `🤖 Bot is thinking...` indicates that the chatbot is trying to give the answer.  

Type `exit` to quit chat or `Ctr + c` to exit directly from the container, or use the following command in another terminal:
```bash
docker compose down
```