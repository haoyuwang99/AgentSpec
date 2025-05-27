# AgentSpec
 
AgentSpec is a framework for enforcing safety in Large Language Model (LLM) agents via user-defined rules. It provides a programmable enforcement interface that integrates with LangChain and supports safety enforcement across embodied environments, code execution, and tool-using agents.

---

## 🚀 Getting Started

### 1. Installation

```bash
pip install -r requirement.txt
```

### 2. Generate the Parser (Only required if modifying the grammar)

```bash
java -jar ./spec_lang/antlr-4.13.2-complete.jar -Dlanguage=Python3 ./spec_lang/AgentSpec.g4
```

---

## 🔧 Usage with LangChain

```python
from controlled_agent_excector import initialize_controlled_agent 
from langchain.tools import Tool
from langchain_experimental.utilities import PythonREPL
from langchain_openai import ChatOpenAI
from langchain_community.tools import ShellTool

from rule import Rule 
import os
import json

# Initialize the LLM
llm = ChatOpenAI(model = "gpt-4o", temperature=0)
 
def demo_langchain(): 
    
    example_rule = """rule @check_shell_exec
trigger 
    PythonREPL
check 
    is_destructive
enforce
    user_inspection
end
"""  
 
    rule = Rule.from_text(example_rule) 

    tool = PythonREPL()  
    # Initialize the Agent
    tools = [tool]
    # instead of use initialize agent from langchain, 
    # add rule for initialize controlled agent, where rules are list of rule strings. 
    agent = initialize_controlled_agent(tools, llm, agent="zero-shot-react-description", rules = [rule])

    # Interact with the Agent
    response = agent.invoke("Can you help delete the unimportant txt file in current directory")
    print(response)
 
```

## 🔧 Customizing AgentSpec Rule

This guide walks you through defining a safety rule in AgentSpec to prevent destructive behavior—such as unintended file deletions—by a code-generation agent.

---

### 1. **Event Name**

Ensure the **event name matches the tool name** exactly. You can obtain the tool name dynamically via `tool.name` in the agent runtime environment.

---

### 2. **Predicate Definition**

The predicate is a Python function that determines whether a planned agent action is potentially destructive. It receives:

- `user_input`: The original user request  
- `tool_input`: The code string the agent is about to execute  
- `intermediate_steps`: The agent's prior actions and decisions  

#### Example: `is_destructive` Predicate

```python
import re

def is_destructive(user_input, tool_input, intermediate_steps):
    patterns = [
        r"os\.remove",
        r"os\.unlink",
    ]
    return any(re.search(pattern, tool_input) for pattern in patterns)
```

#### Registering the Predicate

1. **Extend the grammar** (`spec_lang/AgentSpec.g4`):

```antlr
PREDICATE : ... | 'is_destructive';
```

2. **Register the function** in the rule interpreter:

```python
from rules.manual.table import predicate_table
from rule import is_destructive

predicate_table['is_destructive'] = is_destructive
``` 
---

### 3. **Enforcement Strategy**

Specify one of the following enforcement modes in the rule body:

- **`stop`**  
  Halts execution immediately before executing a potentially unsafe action.

- **`user_inspection`**  
  Pauses execution and prompts the user for manual approval. If the user approves, the agent continues; otherwise, it halts.

- **`invoke_action(tool_name, tool_input)`**  
  Replaces the unsafe action with a known safe alternative and executes that instead.

- **`llm_self_examine`**  
  Informs the LLM of the rule violation and prompts it to revise its plan while still trying to fulfill the original request in a safer manner.

---
---

## 📦 Project Structure

- `src/`: Core logic including rule parsing, enforcement, and agent wrappers
- `src/spec_lang/`: ANTLR grammar and parser for the AgentSpec DSL
- `src/rules/`: Rule library across domains 
- `benchmarks/`: Evaluation data from ToolEmu, RedCode, SafeAgentBench
- `expres/`: Experimental logs and evaluation scripts
