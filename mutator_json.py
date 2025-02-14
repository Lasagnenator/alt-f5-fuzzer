import sys
import json
import numpy as np
from mutator_base import BaseMutator
from format_finder import try_json
from typing import Any

class JsonIntMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        int_index = int.from_bytes(input[0].tobytes()[2:4], "little")
        int_set = int.from_bytes(input[1].tobytes()[2:4], "little")
        multiplier = (input[1] * 2 - 1) * int_set

        if not try_json(text):
            return text
        try:
            j = json.loads(text)
            if isinstance(j, dict):
                int_index %= json_count_dict(j, int)
                json_update_dict(j, int, int_index, multiplier, 0)
            elif isinstance(j, list):
                int_index %= json_count_list(j, int)
                json_update_list(j, int, int_index, multiplier, 0)

            return json.dumps(j).encode()
        except:
            return text

    def get_dimension(self) -> "int":
        """
        First element of vector = which int to modify
        Second element of vector = what to set it to.
        """
        return 2

    def get_name(self) -> "str":
        return "Change an int in json"

class JsonExtremeIntMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        int_index = int.from_bytes(input[0].tobytes()[2:4], "little")
        multiplier = input[1] * 2 - 1

        if multiplier <= -0.99: multiplier = -sys.maxsize - 1
        elif -0.01 <= multiplier <= 0.01: multiplier = 0
        elif multiplier >= 0.99: multiplier = sys.maxsize

        if not try_json(text):
            return text
        j = json.loads(text)
        if isinstance(j, dict):
            int_index %= json_count_dict(j, int)
            json_update_dict(j, int, int_index, multiplier, 0)
        elif isinstance(j, list):
            int_index %= json_count_list(j, int)
            json_update_list(j, int, int_index, multiplier, 0)

        return json.dumps(j).encode()

    def get_dimension(self) -> "int":
        """
        First element of vector = which int to modify
        Second element of vector = what to set it to.
        """
        return 2

    def get_name(self) -> "str":
        return "Change an int to extreme values in json"

class JsonFloatInfMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        float_index = int.from_bytes(input[0].tobytes()[2:4], "little")
        multiplier = input[1] * 2 - 1
 
        if multiplier <= -0.99: multiplier = float("-inf")
        elif -0.01 <= multiplier <= 0.01: multiplier = 0.0
        elif multiplier >= 0.99: multiplier = float("inf")

        if not try_json(text):
            return text
        try:
            j = json.loads(text)
            if isinstance(j, dict):
                float_index %= json_count_dict(j, float)
                json_update_dict(j, float, float_index, multiplier, 0)
            elif isinstance(j, list):
                float_index %= json_count_list(j, float)
                json_update_list(j, float, float_index, multiplier, 0)

            return json.dumps(j).encode()
        except:
            return text

    def get_dimension(self) -> "int":
        """
        First element of vector = which float to modify
        Second element of vector = what to set it to.
        """
        return 2

    def get_name(self) -> "str":
        return "Change a float to +-inf in json"

class JsonFloatNanMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        float_index = int.from_bytes(input[0].tobytes()[2:4], "little")
        multiplier = input[1] * 2 - 1
 
        if multiplier <= -0.99: multiplier = float("nan")
        elif -0.01 <= multiplier <= 0.01: multiplier = 0.0
        elif multiplier >= 0.99: multiplier = float("nan")

        if not try_json(text):
            return text
        j = json.loads(text)
        if isinstance(j, dict):
            float_index %= json_count_dict(j, float)
            json_update_dict(j, float, float_index, multiplier, 0)
        elif isinstance(j, list):
            float_index %= json_count_list(j, float)
            json_update_list(j, float, float_index, multiplier, 0)

        return json.dumps(j).encode()

    def get_dimension(self) -> "int":
        """
        First element of vector = which float to modify
        Second element of vector = what to set it to.
        """
        return 2

    def get_name(self) -> "str":
        return "Change a float to nan in json"

class JsonListRepeatMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        list_index = int.from_bytes(input[0].tobytes()[2:4], "little") % len(text)
        multiplier = int.from_bytes(input[1].tobytes()[2:4], "little")

        if len(text) * multiplier > 10000: return text

        if not try_json(text):
            return text
        j = json.loads(text)
        if isinstance(j, dict):
            json_update_dict(j, list, list_index, multiplier, 0)
        elif isinstance(j, list):
            json_update_list(j, list, list_index, multiplier, 0)

        return json.dumps(j).encode()

    def get_dimension(self) -> "int":
        """
        First element of vector = which list to modify
        Second element of vector = number to repeat
        """
        return 2

    def get_name(self) -> "str":
        return "Repeat a list in json"

class JsonEntryRepeatMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        key_index = int.from_bytes(input[0].tobytes()[2:4], "little") % len(text)
        multiplier = int.from_bytes(input[1].tobytes()[2:4], "little")

        if len(text) * multiplier > 10000: return text

        if not try_json(text):
            return text
        j = json.loads(text)
        if isinstance(j, dict):
            json_update_dict(j, (str, Any), key_index, multiplier, 0)
        elif isinstance(j, list):
            json_update_list(j, (str, Any), key_index, multiplier, 0)

        return json.dumps(j).encode()

    def get_dimension(self) -> "int":
        """
        First element of vector = which key to modify
        Second element of vector = number to repeat
        """
        return 2

    def get_name(self) -> "str":
        return "Repeat a key in json"

class JsonChangeTypeMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        index = int.from_bytes(input[0].tobytes()[2:4], "little") % len(text)

        type_from = self.get_type(input[1])
        type_to = self.get_type(input[2])

        if not try_json(text):
            return text
        j = json.loads(text)
        if isinstance(j, dict):
            json_update_type_dict(j, type_from, type_to, index, 0)
        elif isinstance(j, list):
            json_update_type_list(j, type_from, type_to, index, 0)

        return json.dumps(j).encode()

    def get_dimension(self) -> "int":
        """
        First element of vector = which element to modify
        Second element of vector = which type to modify
        Third element of vector = type to change to
        """
        return 3

    def get_name(self) -> "str":
        return "Change a type in json"
    
    def get_type(self, int):
        if int <= 0.2: return 'int'
        elif 0.2 < int <= 0.4: return 'float'
        elif 0.4 < int <= 0.6: return 'str'
        elif 0.6 < int <= 0.8: return 'list'
        elif int > 0.8: return 'dict'

def json_update_dict(json: dict, target_type, target_index: int, multiplier: float, cur_index = 0):
    for k, v in json.items():
        if target_type == (str, Any):
            if cur_index == target_index:
                if multiplier == 0:
                    json.pop(k)
                elif multiplier > 1:
                    for i in range(0, multiplier):
                        json.add(k, v)
                return
            cur_index += 1
        elif isinstance(v, target_type):
            if cur_index == target_index:
                json[k] = target_type(json[k] * multiplier)
                return
            cur_index += 1
        elif isinstance(v, dict):
            json_update_dict(v, target_type, target_index, multiplier, cur_index)
        elif isinstance(v, list):
            json_update_list(v, target_type, target_index, multiplier, cur_index)

def json_update_list(json: list, target_type, target_index: int, multiplier: float, cur_index = 0):
    for i, v in enumerate(json):
        if target_type == (str, Any):
            if cur_index == target_index:
                if multiplier == 0:
                    json.pop(i)
                elif multiplier > 1:
                    for k in range(0, multiplier):
                        json.add(i, v)
                return
            cur_index += 1
        elif isinstance(v, target_type):
            if cur_index == target_index:
                json[i] = target_type(json[i] * multiplier)
                return
            cur_index += 1
        elif isinstance(v, dict):
            json_update_dict(v, target_type, target_index, multiplier, cur_index)
        elif isinstance(v, list):
            json_update_list(v, target_type, target_index, multiplier, cur_index)

def json_count_dict(json: dict, target_type):
    count = 0
    for k, v in json.items():
        if isinstance(v, target_type):
            count += 1
        elif isinstance(v, dict):
            count += json_count_dict(v, target_type)
        elif isinstance(v, list):
            count += json_count_list(v, target_type)
    return count

def json_count_list(json: list, target_type):
    count = 0
    for i, v in enumerate(json):
        if isinstance(v, target_type):
            count += 1
        elif isinstance(v, dict):
            count += json_count_dict(v, target_type)
        elif isinstance(v, list):
            count += json_count_list(v, target_type)
    return count

def json_update_type_dict(json: dict, type_from, type_to, target_index: int, cur_index = 0):
    for k, v in json.items():
        if type_from == 'str':
            if isinstance(k, str) and cur_index == target_index:
                if type_to == 'str':
                    return

                json[change_from_str(k, type_to)] = json.pop(k)
                return
            elif isinstance(v, str) and cur_index == target_index:
                if type_to == 'str':
                    return

                json[k] = change_from_str(v, type_to)
                return
            cur_index += 1
        elif type_from == 'int':
            if isinstance(k, int) and cur_index == target_index:
                if type_to == 'int':
                    return

                json[change_from_int(k, type_to)] = json.pop(k)
                return
            elif isinstance(v, int) and cur_index == target_index:
                if type_to == 'int':
                    return

                json[k] = change_from_int(v, type_to)
                return
            cur_index += 1
        elif type_from == 'float':
            if isinstance(k, float) and cur_index == target_index:
                if type_to == 'float':
                    return

                json[change_from_float(k, type_to)] = json.pop(k)
                return
            elif isinstance(v, float) and cur_index == target_index:
                if type_to == 'float':
                    return

                json[k] = change_from_float(v, type_to)
                return
            cur_index += 1
        elif type_from == 'list':
            if isinstance(k, list) and cur_index == target_index:
                if type_to == 'list':
                    return

                json[change_from_list(k, type_to)] = json.pop(k)
                return
            elif isinstance(v, list) and cur_index == target_index:
                if type_to == 'list':
                    return

                json[k] = change_from_list(v, type_to)
                return
            cur_index += 1
        elif type_from == 'dict':
            if isinstance(k, dict) and cur_index == target_index:
                if type_to == 'dict':
                    return

                json[change_from_dict(k, type_to)] = json.pop(k)
                return
            elif isinstance(v, dict) and cur_index == target_index:
                if type_to == 'dict':
                    return

                json[k] = change_from_dict(v, type_to)
                return
            cur_index += 1
        elif isinstance(v, dict):
            json_update_dict(v, type_from, type_to, target_index, cur_index)
        elif isinstance(v, list):
            json_update_list(v, type_from, type_to, target_index, cur_index)

