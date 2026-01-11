# Generated from spec_lang/AgentSpec.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .AgentSpecParser import AgentSpecParser
else:
    from AgentSpecParser import AgentSpecParser

# This class defines a complete listener for a parse tree produced by AgentSpecParser.
class AgentSpecListener(ParseTreeListener):

    # Enter a parse tree produced by AgentSpecParser#program.
    def enterProgram(self, ctx:AgentSpecParser.ProgramContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#program.
    def exitProgram(self, ctx:AgentSpecParser.ProgramContext):
        pass


    # Enter a parse tree produced by AgentSpecParser#rule.
    def enterRule(self, ctx:AgentSpecParser.RuleContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#rule.
    def exitRule(self, ctx:AgentSpecParser.RuleContext):
        pass


    # Enter a parse tree produced by AgentSpecParser#ruleClause.
    def enterRuleClause(self, ctx:AgentSpecParser.RuleClauseContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#ruleClause.
    def exitRuleClause(self, ctx:AgentSpecParser.RuleClauseContext):
        pass


    # Enter a parse tree produced by AgentSpecParser#triggerClause.
    def enterTriggerClause(self, ctx:AgentSpecParser.TriggerClauseContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#triggerClause.
    def exitTriggerClause(self, ctx:AgentSpecParser.TriggerClauseContext):
        pass


    # Enter a parse tree produced by AgentSpecParser#checkClause.
    def enterCheckClause(self, ctx:AgentSpecParser.CheckClauseContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#checkClause.
    def exitCheckClause(self, ctx:AgentSpecParser.CheckClauseContext):
        pass


    # Enter a parse tree produced by AgentSpecParser#enforceClause.
    def enterEnforceClause(self, ctx:AgentSpecParser.EnforceClauseContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#enforceClause.
    def exitEnforceClause(self, ctx:AgentSpecParser.EnforceClauseContext):
        pass


    # Enter a parse tree produced by AgentSpecParser#event.
    def enterEvent(self, ctx:AgentSpecParser.EventContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#event.
    def exitEvent(self, ctx:AgentSpecParser.EventContext):
        pass


    # Enter a parse tree produced by AgentSpecParser#kvPair.
    def enterKvPair(self, ctx:AgentSpecParser.KvPairContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#kvPair.
    def exitKvPair(self, ctx:AgentSpecParser.KvPairContext):
        pass


    # Enter a parse tree produced by AgentSpecParser#value.
    def enterValue(self, ctx:AgentSpecParser.ValueContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#value.
    def exitValue(self, ctx:AgentSpecParser.ValueContext):
        pass


    # Enter a parse tree produced by AgentSpecParser#enforcement.
    def enterEnforcement(self, ctx:AgentSpecParser.EnforcementContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#enforcement.
    def exitEnforcement(self, ctx:AgentSpecParser.EnforcementContext):
        pass


    # Enter a parse tree produced by AgentSpecParser#actionInvoke.
    def enterActionInvoke(self, ctx:AgentSpecParser.ActionInvokeContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#actionInvoke.
    def exitActionInvoke(self, ctx:AgentSpecParser.ActionInvokeContext):
        pass


    # Enter a parse tree produced by AgentSpecParser#number.
    def enterNumber(self, ctx:AgentSpecParser.NumberContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#number.
    def exitNumber(self, ctx:AgentSpecParser.NumberContext):
        pass


    # Enter a parse tree produced by AgentSpecParser#predicate.
    def enterPredicate(self, ctx:AgentSpecParser.PredicateContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#predicate.
    def exitPredicate(self, ctx:AgentSpecParser.PredicateContext):
        pass


    # Enter a parse tree produced by AgentSpecParser#predicate_func.
    def enterPredicate_func(self, ctx:AgentSpecParser.Predicate_funcContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#predicate_func.
    def exitPredicate_func(self, ctx:AgentSpecParser.Predicate_funcContext):
        pass


    # Enter a parse tree produced by AgentSpecParser#namespace.
    def enterNamespace(self, ctx:AgentSpecParser.NamespaceContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#namespace.
    def exitNamespace(self, ctx:AgentSpecParser.NamespaceContext):
        pass


    # Enter a parse tree produced by AgentSpecParser#config.
    def enterConfig(self, ctx:AgentSpecParser.ConfigContext):
        pass

    # Exit a parse tree produced by AgentSpecParser#config.
    def exitConfig(self, ctx:AgentSpecParser.ConfigContext):
        pass



del AgentSpecParser