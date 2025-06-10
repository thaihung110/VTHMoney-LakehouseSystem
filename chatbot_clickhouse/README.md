# DataMart Chatbot

## Introduction

The DataMart Chatbot is a Streamlit application that allows users to interact with data through natural language questions. The application utilizes libraries such as Langchain and Bokeh to display charts and analyze data.

## Requirements

Before running the application, ensure that you have installed the necessary libraries. You can use `pip` to install the following libraries:

```bash
pip install streamlit langchain langchain-mcp-adapters langgraph mcp python-dotenv matplotlib plotly seaborn altair bokeh
```

## Configuration

1. **Create a `.env` file**: Create a `.env` file in the root directory of the project and add the necessary environment variables: ANTHROPIC_API_KEY=your_api_key_here
2. **Configure ClickHouse connection**: Ensure that you have correctly configured the connection information to ClickHouse in `langchain_cli.py`:

```python
async def run_agent_stream(prompt: str):
    server_params = StdioServerParameters(
        command="uv",
        args=[
            "run",
            "--with",
            "mcp-clickhouse",
            "--python",
            "3.13",
            "mcp-clickhouse",
        ],
        env={
            "CLICKHOUSE_HOST": "<clickhouse-host>",
            "CLICKHOUSE_PORT": "<clickhouse-port>",
            "CLICKHOUSE_USER": "<clickhouse-user>",
            "CLICKHOUSE_PASSWORD": "<clickhouse-password>",
            "CLICKHOUSE_SECURE": "false",
        },
    )
```

## Running the Application

Once you have installed the libraries and configured everything, you can run the application with the following command:

```bash
streamlit run chatbot_clickhouse/chat_ui.py
```

## Usage

1. Open your browser and navigate to `http://localhost:8501`.
2. Enter your question in the input box and click the "Send" button.
3. The application will process the question and display the results in the form of charts.

## Notes

- Ensure that ClickHouse is running and accessible from the application.
- If you encounter errors, please check the environment variables and connection configuration.
