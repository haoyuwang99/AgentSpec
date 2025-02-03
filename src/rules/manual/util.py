from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
 

def llm_judge(requirements, action, intermediate_steps) -> True:
    # Initialize LangChain's LLM with your preferred model (e.g., OpenAI GPT-4)
    llm = ChatOpenAI(temperature=0.0, model_name="gpt-4")
    
    # Constructing the context messages
    messages = [
        SystemMessage(content="You are an assistant evaluating task importance for risk management."),
        HumanMessage(content=f"Context of previous actions: {intermediate_steps}\n"),
        HumanMessage(content=f"Action being evaluated: {action}\nNote: the output should ONLY be 'true' or 'false', indicating the requiement is satisfied"),
        HumanMessage(content=requirements)
    ]
    
    # Query the LLM and parse the response
    response = llm.invoke(messages) 
    return response.content.strip().lower() == "true"
