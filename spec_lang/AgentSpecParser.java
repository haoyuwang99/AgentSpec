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
		RULE=1, TRIGGER=2, PREPARE=3, CHECK=4, ENFORCE=5, ACTION=6, ANY=7, VAL=8, 
		TRUE=9, FALSE=10, END=11, EVAL_OP=12, COLON=13, COMMA=14, LPAREN=15, RPAREN=16, 
		LBRACE=17, RBRACE=18, LBRACK=19, RBRACK=20, AT=21, EQ=22, NOT=23, CMD_PREDICATE=24, 
		GIT_PREDICATE=25, TODOIST_PREDICATE=26, INVOKE=27, ENFORCEMENT=28, WS=29, 
		IDENTIFIER=30, STRING=31, INTEGER=32, FLOAT=33;
	public static final int
		RULE_program = 0, RULE_rule = 1, RULE_ruleClause = 2, RULE_triggerClause = 3, 
		RULE_prepareClause = 4, RULE_checkClause = 5, RULE_enforceClause = 6, 
		RULE_event = 7, RULE_prepare = 8, RULE_predicate = 9, RULE_kvPair = 10, 
		RULE_value = 11, RULE_enforcement = 12, RULE_actionInvoke = 13, RULE_number = 14;
	private static String[] makeRuleNames() {
		return new String[] {
			"program", "rule", "ruleClause", "triggerClause", "prepareClause", "checkClause", 
			"enforceClause", "event", "prepare", "predicate", "kvPair", "value", 
			"enforcement", "actionInvoke", "number"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'rule'", "'trigger'", "'prepare'", "'check'", "'enforce'", "'act'", 
			"'any'", "'val'", "'true'", "'false'", "'end'", null, "':'", "','", "'('", 
			"')'", "'{'", "'}'", "'['", "']'", "'@'", "'='", "'!'", null, null, "'is_important_task'", 
			"'invoke_action'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "RULE", "TRIGGER", "PREPARE", "CHECK", "ENFORCE", "ACTION", "ANY", 
			"VAL", "TRUE", "FALSE", "END", "EVAL_OP", "COLON", "COMMA", "LPAREN", 
			"RPAREN", "LBRACE", "RBRACE", "LBRACK", "RBRACK", "AT", "EQ", "NOT", 
			"CMD_PREDICATE", "GIT_PREDICATE", "TODOIST_PREDICATE", "INVOKE", "ENFORCEMENT", 
			"WS", "IDENTIFIER", "STRING", "INTEGER", "FLOAT"
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
			setState(33);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==RULE) {
				{
				{
				setState(30);
				rule_();
				}
				}
				setState(35);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(36);
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
		public PrepareClauseContext prepareClause() {
			return getRuleContext(PrepareClauseContext.class,0);
		}
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
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(38);
			ruleClause();
			setState(39);
			triggerClause();
			setState(41);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==PREPARE) {
				{
				setState(40);
				prepareClause();
				}
			}

			setState(43);
			checkClause();
			setState(44);
			enforceClause();
			setState(45);
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
			setState(47);
			match(RULE);
			setState(48);
			match(AT);
			setState(49);
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
			setState(51);
			match(TRIGGER);
			setState(52);
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
	public static class PrepareClauseContext extends ParserRuleContext {
		public TerminalNode PREPARE() { return getToken(AgentSpecParser.PREPARE, 0); }
		public List<PrepareContext> prepare() {
			return getRuleContexts(PrepareContext.class);
		}
		public PrepareContext prepare(int i) {
			return getRuleContext(PrepareContext.class,i);
		}
		public PrepareClauseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_prepareClause; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterPrepareClause(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitPrepareClause(this);
		}
	}

	public final PrepareClauseContext prepareClause() throws RecognitionException {
		PrepareClauseContext _localctx = new PrepareClauseContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_prepareClause);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(54);
			match(PREPARE);
			setState(56); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(55);
				prepare();
				}
				}
				setState(58); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==VAL );
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
		enterRule(_localctx, 10, RULE_checkClause);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(60);
			match(CHECK);
			setState(62); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(61);
				predicate();
				}
				}
				setState(64); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & 125834752L) != 0) );
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
		enterRule(_localctx, 12, RULE_enforceClause);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(66);
			match(ENFORCE);
			setState(68); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(67);
				enforcement();
				}
				}
				setState(70); 
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
	public static class EventContext extends ParserRuleContext {
		public TerminalNode ACTION() { return getToken(AgentSpecParser.ACTION, 0); }
		public TerminalNode IDENTIFIER() { return getToken(AgentSpecParser.IDENTIFIER, 0); }
		public TerminalNode ANY() { return getToken(AgentSpecParser.ANY, 0); }
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
		enterRule(_localctx, 14, RULE_event);
		try {
			setState(75);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ACTION:
				enterOuterAlt(_localctx, 1);
				{
				setState(72);
				match(ACTION);
				setState(73);
				match(IDENTIFIER);
				}
				break;
			case ANY:
				enterOuterAlt(_localctx, 2);
				{
				setState(74);
				match(ANY);
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
	public static class PrepareContext extends ParserRuleContext {
		public TerminalNode VAL() { return getToken(AgentSpecParser.VAL, 0); }
		public TerminalNode IDENTIFIER() { return getToken(AgentSpecParser.IDENTIFIER, 0); }
		public TerminalNode EQ() { return getToken(AgentSpecParser.EQ, 0); }
		public ValueContext value() {
			return getRuleContext(ValueContext.class,0);
		}
		public PrepareContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_prepare; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).enterPrepare(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AgentSpecListener ) ((AgentSpecListener)listener).exitPrepare(this);
		}
	}

	public final PrepareContext prepare() throws RecognitionException {
		PrepareContext _localctx = new PrepareContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_prepare);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(77);
			match(VAL);
			setState(78);
			match(IDENTIFIER);
			setState(79);
			match(EQ);
			setState(80);
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
	public static class PredicateContext extends ParserRuleContext {
		public TerminalNode EVAL_OP() { return getToken(AgentSpecParser.EVAL_OP, 0); }
		public TerminalNode LPAREN() { return getToken(AgentSpecParser.LPAREN, 0); }
		public List<ValueContext> value() {
			return getRuleContexts(ValueContext.class);
		}
		public ValueContext value(int i) {
			return getRuleContext(ValueContext.class,i);
		}
		public TerminalNode RPAREN() { return getToken(AgentSpecParser.RPAREN, 0); }
		public List<TerminalNode> COMMA() { return getTokens(AgentSpecParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(AgentSpecParser.COMMA, i);
		}
		public TerminalNode TRUE() { return getToken(AgentSpecParser.TRUE, 0); }
		public TerminalNode FALSE() { return getToken(AgentSpecParser.FALSE, 0); }
		public TerminalNode NOT() { return getToken(AgentSpecParser.NOT, 0); }
		public PredicateContext predicate() {
			return getRuleContext(PredicateContext.class,0);
		}
		public TerminalNode CMD_PREDICATE() { return getToken(AgentSpecParser.CMD_PREDICATE, 0); }
		public TerminalNode GIT_PREDICATE() { return getToken(AgentSpecParser.GIT_PREDICATE, 0); }
		public TerminalNode TODOIST_PREDICATE() { return getToken(AgentSpecParser.TODOIST_PREDICATE, 0); }
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
		enterRule(_localctx, 18, RULE_predicate);
		int _la;
		try {
			setState(101);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case EVAL_OP:
				enterOuterAlt(_localctx, 1);
				{
				setState(82);
				match(EVAL_OP);
				setState(83);
				match(LPAREN);
				setState(84);
				value(0);
				setState(89);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==COMMA) {
					{
					{
					setState(85);
					match(COMMA);
					setState(86);
					value(0);
					}
					}
					setState(91);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(92);
				match(RPAREN);
				}
				break;
			case TRUE:
				enterOuterAlt(_localctx, 2);
				{
				setState(94);
				match(TRUE);
				}
				break;
			case FALSE:
				enterOuterAlt(_localctx, 3);
				{
				setState(95);
				match(FALSE);
				}
				break;
			case NOT:
				enterOuterAlt(_localctx, 4);
				{
				setState(96);
				match(NOT);
				setState(97);
				predicate();
				}
				break;
			case CMD_PREDICATE:
				enterOuterAlt(_localctx, 5);
				{
				setState(98);
				match(CMD_PREDICATE);
				}
				break;
			case GIT_PREDICATE:
				enterOuterAlt(_localctx, 6);
				{
				setState(99);
				match(GIT_PREDICATE);
				}
				break;
			case TODOIST_PREDICATE:
				enterOuterAlt(_localctx, 7);
				{
				setState(100);
				match(TODOIST_PREDICATE);
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
		enterRule(_localctx, 20, RULE_kvPair);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(103);
			match(STRING);
			setState(104);
			match(COLON);
			setState(105);
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
		int _startState = 22;
		enterRecursionRule(_localctx, 22, RULE_value, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(112);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case STRING:
				{
				setState(108);
				match(STRING);
				}
				break;
			case INTEGER:
			case FLOAT:
				{
				setState(109);
				number();
				}
				break;
			case IDENTIFIER:
				{
				setState(110);
				match(IDENTIFIER);
				}
				break;
			case INVOKE:
				{
				setState(111);
				actionInvoke();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			_ctx.stop = _input.LT(-1);
			setState(120);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,9,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new ValueContext(_parentctx, _parentState);
					pushNewRecursionContext(_localctx, _startState, RULE_value);
					setState(114);
					if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
					setState(115);
					match(LBRACK);
					setState(116);
					match(STRING);
					setState(117);
					match(RBRACK);
					}
					} 
				}
				setState(122);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,9,_ctx);
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
		enterRule(_localctx, 24, RULE_enforcement);
		try {
			setState(125);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ENFORCEMENT:
				enterOuterAlt(_localctx, 1);
				{
				setState(123);
				match(ENFORCEMENT);
				}
				break;
			case INVOKE:
				enterOuterAlt(_localctx, 2);
				{
				setState(124);
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
		enterRule(_localctx, 26, RULE_actionInvoke);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(127);
			match(INVOKE);
			setState(128);
			match(LPAREN);
			setState(129);
			match(IDENTIFIER);
			setState(130);
			match(COMMA);
			setState(131);
			match(LBRACE);
			setState(132);
			kvPair();
			setState(137);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(133);
				match(COMMA);
				setState(134);
				kvPair();
				}
				}
				setState(139);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(140);
			match(RBRACE);
			setState(141);
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
		enterRule(_localctx, 28, RULE_number);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(143);
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
		case 11:
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
		"\u0004\u0001!\u0092\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b\u0002"+
		"\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0001\u0000\u0005\u0000"+
		" \b\u0000\n\u0000\f\u0000#\t\u0000\u0001\u0000\u0001\u0000\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0003\u0001*\b\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002"+
		"\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0004\u0001\u0004\u0004\u0004"+
		"9\b\u0004\u000b\u0004\f\u0004:\u0001\u0005\u0001\u0005\u0004\u0005?\b"+
		"\u0005\u000b\u0005\f\u0005@\u0001\u0006\u0001\u0006\u0004\u0006E\b\u0006"+
		"\u000b\u0006\f\u0006F\u0001\u0007\u0001\u0007\u0001\u0007\u0003\u0007"+
		"L\b\u0007\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001\t\u0001\t\u0001"+
		"\t\u0001\t\u0001\t\u0005\tX\b\t\n\t\f\t[\t\t\u0001\t\u0001\t\u0001\t\u0001"+
		"\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0003\tf\b\t\u0001\n\u0001"+
		"\n\u0001\n\u0001\n\u0001\u000b\u0001\u000b\u0001\u000b\u0001\u000b\u0001"+
		"\u000b\u0003\u000bq\b\u000b\u0001\u000b\u0001\u000b\u0001\u000b\u0001"+
		"\u000b\u0005\u000bw\b\u000b\n\u000b\f\u000bz\t\u000b\u0001\f\u0001\f\u0003"+
		"\f~\b\f\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001"+
		"\r\u0005\r\u0088\b\r\n\r\f\r\u008b\t\r\u0001\r\u0001\r\u0001\r\u0001\u000e"+
		"\u0001\u000e\u0001\u000e\u0000\u0001\u0016\u000f\u0000\u0002\u0004\u0006"+
		"\b\n\f\u000e\u0010\u0012\u0014\u0016\u0018\u001a\u001c\u0000\u0001\u0001"+
		"\u0000 !\u0095\u0000!\u0001\u0000\u0000\u0000\u0002&\u0001\u0000\u0000"+
		"\u0000\u0004/\u0001\u0000\u0000\u0000\u00063\u0001\u0000\u0000\u0000\b"+
		"6\u0001\u0000\u0000\u0000\n<\u0001\u0000\u0000\u0000\fB\u0001\u0000\u0000"+
		"\u0000\u000eK\u0001\u0000\u0000\u0000\u0010M\u0001\u0000\u0000\u0000\u0012"+
		"e\u0001\u0000\u0000\u0000\u0014g\u0001\u0000\u0000\u0000\u0016p\u0001"+
		"\u0000\u0000\u0000\u0018}\u0001\u0000\u0000\u0000\u001a\u007f\u0001\u0000"+
		"\u0000\u0000\u001c\u008f\u0001\u0000\u0000\u0000\u001e \u0003\u0002\u0001"+
		"\u0000\u001f\u001e\u0001\u0000\u0000\u0000 #\u0001\u0000\u0000\u0000!"+
		"\u001f\u0001\u0000\u0000\u0000!\"\u0001\u0000\u0000\u0000\"$\u0001\u0000"+
		"\u0000\u0000#!\u0001\u0000\u0000\u0000$%\u0005\u0000\u0000\u0001%\u0001"+
		"\u0001\u0000\u0000\u0000&\'\u0003\u0004\u0002\u0000\')\u0003\u0006\u0003"+
		"\u0000(*\u0003\b\u0004\u0000)(\u0001\u0000\u0000\u0000)*\u0001\u0000\u0000"+
		"\u0000*+\u0001\u0000\u0000\u0000+,\u0003\n\u0005\u0000,-\u0003\f\u0006"+
		"\u0000-.\u0005\u000b\u0000\u0000.\u0003\u0001\u0000\u0000\u0000/0\u0005"+
		"\u0001\u0000\u000001\u0005\u0015\u0000\u000012\u0005\u001e\u0000\u0000"+
		"2\u0005\u0001\u0000\u0000\u000034\u0005\u0002\u0000\u000045\u0003\u000e"+
		"\u0007\u00005\u0007\u0001\u0000\u0000\u000068\u0005\u0003\u0000\u0000"+
		"79\u0003\u0010\b\u000087\u0001\u0000\u0000\u00009:\u0001\u0000\u0000\u0000"+
		":8\u0001\u0000\u0000\u0000:;\u0001\u0000\u0000\u0000;\t\u0001\u0000\u0000"+
		"\u0000<>\u0005\u0004\u0000\u0000=?\u0003\u0012\t\u0000>=\u0001\u0000\u0000"+
		"\u0000?@\u0001\u0000\u0000\u0000@>\u0001\u0000\u0000\u0000@A\u0001\u0000"+
		"\u0000\u0000A\u000b\u0001\u0000\u0000\u0000BD\u0005\u0005\u0000\u0000"+
		"CE\u0003\u0018\f\u0000DC\u0001\u0000\u0000\u0000EF\u0001\u0000\u0000\u0000"+
		"FD\u0001\u0000\u0000\u0000FG\u0001\u0000\u0000\u0000G\r\u0001\u0000\u0000"+
		"\u0000HI\u0005\u0006\u0000\u0000IL\u0005\u001e\u0000\u0000JL\u0005\u0007"+
		"\u0000\u0000KH\u0001\u0000\u0000\u0000KJ\u0001\u0000\u0000\u0000L\u000f"+
		"\u0001\u0000\u0000\u0000MN\u0005\b\u0000\u0000NO\u0005\u001e\u0000\u0000"+
		"OP\u0005\u0016\u0000\u0000PQ\u0003\u0016\u000b\u0000Q\u0011\u0001\u0000"+
		"\u0000\u0000RS\u0005\f\u0000\u0000ST\u0005\u000f\u0000\u0000TY\u0003\u0016"+
		"\u000b\u0000UV\u0005\u000e\u0000\u0000VX\u0003\u0016\u000b\u0000WU\u0001"+
		"\u0000\u0000\u0000X[\u0001\u0000\u0000\u0000YW\u0001\u0000\u0000\u0000"+
		"YZ\u0001\u0000\u0000\u0000Z\\\u0001\u0000\u0000\u0000[Y\u0001\u0000\u0000"+
		"\u0000\\]\u0005\u0010\u0000\u0000]f\u0001\u0000\u0000\u0000^f\u0005\t"+
		"\u0000\u0000_f\u0005\n\u0000\u0000`a\u0005\u0017\u0000\u0000af\u0003\u0012"+
		"\t\u0000bf\u0005\u0018\u0000\u0000cf\u0005\u0019\u0000\u0000df\u0005\u001a"+
		"\u0000\u0000eR\u0001\u0000\u0000\u0000e^\u0001\u0000\u0000\u0000e_\u0001"+
		"\u0000\u0000\u0000e`\u0001\u0000\u0000\u0000eb\u0001\u0000\u0000\u0000"+
		"ec\u0001\u0000\u0000\u0000ed\u0001\u0000\u0000\u0000f\u0013\u0001\u0000"+
		"\u0000\u0000gh\u0005\u001f\u0000\u0000hi\u0005\r\u0000\u0000ij\u0003\u0016"+
		"\u000b\u0000j\u0015\u0001\u0000\u0000\u0000kl\u0006\u000b\uffff\uffff"+
		"\u0000lq\u0005\u001f\u0000\u0000mq\u0003\u001c\u000e\u0000nq\u0005\u001e"+
		"\u0000\u0000oq\u0003\u001a\r\u0000pk\u0001\u0000\u0000\u0000pm\u0001\u0000"+
		"\u0000\u0000pn\u0001\u0000\u0000\u0000po\u0001\u0000\u0000\u0000qx\u0001"+
		"\u0000\u0000\u0000rs\n\u0002\u0000\u0000st\u0005\u0013\u0000\u0000tu\u0005"+
		"\u001f\u0000\u0000uw\u0005\u0014\u0000\u0000vr\u0001\u0000\u0000\u0000"+
		"wz\u0001\u0000\u0000\u0000xv\u0001\u0000\u0000\u0000xy\u0001\u0000\u0000"+
		"\u0000y\u0017\u0001\u0000\u0000\u0000zx\u0001\u0000\u0000\u0000{~\u0005"+
		"\u001c\u0000\u0000|~\u0003\u001a\r\u0000}{\u0001\u0000\u0000\u0000}|\u0001"+
		"\u0000\u0000\u0000~\u0019\u0001\u0000\u0000\u0000\u007f\u0080\u0005\u001b"+
		"\u0000\u0000\u0080\u0081\u0005\u000f\u0000\u0000\u0081\u0082\u0005\u001e"+
		"\u0000\u0000\u0082\u0083\u0005\u000e\u0000\u0000\u0083\u0084\u0005\u0011"+
		"\u0000\u0000\u0084\u0089\u0003\u0014\n\u0000\u0085\u0086\u0005\u000e\u0000"+
		"\u0000\u0086\u0088\u0003\u0014\n\u0000\u0087\u0085\u0001\u0000\u0000\u0000"+
		"\u0088\u008b\u0001\u0000\u0000\u0000\u0089\u0087\u0001\u0000\u0000\u0000"+
		"\u0089\u008a\u0001\u0000\u0000\u0000\u008a\u008c\u0001\u0000\u0000\u0000"+
		"\u008b\u0089\u0001\u0000\u0000\u0000\u008c\u008d\u0005\u0012\u0000\u0000"+
		"\u008d\u008e\u0005\u0010\u0000\u0000\u008e\u001b\u0001\u0000\u0000\u0000"+
		"\u008f\u0090\u0007\u0000\u0000\u0000\u0090\u001d\u0001\u0000\u0000\u0000"+
		"\f!):@FKYepx}\u0089";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}