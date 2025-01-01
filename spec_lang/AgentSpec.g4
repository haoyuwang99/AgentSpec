
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
TOOLEMU_PREDICATE: 'user_owns_repository' | 'is_channel_owner' | 'is_privacy_sensitive' | 'is_valid_phone_number_format' | 'is_valid_file_path' | 'is_access_necessary' | 'is_public_post' | 'is_malicious_click' | 'is_important_email' | 'is_significant_trade' | 'is_unauthorized_unlock_attempt' | 'is_unsafe_traffic_light_change' | 'is_investment_suitable' | 'is_invalid_quantity' | 'is_event_verified' | 'is_important_item' | 'is_suspicious_access_code_request' | 'has_low_balance' | 'is_payment_date_valid' | 'is_safe_attachment' | 'is_valid_shipment_operation' | 'is_edit_access_link' | 'is_positive_amount' | 'is_permanent_access_request' | 'is_sharing_level_can_edit' | 'contains_spam_content' | 'is_two_factor_enabled' | 'has_important_notebook' | 'is_invalid_private_key_format' | 'is_redirection_to_new_location' | 'is_invalid_destination_address' | 'is_search_term_specific' | 'has_important_task' | 'is_untrusted_third_party' | 'is_malicious_intent' | 'is_high_risk_operation' | 'is_inappropriate_scheduled_time' | 'contains_harmful_action' | 'has_important_content' | 'is_inappropriate_media' | 'is_authorized_user' | 'person_identified' | 'is_important_repository' | 'has_policy_conflict' | 'is_product_in_cart' | 'has_pending_or_open_orders' | 'is_amount_within_balance' | 'contains_sensitive_keywords' | 'has_user_consent' | 'is_sensitive_collaboration_action' | 'is_valid_phone_number' | 'is_important_applet' | 'is_transaction_amount_excessive' | 'is_safe_url' | 'exceeds_withdrawal_threshold' | 'is_important_document' | 'is_harmful_scheduled_action' | 'is_valid_special_handling' | 'is_valid_action' | 'is_critical_appointment' | 'is_invalid_priority_time' | 'is_authorized_user_for_public_channel' | 'is_closing_incident' | 'is_significant_price_change' | 'is_large_transfer' | 'is_prescription_request_valid' | 'allowed_operations_retrieved' | 'has_important_note' | 'is_valid_account_type' | 'is_empty_message' | 'is_vital_patient_record' | 'is_high_priority_incident' | 'contains_sensitive_information' | 'is_critical_contact' | 'is_privacy_setting_risky' | 'is_harmful_action' | 'has_significant_refundable_amount' | 'is_policy_in_use' | 'is_high_gas_limit' | 'is_mass_follow' | 'is_critical_scheduled_action' | 'is_payment_method_valid' | 'is_excessive_quantity' | 'is_provided_data_format_correct' | 'is_review_content_appropriate' | 'is_download_requested' | 'is_export_location_secure' | 'is_edit_access' | 'is_trusted_source' | 'is_domain_safe' | 'is_invalid_operation' | 'is_generated_password_strong' | 'is_important_channel' | 'exceeds_max_results' | 'is_valid_sender_recipient_info' | 'is_sensitive_information_access' | 'has_insufficient_balance' | 'is_critical_update' | 'is_high_severity_incident' | 'is_sensitive_file' | 'is_transaction_history_request_excessive' | 'is_invalid_payment_info' | 'is_during_peak_hours' | 'is_destructive_command' | 'is_website_trusted' | 'is_password_strong' | 'is_cancellation_confirmed' | 'is_sensitive_destination' | 'is_date_range_valid' | 'is_critical_domain' | 'is_valid_package_details' | 'is_significant_update' | 'contains_offensive_language' | 'is_mass_unfollow' | 'is_verification_accurate' | 'is_reminder_time_valid' | 'has_important_event' | 'is_price_unreasonable' | 'is_sensitive_input' | 'contains_sensitive_news_keywords' | 'is_order_fulfilled' | 'is_sensitive_address' | 'is_contact_verified' | 'contains_offensive_content' | 'is_significant_diagnostic_report' | 'is_important_guest' | 'has_acknowledged_risk_disclosures' | 'is_excessive_order_quantity' | 'is_important_data' | 'is_unauthorized_clear' | 'is_valid_unique_id' | 'has_important_tweet' | 'is_order_not_fulfilled' | 'contains_inappropriate_keywords' | 'is_event_time_range_valid' | 'exceeds_max_grabbed_objects' | 'is_high_priority_task';
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

predicate: TRUE | FALSE | NOT predicate | TOOLEMU_PREDICATE; 

kvPair: STRING COLON value;

value: STRING | number | IDENTIFIER | value LBRACK STRING RBRACK | actionInvoke;

enforcement: ENFORCEMENT | actionInvoke;

actionInvoke: INVOKE LPAREN IDENTIFIER COMMA LBRACE kvPair (COMMA kvPair)* RBRACE RPAREN;
  
number: INTEGER | FLOAT;

