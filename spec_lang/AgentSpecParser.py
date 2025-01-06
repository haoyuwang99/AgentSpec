# Generated from spec_lang/AgentSpec.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,28,117,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        1,0,5,0,30,8,0,10,0,12,0,33,9,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,
        1,2,1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,4,1,4,4,4,54,8,4,11,4,12,4,
        55,1,5,1,5,4,5,60,8,5,11,5,12,5,61,1,6,1,6,1,7,1,7,1,8,1,8,1,8,1,
        8,1,8,3,8,73,8,8,1,9,1,9,1,9,1,9,1,10,1,10,1,10,1,10,1,10,3,10,84,
        8,10,1,10,1,10,1,10,1,10,5,10,90,8,10,10,10,12,10,93,9,10,1,11,1,
        11,3,11,97,8,11,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,5,12,107,
        8,12,10,12,12,12,110,9,12,1,12,1,12,1,12,1,13,1,13,1,13,0,1,20,14,
        0,2,4,6,8,10,12,14,16,18,20,22,24,26,0,2,2,0,5,5,25,25,1,0,27,28,
        114,0,31,1,0,0,0,2,36,1,0,0,0,4,42,1,0,0,0,6,46,1,0,0,0,8,51,1,0,
        0,0,10,57,1,0,0,0,12,63,1,0,0,0,14,65,1,0,0,0,16,72,1,0,0,0,18,74,
        1,0,0,0,20,83,1,0,0,0,22,96,1,0,0,0,24,98,1,0,0,0,26,114,1,0,0,0,
        28,30,3,2,1,0,29,28,1,0,0,0,30,33,1,0,0,0,31,29,1,0,0,0,31,32,1,
        0,0,0,32,34,1,0,0,0,33,31,1,0,0,0,34,35,5,0,0,1,35,1,1,0,0,0,36,
        37,3,4,2,0,37,38,3,6,3,0,38,39,3,8,4,0,39,40,3,10,5,0,40,41,5,8,
        0,0,41,3,1,0,0,0,42,43,5,1,0,0,43,44,5,18,0,0,44,45,5,25,0,0,45,
        5,1,0,0,0,46,47,5,2,0,0,47,48,3,14,7,0,48,49,5,15,0,0,49,50,3,12,
        6,0,50,7,1,0,0,0,51,53,5,3,0,0,52,54,3,16,8,0,53,52,1,0,0,0,54,55,
        1,0,0,0,55,53,1,0,0,0,55,56,1,0,0,0,56,9,1,0,0,0,57,59,5,4,0,0,58,
        60,3,22,11,0,59,58,1,0,0,0,60,61,1,0,0,0,61,59,1,0,0,0,61,62,1,0,
        0,0,62,11,1,0,0,0,63,64,7,0,0,0,64,13,1,0,0,0,65,66,7,0,0,0,66,15,
        1,0,0,0,67,73,5,6,0,0,68,73,5,7,0,0,69,70,5,20,0,0,70,73,3,16,8,
        0,71,73,5,21,0,0,72,67,1,0,0,0,72,68,1,0,0,0,72,69,1,0,0,0,72,71,
        1,0,0,0,73,17,1,0,0,0,74,75,5,26,0,0,75,76,5,9,0,0,76,77,3,20,10,
        0,77,19,1,0,0,0,78,79,6,10,-1,0,79,84,5,26,0,0,80,84,3,26,13,0,81,
        84,5,25,0,0,82,84,3,24,12,0,83,78,1,0,0,0,83,80,1,0,0,0,83,81,1,
        0,0,0,83,82,1,0,0,0,84,91,1,0,0,0,85,86,10,2,0,0,86,87,5,16,0,0,
        87,88,5,26,0,0,88,90,5,17,0,0,89,85,1,0,0,0,90,93,1,0,0,0,91,89,
        1,0,0,0,91,92,1,0,0,0,92,21,1,0,0,0,93,91,1,0,0,0,94,97,5,23,0,0,
        95,97,3,24,12,0,96,94,1,0,0,0,96,95,1,0,0,0,97,23,1,0,0,0,98,99,
        5,22,0,0,99,100,5,11,0,0,100,101,5,25,0,0,101,102,5,10,0,0,102,103,
        5,13,0,0,103,108,3,18,9,0,104,105,5,10,0,0,105,107,3,18,9,0,106,
        104,1,0,0,0,107,110,1,0,0,0,108,106,1,0,0,0,108,109,1,0,0,0,109,
        111,1,0,0,0,110,108,1,0,0,0,111,112,5,14,0,0,112,113,5,12,0,0,113,
        25,1,0,0,0,114,115,7,1,0,0,115,27,1,0,0,0,8,31,55,61,72,83,91,96,
        108
    ]