def json_update_type_list(json: dict, type_from, type_to, target_index: int, cur_index = 0):
    for i, v in enumerate(json):
        if type_from == 'str':
            if isinstance(i, str) and cur_index == target_index:
                if type_to == 'str':
                    return

                json[change_from_str(i, type_to)] = json.pop(i)
                return
            elif isinstance(v, str) and cur_index == target_index:
                    if type_to == 'str':
                        return

                    json[i] = change_from_str(v, type_to)
                    return
            cur_index += 1
        elif type_from == 'int':
            if isinstance(i, int) and cur_index == target_index:
                if type_to == 'int':
                    return

                json[change_from_int(i, type_to)] = json.pop(i)
                return
            elif isinstance(v, int) and cur_index == target_index:
                if type_to == 'int':
                    return

                json[i] = change_from_int(v, type_to)
                return
            cur_index += 1
        elif type_from == 'float':
            if isinstance(i, float) and cur_index == target_index:
                if type_to == 'float':
                    return

                json[change_from_float(i, type_to)] = json.pop(i)
                return
            elif isinstance(v, float) and cur_index == target_index:
                if type_to == 'float':
                    return

                json[i] = change_from_float(v, type_to)
                return
            cur_index += 1
        elif type_from == 'list':
            if isinstance(i, list) and cur_index == target_index:
                if type_to == 'list':
                    return

                json[change_from_list(i, type_to)] = json.pop(i)
                return
            elif isinstance(v, list) and cur_index == target_index:
                if type_to == 'list':
                    return

                json[i] = change_from_list(v, type_to)
                return
            cur_index += 1
        elif type_from == 'dict':
            if isinstance(i, dict) and cur_index == target_index:
                if type_to == 'dict':
                    return

                json[change_from_dict(i, type_to)] = json.pop(i)
                return
            elif isinstance(v, dict) and cur_index == target_index:
                if type_to == 'dict':
                    return

                json[i] = change_from_dict(v, type_to)
                return
            cur_index += 1
        elif isinstance(v, dict):
            json_update_dict(v, type_from, type_to, target_index, cur_index)
        elif isinstance(v, list):
            json_update_list(v, type_from, type_to, target_index, cur_index)

def change_from_str(k, type_to):
    new = ''
    if type_to == 'float':
        new = f'{int.from_bytes(k.encode()[2:4], "little")}.0'
    elif type_to == 'int':
        new = int.from_bytes(k.encode()[2:4], "little")
    elif type_to == 'list':
        new = f'[{k}]'
    else:
        new = '{"' + f'{k}": "{k}' + '"}'

    return new

def change_from_int(k, type_to):
    new = ''
    if type_to == 'float':
        new = f'{k}.0'
    elif type_to == 'str':
        new = f'"{k}"'
    elif type_to == 'list':
        new = f'[{k}]'
    else:
        new = '{"' + f'{k}": "{k}' + '"}'

    return new

def change_from_float(k, type_to):
    new = ''
    if type_to == 'int':
        new = f'{int(k)}'
    elif type_to == 'str':
        new = f'"{k}"'
    elif type_to == 'list':
        new = f'[{k}]'
    else:
        new = '{"' + f'{k}": "{k}' + '"}'

    return new

def change_from_list(k, type_to):
    new = ''
    if type_to == 'int':
        new = int.from_bytes(k.encode()[2:4], "little")
    elif type_to == 'str':
        new = ', '.join(item.strip() for item in k[1:-1].split(","))
    elif type_to == 'float':
        new = f'{int.from_bytes(k.encode()[2:4], "little")}.0'
    else:
        new = '{"' + f'{k}": "{k}' + '"}'

    return new

def change_from_dict(k, type_to):
    new = ''
    if type_to == 'int':
        new = int.from_bytes(k.encode()[2:4], "little")
    elif type_to == 'str':
        new = f'{k}'
    elif type_to == 'float':
        new = f'{int.from_bytes(k.encode()[2:4], "little")}.0'
    else:
        new = '["' + f'{k}": "{k}' + '"]'

    return new
