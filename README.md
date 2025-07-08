# AI_Agents

Creating an AI agent using Langchain and Langraph.

## Project Directory Structure

```
AI_Agents/
│   README.md
│   requirements.txt
│
├── src/
│   ├── ai_agent_langraph.ipynb
│   ├── langraph_w_mcp.py
│   ├── mcp/
│   │   └── math_server.py
│   └── ...
│
└── ...
```



## Setup Instructions

### 1. Create a Python virtual environment

On Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

### 2. Install required packages from a requirements file

```sh
pip install -r requirements.txt
```

---

## Summary of files in `src/`

- **ai_agent_langraph.ipynb**: Jupyter notebook for experimenting with AI agents using LangGraph and Langchain.
- **langraph_w_mcp.py**: Script integrating LangGraph with the MCP protocol for tool usage.

    Run from the command line:
    ```sh
    python src/langraph_w_mcp.py
    ```

- **mcp/math_server.py**: MCP server providing math functions (e.g., remainder).






