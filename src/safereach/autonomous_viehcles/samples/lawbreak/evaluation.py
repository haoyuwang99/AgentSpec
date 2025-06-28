from EXtraction import ExtractAll
from AssertionExtraction import SingleAssertion
from map_for_bridge import get_map_info
from GeneticAlgorithm import EncodedTestCase
import pickle

def evaluation(weather):
    map_name = "sunnyvale"
    #map_name = "san"
    map_info = get_map_info(map_name)
    with open('apollo_record/wk_record/S9/Apollo_trace.pickle', 'rb') as file:
        output_Apollo_trace = pickle.load(file)
    file.close()
    with open('apollo_record/wk_record/S9/my_trace.pickle', 'rb') as file:
      output_my_trace = pickle.load(file)
    file.close()
    
    extracted_data = ExtractAll('law.txt', True)
    specifications_in_scenario = extracted_data.Get_Specifications()
    for spec_index in range(len(specifications_in_scenario)):
            first_specification = specifications_in_scenario[spec_index]
            single_specification = SingleAssertion(first_specification, map_info)
            _lawbreak(output_Apollo_trace, single_specification, weather)
            _lawbreak(output_my_trace, single_specification, weather)

def _lawbreak(trace, single_spec, weather):

    encoded_testcase = EncodedTestCase(trace, single_spec, weather)
    
    if encoded_testcase.muti_fitness == {}:
        encoded_testcase.compute_muti_fitness()
    

if __name__ == "__main__":
    weather = {'rain' : 0.0,  'snow': 0.1, 'fog' : 0.0}
    evaluation(weather)