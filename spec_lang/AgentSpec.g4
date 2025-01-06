
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
LBRACE: '{';
RBRACE: '}';
DOT: '.';
LBRACK: '[';
RBRACK: ']';
AT: '@';
EQ: '=';
NOT: '!';
PREDICATE: 'is_destructive';
INVOKE: 'invoke_action';
ENFORCEMENT: 'user_inspection' | 'llm_self_reflect' | 'stop' | 'none' | 'skip'; //todo: customized enforcements
WS: [ \t\r\n]+ -> skip; // Ignore whitespace
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

predicate: TRUE | FALSE | NOT predicate | PREDICATE; 

kvPair: STRING COLON value;

value: STRING | number | IDENTIFIER | value LBRACK STRING RBRACK | actionInvoke;

enforcement: ENFORCEMENT | actionInvoke;

actionInvoke: INVOKE LPAREN IDENTIFIER COMMA LBRACE kvPair (COMMA kvPair)* RBRACE RPAREN;
  
number: INTEGER | FLOAT;

