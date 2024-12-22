# CodeAct Agent Rules for Bug-Fixing in Swe-Bench

This document integrates all the rules developed to guide the CodeAct Agent in performing **bug-fixing tasks** while adhering to best practices for safety, correctness, and Git version control.

## Action Space:
```python
"""
- CmdRunAction(command) - bash command to run
- IPythonRunCellAction(code) - IPython code to run
- AgentDelegateAction(agent, inputs) - delegate action for (sub)task
- MessageAction(content) - Message action to run (e.g. ask for clarification)
- AgentFinishAction() - end the interaction
"""
```

---

## Rules:

### 1. Safe Shell Command Execution
```plaintext
rule @safe_shell_execution
trigger CmdRunAction(command)
check
  - command does not contain destructive operations (e.g., rm, dd, sudo)
  - command avoids redirections to system-critical paths (e.g., /dev/, /bin/)
  - command length <= 200 characters
enforce
  - ask for user inspection: "The command '${command}' appears to have a potential risk. Would you like to review it?"
  - self-examinate: "Does the command align with safe practices?"
  - abort action if any risk condition holds
end
```
 

# Git

### 6. Use a Dedicated Bug-Fix Branch
```plaintext
rule @use_dedicated_branch
trigger CmdRunAction(command)
check
  - command contains 'git commit' or 'git push'
  - the current branch name not starts with 'bugfix/' or 'fix/'
enforce
  - abort action: "Commits should happen on a dedicated bug-fix branch (e.g., 'bugfix/<issue-id>')."
  - ask for user inspection: "You are committing on branch '${current_branch}'. Would you like me to create a dedicated branch for this fix?"
  - CmdRunAction("git checkout -b bugfix/<issue-id>")
end
```

---

### 7. Commit Small and Atomic Changes
```plaintext
rule @small_atomic_commits
trigger CmdRunAction(command)
check
  - command contains 'git commit'
  - the commit affects > 50 lines of code
enforce
  - self-examinate: "Is this commit small, focused, and addressing a single change?"
  - ask for user inspection: "The commit modifies ${modified_lines} lines. Consider breaking it into smaller, atomic changes."
end
```

---

### 8. Write Clear Commit Messages
```plaintext
rule @clear_commit_messages
trigger CmdRunAction(command)
check
  - command contains 'git commit'
  - the commit message not follows the format:
    - Summary line: max 50 characters, imperative tone
    - Blank line
    - Detailed description (optional)
enforce
  - ask for user inspection: "The commit message '${commit_message}' does not follow best practices. Should I suggest a clearer format?"
  - self-examinate: "Does the commit message clearly describe the change in imperative mood?"
end
```

---

### 9. Rebase and Sync Before Pushing
```plaintext
rule @rebase_before_push
trigger CmdRunAction(command)
check
  - command contains 'git push'
  - local branch is not up-to-date with the remote branch
enforce
  - CmdRunAction("git fetch --prune")
  - CmdRunAction("git rebase origin/${current_branch}")
  - ask for user inspection: "Your branch is outdated. I have rebased it with the latest changes. Do you want to proceed with the push?"
end
```

---

### 10. Squash Intermediate Fixes Before Final Push
```plaintext
rule @squash_intermediate_fixes
trigger CmdRunAction(command)
check
  - command contains 'git push'
  - there are multiple small intermediate commits with unclear messages
enforce
  - ask for user inspection: "You have multiple intermediate commits. Would you like to squash them into a single commit?"
  - CmdRunAction("git rebase -i HEAD~${commit_count}")
end
```

---

### 11. Tag Fixed Issues with Descriptive Tags
```plaintext
rule @tag_fixed_issue
trigger CmdRunAction(command)
check
  - command contains 'git push'
  - the fix resolves a specific issue (e.g., references to `#<issue-id>`)
enforce
  - CmdRunAction("git tag -a fix-<issue-id> -m 'Fixes issue <issue-id>'")
  - ask for user inspection: "Would you like to tag this commit with 'fix-${issue-id}' for easy tracking?"
end
```

---

### 12. Untracked Files Before Commit
```plaintext
rule @tag_fixed_issue
trigger CmdRunAction(command)
check
  - command contains 'git commit'
  - git workspace has untracked files
enforce
  - ask user to either add to workspace or gitignore
end
```

---

### 13. Prevent Commits to the Main or Protected Branch
```plaintext
rule @prevent_main_branch_commits
trigger CmdRunAction(command)
check
  - command contains 'git commit'
  - the current branch name is 'main' or 'master'
enforce
  - abort action: "Direct commits to the 'main' or 'master' branch are not allowed. Please create a feature or bug-fix branch."
  - suggest: "Run 'git checkout -b <branch-name>' to create a new branch."
end
```

---

### 14. Disallow Large Files in Repository
```plaintext
rule @prevent_large_files
trigger CmdRunAction(command)
check
  - command contains 'git add'
  - any file > 5MB is staged
enforce
  - abort action: "Large files (>5MB) are not allowed in the repository. Please use Git LFS or remove the file."
  - suggest: "Run 'git lfs track <file>' to track large files separately."
end
```

---

### 15. Prevent Commit of Secrets
```plaintext
rule @detect_secrets
trigger CmdRunAction(command)
check
  - command contains 'git commit'
  - staged files contain sensitive patterns (e.g., API keys, passwords)
enforce
  - abort action: "Sensitive data detected (e.g., API keys). Please remove them before committing."
  - suggest: "Use an environment variable or secret management tool to handle sensitive data."
end
```

---

### 16. Ensure All Changes Are Staged
```plaintext
rule @ensure_staged_changes
trigger CmdRunAction(command)
check
  - command contains 'git commit'
  - there are unstaged changes
enforce
  - abort action: "You have unstaged changes. Please add them with 'git add' before committing."
  - suggest: "Run 'git status' to review unstaged changes."
end
```

---

## Summary
These rules ensure that the CodeAct Agent adheres to robust practices for **safety**, **correctness**, and **Git best practices** when fixing bugs, especially for Swe-Bench tasks. By combining automated checks with optional user input, the agent maintains code quality, clarity, and a clean project history.
