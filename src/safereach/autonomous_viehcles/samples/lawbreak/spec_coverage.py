import itertools
import operator

from AssertionExtraction import AllAssertions, SingleAssertion
import copy
from parser.ast import Parse



def remove(s, indx):
    ss = copy.deepcopy(s)
    return ''.join(x for x in ss if ss.index(x) != indx)

# input_file = 'input-test.txt'
# ast_ = Parse(input_file)
# trace_list = ast_.get_traces()
# scenario_name = 'scenario0'
#
# specification_obj = AllAssertions(trace_list)
# specification = specification_obj.get_specifications_in_scenario(scenario_name)
# spec_NO = len(specification)
# map_name = specification_obj.ScenarioMap[scenario_name]
# ego_position = (553090.0522572036, 4182687.8, 0)
# single_spec_class = SingleAssertion(specification[0], map_name, ego_position)
# print(type(single_spec_class.translated_statement))
# print(single_spec_class.translated_statement)
# spec_str = single_spec_class.translated_statement
# operator = ['always', 'and', 'eventually', '->', 'until']
#
# stack = []
# left_bracket_index = []
# right_bracket_index = []
# item_list = []
# index = 0
# predicate = dict()
# total_item  = ""
# item = ""
# atomic_predicate = set()
#
#
# length = len(spec_str)
# new_spec_str = copy.deepcopy(spec_str)
# repeated_bracket =[]
# original_predicate = []
#
# for i in range(length):
#     char = spec_str[i]
#     if char == '(':
#         flag = True
#         stack.append(char)
#         left_bracket_index.append(i)
#     elif char == ')':
#         if len(stack) < 1:
#             label = False
#             break
#         else:
#             left_index = left_bracket_index.pop()
#             item = spec_str[left_index+1: i]
#             if flag:
#                 atomic_predicate.add(item)
#                 flag = False
#             original_predicate.append(item)
#             stack.pop()
#
# deleted_item = []
# for i in range(len(original_predicate)-1):
#     item1 = original_predicate[i+1]
#     item2 = original_predicate[i]
#     if item1.replace(item2, '') == "()":
#         deleted_item.append(i+1)
#
# # deleted_item.sort(reverse=True)
# # for i in deleted_item:
# #     del original_predicate[i]
#
# k = 0
# index = 0
# key_original_predicate = dict()
# atomic_keys = []
#
# keys = []
# for i in range(len(original_predicate)):
#     if original_predicate[i] in atomic_predicate:
#         index += 1
#         key = "x" + str(index)
#         predicate[key] = key
#         atomic_predicate.remove(original_predicate[i])
#         keys.append(key)
#         key_original_predicate[key] = i
#         atomic_keys.append(key)
#     else:
#         item = original_predicate[i]
#         for j in range(len(keys)-1, -1, -1):
#             _key = keys[j]
#             original_index = key_original_predicate[_key]
#             item = item.replace(original_predicate[original_index], _key)
#         item = item.replace("(", "")
#         item = item.replace(")", "")
#         if item in predicate.keys():
#             continue
#         else:
#             index += 1
#             key = "x" + str(index)
#             predicate[key] = item
#             keys.append(key)
#             key_original_predicate[key] = i

# original_predicate: [
#                       'q1>=1.0',
#                       'q2>=1.0',
#                       '(q1>=1.0) and (q2>=1.0)',
#                       'q3>=1.0',
#                       '((q1>=1.0) and (q2>=1.0)) and (q3>=1.0)', '
#                       (((q1>=1.0) and (q2>=1.0)) and (q3>=1.0))',
#                       'q1>=1.0',
#                       '((((q1>=1.0) and (q2>=1.0)) and (q3>=1.0))) -> (q1>=1.0)',
#                       '(((((q1>=1.0) and (q2>=1.0)) and (q3>=1.0))) -> (q1>=1.0))',
#                       'always ((((((q1>=1.0) and (q2>=1.0)) and (q3>=1.0))) -> (q1>=1.0)))',
#                       'q2>=1.0',
#                       'q3>=1.0',
#                       '(q2>=1.0) -> (q3>=1.0)',
#                       '((q2>=1.0) -> (q3>=1.0))',
#                       'eventually (((q2>=1.0) -> (q3>=1.0)))',
#                       '(always ((((((q1>=1.0) and (q2>=1.0)) and (q3>=1.0))) -> (q1>=1.0)))) and (eventually (((q2>=1.0) -> (q3>=1.0))))'
#                       ]

