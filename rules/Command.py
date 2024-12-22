import re

# general property for command
class Command:
    def __init__(self, command: str):
        self.command = command 

    def is_non_destructive(self) -> bool:
        """Check if the command contains destructive operations."""
        destructive_patterns = [r"\brm\b", r"\bdd\b", r"\bsudo\b"]
        return not any(re.search(pattern, self.command) for pattern in destructive_patterns)

    def has_critical_redirection(self) -> bool:
        """Check if the command avoids redirections to system-critical paths."""
        critical_paths = [r"/dev/", r"/bin/"]
        redirection_patterns = [r">\s*(\S+)", r"\|\s*(\S+)"]  # Matches > or |
        for redirection in redirection_patterns:
            matches = re.findall(redirection, self.command)
            for match in matches:
                if any(critical_path in match for critical_path in critical_paths):
                    return False
        return True

    def is_within_length_limit(self, length_limit: int = 200) -> bool:
        """Check if the command length is within the specified limit."""
        return len(self.command) <= length_limit
    
 