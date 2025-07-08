import os
import asyncio
from contextlib import asynccontextmanager
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model
from IPython.display import Image, display

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

async def make_graph():
    mcp_client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["src/mcp/math_server.py"],
                "transport": "stdio",
            }
        }
    )

    mcp_tools = await mcp_client.get_tools()
    print(f"Available tools: {[tool.name for tool in mcp_tools]}")
    
    llm = init_chat_model(
        model = "gpt-4o-mini",
        model_provider="openai",
        temperature=0,
        max_tokens = 50
    )

    llm_with_tool = llm.bind_tools(mcp_tools)

    def call_model(state: State):
        messages = state["messages"]
        response = llm_with_tool.invoke(messages)
        return {"messages": [response]}

    graph_builder = StateGraph(State)
    graph_builder.add_node(call_model)
    graph_builder.add_node("tool", ToolNode(mcp_tools))
    graph_builder.add_edge(START, "call_model")
    graph_builder.add_conditional_edges(
        "call_model",
        tools_condition,
        {
            "tools": "tool",
            END: END,
        },
    )
    graph_builder.add_edge("tool", "call_model")
    graph = graph_builder.compile()
    graph.name = "Tool Agent"
    return graph

async def chat():
    graph = await make_graph()
    messages = []
    print("Type 'exit' to end the chat.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        messages.append(HumanMessage(content=user_input))
        result = await graph.ainvoke({"messages": messages})
        # Get the latest AI message
        ai_msg = result["messages"][-1]
        print("AI:", ai_msg.content)
        messages.append(ai_msg)

if __name__ == "__main__":
    asyncio.run(chat())