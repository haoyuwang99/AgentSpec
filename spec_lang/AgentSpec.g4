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
CMD_PREDICATE: 'is_git' | 'has_critical_redirection' | 'is_destructive' | 'is_within_length_limit' ;
GIT_PREDICATE: 'is_on_dedicated_branch' | 'is_commit' | 'is_push' | 'is_minimal_change_commit' | 'is_up_to_date' | 'is_commit_msg_readable' | 'has_untracked_files';
INVOKE: 'invoke_action';
ENFORCEMENT: 'user_inspection' | 'llm_self_reflect' | 'stop' | 'none'; //todo: customized enforcements
WS: [ \t\r\n]+ -> skip; // Ignore whitespace
IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*; // Identifier rule
STRING: '"' .*? '"'; // String literal
INTEGER: [0-9]+;                         // Whole numbers
FLOAT: [0-9]+ '.' [0-9]* | '.' [0-9]+;   // Decimal numbers

// Parser Rules
program: rule* EOF; 

rule: ruleClause
      triggerClause
      prepareClause?
      checkClause
      enforceClause
      END;

ruleClause: RULE AT IDENTIFIER;

triggerClause: TRIGGER event;

prepareClause: PREPARE prepare+;

checkClause: CHECK predicate+;

enforceClause: ENFORCE enforcement+; 

event: ACTION IDENTIFIER | ANY;

prepare: VAL IDENTIFIER EQ value;

predicate: EVAL_OP LPAREN value (COMMA value)* RPAREN | TRUE | FALSE | NOT predicate | CMD_PREDICATE | GIT_PREDICATE; 

kvPair: STRING COLON value;

value: STRING | number | IDENTIFIER | value LBRACK STRING RBRACK | actionInvoke;

enforcement: ENFORCEMENT | actionInvoke;

actionInvoke: INVOKE LPAREN IDENTIFIER COMMA LBRACE kvPair (COMMA kvPair)* RBRACE RPAREN;
  
number: INTEGER | FLOAT;
