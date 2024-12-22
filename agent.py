from abc import abstractmethod

class Action():

    def from_langchain():
        pass
    
    def from_gym():
        pass

    pass

class ControlledAgent():

    @abstractmethod
    def plan():
        pass

    @abstractmethod
    def invoke():
        pass