class AgentSpecParser ( Parser ):

    grammarFileName = "AgentSpec.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'rule'", "'trigger'", "'check'", "'enforce'", 
                     "'any'", "'true'", "'false'", "'end'", "':'", "','", 
                     "'('", "')'", "'{'", "'}'", "'.'", "'['", "']'", "'@'", 
                     "'='", "'!'", "'is_destructive'", "'invoke_action'" ]

    symbolicNames = [ "<INVALID>", "RULE", "TRIGGER", "CHECK", "ENFORCE", 
                      "ANY", "TRUE", "FALSE", "END", "COLON", "COMMA", "LPAREN", 
                      "RPAREN", "LBRACE", "RBRACE", "DOT", "LBRACK", "RBRACK", 
                      "AT", "EQ", "NOT", "PREDICATE", "INVOKE", "ENFORCEMENT", 
                      "WS", "IDENTIFIER", "STRING", "INTEGER", "FLOAT" ]

    RULE_program = 0
    RULE_rule = 1
    RULE_ruleClause = 2
    RULE_triggerClause = 3
    RULE_checkClause = 4
    RULE_enforceClause = 5
    RULE_tool = 6
    RULE_toolkit = 7
    RULE_predicate = 8
    RULE_kvPair = 9
    RULE_value = 10
    RULE_enforcement = 11
    RULE_actionInvoke = 12
    RULE_number = 13

    ruleNames =  [ "program", "rule", "ruleClause", "triggerClause", "checkClause", 
                   "enforceClause", "tool", "toolkit", "predicate", "kvPair", 
                   "value", "enforcement", "actionInvoke", "number" ]

    EOF = Token.EOF
    RULE=1
    TRIGGER=2
    CHECK=3
    ENFORCE=4
    ANY=5
    TRUE=6
    FALSE=7
    END=8
    COLON=9
    COMMA=10
    LPAREN=11
    RPAREN=12
    LBRACE=13
    RBRACE=14
    DOT=15
    LBRACK=16
    RBRACK=17
    AT=18
    EQ=19
    NOT=20
    PREDICATE=21
    INVOKE=22
    ENFORCEMENT=23
    WS=24
    IDENTIFIER=25
    STRING=26
    INTEGER=27
    FLOAT=28

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(AgentSpecParser.EOF, 0)

        def rule_(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AgentSpecParser.RuleContext)
            else:
                return self.getTypedRuleContext(AgentSpecParser.RuleContext,i)


        def getRuleIndex(self):
            return AgentSpecParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = AgentSpecParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 28
                self.rule_()
                self.state = 33
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 34
            self.match(AgentSpecParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ruleClause(self):
            return self.getTypedRuleContext(AgentSpecParser.RuleClauseContext,0)


        def triggerClause(self):
            return self.getTypedRuleContext(AgentSpecParser.TriggerClauseContext,0)


        def checkClause(self):
            return self.getTypedRuleContext(AgentSpecParser.CheckClauseContext,0)


        def enforceClause(self):
            return self.getTypedRuleContext(AgentSpecParser.EnforceClauseContext,0)


        def END(self):
            return self.getToken(AgentSpecParser.END, 0)

        def getRuleIndex(self):
            return AgentSpecParser.RULE_rule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRule" ):
                listener.enterRule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRule" ):
                listener.exitRule(self)




    def rule_(self):

        localctx = AgentSpecParser.RuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_rule)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.ruleClause()
            self.state = 37
            self.triggerClause()
            self.state = 38
            self.checkClause()
            self.state = 39
            self.enforceClause()
            self.state = 40
            self.match(AgentSpecParser.END)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RuleClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RULE(self):
            return self.getToken(AgentSpecParser.RULE, 0)

        def AT(self):
            return self.getToken(AgentSpecParser.AT, 0)

        def IDENTIFIER(self):
            return self.getToken(AgentSpecParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return AgentSpecParser.RULE_ruleClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRuleClause" ):
                listener.enterRuleClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRuleClause" ):
                listener.exitRuleClause(self)




    def ruleClause(self):

        localctx = AgentSpecParser.RuleClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_ruleClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self.match(AgentSpecParser.RULE)
            self.state = 43
            self.match(AgentSpecParser.AT)
            self.state = 44
            self.match(AgentSpecParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TriggerClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRIGGER(self):
            return self.getToken(AgentSpecParser.TRIGGER, 0)

        def toolkit(self):
            return self.getTypedRuleContext(AgentSpecParser.ToolkitContext,0)


        def DOT(self):
            return self.getToken(AgentSpecParser.DOT, 0)

        def tool(self):
            return self.getTypedRuleContext(AgentSpecParser.ToolContext,0)


        def getRuleIndex(self):
            return AgentSpecParser.RULE_triggerClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTriggerClause" ):
                listener.enterTriggerClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTriggerClause" ):
                listener.exitTriggerClause(self)




    def triggerClause(self):

        localctx = AgentSpecParser.TriggerClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_triggerClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            self.match(AgentSpecParser.TRIGGER)
            self.state = 47
            self.toolkit()
            self.state = 48
            self.match(AgentSpecParser.DOT)
            self.state = 49
            self.tool()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CheckClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CHECK(self):
            return self.getToken(AgentSpecParser.CHECK, 0)

        def predicate(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AgentSpecParser.PredicateContext)
            else:
                return self.getTypedRuleContext(AgentSpecParser.PredicateContext,i)


        def getRuleIndex(self):
            return AgentSpecParser.RULE_checkClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCheckClause" ):
                listener.enterCheckClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCheckClause" ):
                listener.exitCheckClause(self)




    def checkClause(self):

        localctx = AgentSpecParser.CheckClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_checkClause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            self.match(AgentSpecParser.CHECK)
            self.state = 53 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 52
                self.predicate()
                self.state = 55 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 3145920) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnforceClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ENFORCE(self):
            return self.getToken(AgentSpecParser.ENFORCE, 0)

        def enforcement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AgentSpecParser.EnforcementContext)
            else:
                return self.getTypedRuleContext(AgentSpecParser.EnforcementContext,i)


        def getRuleIndex(self):
            return AgentSpecParser.RULE_enforceClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnforceClause" ):
                listener.enterEnforceClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnforceClause" ):
                listener.exitEnforceClause(self)




    def enforceClause(self):

        localctx = AgentSpecParser.EnforceClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_enforceClause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self.match(AgentSpecParser.ENFORCE)
            self.state = 59 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 58
                self.enforcement()
                self.state = 61 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==22 or _la==23):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ToolContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(AgentSpecParser.IDENTIFIER, 0)

        def ANY(self):
            return self.getToken(AgentSpecParser.ANY, 0)

        def getRuleIndex(self):
            return AgentSpecParser.RULE_tool

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTool" ):
                listener.enterTool(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTool" ):
                listener.exitTool(self)




    def tool(self):

        localctx = AgentSpecParser.ToolContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_tool)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            _la = self._input.LA(1)
            if not(_la==5 or _la==25):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ToolkitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(AgentSpecParser.IDENTIFIER, 0)

        def ANY(self):
            return self.getToken(AgentSpecParser.ANY, 0)

        def getRuleIndex(self):
            return AgentSpecParser.RULE_toolkit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterToolkit" ):
                listener.enterToolkit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitToolkit" ):
                listener.exitToolkit(self)




    def toolkit(self):

        localctx = AgentSpecParser.ToolkitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_toolkit)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            _la = self._input.LA(1)
            if not(_la==5 or _la==25):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PredicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRUE(self):
            return self.getToken(AgentSpecParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(AgentSpecParser.FALSE, 0)

        def NOT(self):
            return self.getToken(AgentSpecParser.NOT, 0)

        def predicate(self):
            return self.getTypedRuleContext(AgentSpecParser.PredicateContext,0)


        def PREDICATE(self):
            return self.getToken(AgentSpecParser.PREDICATE, 0)

        def getRuleIndex(self):
            return AgentSpecParser.RULE_predicate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPredicate" ):
                listener.enterPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPredicate" ):
                listener.exitPredicate(self)




    def predicate(self):

        localctx = AgentSpecParser.PredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_predicate)
        try:
            self.state = 72
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [6]:
                self.enterOuterAlt(localctx, 1)
                self.state = 67
                self.match(AgentSpecParser.TRUE)
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 68
                self.match(AgentSpecParser.FALSE)
                pass
            elif token in [20]:
                self.enterOuterAlt(localctx, 3)
                self.state = 69
                self.match(AgentSpecParser.NOT)
                self.state = 70
                self.predicate()
                pass
            elif token in [21]:
                self.enterOuterAlt(localctx, 4)
                self.state = 71
                self.match(AgentSpecParser.PREDICATE)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KvPairContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(AgentSpecParser.STRING, 0)

        def COLON(self):
            return self.getToken(AgentSpecParser.COLON, 0)

        def value(self):
            return self.getTypedRuleContext(AgentSpecParser.ValueContext,0)


        def getRuleIndex(self):
            return AgentSpecParser.RULE_kvPair

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKvPair" ):
                listener.enterKvPair(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKvPair" ):
                listener.exitKvPair(self)




    def kvPair(self):

        localctx = AgentSpecParser.KvPairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_kvPair)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74
            self.match(AgentSpecParser.STRING)
            self.state = 75
            self.match(AgentSpecParser.COLON)
            self.state = 76
            self.value(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(AgentSpecParser.STRING, 0)

        def number(self):
            return self.getTypedRuleContext(AgentSpecParser.NumberContext,0)


        def IDENTIFIER(self):
            return self.getToken(AgentSpecParser.IDENTIFIER, 0)

        def actionInvoke(self):
            return self.getTypedRuleContext(AgentSpecParser.ActionInvokeContext,0)


        def value(self):
            return self.getTypedRuleContext(AgentSpecParser.ValueContext,0)


        def LBRACK(self):
            return self.getToken(AgentSpecParser.LBRACK, 0)

        def RBRACK(self):
            return self.getToken(AgentSpecParser.RBRACK, 0)

        def getRuleIndex(self):
            return AgentSpecParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)



    def value(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = AgentSpecParser.ValueContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 20
        self.enterRecursionRule(localctx, 20, self.RULE_value, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [26]:
                self.state = 79
                self.match(AgentSpecParser.STRING)
                pass
            elif token in [27, 28]:
                self.state = 80
                self.number()
                pass
            elif token in [25]:
                self.state = 81
                self.match(AgentSpecParser.IDENTIFIER)
                pass
            elif token in [22]:
                self.state = 82
                self.actionInvoke()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 91
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = AgentSpecParser.ValueContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_value)
                    self.state = 85
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 86
                    self.match(AgentSpecParser.LBRACK)
                    self.state = 87
                    self.match(AgentSpecParser.STRING)
                    self.state = 88
                    self.match(AgentSpecParser.RBRACK) 
                self.state = 93
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class EnforcementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ENFORCEMENT(self):
            return self.getToken(AgentSpecParser.ENFORCEMENT, 0)

        def actionInvoke(self):
            return self.getTypedRuleContext(AgentSpecParser.ActionInvokeContext,0)


        def getRuleIndex(self):
            return AgentSpecParser.RULE_enforcement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnforcement" ):
                listener.enterEnforcement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnforcement" ):
                listener.exitEnforcement(self)




    def enforcement(self):

        localctx = AgentSpecParser.EnforcementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_enforcement)
        try:
            self.state = 96
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                self.enterOuterAlt(localctx, 1)
                self.state = 94
                self.match(AgentSpecParser.ENFORCEMENT)
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 2)
                self.state = 95
                self.actionInvoke()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ActionInvokeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INVOKE(self):
            return self.getToken(AgentSpecParser.INVOKE, 0)

        def LPAREN(self):
            return self.getToken(AgentSpecParser.LPAREN, 0)

        def IDENTIFIER(self):
            return self.getToken(AgentSpecParser.IDENTIFIER, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(AgentSpecParser.COMMA)
            else:
                return self.getToken(AgentSpecParser.COMMA, i)

        def LBRACE(self):
            return self.getToken(AgentSpecParser.LBRACE, 0)

        def kvPair(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AgentSpecParser.KvPairContext)
            else:
                return self.getTypedRuleContext(AgentSpecParser.KvPairContext,i)


        def RBRACE(self):
            return self.getToken(AgentSpecParser.RBRACE, 0)

        def RPAREN(self):
            return self.getToken(AgentSpecParser.RPAREN, 0)

        def getRuleIndex(self):
            return AgentSpecParser.RULE_actionInvoke

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterActionInvoke" ):
                listener.enterActionInvoke(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitActionInvoke" ):
                listener.exitActionInvoke(self)




    def actionInvoke(self):

        localctx = AgentSpecParser.ActionInvokeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_actionInvoke)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 98
            self.match(AgentSpecParser.INVOKE)
            self.state = 99
            self.match(AgentSpecParser.LPAREN)
            self.state = 100
            self.match(AgentSpecParser.IDENTIFIER)
            self.state = 101
            self.match(AgentSpecParser.COMMA)
            self.state = 102
            self.match(AgentSpecParser.LBRACE)
            self.state = 103
            self.kvPair()
            self.state = 108
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==10:
                self.state = 104
                self.match(AgentSpecParser.COMMA)
                self.state = 105
                self.kvPair()
                self.state = 110
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 111
            self.match(AgentSpecParser.RBRACE)
            self.state = 112
            self.match(AgentSpecParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER(self):
            return self.getToken(AgentSpecParser.INTEGER, 0)

        def FLOAT(self):
            return self.getToken(AgentSpecParser.FLOAT, 0)

        def getRuleIndex(self):
            return AgentSpecParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)




    def number(self):

        localctx = AgentSpecParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 114
            _la = self._input.LA(1)
            if not(_la==27 or _la==28):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[10] = self.value_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def value_sempred(self, localctx:ValueContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         




