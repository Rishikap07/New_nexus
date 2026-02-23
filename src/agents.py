import operator
from typing import Annotated,List,TypedDict
from langchain_core.messages import BaseMessage,SystemMessage,HumanMessage,AIMessage
from langchain.graph import StateGraph,END
from langchain_ollama import ChatOllama

class AgentState(TypedDict):
    messages:Annotated[List[BaseMessage], operator.add]

    researcher_data:List[str]
    chart_data:List[dict]

def researcher_node(state:AgentState):
    print('\n---(Agent:Researcher) is gatthering deta')
    