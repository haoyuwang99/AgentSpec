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
from langchain.chat_models import ChatOpenAI
from langchain_community.tools import ShellTool
from rule import Rule

llm = ChatOpenAI(model = "gpt-4o-mini", temperature=0)   
rule = Rule.from_text(example_rule)
tool = ShellTool()
tools = [tool]

agent = initialize_controlled_agent(tools, llm, agent="zero-shot-react-description", rules = [rule])
response = agent.invoke("Can you help delete the file named a.txt in current directory?")
```

---

## 📦 Project Structure

- `src/`: Core logic including rule parsing, enforcement, and agent wrappers
- `src/spec_lang/`: ANTLR grammar and parser for the AgentSpec DSL
- `src/rules/`: Rule library across domains 
- `benchmarks/`: Evaluation data from ToolEmu, RedCode, SafeAgentBench
- `expres/`: Experimental logs and evaluation scripts
