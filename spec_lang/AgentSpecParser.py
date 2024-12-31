# Generated from AgentSpec.g4 by ANTLR 4.13.2
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
        4,1,27,111,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,1,0,5,0,
        28,8,0,10,0,12,0,31,9,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,
        1,2,1,2,1,3,1,3,1,3,1,4,1,4,4,4,50,8,4,11,4,12,4,51,1,5,1,5,4,5,
        56,8,5,11,5,12,5,57,1,6,1,6,1,7,1,7,1,7,1,7,1,7,3,7,67,8,7,1,8,1,
        8,1,8,1,8,1,9,1,9,1,9,1,9,1,9,3,9,78,8,9,1,9,1,9,1,9,1,9,5,9,84,
        8,9,10,9,12,9,87,9,9,1,10,1,10,3,10,91,8,10,1,11,1,11,1,11,1,11,
        1,11,1,11,1,11,1,11,5,11,101,8,11,10,11,12,11,104,9,11,1,11,1,11,
        1,11,1,12,1,12,1,12,0,1,18,13,0,2,4,6,8,10,12,14,16,18,20,22,24,
        0,2,2,0,5,5,24,24,1,0,26,27,109,0,29,1,0,0,0,2,34,1,0,0,0,4,40,1,
        0,0,0,6,44,1,0,0,0,8,47,1,0,0,0,10,53,1,0,0,0,12,59,1,0,0,0,14,66,
        1,0,0,0,16,68,1,0,0,0,18,77,1,0,0,0,20,90,1,0,0,0,22,92,1,0,0,0,
        24,108,1,0,0,0,26,28,3,2,1,0,27,26,1,0,0,0,28,31,1,0,0,0,29,27,1,
        0,0,0,29,30,1,0,0,0,30,32,1,0,0,0,31,29,1,0,0,0,32,33,5,0,0,1,33,
        1,1,0,0,0,34,35,3,4,2,0,35,36,3,6,3,0,36,37,3,8,4,0,37,38,3,10,5,
        0,38,39,5,8,0,0,39,3,1,0,0,0,40,41,5,1,0,0,41,42,5,17,0,0,42,43,
        5,24,0,0,43,5,1,0,0,0,44,45,5,2,0,0,45,46,3,12,6,0,46,7,1,0,0,0,
        47,49,5,3,0,0,48,50,3,14,7,0,49,48,1,0,0,0,50,51,1,0,0,0,51,49,1,
        0,0,0,51,52,1,0,0,0,52,9,1,0,0,0,53,55,5,4,0,0,54,56,3,20,10,0,55,
        54,1,0,0,0,56,57,1,0,0,0,57,55,1,0,0,0,57,58,1,0,0,0,58,11,1,0,0,
        0,59,60,7,0,0,0,60,13,1,0,0,0,61,67,5,6,0,0,62,67,5,7,0,0,63,64,
        5,19,0,0,64,67,3,14,7,0,65,67,5,20,0,0,66,61,1,0,0,0,66,62,1,0,0,
        0,66,63,1,0,0,0,66,65,1,0,0,0,67,15,1,0,0,0,68,69,5,25,0,0,69,70,
        5,9,0,0,70,71,3,18,9,0,71,17,1,0,0,0,72,73,6,9,-1,0,73,78,5,25,0,
        0,74,78,3,24,12,0,75,78,5,24,0,0,76,78,3,22,11,0,77,72,1,0,0,0,77,
        74,1,0,0,0,77,75,1,0,0,0,77,76,1,0,0,0,78,85,1,0,0,0,79,80,10,2,
        0,0,80,81,5,15,0,0,81,82,5,25,0,0,82,84,5,16,0,0,83,79,1,0,0,0,84,
        87,1,0,0,0,85,83,1,0,0,0,85,86,1,0,0,0,86,19,1,0,0,0,87,85,1,0,0,
        0,88,91,5,22,0,0,89,91,3,22,11,0,90,88,1,0,0,0,90,89,1,0,0,0,91,
        21,1,0,0,0,92,93,5,21,0,0,93,94,5,11,0,0,94,95,5,24,0,0,95,96,5,
        10,0,0,96,97,5,13,0,0,97,102,3,16,8,0,98,99,5,10,0,0,99,101,3,16,
        8,0,100,98,1,0,0,0,101,104,1,0,0,0,102,100,1,0,0,0,102,103,1,0,0,
        0,103,105,1,0,0,0,104,102,1,0,0,0,105,106,5,14,0,0,106,107,5,12,
        0,0,107,23,1,0,0,0,108,109,7,1,0,0,109,25,1,0,0,0,8,29,51,57,66,
        77,85,90,102
    ]

