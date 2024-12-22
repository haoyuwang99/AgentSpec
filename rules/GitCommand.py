from Command import Command
import re 
import subprocess


class GitCommand(Command):
    def __init__(self, command: str):
        super().__init__(command)
        self.current_branch = self.get_current_branch()
    
    ##helper function
    def get_current_branch(self) -> str:
        """Retrieve the current git branch name."""
        try:
            result = subprocess.check_output(["git", "branch", "--show-current"], stderr=subprocess.DEVNULL)
            return result.decode("utf-8").strip()
        except subprocess.CalledProcessError:
            return "unknown" 
    
    def get_modified_lines(self) -> int:
        """Retrieve the number of lines modified in the commit."""
        try:
            result = subprocess.check_output(["git", "diff", "--cached", "--numstat"], stderr=subprocess.DEVNULL)
            lines = result.decode("utf-8").splitlines()
            total_lines = sum(int(line.split()[0]) + int(line.split()[1]) for line in lines if line)
            return total_lines
        except subprocess.CalledProcessError:
            return 0
         
    def get_commit_message(self) -> str:
        """Retrieve the commit message from the cmd."""
        if not self.is_commit():
            raise ValueError(" ") 
        match = re.search(r"git commit(?: -m '([^']*)'| -m \"([^\"]*)\")", self.command)
        if match:
            # Check for single quotes or double quotes
            return match.group(1) or match.group(2) 
        return ""

    #predicates
    def is_on_dedicated_branch(self) -> bool:
        """Check if the current branch starts with 'bugfix/' or 'fix/'."""
        return self.current_branch.startswith("bugfix/") or self.current_branch.startswith("fix/")

    def is_commit(self) -> str:  
        return "git commit" in self.command

    def is_push(self) -> bool:
        return "git push" in self.command 
    
    def is_minimal_change_commit(self):
        return self.get_modified_lines() <= 50
     
    def is_up_to_date(self) -> bool:
        """Check if the local branch is up-to-date with the remote."""
        if "git push" not in self.command:
            return True

        # Extract target branch from the push command
        match = re.search(r"git push (?:origin )?(\S+)", self.command)
        target_branch = match.group(1) if match else self.current_branch

        try:
            # Fetch remote updates
            subprocess.run(["git", "fetch", "--prune"], check=True, stderr=subprocess.DEVNULL)

            # Check if the local branch is behind the remote
            result = subprocess.check_output(["git", "rev-list", "--left-right", f"{target_branch}...origin/{target_branch}"], stderr=subprocess.DEVNULL)
            behind_commits = [line for line in result.decode("utf-8").splitlines() if line.startswith("<")]

            if behind_commits:
                print(f"Your branch '{target_branch}' is behind the remote branch. Please pull or rebase before pushing.")
                return False
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to check if branch '{target_branch}' is up-to-date.")
            return False
    
    def is_commit_msg_readable(self):
        commit_message = self.get_commit_message()
        lines = commit_message.split("\n") 
        return len(lines)> 50 

    def has_untracked_files(self):
        result = subprocess.check_output(["git", "status", "--porcelain"], stderr=subprocess.DEVNULL)
        lines = result.decode("utf-8").splitlines() 
        return len( lines) > 0 and lines[0].startswith("??")

    def enforce_untracked_files(self):
        """Check for untracked files before committing."""
        if "git commit" in self.command and self.has_untracked_files():
            try:
                result = subprocess.check_output(["git", "status", "--porcelain"], stderr=subprocess.DEVNULL)
                untracked_files = [line[3:] for line in result.decode("utf-8").splitlines() if line.startswith("??")]
                if untracked_files:
                    print("You have untracked files:")
                    for file in untracked_files:  
                        user_response = input(f"Would you like to add {file} to the commit? (y/n): ").strip().lower()
                        if user_response == "y":
                            for file in untracked_files:
                                subprocess.run(["git", "add", file], check=True)
                            print("Untracked files have been added.")
                        else:
                            print("Untracked files were not added.") 
            except subprocess.CalledProcessError:
                print("Failed to check for untracked files.")

    def enforce_branch_rules(self):
        """Enforce rules if the command violates the branch naming policy (i.e., user expect agent commit on specific branch)."""
        if self.is_commit() and not self.is_on_dedicated_branch():
            print(f"Commits should happen on a dedicated bug-fix branch (e.g., 'bugfix/<issue-id>').")
            print(f"You are committing on branch '{self.current_branch}'. Would you like me to create a dedicated branch for this fix?")
            new_branch_name = "bugfix/<issue-id>"  # Placeholder: Replace with actual issue ID handling logic
            print(f"Switching to branch: {new_branch_name}")
            subprocess.run(["git", "checkout", "-b", new_branch_name])


    def enforce_commit_size_rules(self):
        """Enforce rules if the commit modifies too many lines."""
        if self.is_commit() and self.is_complex_commit():  
            print(f"The commit modifies more than 50 lines. Consider breaking it into smaller, atomic changes.")
            print("Is this commit small, focused, and addressing a single change?")


    def enforce_commit_message_rules(self):
        """Enforce rules if the commit message does not follow best practices."""
        if self.is_commit() and not self.has_readable_commit_msg(): 
            commit_message = self.get_commit_message()
            print(f"The commit message '{commit_message}' does not follow best practices.")
            print("Does the commit message clearly describe the change in imperative mood?")
            print("Consider using the format:\n  - Summary line (max 50 characters, imperative tone)\n  - Blank line\n  - Detailed description (optional)")

    def enforce_rebase_before_push(self):
        """Enforce rebase and sync before pushing."""
        if self.is_push() and not self.is_up_to_date():
            try:
                subprocess.run(["git", "rebase", f"origin/{self.current_branch}"], check=True)
                print(f"Your branch '{self.current_branch}' is now up-to-date with the remote branch.")
            except subprocess.CalledProcessError:
                print(f"Failed to rebase the branch '{self.current_branch}'. Please resolve conflicts and retry.")

    def enforce_squash_intermediate_fixes(self):
        """Enforce squashing of intermediate commits before the final push."""
        if self in self.command:
            try:
                result = subprocess.check_output(["git", "log", "--oneline"], stderr=subprocess.DEVNULL)
                commits = result.decode("utf-8").splitlines()
                if len(commits) > 1:
                    print("You have multiple intermediate commits. Consider squashing them into a single commit.")
                    print("Would you like to proceed with an interactive rebase?")
                    subprocess.run(["git", "rebase", "-i", f"HEAD~{len(commits)}"])
            except subprocess.CalledProcessError:
                print("Failed to prepare for squashing commits.")

    def enforce_tagging_fixed_issues(self):
        """Enforce tagging commits that fix specific issues."""
        if "git push" in self.command:
            commit_message = self.get_commit_message()
            match = re.search(r"#(\d+)", commit_message)
            if match:
                issue_id = match.group(1)
                tag_name = f"fix-{issue_id}"
                try:
                    subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Fixes issue {issue_id}"], check=True)
                    print(f"Tagged the commit with '{tag_name}'.")
                except subprocess.CalledProcessError:
                    print(f"Failed to tag the commit with '{tag_name}'.")
 