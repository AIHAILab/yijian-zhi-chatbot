# Yijian Zhi Chatbot
A RAG chatbot based on OpenAI API that can answer questions about "Yijian Zhi" (夷堅志).

![App Banner 1](./public/demo_1.png)

![App Banner 2](./public/demo_2.png)

## Installation

Follow these steps to install and set up:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/youkwan/yijian-zhi-chatbot.git
    cd ./yijian-zhi-chatbot/
    ```

2.  **Configure Environment Variables:**
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
    Then, open the `.env` file with a text editor and fill in the required configuration values (e.g., OPENAI API key, LangSmith API key, etc.).

3.  **Run the application:**

    You can choose one of the following methods to run the application.

    ### Option 1: Docker (Recommended)
    
    This is the recommended way to run the application.

    **Build and Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    The app will start and run at http://localhost:8000
    
    ### Option 2: Manual Setup (without Docker)
    
    **1. Install uv(if not already installed):**
    This project uses [uv](https://github.com/astral-sh/uv) to manage the virtual environment and dependencies. If you don't have uv installed, follow the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

    **2. Start the Application:**
    Run:
    ```bash
    uv run run app.py
    ```
    The app will start and run at http://localhost:8000