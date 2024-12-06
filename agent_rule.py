class Rule:

    def __init__(self, rule_str, event) -> None:
        self.rule_str = rule_str
        self.event = event

    def triggered(self, action_name):
        return self.event == "any" or action_name == self.event
    
    