grammar AgentSpec;

// Lexer Rules
RULE: 'rule';
TRIGGER: 'trigger';
PREPARE: 'prepare';
CHECK: 'check';
ENFORCE: 'enforce';  
ACTION: 'act';
ANY: 'any'; 
VAL: 'val';
TRUE: 'true';
FALSE: 'false'; 
END: 'end';
EVAL_OP: 'gt' | 'lt' | 'eq' | 'geq' | 'leq' | 'llm_judge' | 'tool_emu_judge'; // todo: customized evaluator
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
NOT: '!';
INVOKE: 'invoke_action';
ENFORCEMENT: 'user_inspection' | 'llm_self_reflect' | 'none'; //todo: customized enforcements
WS: [ \t\r\n]+ -> skip; // Ignore whitespace
IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*; // Identifier rule
STRING: '"' .*? '"'; // String literal
INTEGER: [0-9]+;                         // Whole numbers
FLOAT: [0-9]+ '.' [0-9]* | '.' [0-9]+;   // Decimal numbers

// Parser Rules
program: rule* EOF; 

rule: RULE AT IDENTIFIER
      triggerClause
      prepareClause?
      checkClause
      enforceClause
      END;

triggerClause: TRIGGER event;

prepareClause: PREPARE prepare+;

checkClause: CHECK condition+;

enforceClause: ENFORCE enforcement+; 

event: ACTION IDENTIFIER | ANY;

prepare: VAL IDENTIFIER EQ value;

condition: EVAL_OP LPAREN value (COMMA value)* RPAREN | TRUE | FALSE | NOT condition; 

kvPair: STRING COLON value;

value: STRING | number | IDENTIFIER | value LBRACK STRING RBRACK | actionInvoke;

enforcement: ENFORCEMENT | actionInvoke;

actionInvoke: INVOKE LPAREN IDENTIFIER COMMA LBRACE kvPair (COMMA kvPair)* RBRACE RPAREN;
  
number: INTEGER | FLOAT;
