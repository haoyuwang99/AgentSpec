import copy

from parser.ast import Parse
# from TestCaseExtraction import AllTestCase
from AssertionExtraction import AllAssertions
import json

class ExtractAll:
    def __init__(self, inputfile, isGroundTruth):
        _ast = Parse(inputfile)
        self.SpecificationObj = AllAssertions(_ast.get_traces())

    def Get_Specifications(self):
        _specification = copy.deepcopy(self.SpecificationObj.ScenarioSpec)
        return _specification


if __name__ == "__main__":
    file = 'test_cases/input_test.txt'
    isGroundTruth = True
    extracted_data = ExtractAll(file, isGroundTruth)
    agents = extracted_data.Get_AllAgents()
    print(agents)
    testcases = extracted_data.Get_TestCastINJsonList()
    spec = extracted_data.Get_Specifications()
    maps = extracted_data.Get_AllMaps()
    for i in range(len(testcases)):
        print(testcases[i])
    scenario_name = testcases[0]['ScenarioName']
    for i in range(len(spec[scenario_name])):
        print(spec[scenario_name][i])



