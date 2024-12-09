from abc import abstractmethod

ENFORCEMENT_TO_CLASS = {
    
}
class EnforceResult:
    CONTINUE = 1
    SELF_REFLECT = 2
    FINISH = 3

def none():
    return EnforceResult.CONTINUE

def llm_self_reflect():
    return EnforceResult.SELF_REFLECT

def user_inspection():
    return EnforceResult.FINISH

class Enforcement :  
    enforcements = {
        "none" : none,
        "llm_self_reflect": llm_self_reflect,
        "user_inspection" : user_inspection
     }

    def __init__(self, enforce) -> None:
        # index enforcement function 
        self.enforce = enforce

    def get_name(self):
        return self.enforce
    
    @abstractmethod
    def apply(self) -> EnforceResult:
        # todo: ENCAPSULATE THE ENFORCEMENT LOGIC HERE
        return self.enforcements[self.enforce]() 