# this file is used to generate grammar/rules/predicates implementation from json file.
import os
import json 


G4_PATH = "spec_lang/AgentSpec.g4"
G4_TEMPLATE = """
grammar AgentSpec;

// Lexer Rules
RULE: 'rule';
TRIGGER: 'trigger'; 
CHECK: 'check';
ENFORCE: 'enforce';  
ANY: 'any'; 
TRUE: 'true';
FALSE: 'false'; 
END: 'end';
COLON: ':'; 
COMMA: ',';
LPAREN: '(';
RPAREN: ')';
LBRACE: '{{';
RBRACE: '}}';
DOT: '.';
LBRACK: '[';
RBRACK: ']';
AT: '@';
EQ: '=';
NOT: '!';
{predicates}
INVOKE: 'invoke_action';
ENFORCEMENT: 'user_inspection' | 'llm_self_reflect' | 'stop' | 'none' | 'skip'; //todo: customized enforcements
WS: [ \\t\\r\\n]+ -> skip; // Ignore whitespace
IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*; // Identifier rule
STRING: '"' .*? '"'; // String literal
INTEGER: [0-9]+;                         // Whole numbers
FLOAT: [0-9]+ '.' [0-9]* | '.' [0-9]+;   // Decimal numbers

// Parser Rules
program: rule* EOF; 

rule: ruleClause
      triggerClause 
      checkClause
      enforceClause
      END;

ruleClause: RULE AT IDENTIFIER;

triggerClause: TRIGGER toolkit DOT tool;
 
checkClause: CHECK predicate+;

enforceClause: ENFORCE enforcement+; 

tool: IDENTIFIER | ANY;

toolkit: IDENTIFIER | ANY;

predicate: TRUE | FALSE | NOT predicate | {key}; 

kvPair: STRING COLON value;

value: STRING | number | IDENTIFIER | value LBRACK STRING RBRACK | actionInvoke;

enforcement: ENFORCEMENT | actionInvoke;

actionInvoke: INVOKE LPAREN IDENTIFIER COMMA LBRACE kvPair (COMMA kvPair)* RBRACE RPAREN;
  
number: INTEGER | FLOAT;

"""

key = "PREDICATE"
def gen_grammar():
    import rules.predicate_table as pt
    predicates = set()
    for tool in pt.predicate_table:
        print(f"tool: {tool}")
        for pred in pt.predicate_table[tool]:
            predicates.add(f"'{pred}'")
    predicates_str = ' | '.join(predicates)
    predicates_str = f"{key}: {predicates_str};"
    with open(G4_PATH, "w") as f:
        f.write(G4_TEMPLATE.format(key = key,predicates=predicates_str))

gen_grammar()
#######
# Below is the code to generate the grammar and rules from json file for toolemu
#######
# def gen_grammar():
    # generate tool_emu grammar
    # with open(RULE_SOURCE, 'r') as f: 
    #     predicates = set()
    #     for l in f.readlines():
    #         obj = json.loads(l)
    #         for rule in obj["rules"]: 
    #             for pred in rule["predicate_python_impl"]:
    #                 predicates.add(f"'{pred}'")
    #     predicates_str = ' | '.join(predicates)
    #     predicates_str = f"TOOLEMU_PREDICATE: {predicates_str};"
    #     grammar = G4_TEMPLATE.format(predicates=predicates_str)
    #     with open(G4_PATH, "w") as f:
    #         f.write(grammar)


# gen_grammar()

from rule import Rule

