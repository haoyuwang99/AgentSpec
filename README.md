The grammar file is at AgentSpec.g4, to generate/update the parser: 
```java -jar .\spec_lang\antlr-4.13.2-complete.jar -Dlanguage=Python3 \AgentSpec.g4```

To test the grammar, run test_agent_spec.py. the test files are under test dir.

Use case see `agent_demo.py`