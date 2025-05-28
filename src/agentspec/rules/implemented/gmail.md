 # Langchain Gmail Assistant Rules

### **1. Rule for Avoiding Duplicate Emails**
```plaintext
rule @duplicate_email_check  
trigger SendMessage(CC, BCC, MESSAGE, SUBJECT, TO)  
check  
    TO, CC, or BCC contains the same email multiple times  
enforce  
  - remove duplicates: "The same recipient appears multiple times in TO, CC, or BCC. The email will be adjusted to remove duplicates."  
end  
```
2. Rule for Privacy Protection
```
plaintext 
rule @privacy_protection  
trigger SendMessage(CC, BCC, MESSAGE, SUBJECT, TO)  
check  
    BCC is empty, but email contains multiple recipients in CC  
enforce  
  - move recipients from CC to BCC: "Multiple recipients are in CC. To protect their privacy, they will be moved to BCC."  
end  
```
3. Rule for Email Size
```
plaintext 
rule @email_size_limit  
trigger SendMessage(CC, BCC, MESSAGE, SUBJECT, TO)  
check  
    MESSAGE size exceeds 5 MB or has large attachments  
enforce  
  - warn: "The email size is too large. Consider compressing attachments or using cloud sharing links."  
end  
```
4. Rule for Sensitive Content
```
plaintext 
rule @sensitive_content_check  
trigger SendMessage(CC, BCC, MESSAGE, SUBJECT, TO)  
check  
    MESSAGE contains sensitive keywords (e.g., "password", "confidential", "SSN")  
    TO or CC includes external recipients  
enforce  
  - ask for confirmation: "This email contains sensitive information. Confirm if you want to send it to external recipients."  
end  
```
5. Rule for Formality in Subject
```
rule @subject_formality_check  
trigger SendMessage(CC, BCC, MESSAGE, SUBJECT, TO)  
check  
    SUBJECT contains casual language or emojis when sent to professional contacts (e.g., boss, professor)  
enforce  
  - refine subject: "The subject line will be adjusted to maintain professionalism."  
end  
```
6. Rule for Follow-Up Emails
```
rule @follow_up_check  
trigger SendMessage(CC, BCC, MESSAGE, SUBJECT, TO)  
check  
    a previous message to the same recipient is unanswered within a specific timeframe (e.g., 3 days)  
enforce  
  - add polite follow-up context: "It seems like you're following up. The email will include polite context for better clarity."  
end  
```
7. Rule for Avoiding Empty Subject or Body
```
rule @empty_email_check  
trigger SendMessage(CC, BCC, MESSAGE, SUBJECT, TO)  
check  
    SUBJECT or MESSAGE is empty  
enforce  
  - block and warn: "The email has an empty subject or body. Please complete the email before sending."  
end  
```
8. Rule for Restricting Mass Emails
```
rule @mass_email_check  
trigger SendMessage(CC, BCC, MESSAGE, SUBJECT, TO)  
check  
    TO, CC, and BCC collectively exceed a certain threshold (e.g., 50 recipients)  
enforce  
  - warn: "You are about to send a mass email. Ensure compliance with organizational policies."  
end  
```
9. Rule for Drafting Sensitive Emails
```
rule @sensitive_email_draft_check  
trigger CreateDraft(CC, BCC, MESSAGE, SUBJECT, TO)  
check  
    MESSAGE includes sensitive keywords but is not encrypted  
enforce  
  - suggest encryption: "The draft contains sensitive content. Consider using encryption before sending."  
end  
```
10. Rule for Polite Tone in Request Emails
```
rule @polite_tone_check  
trigger SendMessage(CC, BCC, MESSAGE, SUBJECT, TO)  
check  
    SUBJECT or MESSAGE indicates a request but lacks polite phrases (e.g., "please", "thank you")  
enforce  
  - refine tone: "The email tone will be adjusted to include polite language for better reception."  
end  
```
11. Rule for Preventing Reply-All Storms
```
rule @reply_all_limit_check  
trigger SendMessage(CC, BCC, MESSAGE, SUBJECT, TO)  
check  
    the email is a reply-all to a thread with more than 20 participants  
enforce  
  - warn: "This reply-all will include many recipients. Confirm if this is necessary."  
end  
``` 