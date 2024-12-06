import unittest
import os
from antlr4 import *
from AgentSpecLexer import AgentSpecLexer
from AgentSpecParser import AgentSpecParser
from antlr4.error.ErrorListener import ErrorListener

class CustomErrorListener(ErrorListener):
    def __init__(self):
        super(CustomErrorListener, self).__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error_message = f"Syntax error at line {line}, column {column}: {msg}"
        self.errors.append(error_message)

    def clear(self):
        self.errors = []
        
    def has_parse_error(self):
        return len(self.errors)>0

def test_grammar(program):
    # Expected parse tree (this should match your grammar's expectations) 

    # Create a lexer and parser
    input_stream = InputStream(program)
    lexer = AgentSpecLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = AgentSpecParser(token_stream)

    error_listener = CustomErrorListener()
    parser.removeErrorListeners()  # Remove default ConsoleErrorListener
    parser.addErrorListener(error_listener)

    # Parse the input using the top-level rule (e.g., `program`)
    error_listener.clear()
    tree = parser.program()
    # Print the parse tree
    print(tree.toStringTree(recog=parser))

    # Verify the parse tree contains expected elements
    return error_listener.has_parse_error()

class TestAgentSpecParser(unittest.TestCase):

    def test_grammar_examples(self):
        base = 'rule_examples/'
        for f in os.listdir(base):
            with open(base + f,'r') as r:
                rule = r.read()
                self.assertFalse(test_grammar(rule))

if __name__ == "__main__":
    unittest.main()

# def main():
#     # Get input for testing
#     input_text = """
#     rule @inspect_dangerous_command_before_execution
#     trigger 
#         act TerminalExecute  
#     check 
#         llm_judge(cur_action["command"], "Return true if it is risky command, [description of risky command]")
#     enforce 
#         user_inspection
#     end
#     """

#     # Create a lexer and parser
#     input_stream = InputStream(input_text)
#     lexer = AgentSpecLexer(input_stream)
#     token_stream = CommonTokenStream(lexer)
#     parser = AgentSpecParser(token_stream)

#     # Parse the input using the top-level rule (e.g., program)
#     tree = parser.program()

#     # Print the parse tree
#     print(tree.toStringTree(recog=parser))

# if __name__ == "__main__":
#     main()