
### 1. Prevent Overwriting Critical Variables
```plaintext
rule @prevent_overwriting_critical_variables
trigger IPythonRunCellAction(code)
check
  - code redefines critical variables (e.g., 'sys', 'os', or user-defined protected variables)
enforce
  - abort action: "Critical variable overwrite detected."
  - ask for user confirmation: "Are you sure you want to redefine this variable?"
  - self-examinate: "Consider using different variable names to avoid conflicts."
end

---

### 2. Monitor External Resource Usage
rule @monitor_external_resource_usage
trigger IPythonRunCellAction(code)
check
  - code accesses external resources like files or network calls
  - code does not specify safe paths or timeouts for operations
enforce
  - log action: "External resource usage detected. Logging operation for review."
  - ask for user confirmation: "The code accesses external resources. Do you want to proceed?"
  - self-examinate: "Verify if the external resource access is secure and necessary."
end

---

### 3. Limit Resource-Intensive Python Execution
```plaintext
rule @limit_python_execution
trigger IPythonRunCellAction(code)
check
  - code contains operations with high computational complexity (e.g., nested loops > 2)
enforce
  - abort action: "Execution of resource-heavy code detected."
  - ask for user inspection: "The code may require significant resources. Do you still want to execute it?"
  - self-examinate: "Can the code be simplified or optimized before execution?"
end
```

---

### 4. Ensure Memory Safety 
rule @ensure_memory_safety
trigger IPythonRunCellAction(code)
check
  - code dynamically allocates large data structures (e.g., lists, arrays) without bounds
  - code may lead to memory leaks (e.g., unclosed file handlers)
enforce
  - abort action: "Potential memory issue detected."
  - suggest fixes: "Review the code to ensure proper memory management."
  - self-examinate: "Is the data size or allocation strategy reasonable?"
end

---
 
### 5. Validate Code Safety
```plaintext
rule @validate_code_safety
trigger IPythonRunCellAction(code)
check
  - code includes risky imports (e.g., os.system, subprocess)
  - code contains eval() or exec() functions
enforce
  - ask for user inspection: "The code contains potentially unsafe operations. Would you like to proceed?"
  - self-examinate: "Are the risky functions absolutely necessary for this task?"
  - abort action if risks cannot be justified
end
```

---
 
### 6. Restrict Dangerous File Operations
rule @restrict_dangerous_file_operations
trigger IPythonRunCellAction(code)
check
  - code attempts to modify or delete critical system files
  - code performs file operations without specifying access modes
enforce
  - abort action: "Suspicious file operation detected."
  - ask for user confirmation: "The code attempts a file operation. Are you sure you want to proceed?"
  - self-examinate: "Double-check the file paths and operations to ensure safety."
end

---

### 7.  Regulate Network Requests
rule @regulate_network_requests
trigger IPythonRunCellAction(code)
check
  - code sends network requests without specifying timeouts
  - code accesses untrusted or unknown URLs
enforce
  - log action: "Network request detected. Logging details for review."
  - ask for user confirmation: "The code sends network requests. Do you want to proceed?"
  - self-examinate: "Are the network calls necessary and secure?"
end

---

### 8. Validate External Library Dependencies
rule @validate_library_dependencies
trigger IPythonRunCellAction(code)
check
  - code imports libraries not installed in the current environment
  - code uses libraries with known vulnerabilities
enforce
  - abort action: "Required libraries are not installed or are insecure."
  - suggest fixes: "Install or update libraries to ensure compatibility and security."
end

---

### 9. Detect Hardcoded Sensitive Information 

rule @detect_hardcoded_sensitive_information
trigger IPythonRunCellAction(code)
check
  - code contains hardcoded credentials (e.g., API keys, passwords)
  - code exposes sensitive paths or URLs
enforce
  - abort action: "Sensitive information detected in the code."
  - ask for user review: "Sensitive data found. Are you sure you want to execute this?"
  - suggest fixes: "Consider storing sensitive information in environment variables."
end
