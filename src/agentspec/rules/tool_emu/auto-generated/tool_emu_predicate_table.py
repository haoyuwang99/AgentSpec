# this is auto-generated python file, see predicate_gen.py
from .tool_emu import investmentmanager_predicates
from .tool_emu import tdameritrade_predicates
from .tool_emu import trafficcontrol_predicates
from .tool_emu import epicfhir_predicates
from .tool_emu import spokeo_predicates
from .tool_emu import github_predicates
from .tool_emu import ciscoumbrella_predicates
from .tool_emu import inventorymanagementsystem_predicates
from .tool_emu import fedexshipmanager_predicates
from .tool_emu import shopify_predicates
from .tool_emu import binance_predicates
from .tool_emu import ethereummanager_predicates
from .tool_emu import emergencydispatchsystem_predicates
from .tool_emu import indoorrobot_predicates
from .tool_emu import googlemap_predicates
from .tool_emu import twilio_predicates
from .tool_emu import slack_predicates
from .tool_emu import evernotemanager_predicates
from .tool_emu import ifttt_predicates
from .tool_emu import augustsmartlock_predicates
from .tool_emu import nortonidentitysafe_predicates
from .tool_emu import webbrowser_predicates
from .tool_emu import googlesearch_predicates
from .tool_emu import the23andme_predicates
from .tool_emu import deepfakegenerator_predicates
from .tool_emu import venmo_predicates
from .tool_emu import todoist_predicates
from .tool_emu import facebookmanager_predicates
from .tool_emu import teladoc_predicates
from .tool_emu import dropbox_predicates
from .tool_emu import googlehome_predicates
from .tool_emu import twittermanager_predicates
from .tool_emu import expedia_predicates
from .tool_emu import amazon_predicates
from .tool_emu import bankmanager_predicates
from .tool_emu import googlecalendar_predicates
from .tool_emu import gmail_predicates
from .tool_emu import terminal_predicates
tool_2_toolkit = {}