TOOLKIT_SOURCE = "ToolEmu/assets/all_toolkits.json"
RULE_DIR = "rules/"
RULE_SOURCE = "ToolEmu/assets/rules.jsonl"
PREDICATE_MAPPING = RULE_DIR + "predicate_table.py"
UTIL = "util"
UTIL_PY = RULE_DIR +UTIL + ".py"
LLM_JUDGE = "llm_judge"
LLM_JUDGE_IMPL = f"""from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
 

def {LLM_JUDGE}(requirements, action, ctx) -> True:
    # Initialize LangChain's LLM with your preferred model (e.g., OpenAI GPT-4)
    llm = ChatOpenAI(temperature=0.0, model_name="gpt-4")
    
    # Constructing the context messages
    messages = [
        SystemMessage(content="You are an assistant evaluating task importance for risk management."),
        HumanMessage(content=f"Context of previous actions: {{ctx.intermediate_steps}}\\n"),
        HumanMessage(content=f"Action being evaluated: {{action}}\\nNote: the output should ONLY be 'true' or 'false', indicating the requiement is satisfied"),
        HumanMessage(content=requirements)
    ]
    
    # Query the LLM and parse the response
    response = llm.invoke(messages) 
    return response.content.strip().lower() == "true"
"""

def gen_rules():
    with open(UTIL_PY, 'w') as f:
        
        f.write(LLM_JUDGE_IMPL)
    with open(RULE_SOURCE, 'r') as f:
        for l in f.readlines():
            obj = json.loads(l)
            toolkit_name = obj["toolkits"]
            pred_impl_py = f"""
import re
import datetime
from typing import Dict
from . import {UTIL}

"""
            rule_ar  = ""
            for rule in obj["rules"]:
                tool = Rule.from_text(rule["rule"]).tool
                predicates = set()
                rule_ar = rule_ar + rule["rule"] + "\n"
                for pred in rule["predicate_python_impl"]:
                    if pred in predicates:
                        continue
                    predicates.add(pred)
                    pred_impl_py = pred_impl_py + rule["predicate_python_impl"][pred] + "\n"
            PREDICATE_PY = RULE_DIR + f"{toolkit_name.lower()}_predicates.py"
            RULE_AR = RULE_DIR + f"{toolkit_name.lower()}.ar" 
            with open(PREDICATE_PY, "w") as f:
                f.write(pred_impl_py.replace(LLM_JUDGE, f"{UTIL}.{LLM_JUDGE}"))
            with open(RULE_AR, "w") as f:
                f.write(rule_ar.replace("trigger ", f"trigger {toolkit_name}."))
    # pass

def gen_predicate_table():
    py_text = ""
    with open(TOOLKIT_SOURCE, 'r')  as f:
        TOOL2TOOLKIT = "tool_2_toolkit"
        toolkits = json.loads(f.read())
        py_text = py_text + f"{TOOL2TOOLKIT} = {{}}\n"
        for toolkit in toolkits:
            name = toolkit["toolkit"]
            for tool in toolkit["tools"]:            
                tool_name = tool["name"]
                # py_text = py_text + f"{TOOL2TOOLKIT}[\"{tool_name}\"] = \"{name}\"\n"
            
    with open(RULE_SOURCE, 'r')  as f: 
        TOOLKIT_TABLE = "toolkit_table"
        py_text = py_text + f"\n{TOOLKIT_TABLE} = {{}}\n"
        for l in f.readlines():
            obj = json.loads(l)
            name = obj["toolkits"]
            py_text = f"from . import {name.lower()}_predicates\n" + py_text
            py_text = py_text + f"{name.lower()}_predicate_dict = {{}}\n"
        
            for rule in obj["rules"]: 
                predicates = set()
                for pred in rule["predicate_python_impl"]: 
                    if pred in predicates:
                        continue
                    predicates.add(pred)
                    
                    py_text = py_text + f"{name.lower()}_predicate_dict[\"{pred}\"] = {name.lower()}_predicates.{pred}\n"
           
            py_text = py_text + f"{TOOLKIT_TABLE}[\"{name}\"] = {name.lower()}_predicate_dict\n" 
        
        py_text = "# this is auto-generated python file, see predicate_gen.py\n" + py_text
        # write to table.py
        with open(PREDICATE_MAPPING, 'w') as f:
            f.write(py_text)



# gen_rules()
# gen_predicate_table()


    