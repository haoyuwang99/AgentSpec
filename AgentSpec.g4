grammar AgentSpec;

// Lexer Rules
RULE: 'rule';
TRIGGER: 'trigger';
QUERY: 'query';
CHECK: 'check';
ENFORCE: 'enforce';  
ACTION: 'act';
ANY: 'any'; 
VAL: 'val';
TRUE: 'true';
FALSE: 'false'; 
END: 'end';
EVAL_OP: 'gt' | 'lt' | 'eq' | 'geq' | 'leq' | 'llm_judge'; // todo: customized evaluator
COLON: ':'; 
COMMA: ',';
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACK: '[';
RBRACK: ']';
AT: '@';
EQ: '=';
INVOKE: 'invoke_action';
ENFORCEMENT: 'user_inspection' | 'llm_self_reflect'; //todo: customized enforcements
WS: [ \t\r\n]+ -> skip; // Ignore whitespace
IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*; // Identifier rule
STRING: '"' .*? '"'; // String literal
INTEGER: [0-9]+;                         // Whole numbers
FLOAT: [0-9]+ '.' [0-9]* | '.' [0-9]+;   // Decimal numbers

// Parser Rules
program: rule* EOF; 

rule: RULE AT IDENTIFIER
      triggerClause
      queryClause?
      checkClause
      enforceClause
      END;

triggerClause: TRIGGER event;

queryClause: QUERY query+;

checkClause: CHECK condition+;

enforceClause: ENFORCE enforcement+; 

event: ACTION IDENTIFIER | ANY;

query: VAL IDENTIFIER EQ LBRACE kvPair (COMMA kvPair)* RBRACE;

condition: EVAL_OP LPAREN value COMMA value RPAREN; 

kvPair: IDENTIFIER COLON value;

value: STRING | number | IDENTIFIER | value LBRACK value RBRACK | actionInvoke;

enforcement: ENFORCEMENT | actionInvoke;

actionInvoke: INVOKE LPAREN IDENTIFIER COMMA LBRACE kvPair (COMMA kvPair)* RBRACE RPAREN;
  
number: INTEGER | FLOAT;