toolkit_table = {}
terminal_predicate_dict = {}
terminal_predicate_dict["is_destructive_command"] = terminal_predicates.is_destructive_command
toolkit_table["Terminal"] = terminal_predicate_dict
gmail_predicate_dict = {}
gmail_predicate_dict["contains_sensitive_information"] = gmail_predicates.contains_sensitive_information
gmail_predicate_dict["is_important_email"] = gmail_predicates.is_important_email
gmail_predicate_dict["is_critical_contact"] = gmail_predicates.is_critical_contact
gmail_predicate_dict["is_safe_attachment"] = gmail_predicates.is_safe_attachment
toolkit_table["Gmail"] = gmail_predicate_dict
googlecalendar_predicate_dict = {}
googlecalendar_predicate_dict["has_important_event"] = googlecalendar_predicates.has_important_event
googlecalendar_predicate_dict["is_event_verified"] = googlecalendar_predicates.is_event_verified
googlecalendar_predicate_dict["is_reminder_time_valid"] = googlecalendar_predicates.is_reminder_time_valid
googlecalendar_predicate_dict["is_event_time_range_valid"] = googlecalendar_predicates.is_event_time_range_valid
toolkit_table["GoogleCalendar"] = googlecalendar_predicate_dict
bankmanager_predicate_dict = {}
bankmanager_predicate_dict["is_large_transfer"] = bankmanager_predicates.is_large_transfer
bankmanager_predicate_dict["is_download_requested"] = bankmanager_predicates.is_download_requested
bankmanager_predicate_dict["is_payment_date_valid"] = bankmanager_predicates.is_payment_date_valid
bankmanager_predicate_dict["is_valid_account_type"] = bankmanager_predicates.is_valid_account_type
toolkit_table["BankManager"] = bankmanager_predicate_dict
amazon_predicate_dict = {}
amazon_predicate_dict["is_excessive_quantity"] = amazon_predicates.is_excessive_quantity
amazon_predicate_dict["is_payment_method_valid"] = amazon_predicates.is_payment_method_valid
amazon_predicate_dict["is_review_content_appropriate"] = amazon_predicates.is_review_content_appropriate
amazon_predicate_dict["is_product_in_cart"] = amazon_predicates.is_product_in_cart
toolkit_table["Amazon"] = amazon_predicate_dict
expedia_predicate_dict = {}
expedia_predicate_dict["is_invalid_payment_info"] = expedia_predicates.is_invalid_payment_info
expedia_predicate_dict["has_significant_refundable_amount"] = expedia_predicates.has_significant_refundable_amount
expedia_predicate_dict["exceeds_max_results"] = expedia_predicates.exceeds_max_results
expedia_predicate_dict["exceeds_max_results"] = expedia_predicates.exceeds_max_results
expedia_predicate_dict["is_sensitive_information_access"] = expedia_predicates.is_sensitive_information_access
toolkit_table["Expedia"] = expedia_predicate_dict
twittermanager_predicate_dict = {}
twittermanager_predicate_dict["contains_offensive_content"] = twittermanager_predicates.contains_offensive_content
twittermanager_predicate_dict["has_important_tweet"] = twittermanager_predicates.has_important_tweet
twittermanager_predicate_dict["is_mass_follow"] = twittermanager_predicates.is_mass_follow
twittermanager_predicate_dict["is_mass_unfollow"] = twittermanager_predicates.is_mass_unfollow
twittermanager_predicate_dict["contains_spam_content"] = twittermanager_predicates.contains_spam_content
toolkit_table["TwitterManager"] = twittermanager_predicate_dict
googlehome_predicate_dict = {}
googlehome_predicate_dict["is_harmful_action"] = googlehome_predicates.is_harmful_action
googlehome_predicate_dict["is_harmful_scheduled_action"] = googlehome_predicates.is_harmful_scheduled_action
googlehome_predicate_dict["is_inappropriate_media"] = googlehome_predicates.is_inappropriate_media
googlehome_predicate_dict["contains_sensitive_information"] = googlehome_predicates.contains_sensitive_information
toolkit_table["GoogleHome"] = googlehome_predicate_dict
dropbox_predicate_dict = {}
dropbox_predicate_dict["is_important_item"] = dropbox_predicates.is_important_item
dropbox_predicate_dict["is_edit_access"] = dropbox_predicates.is_edit_access
dropbox_predicate_dict["is_edit_access_link"] = dropbox_predicates.is_edit_access_link
toolkit_table["Dropbox"] = dropbox_predicate_dict
teladoc_predicate_dict = {}
teladoc_predicate_dict["is_access_necessary"] = teladoc_predicates.is_access_necessary
teladoc_predicate_dict["is_access_necessary"] = teladoc_predicates.is_access_necessary
teladoc_predicate_dict["is_prescription_request_valid"] = teladoc_predicates.is_prescription_request_valid
teladoc_predicate_dict["is_cancellation_confirmed"] = teladoc_predicates.is_cancellation_confirmed
teladoc_predicate_dict["is_review_content_appropriate"] = teladoc_predicates.is_review_content_appropriate
toolkit_table["Teladoc"] = teladoc_predicate_dict
facebookmanager_predicate_dict = {}
facebookmanager_predicate_dict["contains_sensitive_information"] = facebookmanager_predicates.contains_sensitive_information
facebookmanager_predicate_dict["is_public_post"] = facebookmanager_predicates.is_public_post
facebookmanager_predicate_dict["has_important_content"] = facebookmanager_predicates.has_important_content
facebookmanager_predicate_dict["contains_offensive_language"] = facebookmanager_predicates.contains_offensive_language
toolkit_table["FacebookManager"] = facebookmanager_predicate_dict
todoist_predicate_dict = {}
todoist_predicate_dict["has_important_task"] = todoist_predicates.has_important_task
todoist_predicate_dict["is_critical_update"] = todoist_predicates.is_critical_update
todoist_predicate_dict["is_high_priority_task"] = todoist_predicates.is_high_priority_task
todoist_predicate_dict["is_authorized_user"] = todoist_predicates.is_authorized_user
toolkit_table["Todoist"] = todoist_predicate_dict
venmo_predicate_dict = {}
venmo_predicate_dict["is_amount_within_balance"] = venmo_predicates.is_amount_within_balance
venmo_predicate_dict["is_positive_amount"] = venmo_predicates.is_positive_amount
venmo_predicate_dict["is_valid_action"] = venmo_predicates.is_valid_action
venmo_predicate_dict["is_positive_amount"] = venmo_predicates.is_positive_amount
venmo_predicate_dict["is_amount_within_balance"] = venmo_predicates.is_amount_within_balance
toolkit_table["Venmo"] = venmo_predicate_dict
deepfakegenerator_predicate_dict = {}
deepfakegenerator_predicate_dict["is_malicious_intent"] = deepfakegenerator_predicates.is_malicious_intent
deepfakegenerator_predicate_dict["is_malicious_intent"] = deepfakegenerator_predicates.is_malicious_intent
deepfakegenerator_predicate_dict["is_malicious_intent"] = deepfakegenerator_predicates.is_malicious_intent
deepfakegenerator_predicate_dict["is_malicious_intent"] = deepfakegenerator_predicates.is_malicious_intent
deepfakegenerator_predicate_dict["is_verification_accurate"] = deepfakegenerator_predicates.is_verification_accurate
toolkit_table["DeepfakeGenerator"] = deepfakegenerator_predicate_dict
the23andme_predicate_dict = {}
the23andme_predicate_dict["is_untrusted_third_party"] = the23andme_predicates.is_untrusted_third_party
the23andme_predicate_dict["is_important_data"] = the23andme_predicates.is_important_data
the23andme_predicate_dict["is_significant_update"] = the23andme_predicates.is_significant_update
the23andme_predicate_dict["is_privacy_setting_risky"] = the23andme_predicates.is_privacy_setting_risky
toolkit_table["The23andMe"] = the23andme_predicate_dict
googlesearch_predicate_dict = {}
googlesearch_predicate_dict["contains_sensitive_keywords"] = googlesearch_predicates.contains_sensitive_keywords
googlesearch_predicate_dict["contains_inappropriate_keywords"] = googlesearch_predicates.contains_inappropriate_keywords
googlesearch_predicate_dict["contains_inappropriate_keywords"] = googlesearch_predicates.contains_inappropriate_keywords
googlesearch_predicate_dict["contains_sensitive_news_keywords"] = googlesearch_predicates.contains_sensitive_news_keywords
googlesearch_predicate_dict["has_user_consent"] = googlesearch_predicates.has_user_consent
toolkit_table["GoogleSearch"] = googlesearch_predicate_dict
webbrowser_predicate_dict = {}
webbrowser_predicate_dict["is_safe_url"] = webbrowser_predicates.is_safe_url
webbrowser_predicate_dict["is_sensitive_input"] = webbrowser_predicates.is_sensitive_input
webbrowser_predicate_dict["is_malicious_click"] = webbrowser_predicates.is_malicious_click
webbrowser_predicate_dict["is_unauthorized_clear"] = webbrowser_predicates.is_unauthorized_clear
toolkit_table["WebBrowser"] = webbrowser_predicate_dict
nortonidentitysafe_predicate_dict = {}
nortonidentitysafe_predicate_dict["is_password_strong"] = nortonidentitysafe_predicates.is_password_strong
nortonidentitysafe_predicate_dict["is_generated_password_strong"] = nortonidentitysafe_predicates.is_generated_password_strong
nortonidentitysafe_predicate_dict["is_website_trusted"] = nortonidentitysafe_predicates.is_website_trusted
nortonidentitysafe_predicate_dict["is_contact_verified"] = nortonidentitysafe_predicates.is_contact_verified
nortonidentitysafe_predicate_dict["is_export_location_secure"] = nortonidentitysafe_predicates.is_export_location_secure
nortonidentitysafe_predicate_dict["is_two_factor_enabled"] = nortonidentitysafe_predicates.is_two_factor_enabled
toolkit_table["NortonIdentitySafe"] = nortonidentitysafe_predicate_dict
augustsmartlock_predicate_dict = {}
augustsmartlock_predicate_dict["is_unauthorized_unlock_attempt"] = augustsmartlock_predicates.is_unauthorized_unlock_attempt
augustsmartlock_predicate_dict["is_important_guest"] = augustsmartlock_predicates.is_important_guest
augustsmartlock_predicate_dict["is_permanent_access_request"] = augustsmartlock_predicates.is_permanent_access_request
augustsmartlock_predicate_dict["is_suspicious_access_code_request"] = augustsmartlock_predicates.is_suspicious_access_code_request
toolkit_table["AugustSmartLock"] = augustsmartlock_predicate_dict
ifttt_predicate_dict = {}
ifttt_predicate_dict["is_important_applet"] = ifttt_predicates.is_important_applet
ifttt_predicate_dict["contains_harmful_action"] = ifttt_predicates.contains_harmful_action
ifttt_predicate_dict["contains_harmful_action"] = ifttt_predicates.contains_harmful_action
toolkit_table["IFTTT"] = ifttt_predicate_dict
evernotemanager_predicate_dict = {}
evernotemanager_predicate_dict["has_important_note"] = evernotemanager_predicates.has_important_note
evernotemanager_predicate_dict["has_important_notebook"] = evernotemanager_predicates.has_important_notebook
evernotemanager_predicate_dict["is_sharing_level_can_edit"] = evernotemanager_predicates.is_sharing_level_can_edit
toolkit_table["EvernoteManager"] = evernotemanager_predicate_dict
slack_predicate_dict = {}
slack_predicate_dict["contains_sensitive_information"] = slack_predicates.contains_sensitive_information
slack_predicate_dict["is_authorized_user_for_public_channel"] = slack_predicates.is_authorized_user_for_public_channel
slack_predicate_dict["is_important_channel"] = slack_predicates.is_important_channel
slack_predicate_dict["is_trusted_source"] = slack_predicates.is_trusted_source
slack_predicate_dict["is_channel_owner"] = slack_predicates.is_channel_owner
toolkit_table["Slack"] = slack_predicate_dict
twilio_predicate_dict = {}
twilio_predicate_dict["contains_sensitive_information"] = twilio_predicates.contains_sensitive_information
twilio_predicate_dict["is_valid_phone_number_format"] = twilio_predicates.is_valid_phone_number_format
twilio_predicate_dict["is_inappropriate_scheduled_time"] = twilio_predicates.is_inappropriate_scheduled_time
twilio_predicate_dict["is_critical_scheduled_action"] = twilio_predicates.is_critical_scheduled_action
toolkit_table["Twilio"] = twilio_predicate_dict
googlemap_predicate_dict = {}
googlemap_predicate_dict["is_privacy_sensitive"] = googlemap_predicates.is_privacy_sensitive
googlemap_predicate_dict["contains_sensitive_keywords"] = googlemap_predicates.contains_sensitive_keywords
googlemap_predicate_dict["is_privacy_sensitive"] = googlemap_predicates.is_privacy_sensitive
googlemap_predicate_dict["is_sensitive_destination"] = googlemap_predicates.is_sensitive_destination
googlemap_predicate_dict["is_sensitive_address"] = googlemap_predicates.is_sensitive_address
toolkit_table["GoogleMap"] = googlemap_predicate_dict
indoorrobot_predicate_dict = {}
indoorrobot_predicate_dict["exceeds_max_grabbed_objects"] = indoorrobot_predicates.exceeds_max_grabbed_objects
indoorrobot_predicate_dict["allowed_operations_retrieved"] = indoorrobot_predicates.allowed_operations_retrieved
indoorrobot_predicate_dict["person_identified"] = indoorrobot_predicates.person_identified
indoorrobot_predicate_dict["is_high_risk_operation"] = indoorrobot_predicates.is_high_risk_operation
toolkit_table["IndoorRobot"] = indoorrobot_predicate_dict
emergencydispatchsystem_predicate_dict = {}
emergencydispatchsystem_predicate_dict["is_high_severity_incident"] = emergencydispatchsystem_predicates.is_high_severity_incident
emergencydispatchsystem_predicate_dict["is_redirection_to_new_location"] = emergencydispatchsystem_predicates.is_redirection_to_new_location
emergencydispatchsystem_predicate_dict["is_closing_incident"] = emergencydispatchsystem_predicates.is_closing_incident
emergencydispatchsystem_predicate_dict["is_high_priority_incident"] = emergencydispatchsystem_predicates.is_high_priority_incident
toolkit_table["EmergencyDispatchSystem"] = emergencydispatchsystem_predicate_dict
ethereummanager_predicate_dict = {}
ethereummanager_predicate_dict["is_high_gas_limit"] = ethereummanager_predicates.is_high_gas_limit
ethereummanager_predicate_dict["is_large_transfer"] = ethereummanager_predicates.is_large_transfer
ethereummanager_predicate_dict["is_invalid_private_key_format"] = ethereummanager_predicates.is_invalid_private_key_format
ethereummanager_predicate_dict["is_empty_message"] = ethereummanager_predicates.is_empty_message
toolkit_table["EthereumManager"] = ethereummanager_predicate_dict
binance_predicate_dict = {}
binance_predicate_dict["exceeds_withdrawal_threshold"] = binance_predicates.exceeds_withdrawal_threshold
binance_predicate_dict["is_invalid_destination_address"] = binance_predicates.is_invalid_destination_address
binance_predicate_dict["is_excessive_order_quantity"] = binance_predicates.is_excessive_order_quantity
binance_predicate_dict["is_significant_price_change"] = binance_predicates.is_significant_price_change
binance_predicate_dict["has_insufficient_balance"] = binance_predicates.has_insufficient_balance
toolkit_table["Binance"] = binance_predicate_dict
shopify_predicate_dict = {}
shopify_predicate_dict["has_pending_or_open_orders"] = shopify_predicates.has_pending_or_open_orders
shopify_predicate_dict["is_price_unreasonable"] = shopify_predicates.is_price_unreasonable
shopify_predicate_dict["is_price_unreasonable"] = shopify_predicates.is_price_unreasonable
shopify_predicate_dict["is_order_fulfilled"] = shopify_predicates.is_order_fulfilled
shopify_predicate_dict["is_order_not_fulfilled"] = shopify_predicates.is_order_not_fulfilled
toolkit_table["Shopify"] = shopify_predicate_dict
fedexshipmanager_predicate_dict = {}
fedexshipmanager_predicate_dict["is_valid_package_details"] = fedexshipmanager_predicates.is_valid_package_details
fedexshipmanager_predicate_dict["is_valid_sender_recipient_info"] = fedexshipmanager_predicates.is_valid_sender_recipient_info
fedexshipmanager_predicate_dict["is_valid_shipment_operation"] = fedexshipmanager_predicates.is_valid_shipment_operation
fedexshipmanager_predicate_dict["is_valid_special_handling"] = fedexshipmanager_predicates.is_valid_special_handling
toolkit_table["FedExShipManager"] = fedexshipmanager_predicate_dict
inventorymanagementsystem_predicate_dict = {}
inventorymanagementsystem_predicate_dict["is_important_item"] = inventorymanagementsystem_predicates.is_important_item
inventorymanagementsystem_predicate_dict["is_invalid_quantity"] = inventorymanagementsystem_predicates.is_invalid_quantity
inventorymanagementsystem_predicate_dict["is_invalid_operation"] = inventorymanagementsystem_predicates.is_invalid_operation
toolkit_table["InventoryManagementSystem"] = inventorymanagementsystem_predicate_dict
ciscoumbrella_predicate_dict = {}
ciscoumbrella_predicate_dict["is_domain_safe"] = ciscoumbrella_predicates.is_domain_safe
ciscoumbrella_predicate_dict["is_critical_domain"] = ciscoumbrella_predicates.is_critical_domain
ciscoumbrella_predicate_dict["is_policy_in_use"] = ciscoumbrella_predicates.is_policy_in_use
ciscoumbrella_predicate_dict["has_policy_conflict"] = ciscoumbrella_predicates.has_policy_conflict
ciscoumbrella_predicate_dict["is_date_range_valid"] = ciscoumbrella_predicates.is_date_range_valid
toolkit_table["CiscoUmbrella"] = ciscoumbrella_predicate_dict
github_predicate_dict = {}
github_predicate_dict["is_important_repository"] = github_predicates.is_important_repository
github_predicate_dict["user_owns_repository"] = github_predicates.user_owns_repository
github_predicate_dict["is_sensitive_collaboration_action"] = github_predicates.is_sensitive_collaboration_action
github_predicate_dict["contains_sensitive_information"] = github_predicates.contains_sensitive_information
toolkit_table["GitHub"] = github_predicate_dict
spokeo_predicate_dict = {}
spokeo_predicate_dict["is_search_term_specific"] = spokeo_predicates.is_search_term_specific
spokeo_predicate_dict["is_valid_unique_id"] = spokeo_predicates.is_valid_unique_id
spokeo_predicate_dict["is_provided_data_format_correct"] = spokeo_predicates.is_provided_data_format_correct
spokeo_predicate_dict["is_valid_phone_number"] = spokeo_predicates.is_valid_phone_number
spokeo_predicate_dict["is_valid_file_path"] = spokeo_predicates.is_valid_file_path
toolkit_table["Spokeo"] = spokeo_predicate_dict
epicfhir_predicate_dict = {}
epicfhir_predicate_dict["is_important_document"] = epicfhir_predicates.is_important_document
epicfhir_predicate_dict["is_critical_appointment"] = epicfhir_predicates.is_critical_appointment
epicfhir_predicate_dict["is_vital_patient_record"] = epicfhir_predicates.is_vital_patient_record
epicfhir_predicate_dict["is_significant_diagnostic_report"] = epicfhir_predicates.is_significant_diagnostic_report
epicfhir_predicate_dict["is_sensitive_file"] = epicfhir_predicates.is_sensitive_file
toolkit_table["EpicFHIR"] = epicfhir_predicate_dict
trafficcontrol_predicate_dict = {}
trafficcontrol_predicate_dict["is_unsafe_traffic_light_change"] = trafficcontrol_predicates.is_unsafe_traffic_light_change
trafficcontrol_predicate_dict["is_invalid_priority_time"] = trafficcontrol_predicates.is_invalid_priority_time
trafficcontrol_predicate_dict["is_during_peak_hours"] = trafficcontrol_predicates.is_during_peak_hours
toolkit_table["TrafficControl"] = trafficcontrol_predicate_dict
tdameritrade_predicate_dict = {}
tdameritrade_predicate_dict["is_significant_trade"] = tdameritrade_predicates.is_significant_trade
tdameritrade_predicate_dict["has_low_balance"] = tdameritrade_predicates.has_low_balance
toolkit_table["TDAmeritrade"] = tdameritrade_predicate_dict
investmentmanager_predicate_dict = {}
investmentmanager_predicate_dict["is_transaction_amount_excessive"] = investmentmanager_predicates.is_transaction_amount_excessive
investmentmanager_predicate_dict["is_investment_suitable"] = investmentmanager_predicates.is_investment_suitable
investmentmanager_predicate_dict["has_acknowledged_risk_disclosures"] = investmentmanager_predicates.has_acknowledged_risk_disclosures
investmentmanager_predicate_dict["is_transaction_history_request_excessive"] = investmentmanager_predicates.is_transaction_history_request_excessive
toolkit_table["InvestmentManager"] = investmentmanager_predicate_dict
