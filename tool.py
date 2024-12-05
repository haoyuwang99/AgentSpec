
def add(a, b) :
    return a + b

class Tool(object): 
    def __init__(self, name, arg_dict) -> None:
        self.name = name
        self.arg_dict = arg_dict 

    def invoke(self):
        # TODO: make it a real tool call
        return {"light": "test", "traffic_id": "vehicle-east-west", "traffic_light_state": "green"}

# class AddTool(BaseTool):
#     def __init__(self) -> None:
#         super().__init__()
#         self.name = "add"

#     def set_id(self, id):
#         self.name = id

#     def get_id(self):
#         return self.name
    
#     def get_signature():
#         return {
#             "input": {
#                 "a" : int,
#                 "b" : int
#             },
#             "output":  [int] 
#         }

#     def run():
#         pass

