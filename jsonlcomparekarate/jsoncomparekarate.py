import json
import re

class _Compare(object):
    def __init__(self):
        self.is_in1_template = False
        self.is_in2_template = False
        self.supported_hash_types = ["#string", "#integer", "#float", "#boolean", "#bool", "#number", "#object", "#list",
                                     "#[", "#regex"]

    # Documentation
    # This function checks if the input is a valid JSON object. Returns True if the input is a valid JSON object, else
    # returns False.
    def is_valid_json_object(self, json_input):
        if isinstance(json_input, (dict, list)):
            try:
                # Try to serialize the object back to a JSON string
                json.dumps(json_input)
                return True  # If serialization is successful, it's a valid JSON object
            except (TypeError, ValueError):
                return False  # If serialization fails, it's not a valid JSON-like object
        return False  # If it's not a dictionary or list, it's not valid JSON-like object

    # Documentation
    # This function compares two JSONs. It takes two inputs, input_json1 and input_json2. It iterates over the keys of
    # input_json1 and compares the values of the keys in input_json1 with the corresponding keys in input_json2. If the
    # value of a key in input_json1 is a string and starts with "#", it is considered as a template value. The function
    # then compares the value of the key in input_json2 with the template value. If the value of a key in input_json1 is
    # a dictionary, the function recursively calls itself to compare the values of the keys in the dictionary. If the
    # value of a key in input_json1 is a list, the function compares the values of the elements in the list. If the
    # value of a key in input_json1 is a string, boolean, integer, or float, the function compares the value of the key
    # in input_json2 with the value of the key in input_json1. If the values are not equal, the function returns False.
    # If the values are equal, the function returns True.
    # Parameters
    # input_json1: dict (can be a template)
    # input_json2: dict
    def compare_jsons(self, input_json1, input_json2):
        for (k1, v1) in input_json1.items():
            #print(f"Starting comparison for key: {k1}, Expected Value: {v1}")

            # if the value is an optional value: specified by ##object, do nothing and continue
            if isinstance(v1, str) and v1.startswith("##"):
                continue

            # if the value is a string and starts with #, it is a template value so we need to compare it with the
            # corresponding value in input_json2
            if isinstance(v1, str) and v1.startswith("#"):

                #remove spaces and convert to lower case
                v1_no_space = v1.replace(" ", "").lower()

                if v1_no_space == "#string":
                    # if v1 is #string, in input_json2 ensure that v2 is a string; if not, return False, else continue
                    if not (k1 in input_json2 and isinstance(input_json2[k1], str)):
                        return False
                    else:
                        continue
                elif v1_no_space == "#integer":
                    # if v1 is #integer, in input_json2 ensure that v2 is a integer; if not, return False, else continue
                    if not (k1 in input_json2 and isinstance(input_json2[k1], int)):
                        return False
                    else:
                        continue
                elif v1_no_space == "#float":
                    # if v1 is #float, in input_json2 ensure that v2 is a float; if not, return False, else continue
                    if not (k1 in input_json2 and isinstance(input_json2[k1], float)):
                        return False
                    else:
                        continue
                elif v1_no_space == "#boolean" or v1 == "#bool":
                    # if v1 is #boolean, in input_json2 ensure that v2 is a boolean; if not, return False, else continue
                    if not (k1 in input_json2 and isinstance(input_json2[k1], bool)):
                        return False
                    else:
                        continue
                elif v1_no_space == "#number":
                    # if v1 is #number, in input_json2 ensure that v2 is a number; if not, return False, else continue
                    if not (k1 in input_json2 and (isinstance(input_json2[k1], int) or isinstance(input_json2[k1], float))):
                        return False
                    else:
                        continue
                elif v1_no_space == "#object":
                    # if v1 is #pbject, in input_json2 ensure that v2 is a dictionary; if not, return False, else continue
                    if not (k1 in input_json2 and isinstance(input_json2[k1], dict)):
                        return False
                    else:
                        continue
                elif v1_no_space == "#list":
                    # if v1 is #list, in input_json2 ensure that v2 is a list; if not, return False, else continue
                    if not (k1 in input_json2 and isinstance(input_json2[k1], list)):
                        return False
                    else:
                        continue
                elif v1_no_space.startswith("#["):
                    # if v1 starts with #[, in input_json2 ensure that v2 is a list of appropriate length; if not,
                    # return False, else continue
                    if v1_no_space == "#[]":
                        if not (k1 in input_json2 and isinstance(input_json2[k1], list) and len(input_json2[k1]) == 0):
                            return False
                        else:
                            continue
                    elif v1_no_space == "#[_>0]":
                        if not (k1 in input_json2 and isinstance(input_json2[k1], list) and len(input_json2[k1]) > 0):
                            return False
                        else:
                            continue
                    elif v1_no_space == "#[_>=0]":
                        if not (k1 in input_json2 and isinstance(input_json2[k1], list) and len(input_json2[k1]) >= 0):
                            return False
                        else:
                            continue
                    else:
                        print(f"Invalid list value found: {v1}")
                elif v1_no_space.startswith("#regex"):
                    # if v1 starts #regex, in input_json2 ensure that v2 matches the regex; if not, return False, else
                    # continue
                    #print(f"In the regex block: {v1}")
                    if v1_no_space.startswith("#regex"):
                        v1 = v1.replace("#regex ", "")
                    if not (k1 in input_json2):
                        return False
                    else:
                        v2 = input_json2[k1]
                        find = re.findall(v1, v2)
                        assert len(find) > 0, f"Cannot find the pattern in the string {v2}"
                        if not find:
                            print("re compare failed, empty match, see next line")
                            return False
                        if not find[0] == v2:
                            print(f"re compare failed, found {find[0]}, expect {v2}, see next line")
                            return False
                        continue
                else:
                    print(f"Invalid value found: {v1}")

            # if the value is string compare it with the corresponding value in input_json2 and continue if same, else
            # return False
            if isinstance(v1, str):
                if k1 in input_json2 and isinstance(input_json2[k1], str) and input_json1[k1] == input_json2[k1]:
                    continue
                else:
                    return False

            # if the value is boolean compare it with the corresponding value in input_json2 and continue if same, else
            # return False
            if isinstance(v1, bool):
                if k1 in input_json2 and isinstance(input_json2[k1], bool) and input_json1[k1] == input_json2[k1]:
                    continue
                else:
                    return False

            # if the value is int or float compare it with the corresponding value in input_json2 and continue if same,
            # else return False
            if isinstance(v1, int) or isinstance(v1, float):
                if k1 in input_json2 and (isinstance(input_json2[k1], int) or isinstance(input_json2[k1], float)) and input_json1[k1] == input_json2[k1]:
                    continue
                else:
                    return False

            # if the value is dictionary, iterate over all the key value pairs; return False if mismatch, continue if
            # all matches
            if isinstance(v1, dict):
                d1 = input_json1[k1]
                if k1 in input_json2 and isinstance(input_json2[k1], dict):
                    d2 = input_json2[k1]
                    return self.compare_jsons(d1, d2)

            # if the value is list, compare the elements of the list. If the lists are different, return False, else
            # continue
            if isinstance(v1, list):
                l1 = input_json1[k1]
                l2 = None
                if k1 in input_json2 and isinstance(input_json2[k1], list):
                    l2 = input_json2[k1]
                    if len(l1) != len(l2):
                        print(f"Lengths of lists for key {k1} are different: {l1}, {l2}")
                        return False
                return self.compare_lists(l1, l2)
        return True

    # Documentation
    # This function validates the input dictionaries for key value based comparison. It takes two inputs, input_dict1
    # and input_dict2. If any of the supported_hash_types are present in the input dictionaries, then they are marked as
    # template dictionary. The template dictionary has values indicating the type of value expected for a given key. The
    # values in the template dictionary can also indicate present or absence of a particular key. The function also
    # ensures that only one of the two input dictionaries is a template and throws an error if both inputs are
    # templates. Further it compares the two dictionaries and if the values are not equal, the function returns False.
    # If the values are equal, the function returns True.
    def compare_dicts(self, input_dict1, input_dict2):
        self.is_in1_template = False
        self.is_in2_template = False
        ijd1 = json.dumps(input_dict1)
        ijd2 = json.dumps(input_dict2)

        if any(x in ijd1 for x in self.supported_hash_types):
            self.is_in1_template = True
            #print("Hash found in input_json1")
        if any(x in ijd2 for x in self.supported_hash_types):
            self.is_in2_template = True
            #print("Hash found in input_json2")

        if self.is_in1_template and self.is_in2_template:
            print("Template is a JSON which has values referring to optional fields")
            raise Exception("Both inputs are templates. Only one input can be a template")

        if self.is_in2_template:
            #print("flipping the input dictionaries for internal comparison")
            return self.compare_jsons(input_dict2, input_dict1)
        else:
            return self.compare_jsons(input_dict1, input_dict2)

    # Documentation
    # This function compares the elements of two lists in order. If one of the elements in the list is a template or is
    # of the type list or dictionary, it will compare the elements of both lists accordingly.
    def compare_list_elements_in_order(self, input_list1, input_list2):
        for i, elem in enumerate(input_list1):
            if isinstance(elem, str) and elem.startswith("#regex"):
                a = elem.replace("#regex ", "")
                b = input_list2[i]
                find = re.findall(a, b)
                if not find:
                    return False
            elif isinstance(elem, dict):
                if not self.compare_jsons(elem, input_list2[i]):
                    return False
            elif isinstance(elem, list):
                if not self.compare_lists(elem, input_list2[i]):
                    return False
            else:
                if elem != input_list2[i]:
                    return False
        return True

    def compare_list_elements_out_of_order(self, input_list1, input_list2):
        if input_list1[0] and isinstance(input_list1[0], dict):
            ils1 = sorted(input_list1, key=lambda x: str(x))
            ils2 = sorted(input_list2, key=lambda x: str(x))
            return self.compare_list_elements_in_order(ils1, ils2)
        elif input_list1[0] and isinstance(input_list1[0], list):
            ils1 = sorted(input_list1)
            ils2 = sorted(input_list2)
            return self.compare_list_elements_in_order(ils1, ils2)
        else:
            ils1 = sorted(input_list1)
            ils2 = sorted(input_list2)
            return ils1 == ils2


    # Documentation
    # This function compares two lists, input_list1 and input_list2. It takes two inputs, input_list1 and input_list2.
    # Unless one of the lists is a template or in_order is set to True, the lists will be compared out of order. If all
    # the elements in the list are not of the same type, the function will do in order comparison.
    def compare_lists(self, input_list1, input_list2, in_order=False):
        #print(f"input_list1: {input_list1}, input_list2: {input_list2}")
        self.is_in1_template = False
        self.is_in2_template = False

        # check if all elements in the list are of the same type, if not then return False
        if len(input_list1) and not all(type(item) == type(input_list1[0]) for item in input_list1):
            in_order = True
        if len(input_list2) and not all(type(item) == type(input_list2[0]) for item in input_list2):
            in_order = True

        for elem in input_list1:
            if isinstance(elem, str) and any(x in elem for x in self.supported_hash_types):
                self.is_in1_template = True
                #print("Hash found in input_list1")
                break
        for elem in input_list2:
            if isinstance(elem, str) and any(x in elem for x in self.supported_hash_types):
                self.is_in2_template = True
                #print("Hash found in input_list2")
                break

        if self.is_in1_template and self.is_in2_template:
            print("Template is a List which has values referring to optional fields")
            raise Exception("Both inputs are templates. Only one input can be a template")

        if len(input_list1) != len(input_list2):
            print(f"Lengths of list1 ({len(input_list1)}) and list2 ({len(input_list2)}) are different")
            return False

        if self.is_in2_template:
            #print("flipping the input lists for internal comparison")
            input_list1, input_list2 = input_list2, input_list1

        if (self.is_in1_template or self.is_in2_template) or in_order:
            # one of the lists is a template and so we need to do in order comparison
            return self.compare_list_elements_in_order(input_list1, input_list2)
        else:
            # none of the lists are templates and so we can do out of order comparison
            return self.compare_list_elements_out_of_order(input_list1, input_list2)

    # Documentation
    # This function compares two inputs, in1 and in2. If the inputs are lists, the function calls the compare_lists
    # function. If the inputs are dictionaries, the function calls the compare_dicts function. If the inputs are not
    # lists or dictionaries, the function compares the inputs directly. If the inputs are equal, the function returns
    # True. If the inputs are not equal, the function returns False.
    def compare(self, in1, in2, strict_json_check):
        print(f"in1: {in1}, in1 type: {type(in1)}, in2: {in2}, int2 type: {type(in2)}")
        if strict_json_check:
            assert self.is_valid_json_object(in1)
            assert self.is_valid_json_object(in2)

        if isinstance(in1, list) and isinstance(in2, list):
            return self.compare_lists(in1, in2)
        elif isinstance(in1, dict) and isinstance(in2, dict):
            return self.compare_dicts(in1, in2)
        else:
            #print(f"{type(in1)} and {type(in2)} are not of type list or dict. Doing direct comparison..")
            return in1 == in2

def compare(a, b, strict_json_check=False):
    return _Compare().compare(a, b, strict_json_check)