class AgentSpecParser ( Parser ):

    grammarFileName = "AgentSpec.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'rule'", "'trigger'", "'check'", "'enforce'", 
                     "'any'", "'true'", "'false'", "'end'", "':'", "','", 
                     "'('", "')'", "'{'", "'}'", "'['", "']'", "'@'", "'='", 
                     "'!'", "<INVALID>", "'invoke_action'" ]

    symbolicNames = [ "<INVALID>", "RULE", "TRIGGER", "CHECK", "ENFORCE", 
                      "ANY", "TRUE", "FALSE", "END", "COLON", "COMMA", "LPAREN", 
                      "RPAREN", "LBRACE", "RBRACE", "LBRACK", "RBRACK", 
                      "AT", "EQ", "NOT", "TOOLEMU_PREDICATE", "INVOKE", 
                      "ENFORCEMENT", "WS", "IDENTIFIER", "STRING", "INTEGER", 
                      "FLOAT" ]

    RULE_program = 0
    RULE_rule = 1
    RULE_ruleClause = 2
    RULE_triggerClause = 3
    RULE_checkClause = 4
    RULE_enforceClause = 5
    RULE_event = 6
    RULE_predicate = 7
    RULE_kvPair = 8
    RULE_value = 9
    RULE_enforcement = 10
    RULE_actionInvoke = 11
    RULE_number = 12

    ruleNames =  [ "program", "rule", "ruleClause", "triggerClause", "checkClause", 
                   "enforceClause", "event", "predicate", "kvPair", "value", 
                   "enforcement", "actionInvoke", "number" ]

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
    LBRACK=15
    RBRACK=16
    AT=17
    EQ=18
    NOT=19
    TOOLEMU_PREDICATE=20
    INVOKE=21
    ENFORCEMENT=22
    WS=23
    IDENTIFIER=24
    STRING=25
    INTEGER=26
    FLOAT=27

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
            self.state = 29
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 26
                self.rule_()
                self.state = 31
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 32
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
            self.state = 34
            self.ruleClause()
            self.state = 35
            self.triggerClause()
            self.state = 36
            self.checkClause()
            self.state = 37
            self.enforceClause()
            self.state = 38
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
            self.state = 40
            self.match(AgentSpecParser.RULE)
            self.state = 41
            self.match(AgentSpecParser.AT)
            self.state = 42
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

        def event(self):
            return self.getTypedRuleContext(AgentSpecParser.EventContext,0)


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
            self.state = 44
            self.match(AgentSpecParser.TRIGGER)
            self.state = 45
            self.event()
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
            self.state = 47
            self.match(AgentSpecParser.CHECK)
            self.state = 49 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 48
                self.predicate()
                self.state = 51 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 1573056) != 0)):
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
            self.state = 53
            self.match(AgentSpecParser.ENFORCE)
            self.state = 55 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 54
                self.enforcement()
                self.state = 57 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==21 or _la==22):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EventContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(AgentSpecParser.IDENTIFIER, 0)

        def ANY(self):
            return self.getToken(AgentSpecParser.ANY, 0)

        def getRuleIndex(self):
            return AgentSpecParser.RULE_event

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEvent" ):
                listener.enterEvent(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEvent" ):
                listener.exitEvent(self)




    def event(self):

        localctx = AgentSpecParser.EventContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_event)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            _la = self._input.LA(1)
            if not(_la==5 or _la==24):
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


        def TOOLEMU_PREDICATE(self):
            return self.getToken(AgentSpecParser.TOOLEMU_PREDICATE, 0)

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
        self.enterRule(localctx, 14, self.RULE_predicate)
        try:
            self.state = 66
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [6]:
                self.enterOuterAlt(localctx, 1)
                self.state = 61
                self.match(AgentSpecParser.TRUE)
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 62
                self.match(AgentSpecParser.FALSE)
                pass
            elif token in [19]:
                self.enterOuterAlt(localctx, 3)
                self.state = 63
                self.match(AgentSpecParser.NOT)
                self.state = 64
                self.predicate()
                pass
            elif token in [20]:
                self.enterOuterAlt(localctx, 4)
                self.state = 65
                self.match(AgentSpecParser.TOOLEMU_PREDICATE)
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
        self.enterRule(localctx, 16, self.RULE_kvPair)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 68
            self.match(AgentSpecParser.STRING)
            self.state = 69
            self.match(AgentSpecParser.COLON)
            self.state = 70
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
        _startState = 18
        self.enterRecursionRule(localctx, 18, self.RULE_value, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 77
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [25]:
                self.state = 73
                self.match(AgentSpecParser.STRING)
                pass
            elif token in [26, 27]:
                self.state = 74
                self.number()
                pass
            elif token in [24]:
                self.state = 75
                self.match(AgentSpecParser.IDENTIFIER)
                pass
            elif token in [21]:
                self.state = 76
                self.actionInvoke()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 85
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = AgentSpecParser.ValueContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_value)
                    self.state = 79
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 80
                    self.match(AgentSpecParser.LBRACK)
                    self.state = 81
                    self.match(AgentSpecParser.STRING)
                    self.state = 82
                    self.match(AgentSpecParser.RBRACK) 
                self.state = 87
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
        self.enterRule(localctx, 20, self.RULE_enforcement)
        try:
            self.state = 90
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [22]:
                self.enterOuterAlt(localctx, 1)
                self.state = 88
                self.match(AgentSpecParser.ENFORCEMENT)
                pass
            elif token in [21]:
                self.enterOuterAlt(localctx, 2)
                self.state = 89
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
        self.enterRule(localctx, 22, self.RULE_actionInvoke)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 92
            self.match(AgentSpecParser.INVOKE)
            self.state = 93
            self.match(AgentSpecParser.LPAREN)
            self.state = 94
            self.match(AgentSpecParser.IDENTIFIER)
            self.state = 95
            self.match(AgentSpecParser.COMMA)
            self.state = 96
            self.match(AgentSpecParser.LBRACE)
            self.state = 97
            self.kvPair()
            self.state = 102
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==10:
                self.state = 98
                self.match(AgentSpecParser.COMMA)
                self.state = 99
                self.kvPair()
                self.state = 104
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 105
            self.match(AgentSpecParser.RBRACE)
            self.state = 106
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
        self.enterRule(localctx, 24, self.RULE_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 108
            _la = self._input.LA(1)
            if not(_la==26 or _la==27):
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
        self._predicates[9] = self.value_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def value_sempred(self, localctx:ValueContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         




