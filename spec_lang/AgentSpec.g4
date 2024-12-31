
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
LBRACK: '[';
RBRACK: ']';
AT: '@';
EQ: '=';
NOT: '!';
TOOLEMU_PREDICATE: 'is_channel_owner' | 'is_valid_phone_number' | 'is_product_in_cart' | 'is_trusted_source' | 'is_unauthorized_unlock_attempt' | 'is_privacy_sensitive' | 'is_critical_update' | 'is_high_priority_incident' | 'is_order_fulfilled' | 'is_contact_verified' | 'is_privacy_setting_risky' | 'person_identified' | 'is_sharing_level_can_edit' | 'is_cancellation_confirmed' | 'has_important_notebook' | 'is_payment_method_valid' | 'is_valid_package_details' | 'is_payment_date_valid' | 'contains_harmful_action' | 'is_sensitive_address' | 'is_redirection_to_new_location' | 'is_domain_safe' | 'allowed_operations_retrieved' | 'is_invalid_operation' | 'is_significant_update' | 'is_verification_accurate' | 'is_valid_special_handling' | 'is_permanent_access_request' | 'exceeds_withdrawal_threshold' | 'is_valid_unique_id' | 'is_edit_access_link' | 'has_insufficient_balance' | 'is_malicious_intent' | 'is_export_location_secure' | 'is_important_document' | 'is_mass_follow' | 'is_edit_access' | 'is_valid_file_path' | 'has_significant_refundable_amount' | 'is_website_trusted' | 'is_critical_contact' | 'is_download_requested' | 'is_important_channel' | 'is_destructive_command' | 'is_transaction_amount_excessive' | 'is_password_strong' | 'has_user_consent' | 'is_prescription_request_valid' | 'is_unauthorized_clear' | 'is_high_priority_task' | 'is_important_applet' | 'is_sensitive_file' | 'is_large_transfer' | 'is_inappropriate_scheduled_time' | 'has_important_task' | 'is_authorized_user_for_public_channel' | 'is_event_verified' | 'is_significant_diagnostic_report' | 'is_valid_shipment_operation' | 'is_valid_phone_number_format' | 'has_important_note' | 'is_valid_action' | 'contains_spam_content' | 'is_critical_scheduled_action' | 'is_excessive_order_quantity' | 'exceeds_max_results' | 'has_policy_conflict' | 'contains_offensive_content' | 'is_review_content_appropriate' | 'is_reminder_time_valid' | 'is_closing_incident' | 'is_valid_sender_recipient_info' | 'is_critical_domain' | 'is_search_term_specific' | 'is_high_severity_incident' | 'is_mass_unfollow' | 'is_sensitive_collaboration_action' | 'has_important_tweet' | 'exceeds_max_grabbed_objects' | 'user_owns_repository' | 'is_harmful_action' | 'is_two_factor_enabled' | 'is_malicious_click' | 'is_provided_data_format_correct' | 'is_invalid_destination_address' | 'is_invalid_private_key_format' | 'is_inappropriate_media' | 'is_important_email' | 'is_sensitive_information_access' | 'contains_sensitive_information' | 'is_amount_within_balance' | 'is_generated_password_strong' | 'is_invalid_quantity' | 'is_important_item' | 'is_invalid_priority_time' | 'has_important_content' | 'is_positive_amount' | 'is_critical_appointment' | 'is_high_risk_operation' | 'is_sensitive_input' | 'is_unsafe_traffic_light_change' | 'is_vital_patient_record' | 'is_date_range_valid' | 'is_important_guest' | 'has_low_balance' | 'has_important_event' | 'is_valid_account_type' | 'is_authorized_user' | 'is_price_unreasonable' | 'is_event_time_range_valid' | 'contains_sensitive_news_keywords' | 'is_important_data' | 'is_high_gas_limit' | 'is_safe_attachment' | 'is_important_repository' | 'contains_sensitive_keywords' | 'is_significant_price_change' | 'has_pending_or_open_orders' | 'is_significant_trade' | 'is_excessive_quantity' | 'is_investment_suitable' | 'is_invalid_payment_info' | 'is_sensitive_destination' | 'is_policy_in_use' | 'has_acknowledged_risk_disclosures' | 'is_untrusted_third_party' | 'is_access_necessary' | 'is_during_peak_hours' | 'is_public_post' | 'contains_offensive_language' | 'is_order_not_fulfilled' | 'is_transaction_history_request_excessive' | 'contains_inappropriate_keywords' | 'is_harmful_scheduled_action' | 'is_empty_message' | 'is_safe_url' | 'is_suspicious_access_code_request';
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

triggerClause: TRIGGER event;
 
checkClause: CHECK predicate+;

enforceClause: ENFORCE enforcement+; 

event: IDENTIFIER | ANY;

predicate: TRUE | FALSE | NOT predicate | TOOLEMU_PREDICATE; 

kvPair: STRING COLON value;

value: STRING | number | IDENTIFIER | value LBRACK STRING RBRACK | actionInvoke;

enforcement: ENFORCEMENT | actionInvoke;

actionInvoke: INVOKE LPAREN IDENTIFIER COMMA LBRACE kvPair (COMMA kvPair)* RBRACE RPAREN;
  
number: INTEGER | FLOAT;

