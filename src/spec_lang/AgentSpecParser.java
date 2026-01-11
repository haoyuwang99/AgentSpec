// Generated from spec_lang/AgentSpec.g4 by ANTLR 4.13.2
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
		LBRACK=16, RBRACK=17, AT=18, EQ=19, NOT=20, PREDICATE=21, INVOKE=22, ENFORCEMENT=23, 
		WS=24, IDENTIFIER=25, STRING=26, INTEGER=27, FLOAT=28, STATE_CHANGE=29, 
		BEFORE_ACTION=30, AFTER_ACTION=31, FINISH=32;
	public static final int
		RULE_program = 0, RULE_rule = 1, RULE_ruleClause = 2, RULE_triggerClause = 3, 
		RULE_checkClause = 4, RULE_enforceClause = 5, RULE_event = 6, RULE_kvPair = 7, 
		RULE_value = 8, RULE_enforcement = 9, RULE_actionInvoke = 10, RULE_number = 11, 
		RULE_predicate = 12, RULE_predicate_func = 13, RULE_namespace = 14, RULE_config = 15;
	private static String[] makeRuleNames() {
		return new String[] {
			"program", "rule", "ruleClause", "triggerClause", "checkClause", "enforceClause", 
			"event", "kvPair", "value", "enforcement", "actionInvoke", "number", 
			"predicate", "predicate_func", "namespace", "config"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'rule'", "'trigger'", "'check'", "'enforce'", "'any'", "'true'", 
			"'false'", "'end'", "':'", "','", "'('", "')'", "'{'", "'}'", "'.'", 
			"'['", "']'", "'@'", "'='", "'!'", null, "'invoke_action'", null, null, 
			null, null, null, null, "'state_change'", "'before_action'", "'after_action'", 
			"'finish'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "RULE", "TRIGGER", "CHECK", "ENFORCE", "ANY", "TRUE", "FALSE", 
			"END", "COLON", "COMMA", "LPAREN", "RPAREN", "LBRACE", "RBRACE", "DOT", 
			"LBRACK", "RBRACK", "AT", "EQ", "NOT", "PREDICATE", "INVOKE", "ENFORCEMENT", 
			"WS", "IDENTIFIER", "STRING", "INTEGER", "FLOAT", "STATE_CHANGE", "BEFORE_ACTION", 
			"AFTER_ACTION", "FINISH"
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
			setState(35);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==RULE) {
				{
				{
				setState(32);
				rule_();
				}
				}
				setState(37);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(38);
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
			setState(40);
			ruleClause();
			setState(41);
			triggerClause();
			setState(42);
			checkClause();
			setState(43);
			enforceClause();
			setState(44);
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
			setState(46);
			match(RULE);
			setState(47);
			match(AT);
			setState(48);
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
		public EventContext event() {
			return getRuleContext(EventContext.class,0);
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
			setState(50);
			match(TRIGGER);
			setState(51);
			event();
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
			setState(53);
			match(CHECK);
			setState(55); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(54);
				predicate();
				}
				}
				setState(57); 
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
			setState(59);
			match(ENFORCE);
			setState(61); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(60);
				enforcement();
				}
				}
				setState(63); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & 46137344L) != 0) );
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
	public static class EventContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(AgentSpecParser.IDENTIFIER, 0); }
		public TerminalNode STATE_CHANGE() { return getToken(AgentSpecParser.STATE_CHANGE, 0); }
		public TerminalNode BEFORE_ACTION() { return getToken(AgentSpecParser.BEFORE_ACTION, 0); }
		public TerminalNode AFTER_ACTION() { return getToken(AgentSpecParser.AFTER_ACTION, 0); }
		public TerminalNode FINISH() { return getToken(AgentSpecParser.FINISH, 0); }
		public EventContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_event; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterEvent(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitEvent(this);
		}
	}

	public final EventContext event() throws RecognitionException {
		EventContext _localctx = new EventContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_event);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(65);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 8086618112L) != 0)) ) {
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
		enterRule(_localctx, 14, RULE_kvPair);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(67);
			match(STRING);
			setState(68);
			match(COLON);
			setState(69);
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
		int _startState = 16;
		enterRecursionRule(_localctx, 16, RULE_value, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(76);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case STRING:
				{
				setState(72);
				match(STRING);
				}
				break;
			case INTEGER:
			case FLOAT:
				{
				setState(73);
				number();
				}
				break;
			case IDENTIFIER:
				{
				setState(74);
				match(IDENTIFIER);
				}
				break;
			case INVOKE:
				{
				setState(75);
				actionInvoke();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			_ctx.stop = _input.LT(-1);
			setState(84);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,4,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new ValueContext(_parentctx, _parentState);
					pushNewRecursionContext(_localctx, _startState, RULE_value);
					setState(78);
					if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
					setState(79);
					match(LBRACK);
					setState(80);
					match(STRING);
					setState(81);
					match(RBRACK);
					}
					} 
				}
				setState(86);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,4,_ctx);
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
		public ConfigContext config() {
			return getRuleContext(ConfigContext.class,0);
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
		enterRule(_localctx, 18, RULE_enforcement);
		try {
			setState(90);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ENFORCEMENT:
				enterOuterAlt(_localctx, 1);
				{
				setState(87);
				match(ENFORCEMENT);
				}
				break;
			case INVOKE:
				enterOuterAlt(_localctx, 2);
				{
				setState(88);
				actionInvoke();
				}
				break;
			case IDENTIFIER:
				enterOuterAlt(_localctx, 3);
				{
				setState(89);
				config();
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
		enterRule(_localctx, 20, RULE_actionInvoke);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(92);
			match(INVOKE);
			setState(93);
			match(LPAREN);
			setState(94);
			match(IDENTIFIER);
			setState(95);
			match(COMMA);
			setState(96);
			match(LBRACE);
			setState(97);
			kvPair();
			setState(102);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(98);
				match(COMMA);
				setState(99);
				kvPair();
				}
				}
				setState(104);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(105);
			match(RBRACE);
			setState(106);
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
		enterRule(_localctx, 22, RULE_number);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(108);
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

	@SuppressWarnings("CheckReturnValue")
	public static class PredicateContext extends ParserRuleContext {
		public TerminalNode TRUE() { return getToken(AgentSpecParser.TRUE, 0); }
		public TerminalNode FALSE() { return getToken(AgentSpecParser.FALSE, 0); }
		public TerminalNode NOT() { return getToken(AgentSpecParser.NOT, 0); }
		public PredicateContext predicate() {
			return getRuleContext(PredicateContext.class,0);
		}
		public TerminalNode PREDICATE() { return getToken(AgentSpecParser.PREDICATE, 0); }
		public Predicate_funcContext predicate_func() {
			return getRuleContext(Predicate_funcContext.class,0);
		}
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
		enterRule(_localctx, 24, RULE_predicate);
		try {
			setState(116);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case TRUE:
				enterOuterAlt(_localctx, 1);
				{
				setState(110);
				match(TRUE);
				}
				break;
			case FALSE:
				enterOuterAlt(_localctx, 2);
				{
				setState(111);
				match(FALSE);
				}
				break;
			case NOT:
				enterOuterAlt(_localctx, 3);
				{
				setState(112);
				match(NOT);
				setState(113);
				predicate();
				}
				break;
			case PREDICATE:
				enterOuterAlt(_localctx, 4);
				{
				setState(114);
				match(PREDICATE);
				}
				break;
			case IDENTIFIER:
				enterOuterAlt(_localctx, 5);
				{
				setState(115);
				predicate_func();
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
	public static class Predicate_funcContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(AgentSpecParser.IDENTIFIER, 0); }
		public TerminalNode LPAREN() { return getToken(AgentSpecParser.LPAREN, 0); }
		public NumberContext number() {
			return getRuleContext(NumberContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(AgentSpecParser.RPAREN, 0); }
		public Predicate_funcContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_predicate_func; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterPredicate_func(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitPredicate_func(this);
		}
	}

	public final Predicate_funcContext predicate_func() throws RecognitionException {
		Predicate_funcContext _localctx = new Predicate_funcContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_predicate_func);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(118);
			match(IDENTIFIER);
			setState(119);
			match(LPAREN);
			setState(120);
			number();
			setState(121);
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
	public static class NamespaceContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(AgentSpecParser.IDENTIFIER, 0); }
		public TerminalNode COLON() { return getToken(AgentSpecParser.COLON, 0); }
		public NamespaceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_namespace; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterNamespace(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitNamespace(this);
		}
	}

	public final NamespaceContext namespace() throws RecognitionException {
		NamespaceContext _localctx = new NamespaceContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_namespace);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(123);
			match(IDENTIFIER);
			setState(124);
			match(COLON);
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
	public static class ConfigContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(AgentSpecParser.IDENTIFIER, 0); }
		public TerminalNode EQ() { return getToken(AgentSpecParser.EQ, 0); }
		public NumberContext number() {
			return getRuleContext(NumberContext.class,0);
		}
		public List<NamespaceContext> namespace() {
			return getRuleContexts(NamespaceContext.class);
		}
		public NamespaceContext namespace(int i) {
			return getRuleContext(NamespaceContext.class,i);
		}
		public ConfigContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_config; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterConfig(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitConfig(this);
		}
	}

	public final ConfigContext config() throws RecognitionException {
		ConfigContext _localctx = new ConfigContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_config);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(127); 
			_errHandler.sync(this);
			_alt = 1;
			do {
				switch (_alt) {
				case 1:
					{
					{
					setState(126);
					namespace();
					}
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(129); 
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,8,_ctx);
			} while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER );
			setState(131);
			match(IDENTIFIER);
			setState(132);
			match(EQ);
			setState(133);
			number();
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
		case 8:
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
		"\u0004\u0001 \u0088\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b\u0002"+
		"\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002\u000f\u0007\u000f"+
		"\u0001\u0000\u0005\u0000\"\b\u0000\n\u0000\f\u0000%\t\u0000\u0001\u0000"+
		"\u0001\u0000\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0003"+
		"\u0001\u0003\u0001\u0003\u0001\u0004\u0001\u0004\u0004\u00048\b\u0004"+
		"\u000b\u0004\f\u00049\u0001\u0005\u0001\u0005\u0004\u0005>\b\u0005\u000b"+
		"\u0005\f\u0005?\u0001\u0006\u0001\u0006\u0001\u0007\u0001\u0007\u0001"+
		"\u0007\u0001\u0007\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0003\bM\b"+
		"\b\u0001\b\u0001\b\u0001\b\u0001\b\u0005\bS\b\b\n\b\f\bV\t\b\u0001\t\u0001"+
		"\t\u0001\t\u0003\t[\b\t\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001"+
		"\n\u0001\n\u0001\n\u0005\ne\b\n\n\n\f\nh\t\n\u0001\n\u0001\n\u0001\n\u0001"+
		"\u000b\u0001\u000b\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0003"+
		"\fu\b\f\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\u000e\u0001\u000e"+
		"\u0001\u000e\u0001\u000f\u0004\u000f\u0080\b\u000f\u000b\u000f\f\u000f"+
		"\u0081\u0001\u000f\u0001\u000f\u0001\u000f\u0001\u000f\u0001\u000f\u0000"+
		"\u0001\u0010\u0010\u0000\u0002\u0004\u0006\b\n\f\u000e\u0010\u0012\u0014"+
		"\u0016\u0018\u001a\u001c\u001e\u0000\u0002\u0002\u0000\u0019\u0019\u001d"+
		" \u0001\u0000\u001b\u001c\u0086\u0000#\u0001\u0000\u0000\u0000\u0002("+
		"\u0001\u0000\u0000\u0000\u0004.\u0001\u0000\u0000\u0000\u00062\u0001\u0000"+
		"\u0000\u0000\b5\u0001\u0000\u0000\u0000\n;\u0001\u0000\u0000\u0000\fA"+
		"\u0001\u0000\u0000\u0000\u000eC\u0001\u0000\u0000\u0000\u0010L\u0001\u0000"+
		"\u0000\u0000\u0012Z\u0001\u0000\u0000\u0000\u0014\\\u0001\u0000\u0000"+
		"\u0000\u0016l\u0001\u0000\u0000\u0000\u0018t\u0001\u0000\u0000\u0000\u001a"+
		"v\u0001\u0000\u0000\u0000\u001c{\u0001\u0000\u0000\u0000\u001e\u007f\u0001"+
		"\u0000\u0000\u0000 \"\u0003\u0002\u0001\u0000! \u0001\u0000\u0000\u0000"+
		"\"%\u0001\u0000\u0000\u0000#!\u0001\u0000\u0000\u0000#$\u0001\u0000\u0000"+
		"\u0000$&\u0001\u0000\u0000\u0000%#\u0001\u0000\u0000\u0000&\'\u0005\u0000"+
		"\u0000\u0001\'\u0001\u0001\u0000\u0000\u0000()\u0003\u0004\u0002\u0000"+
		")*\u0003\u0006\u0003\u0000*+\u0003\b\u0004\u0000+,\u0003\n\u0005\u0000"+
		",-\u0005\b\u0000\u0000-\u0003\u0001\u0000\u0000\u0000./\u0005\u0001\u0000"+
		"\u0000/0\u0005\u0012\u0000\u000001\u0005\u0019\u0000\u00001\u0005\u0001"+
		"\u0000\u0000\u000023\u0005\u0002\u0000\u000034\u0003\f\u0006\u00004\u0007"+
		"\u0001\u0000\u0000\u000057\u0005\u0003\u0000\u000068\u0003\u0018\f\u0000"+
		"76\u0001\u0000\u0000\u000089\u0001\u0000\u0000\u000097\u0001\u0000\u0000"+
		"\u00009:\u0001\u0000\u0000\u0000:\t\u0001\u0000\u0000\u0000;=\u0005\u0004"+
		"\u0000\u0000<>\u0003\u0012\t\u0000=<\u0001\u0000\u0000\u0000>?\u0001\u0000"+
		"\u0000\u0000?=\u0001\u0000\u0000\u0000?@\u0001\u0000\u0000\u0000@\u000b"+
		"\u0001\u0000\u0000\u0000AB\u0007\u0000\u0000\u0000B\r\u0001\u0000\u0000"+
		"\u0000CD\u0005\u001a\u0000\u0000DE\u0005\t\u0000\u0000EF\u0003\u0010\b"+
		"\u0000F\u000f\u0001\u0000\u0000\u0000GH\u0006\b\uffff\uffff\u0000HM\u0005"+
		"\u001a\u0000\u0000IM\u0003\u0016\u000b\u0000JM\u0005\u0019\u0000\u0000"+
		"KM\u0003\u0014\n\u0000LG\u0001\u0000\u0000\u0000LI\u0001\u0000\u0000\u0000"+
		"LJ\u0001\u0000\u0000\u0000LK\u0001\u0000\u0000\u0000MT\u0001\u0000\u0000"+
		"\u0000NO\n\u0002\u0000\u0000OP\u0005\u0010\u0000\u0000PQ\u0005\u001a\u0000"+
		"\u0000QS\u0005\u0011\u0000\u0000RN\u0001\u0000\u0000\u0000SV\u0001\u0000"+
		"\u0000\u0000TR\u0001\u0000\u0000\u0000TU\u0001\u0000\u0000\u0000U\u0011"+
		"\u0001\u0000\u0000\u0000VT\u0001\u0000\u0000\u0000W[\u0005\u0017\u0000"+
		"\u0000X[\u0003\u0014\n\u0000Y[\u0003\u001e\u000f\u0000ZW\u0001\u0000\u0000"+
		"\u0000ZX\u0001\u0000\u0000\u0000ZY\u0001\u0000\u0000\u0000[\u0013\u0001"+
		"\u0000\u0000\u0000\\]\u0005\u0016\u0000\u0000]^\u0005\u000b\u0000\u0000"+
		"^_\u0005\u0019\u0000\u0000_`\u0005\n\u0000\u0000`a\u0005\r\u0000\u0000"+
		"af\u0003\u000e\u0007\u0000bc\u0005\n\u0000\u0000ce\u0003\u000e\u0007\u0000"+
		"db\u0001\u0000\u0000\u0000eh\u0001\u0000\u0000\u0000fd\u0001\u0000\u0000"+
		"\u0000fg\u0001\u0000\u0000\u0000gi\u0001\u0000\u0000\u0000hf\u0001\u0000"+
		"\u0000\u0000ij\u0005\u000e\u0000\u0000jk\u0005\f\u0000\u0000k\u0015\u0001"+
		"\u0000\u0000\u0000lm\u0007\u0001\u0000\u0000m\u0017\u0001\u0000\u0000"+
		"\u0000nu\u0005\u0006\u0000\u0000ou\u0005\u0007\u0000\u0000pq\u0005\u0014"+
		"\u0000\u0000qu\u0003\u0018\f\u0000ru\u0005\u0015\u0000\u0000su\u0003\u001a"+
		"\r\u0000tn\u0001\u0000\u0000\u0000to\u0001\u0000\u0000\u0000tp\u0001\u0000"+
		"\u0000\u0000tr\u0001\u0000\u0000\u0000ts\u0001\u0000\u0000\u0000u\u0019"+
		"\u0001\u0000\u0000\u0000vw\u0005\u0019\u0000\u0000wx\u0005\u000b\u0000"+
		"\u0000xy\u0003\u0016\u000b\u0000yz\u0005\f\u0000\u0000z\u001b\u0001\u0000"+
		"\u0000\u0000{|\u0005\u0019\u0000\u0000|}\u0005\t\u0000\u0000}\u001d\u0001"+
		"\u0000\u0000\u0000~\u0080\u0003\u001c\u000e\u0000\u007f~\u0001\u0000\u0000"+
		"\u0000\u0080\u0081\u0001\u0000\u0000\u0000\u0081\u007f\u0001\u0000\u0000"+
		"\u0000\u0081\u0082\u0001\u0000\u0000\u0000\u0082\u0083\u0001\u0000\u0000"+
		"\u0000\u0083\u0084\u0005\u0019\u0000\u0000\u0084\u0085\u0005\u0013\u0000"+
		"\u0000\u0085\u0086\u0003\u0016\u000b\u0000\u0086\u001f\u0001\u0000\u0000"+
		"\u0000\t#9?LTZft\u0081";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}