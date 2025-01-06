// Generated from AgentSpec.g4 by ANTLR 4.13.2
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue", "this-escape"})
public class AgentSpecParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		RULE=1, TRIGGER=2, CHECK=3, ENFORCE=4, ANY=5, TRUE=6, FALSE=7, END=8, 
		COLON=9, COMMA=10, LPAREN=11, RPAREN=12, LBRACE=13, RBRACE=14, DOT=15, 
		LBRACK=16, RBRACK=17, AT=18, EQ=19, NOT=20, TOOLEMU_PREDICATE=21, INVOKE=22, 
		ENFORCEMENT=23, WS=24, IDENTIFIER=25, STRING=26, INTEGER=27, FLOAT=28;
	public static final int
		RULE_program = 0, RULE_rule = 1, RULE_ruleClause = 2, RULE_triggerClause = 3, 
		RULE_checkClause = 4, RULE_enforceClause = 5, RULE_tool = 6, RULE_toolkit = 7, 
		RULE_predicate = 8, RULE_kvPair = 9, RULE_value = 10, RULE_enforcement = 11, 
		RULE_actionInvoke = 12, RULE_number = 13;
	private static String[] makeRuleNames() {
		return new String[] {
			"program", "rule", "ruleClause", "triggerClause", "checkClause", "enforceClause", 
			"tool", "toolkit", "predicate", "kvPair", "value", "enforcement", "actionInvoke", 
			"number"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'rule'", "'trigger'", "'check'", "'enforce'", "'any'", "'true'", 
			"'false'", "'end'", "':'", "','", "'('", "')'", "'{'", "'}'", "'.'", 
			"'['", "']'", "'@'", "'='", "'!'", null, "'invoke_action'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "RULE", "TRIGGER", "CHECK", "ENFORCE", "ANY", "TRUE", "FALSE", 
			"END", "COLON", "COMMA", "LPAREN", "RPAREN", "LBRACE", "RBRACE", "DOT", 
			"LBRACK", "RBRACK", "AT", "EQ", "NOT", "TOOLEMU_PREDICATE", "INVOKE", 
			"ENFORCEMENT", "WS", "IDENTIFIER", "STRING", "INTEGER", "FLOAT"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "AgentSpec.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public AgentSpecParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ProgramContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(AgentSpecParser.EOF, 0); }
		public List<RuleContext> rule_() {
			return getRuleContexts(RuleContext.class);
		}
		public RuleContext rule_(int i) {
			return getRuleContext(RuleContext.class,i);
		}
		public ProgramContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_program; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterProgram(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitProgram(this);
		}
	}

	public final ProgramContext program() throws RecognitionException {
		ProgramContext _localctx = new ProgramContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_program);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(31);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==RULE) {
				{
				{
				setState(28);
				rule_();
				}
				}
				setState(33);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(34);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class RuleContext extends ParserRuleContext {
		public RuleClauseContext ruleClause() {
			return getRuleContext(RuleClauseContext.class,0);
		}
		public TriggerClauseContext triggerClause() {
			return getRuleContext(TriggerClauseContext.class,0);
		}
		public CheckClauseContext checkClause() {
			return getRuleContext(CheckClauseContext.class,0);
		}
		public EnforceClauseContext enforceClause() {
			return getRuleContext(EnforceClauseContext.class,0);
		}
		public TerminalNode END() { return getToken(AgentSpecParser.END, 0); }
		public RuleContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rule; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterRule(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitRule(this);
		}
	}

	public final RuleContext rule_() throws RecognitionException {
		RuleContext _localctx = new RuleContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_rule);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(36);
			ruleClause();
			setState(37);
			triggerClause();
			setState(38);
			checkClause();
			setState(39);
			enforceClause();
			setState(40);
			match(END);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class RuleClauseContext extends ParserRuleContext {
		public TerminalNode RULE() { return getToken(AgentSpecParser.RULE, 0); }
		public TerminalNode AT() { return getToken(AgentSpecParser.AT, 0); }
		public TerminalNode IDENTIFIER() { return getToken(AgentSpecParser.IDENTIFIER, 0); }
		public RuleClauseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ruleClause; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterRuleClause(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitRuleClause(this);
		}
	}

	public final RuleClauseContext ruleClause() throws RecognitionException {
		RuleClauseContext _localctx = new RuleClauseContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_ruleClause);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(42);
			match(RULE);
			setState(43);
			match(AT);
			setState(44);
			match(IDENTIFIER);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class TriggerClauseContext extends ParserRuleContext {
		public TerminalNode TRIGGER() { return getToken(AgentSpecParser.TRIGGER, 0); }
		public ToolkitContext toolkit() {
			return getRuleContext(ToolkitContext.class,0);
		}
		public TerminalNode DOT() { return getToken(AgentSpecParser.DOT, 0); }
		public ToolContext tool() {
			return getRuleContext(ToolContext.class,0);
		}
		public TriggerClauseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_triggerClause; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterTriggerClause(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitTriggerClause(this);
		}
	}

	public final TriggerClauseContext triggerClause() throws RecognitionException {
		TriggerClauseContext _localctx = new TriggerClauseContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_triggerClause);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(46);
			match(TRIGGER);
			setState(47);
			toolkit();
			setState(48);
			match(DOT);
			setState(49);
			tool();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class CheckClauseContext extends ParserRuleContext {
		public TerminalNode CHECK() { return getToken(AgentSpecParser.CHECK, 0); }
		public List<PredicateContext> predicate() {
			return getRuleContexts(PredicateContext.class);
		}
		public PredicateContext predicate(int i) {
			return getRuleContext(PredicateContext.class,i);
		}
		public CheckClauseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_checkClause; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterCheckClause(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitCheckClause(this);
		}
	}

	public final CheckClauseContext checkClause() throws RecognitionException {
		CheckClauseContext _localctx = new CheckClauseContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_checkClause);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(51);
			match(CHECK);
			setState(53); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(52);
				predicate();
				}
				}
				setState(55); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & 36700352L) != 0) );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class EnforceClauseContext extends ParserRuleContext {
		public TerminalNode ENFORCE() { return getToken(AgentSpecParser.ENFORCE, 0); }
		public List<EnforcementContext> enforcement() {
			return getRuleContexts(EnforcementContext.class);
		}
		public EnforcementContext enforcement(int i) {
			return getRuleContext(EnforcementContext.class,i);
		}
		public EnforceClauseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_enforceClause; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterEnforceClause(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitEnforceClause(this);
		}
	}

	public final EnforceClauseContext enforceClause() throws RecognitionException {
		EnforceClauseContext _localctx = new EnforceClauseContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_enforceClause);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(57);
			match(ENFORCE);
			setState(59); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(58);
				enforcement();
				}
				}
				setState(61); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==INVOKE || _la==ENFORCEMENT );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ToolContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(AgentSpecParser.IDENTIFIER, 0); }
		public TerminalNode ANY() { return getToken(AgentSpecParser.ANY, 0); }
		public ToolContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tool; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterTool(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitTool(this);
		}
	}

	public final ToolContext tool() throws RecognitionException {
		ToolContext _localctx = new ToolContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_tool);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(63);
			_la = _input.LA(1);
			if ( !(_la==ANY || _la==IDENTIFIER) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ToolkitContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(AgentSpecParser.IDENTIFIER, 0); }
		public TerminalNode ANY() { return getToken(AgentSpecParser.ANY, 0); }
		public ToolkitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_toolkit; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterToolkit(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitToolkit(this);
		}
	}

	public final ToolkitContext toolkit() throws RecognitionException {
		ToolkitContext _localctx = new ToolkitContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_toolkit);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(65);
			_la = _input.LA(1);
			if ( !(_la==ANY || _la==IDENTIFIER) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PredicateContext extends ParserRuleContext {
		public TerminalNode TRUE() { return getToken(AgentSpecParser.TRUE, 0); }
		public TerminalNode FALSE() { return getToken(AgentSpecParser.FALSE, 0); }
		public TerminalNode NOT() { return getToken(AgentSpecParser.NOT, 0); }
		public PredicateContext predicate() {
			return getRuleContext(PredicateContext.class,0);
		}
		public TerminalNode TOOLEMU_PREDICATE() { return getToken(AgentSpecParser.TOOLEMU_PREDICATE, 0); }
		public TerminalNode IDENTIFIER() { return getToken(AgentSpecParser.IDENTIFIER, 0); }
		public PredicateContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_predicate; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterPredicate(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitPredicate(this);
		}
	}

	public final PredicateContext predicate() throws RecognitionException {
		PredicateContext _localctx = new PredicateContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_predicate);
		try {
			setState(73);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case TRUE:
				enterOuterAlt(_localctx, 1);
				{
				setState(67);
				match(TRUE);
				}
				break;
			case FALSE:
				enterOuterAlt(_localctx, 2);
				{
				setState(68);
				match(FALSE);
				}
				break;
			case NOT:
				enterOuterAlt(_localctx, 3);
				{
				setState(69);
				match(NOT);
				setState(70);
				predicate();
				}
				break;
			case TOOLEMU_PREDICATE:
				enterOuterAlt(_localctx, 4);
				{
				setState(71);
				match(TOOLEMU_PREDICATE);
				}
				break;
			case IDENTIFIER:
				enterOuterAlt(_localctx, 5);
				{
				setState(72);
				match(IDENTIFIER);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class KvPairContext extends ParserRuleContext {
		public TerminalNode STRING() { return getToken(AgentSpecParser.STRING, 0); }
		public TerminalNode COLON() { return getToken(AgentSpecParser.COLON, 0); }
		public ValueContext value() {
			return getRuleContext(ValueContext.class,0);
		}
		public KvPairContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_kvPair; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterKvPair(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitKvPair(this);
		}
	}

	public final KvPairContext kvPair() throws RecognitionException {
		KvPairContext _localctx = new KvPairContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_kvPair);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(75);
			match(STRING);
			setState(76);
			match(COLON);
			setState(77);
			value(0);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ValueContext extends ParserRuleContext {
		public TerminalNode STRING() { return getToken(AgentSpecParser.STRING, 0); }
		public NumberContext number() {
			return getRuleContext(NumberContext.class,0);
		}
		public TerminalNode IDENTIFIER() { return getToken(AgentSpecParser.IDENTIFIER, 0); }
		public ActionInvokeContext actionInvoke() {
			return getRuleContext(ActionInvokeContext.class,0);
		}
		public ValueContext value() {
			return getRuleContext(ValueContext.class,0);
		}
		public TerminalNode LBRACK() { return getToken(AgentSpecParser.LBRACK, 0); }
		public TerminalNode RBRACK() { return getToken(AgentSpecParser.RBRACK, 0); }
		public ValueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_value; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterValue(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitValue(this);
		}
	}

	public final ValueContext value() throws RecognitionException {
		return value(0);
	}

	private ValueContext value(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ValueContext _localctx = new ValueContext(_ctx, _parentState);
		ValueContext _prevctx = _localctx;
		int _startState = 20;
		enterRecursionRule(_localctx, 20, RULE_value, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(84);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case STRING:
				{
				setState(80);
				match(STRING);
				}
				break;
			case INTEGER:
			case FLOAT:
				{
				setState(81);
				number();
				}
				break;
			case IDENTIFIER:
				{
				setState(82);
				match(IDENTIFIER);
				}
				break;
			case INVOKE:
				{
				setState(83);
				actionInvoke();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			_ctx.stop = _input.LT(-1);
			setState(92);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,5,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new ValueContext(_parentctx, _parentState);
					pushNewRecursionContext(_localctx, _startState, RULE_value);
					setState(86);
					if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
					setState(87);
					match(LBRACK);
					setState(88);
					match(STRING);
					setState(89);
					match(RBRACK);
					}
					} 
				}
				setState(94);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,5,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class EnforcementContext extends ParserRuleContext {
		public TerminalNode ENFORCEMENT() { return getToken(AgentSpecParser.ENFORCEMENT, 0); }
		public ActionInvokeContext actionInvoke() {
			return getRuleContext(ActionInvokeContext.class,0);
		}
		public EnforcementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_enforcement; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterEnforcement(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitEnforcement(this);
		}
	}

	public final EnforcementContext enforcement() throws RecognitionException {
		EnforcementContext _localctx = new EnforcementContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_enforcement);
		try {
			setState(97);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ENFORCEMENT:
				enterOuterAlt(_localctx, 1);
				{
				setState(95);
				match(ENFORCEMENT);
				}
				break;
			case INVOKE:
				enterOuterAlt(_localctx, 2);
				{
				setState(96);
				actionInvoke();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ActionInvokeContext extends ParserRuleContext {
		public TerminalNode INVOKE() { return getToken(AgentSpecParser.INVOKE, 0); }
		public TerminalNode LPAREN() { return getToken(AgentSpecParser.LPAREN, 0); }
		public TerminalNode IDENTIFIER() { return getToken(AgentSpecParser.IDENTIFIER, 0); }
		public List<TerminalNode> COMMA() { return getTokens(AgentSpecParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(AgentSpecParser.COMMA, i);
		}
		public TerminalNode LBRACE() { return getToken(AgentSpecParser.LBRACE, 0); }
		public List<KvPairContext> kvPair() {
			return getRuleContexts(KvPairContext.class);
		}
		public KvPairContext kvPair(int i) {
			return getRuleContext(KvPairContext.class,i);
		}
		public TerminalNode RBRACE() { return getToken(AgentSpecParser.RBRACE, 0); }
		public TerminalNode RPAREN() { return getToken(AgentSpecParser.RPAREN, 0); }
		public ActionInvokeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_actionInvoke; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterActionInvoke(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitActionInvoke(this);
		}
	}

	public final ActionInvokeContext actionInvoke() throws RecognitionException {
		ActionInvokeContext _localctx = new ActionInvokeContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_actionInvoke);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(99);
			match(INVOKE);
			setState(100);
			match(LPAREN);
			setState(101);
			match(IDENTIFIER);
			setState(102);
			match(COMMA);
			setState(103);
			match(LBRACE);
			setState(104);
			kvPair();
			setState(109);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(105);
				match(COMMA);
				setState(106);
				kvPair();
				}
				}
				setState(111);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(112);
			match(RBRACE);
			setState(113);
			match(RPAREN);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class NumberContext extends ParserRuleContext {
		public TerminalNode INTEGER() { return getToken(AgentSpecParser.INTEGER, 0); }
		public TerminalNode FLOAT() { return getToken(AgentSpecParser.FLOAT, 0); }
		public NumberContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_number; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterNumber(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitNumber(this);
		}
	}

	public final NumberContext number() throws RecognitionException {
		NumberContext _localctx = new NumberContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_number);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(115);
			_la = _input.LA(1);
			if ( !(_la==INTEGER || _la==FLOAT) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 10:
			return value_sempred((ValueContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean value_sempred(ValueContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 2);
		}
		return true;
	}

	public static final String _serializedATN =
		"\u0004\u0001\u001cv\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b\u0002"+
		"\f\u0007\f\u0002\r\u0007\r\u0001\u0000\u0005\u0000\u001e\b\u0000\n\u0000"+
		"\f\u0000!\t\u0000\u0001\u0000\u0001\u0000\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0002\u0001\u0002\u0001"+
		"\u0002\u0001\u0002\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001"+
		"\u0003\u0001\u0004\u0001\u0004\u0004\u00046\b\u0004\u000b\u0004\f\u0004"+
		"7\u0001\u0005\u0001\u0005\u0004\u0005<\b\u0005\u000b\u0005\f\u0005=\u0001"+
		"\u0006\u0001\u0006\u0001\u0007\u0001\u0007\u0001\b\u0001\b\u0001\b\u0001"+
		"\b\u0001\b\u0001\b\u0003\bJ\b\b\u0001\t\u0001\t\u0001\t\u0001\t\u0001"+
		"\n\u0001\n\u0001\n\u0001\n\u0001\n\u0003\nU\b\n\u0001\n\u0001\n\u0001"+
		"\n\u0001\n\u0005\n[\b\n\n\n\f\n^\t\n\u0001\u000b\u0001\u000b\u0003\u000b"+
		"b\b\u000b\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001"+
		"\f\u0005\fl\b\f\n\f\f\fo\t\f\u0001\f\u0001\f\u0001\f\u0001\r\u0001\r\u0001"+
		"\r\u0000\u0001\u0014\u000e\u0000\u0002\u0004\u0006\b\n\f\u000e\u0010\u0012"+
		"\u0014\u0016\u0018\u001a\u0000\u0002\u0002\u0000\u0005\u0005\u0019\u0019"+
		"\u0001\u0000\u001b\u001ct\u0000\u001f\u0001\u0000\u0000\u0000\u0002$\u0001"+
		"\u0000\u0000\u0000\u0004*\u0001\u0000\u0000\u0000\u0006.\u0001\u0000\u0000"+
		"\u0000\b3\u0001\u0000\u0000\u0000\n9\u0001\u0000\u0000\u0000\f?\u0001"+
		"\u0000\u0000\u0000\u000eA\u0001\u0000\u0000\u0000\u0010I\u0001\u0000\u0000"+
		"\u0000\u0012K\u0001\u0000\u0000\u0000\u0014T\u0001\u0000\u0000\u0000\u0016"+
		"a\u0001\u0000\u0000\u0000\u0018c\u0001\u0000\u0000\u0000\u001as\u0001"+
		"\u0000\u0000\u0000\u001c\u001e\u0003\u0002\u0001\u0000\u001d\u001c\u0001"+
		"\u0000\u0000\u0000\u001e!\u0001\u0000\u0000\u0000\u001f\u001d\u0001\u0000"+
		"\u0000\u0000\u001f \u0001\u0000\u0000\u0000 \"\u0001\u0000\u0000\u0000"+
		"!\u001f\u0001\u0000\u0000\u0000\"#\u0005\u0000\u0000\u0001#\u0001\u0001"+
		"\u0000\u0000\u0000$%\u0003\u0004\u0002\u0000%&\u0003\u0006\u0003\u0000"+
		"&\'\u0003\b\u0004\u0000\'(\u0003\n\u0005\u0000()\u0005\b\u0000\u0000)"+
		"\u0003\u0001\u0000\u0000\u0000*+\u0005\u0001\u0000\u0000+,\u0005\u0012"+
		"\u0000\u0000,-\u0005\u0019\u0000\u0000-\u0005\u0001\u0000\u0000\u0000"+
		"./\u0005\u0002\u0000\u0000/0\u0003\u000e\u0007\u000001\u0005\u000f\u0000"+
		"\u000012\u0003\f\u0006\u00002\u0007\u0001\u0000\u0000\u000035\u0005\u0003"+
		"\u0000\u000046\u0003\u0010\b\u000054\u0001\u0000\u0000\u000067\u0001\u0000"+
		"\u0000\u000075\u0001\u0000\u0000\u000078\u0001\u0000\u0000\u00008\t\u0001"+
		"\u0000\u0000\u00009;\u0005\u0004\u0000\u0000:<\u0003\u0016\u000b\u0000"+
		";:\u0001\u0000\u0000\u0000<=\u0001\u0000\u0000\u0000=;\u0001\u0000\u0000"+
		"\u0000=>\u0001\u0000\u0000\u0000>\u000b\u0001\u0000\u0000\u0000?@\u0007"+
		"\u0000\u0000\u0000@\r\u0001\u0000\u0000\u0000AB\u0007\u0000\u0000\u0000"+
		"B\u000f\u0001\u0000\u0000\u0000CJ\u0005\u0006\u0000\u0000DJ\u0005\u0007"+
		"\u0000\u0000EF\u0005\u0014\u0000\u0000FJ\u0003\u0010\b\u0000GJ\u0005\u0015"+
		"\u0000\u0000HJ\u0005\u0019\u0000\u0000IC\u0001\u0000\u0000\u0000ID\u0001"+
		"\u0000\u0000\u0000IE\u0001\u0000\u0000\u0000IG\u0001\u0000\u0000\u0000"+
		"IH\u0001\u0000\u0000\u0000J\u0011\u0001\u0000\u0000\u0000KL\u0005\u001a"+
		"\u0000\u0000LM\u0005\t\u0000\u0000MN\u0003\u0014\n\u0000N\u0013\u0001"+
		"\u0000\u0000\u0000OP\u0006\n\uffff\uffff\u0000PU\u0005\u001a\u0000\u0000"+
		"QU\u0003\u001a\r\u0000RU\u0005\u0019\u0000\u0000SU\u0003\u0018\f\u0000"+
		"TO\u0001\u0000\u0000\u0000TQ\u0001\u0000\u0000\u0000TR\u0001\u0000\u0000"+
		"\u0000TS\u0001\u0000\u0000\u0000U\\\u0001\u0000\u0000\u0000VW\n\u0002"+
		"\u0000\u0000WX\u0005\u0010\u0000\u0000XY\u0005\u001a\u0000\u0000Y[\u0005"+
		"\u0011\u0000\u0000ZV\u0001\u0000\u0000\u0000[^\u0001\u0000\u0000\u0000"+
		"\\Z\u0001\u0000\u0000\u0000\\]\u0001\u0000\u0000\u0000]\u0015\u0001\u0000"+
		"\u0000\u0000^\\\u0001\u0000\u0000\u0000_b\u0005\u0017\u0000\u0000`b\u0003"+
		"\u0018\f\u0000a_\u0001\u0000\u0000\u0000a`\u0001\u0000\u0000\u0000b\u0017"+
		"\u0001\u0000\u0000\u0000cd\u0005\u0016\u0000\u0000de\u0005\u000b\u0000"+
		"\u0000ef\u0005\u0019\u0000\u0000fg\u0005\n\u0000\u0000gh\u0005\r\u0000"+
		"\u0000hm\u0003\u0012\t\u0000ij\u0005\n\u0000\u0000jl\u0003\u0012\t\u0000"+
		"ki\u0001\u0000\u0000\u0000lo\u0001\u0000\u0000\u0000mk\u0001\u0000\u0000"+
		"\u0000mn\u0001\u0000\u0000\u0000np\u0001\u0000\u0000\u0000om\u0001\u0000"+
		"\u0000\u0000pq\u0005\u000e\u0000\u0000qr\u0005\f\u0000\u0000r\u0019\u0001"+
		"\u0000\u0000\u0000st\u0007\u0001\u0000\u0000t\u001b\u0001\u0000\u0000"+
		"\u0000\b\u001f7=IT\\am";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}