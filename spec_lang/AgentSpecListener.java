// Generated from AgentSpec.g4 by ANTLR 4.13.2
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link AgentSpecParser}.
 */
public interface AgentSpecListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link AgentSpecParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(AgentSpecParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link AgentSpecParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(AgentSpecParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by {@link AgentSpecParser#rule}.
	 * @param ctx the parse tree
	 */
	void enterRule(AgentSpecParser.RuleContext ctx);
	/**
	 * Exit a parse tree produced by {@link AgentSpecParser#rule}.
	 * @param ctx the parse tree
	 */
	void exitRule(AgentSpecParser.RuleContext ctx);
	/**
	 * Enter a parse tree produced by {@link AgentSpecParser#ruleClause}.
	 * @param ctx the parse tree
	 */
	void enterRuleClause(AgentSpecParser.RuleClauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link AgentSpecParser#ruleClause}.
	 * @param ctx the parse tree
	 */
	void exitRuleClause(AgentSpecParser.RuleClauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link AgentSpecParser#triggerClause}.
	 * @param ctx the parse tree
	 */
	void enterTriggerClause(AgentSpecParser.TriggerClauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link AgentSpecParser#triggerClause}.
	 * @param ctx the parse tree
	 */
	void exitTriggerClause(AgentSpecParser.TriggerClauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link AgentSpecParser#prepareClause}.
	 * @param ctx the parse tree
	 */
	void enterPrepareClause(AgentSpecParser.PrepareClauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link AgentSpecParser#prepareClause}.
	 * @param ctx the parse tree
	 */
	void exitPrepareClause(AgentSpecParser.PrepareClauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link AgentSpecParser#checkClause}.
	 * @param ctx the parse tree
	 */
	void enterCheckClause(AgentSpecParser.CheckClauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link AgentSpecParser#checkClause}.
	 * @param ctx the parse tree
	 */
	void exitCheckClause(AgentSpecParser.CheckClauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link AgentSpecParser#enforceClause}.
	 * @param ctx the parse tree
	 */
	void enterEnforceClause(AgentSpecParser.EnforceClauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link AgentSpecParser#enforceClause}.
	 * @param ctx the parse tree
	 */
	void exitEnforceClause(AgentSpecParser.EnforceClauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link AgentSpecParser#event}.
	 * @param ctx the parse tree
	 */
	void enterEvent(AgentSpecParser.EventContext ctx);
	/**
	 * Exit a parse tree produced by {@link AgentSpecParser#event}.
	 * @param ctx the parse tree
	 */
	void exitEvent(AgentSpecParser.EventContext ctx);
	/**
	 * Enter a parse tree produced by {@link AgentSpecParser#prepare}.
	 * @param ctx the parse tree
	 */
	void enterPrepare(AgentSpecParser.PrepareContext ctx);
	/**
	 * Exit a parse tree produced by {@link AgentSpecParser#prepare}.
	 * @param ctx the parse tree
	 */
	void exitPrepare(AgentSpecParser.PrepareContext ctx);
	/**
	 * Enter a parse tree produced by {@link AgentSpecParser#predicate}.
	 * @param ctx the parse tree
	 */
	void enterPredicate(AgentSpecParser.PredicateContext ctx);
	/**
	 * Exit a parse tree produced by {@link AgentSpecParser#predicate}.
	 * @param ctx the parse tree
	 */
	void exitPredicate(AgentSpecParser.PredicateContext ctx);
	/**
	 * Enter a parse tree produced by {@link AgentSpecParser#kvPair}.
	 * @param ctx the parse tree
	 */
	void enterKvPair(AgentSpecParser.KvPairContext ctx);
	/**
	 * Exit a parse tree produced by {@link AgentSpecParser#kvPair}.
	 * @param ctx the parse tree
	 */
	void exitKvPair(AgentSpecParser.KvPairContext ctx);
	/**
	 * Enter a parse tree produced by {@link AgentSpecParser#value}.
	 * @param ctx the parse tree
	 */
	void enterValue(AgentSpecParser.ValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link AgentSpecParser#value}.
	 * @param ctx the parse tree
	 */
	void exitValue(AgentSpecParser.ValueContext ctx);
	/**
	 * Enter a parse tree produced by {@link AgentSpecParser#enforcement}.
	 * @param ctx the parse tree
	 */
	void enterEnforcement(AgentSpecParser.EnforcementContext ctx);
	/**
	 * Exit a parse tree produced by {@link AgentSpecParser#enforcement}.
	 * @param ctx the parse tree
	 */
	void exitEnforcement(AgentSpecParser.EnforcementContext ctx);
	/**
	 * Enter a parse tree produced by {@link AgentSpecParser#actionInvoke}.
	 * @param ctx the parse tree
	 */
	void enterActionInvoke(AgentSpecParser.ActionInvokeContext ctx);
	/**
	 * Exit a parse tree produced by {@link AgentSpecParser#actionInvoke}.
	 * @param ctx the parse tree
	 */
	void exitActionInvoke(AgentSpecParser.ActionInvokeContext ctx);
	/**
	 * Enter a parse tree produced by {@link AgentSpecParser#number}.
	 * @param ctx the parse tree
	 */
	void enterNumber(AgentSpecParser.NumberContext ctx);
	/**
	 * Exit a parse tree produced by {@link AgentSpecParser#number}.
	 * @param ctx the parse tree
	 */
	void exitNumber(AgentSpecParser.NumberContext ctx);
}