# predicate: {'x1': 'x1',
#             'x2': 'x2',
#             'x3': 'x1 and x2',
#             'x4': 'x4',
#             'x5': 'x3 and x4',
#             'x6': 'x5 -> x1',
#             'x7': 'always x6',
#             'x8': 'x2 -> x4',
#             'x9': 'eventually x8',
#             'x10': 'x7 and x9'}
# key_original_predicate: {'x1': 0, 'x2': 1, 'x3': 2, 'x4': 3, 'x5': 4, 'x6': 7, 'x7': 9, 'x8': 12, 'x9': 14, 'x10': 15}
#                          0 -15 are the index of original_predicate
# atomic_keys: ['x1', 'x2', 'x4']

class failure_statement:
    def __init__(self,specification_string):
        self.spec_str = specification_string
        self.original_predicate = []
        self.predicate = dict()
        self.key_original_predicate = dict()
        self.atomic_keys = []
        self.negative_predicate = dict()
        self._spec_parse()

        print(self.spec_str)
        print(self.key_original_predicate)
        # print( self.predicate)




    def _spec_parse(self):
        stack = []
        left_bracket_index = []
        length = len(self.spec_str)
        atomic_predicate = set()

        for i in range(length):
            char = self.spec_str[i]
            if char == '(':
                flag = True
                stack.append(char)
                left_bracket_index.append(i)
            elif char == ')':
                if len(stack) < 1:
                    break
                else:
                    left_index = left_bracket_index.pop()
                    item = self.spec_str[left_index + 1: i]
                    if flag:
                        atomic_predicate.add(item)
                        flag = False
                    self.original_predicate.append(item)
                    stack.pop()

        deleted_item = []
        for i in range(len(self.original_predicate) - 1):
            item1 = self.original_predicate[i + 1]
            item2 = self.original_predicate[i]
            if item1.replace(item2, '') == "()":
                deleted_item.append(i + 1)

        # print(self.original_predicate)
        index = 0
        keys = []
        for i in range(len(self.original_predicate)):
            if self.original_predicate[i] in atomic_predicate:
                index += 1
                key = "x" + str(index)
                self.predicate[key] = key
                # print(self.predicate[key])
                atomic_predicate.remove(self.original_predicate[i])
                keys.append(key)
                self.key_original_predicate[key] = i
                self.atomic_keys.append(key)
                # print(key)
            else:
                item = self.original_predicate[i]
                for j in range(len(keys) - 1, -1, -1):
                    _key = keys[j]
                    original_index = self.key_original_predicate[_key]
                    item = item.replace(self.original_predicate[original_index], _key)
                item = item.replace("(", "")
                item = item.replace(")", "")
                if item in self.predicate.keys():
                    continue
                else:
                    index += 1
                    key = "x" + str(index)
                    self.predicate[key] = item
                    # print(self.predicate[key])
                    keys.append(key)
                    self.key_original_predicate[key] = i

    def _and(self, list_A, list_B):
        '''
            set_A, set_B: a set of strings
        '''
        combine_list = []
        for item in itertools.product(list_A, list_B):
            _item = '(' + item[0] + ') and (' + item[1] + ')'
            combine_list.append(_item)
        return combine_list

    def _until(self, list_A, list_B):
        '''
            set_A, set_B: a set of strings
        '''
        combine_list = []
        for item in zip(list_A, list_B):
            _item = '(' + item[0] + ') until (' + item[1] + ')'
            combine_list.append(_item)
        return combine_list

    def _next(self, list_A):
        combine_list = []
        for item in list_A:
            _item = 'next (' + item + ')'
            combine_list.append(_item)
        return combine_list

    def _FG_operator(self, list_A, FG_operator):
        '''
            set_A, set_B: a set of strings
        '''
        combine_list = []
        for item in list_A:
            _item = FG_operator + '(' + item + ')'
            combine_list.append(_item)
        return combine_list

    def neg_predicate(self):
        predicate_set = copy.deepcopy(self.predicate)
        proceeded_keys = []
        # unproceeded_keys = []
        for item in predicate_set.keys():
            if item in self.atomic_keys:
                # origin_statement = self.original_predicate[self.key_original_predicate[item]]
                self.negative_predicate[item] = ['not (' + item + ')']
                proceeded_keys.append(item)
                # print(item)
            else:
                _predicate = predicate_set[item]
                _predicate_split = self.predicate[item].split()
                # print(self.predicate[item])
                # print(_predicate_split)
                if 'and' in _predicate:
                    left_key = _predicate_split[0]
                    right_key = _predicate_split[2]
                    if left_key in proceeded_keys and right_key in proceeded_keys:
                        sub_predicate1 = self._and(self.negative_predicate[left_key], [right_key])
                        sub_predicate2 = self._and(self.negative_predicate[left_key], self.negative_predicate[right_key])
                        sub_predicate3 = self._and([left_key], self.negative_predicate[right_key])
                        self.negative_predicate[item] = sub_predicate1 + sub_predicate2 + sub_predicate3
                        proceeded_keys.append(item)
                    # else:
                    #     unproceeded_keys.append(item)
                elif 'or' in _predicate:
                    left_key = _predicate_split[0]
                    right_key = _predicate_split[2]
                    if left_key in proceeded_keys and right_key in proceeded_keys:
                        sub_predicate = self._and(self.negative_predicate[left_key], self.negative_predicate[right_key])
                        self.negative_predicate[item] = sub_predicate
                        proceeded_keys.append(item)
                    # else:
                    #     unproceeded_keys.append(item)
                elif '->' in _predicate:
                    left_key = _predicate_split[0]
                    right_key = _predicate_split[2]
                    if left_key in proceeded_keys and right_key in proceeded_keys:
                        sub_predicate = self._and([left_key], self.negative_predicate[right_key])
                        self.negative_predicate[item] = sub_predicate
                        proceeded_keys.append(item)
                elif 'not' in _predicate:
                    key = _predicate_split[1]
                    self.negative_predicate[item] = key
                    proceeded_keys.append(item)
                elif 'always' in _predicate:
                    key = _predicate_split[1]
                    operator0 = _predicate_split[0]
                    operator0 = operator0.replace("always", "eventually")
                    if key in proceeded_keys:
                        sub_predicate = self._FG_operator(self.negative_predicate[key], operator0)
                        self.negative_predicate[item] = sub_predicate
                        proceeded_keys.append(item)
                elif 'eventually' in _predicate:
                    key = _predicate_split[1]
                    operator0 = _predicate_split[0]
                    operator0 = operator0.replace("eventually", "always")            
                    if key in proceeded_keys:
                        sub_predicate = self._FG_operator(self.negative_predicate[key], operator0)
                        self.negative_predicate[item] = sub_predicate
                        proceeded_keys.append(item)
                elif 'until' in _predicate:
                    left_key = _predicate_split[0]
                    right_key = _predicate_split[2]
                    if left_key in proceeded_keys and right_key in proceeded_keys:
                        sub_predicate1 = self._and(self.negative_predicate[left_key], self.negative_predicate[right_key])
                        sub_predicate2 = self._and([left_key], self.negative_predicate[right_key])
                        sub_predicate3 = self._until(sub_predicate2, sub_predicate1)
                        self.negative_predicate[item] = sub_predicate1 + sub_predicate3
                        proceeded_keys.append(item)
                elif 'next' in _predicate:
                    key = _predicate[1]
                    if key in proceeded_keys:
                        sub_predicate   = self._next(self.negative_predicate[key])
                        self.negative_predicate[item] = sub_predicate
                        proceeded_keys.append(item)
        if len(proceeded_keys) < len(predicate_set.keys()):
            pass

        final_item = max(self.key_original_predicate.items(), key=operator.itemgetter(1))[0]
        final_negative = self.negative_predicate[final_item]
        final_negative_origin = []
        for i in range(len(final_negative)):
            statement_i = final_negative[i]
            for item in self.predicate.keys():
                old_string = '(' + item + ')'
                origin_state = self.original_predicate[self.key_original_predicate[item]]
                new_string = '(' + origin_state + ')'
                statement_i = statement_i.replace(old_string, new_string)
            final_negative_origin.append(statement_i)
        return final_negative_origin






if __name__ == "__main__":
    input_file = 'input-test.txt'
    ast_ = Parse(input_file)
    trace_list = ast_.get_traces()
    scenario_name = 'scenario0'

    specification_obj = AllAssertions(trace_list)
    specification = specification_obj.get_specifications_in_scenario(scenario_name)
    spec_NO = len(specification)
    map_name = specification_obj.ScenarioMap[scenario_name]
    ego_position = (553090.0522572036, 4182687.8, 0)
    single_spec_class = SingleAssertion(specification[0], map_name, ego_position)
    print(type(single_spec_class.translated_statement))
    print(single_spec_class.translated_statement)
    spec_str = single_spec_class.translated_statement
    parser = failure_statement(spec_str)
    all_predicate = parser.neg_predicate()
    print(parser)




