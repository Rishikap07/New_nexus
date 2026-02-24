import operator
from typing import Annotated,List,TypedDict
from langchain_core.messages import BaseMessage,SystemMessage,HumanMessage,AIMessage
from langchain.graph import StateGraph,END
from langchain_ollama import ChatOllama
   
class AgentState(TypedDict):
    messages:Annotated[List[BaseMessage], operator.add]

    researcher_data:List[str]
    chart_data:List[dict]

from tools import get_llm_with_tools
llm,llm_with_tools=get_llm_with_tools()


def researcher_node(state:AgentState):
    last_message=state["messages"][-1]
    sys_msg=SystemMessage(content="Your are a data gatherer,user tools")
    response=llm_with_tools.invoke([sys_msg,last_message])
    if hasattr(response,"tool_calls") and response.tool_calls:
        for tool_call in response.tools:
            tool_names=tool_call["name"]
            tool_args=tool_calls["agrs"]
            q=str(tool_args.get("query",""))
        if tool_name=="lookup_policy_docs":
            res=lookup_policy_docs.invoke(q)
        elif tool_name=="web_search_stub":
            res=web_search_stub.invoke(q)
        elif tool_name=="rss_feed_stub":
            res=rss_feed_stub.invoke(q)
        researcher_findings.append(f"Source:{tool_name}\nData:{res}")
    return{"messages":[researcher],"researcher_data":researcher_findings}
def analyst_node(state:AgentState):
    raw_data="\n\n".join(state["research_data"])
    prompt=f"you are a senior analyst.extract trends and numeric data\n{raw_data}"

    response=llm.invoke(prompt)
    return {"messages":[response],"chart_data":[]}

workflow=StateGraph(AgentState)
workflow.add_node("Researcher", researcher_node)
workflow.set_entry_point("Researcher")
workflow.add_edge("Researcher",END)
workflow.compile()