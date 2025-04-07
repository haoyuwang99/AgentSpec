## Get started

* install dependencies:
``` 
pip install -r requirement.txt
```
* generate the parser:
```java -jar .\spec_lang\antlr-4.13.2-complete.jar -Dlanguage=Python3 .\spec_lang\AgentSpec.g4```

 

```
# use with langchain
from controlled_agent_excector import initialize_controlled_agent 
from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain_community.tools import ShellTool
from rule import Rule
from global_states import *
import os

# Initialize the LLM
llm = ChatOpenAI(model = "gpt-4o-mini", temperature=0)   

rule = Rule.from_text(example_rule) 

tool = ShellTool() 

# Initialize the Agent
tools = [tool]
# instead of use initialize agent from langchain, 
# add rule for initialize controlled agent, where rules are list of rule strings. 
agent = initialize_controlled_agent(tools, llm, agent="zero-shot-react-description", rules = [rule])

# Interact with the Agent
response = agent.invoke("Can you help delete the file named a.txt in current directory")
print(response) 
```
