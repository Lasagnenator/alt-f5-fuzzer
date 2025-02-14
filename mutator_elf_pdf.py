import numpy as np
from mutator_base import BaseMutator
import random

class ELFPDFInsertMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        length = len(text)
        if length == 0: return text
        index = int.from_bytes(input[0].tobytes()[2:4], "little") % len(text)
        insert = int.from_bytes(input[1].tobytes()[2:7], "little") % len(text)

        if len(text) >= 10000: return text
        return text[:index] + insert.to_bytes(5, "little") + text[index:]

    def get_dimension(self) -> "int":
        """
        First element of vector = index to insert
        Second element of vector = byte to insert
        """
        return 2
    
    def get_name(self) -> "str":
        return "Insert input between two indexes"

class ELFPDFReplaceMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        length = len(text)
        if length == 0: return text
        start = int.from_bytes(input[0].tobytes()[2:4], "little") % len(text)
        end = int.from_bytes(input[1].tobytes()[2:4], "little") % len(text)
        insert = int.from_bytes(input[2].tobytes()[2:6], "little") % len(text)

        if len(text) >= 10000: return text
        if end < start:
            return text[:end] + insert.to_bytes(4, "little") + text[start:]
        else:
            return text[:start] + insert.to_bytes(4, "little") + text[end:]

    def get_dimension(self) -> "int":
        """
        First element of vector = index to insert
        Second element of vector = byte to insert
        """
        return 3
    
    def get_name(self) -> "str":
        return "Replace input between two indexes"

class ELFPDFAppendMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        length = len(text)
        if length == 0: return text
        start = int.from_bytes(input[0].tobytes()[2:4], "little") % len(text)
        end = int.from_bytes(input[1].tobytes()[2:4], "little") % len(text)
        if len(text) >= 10000: return text

        if end < start:
            return text[:end] + text[start:] + text[end:start]
        else:
            return text[:start] + text[end:] + text[start:end]

    def get_dimension(self) -> "int":
        """
        First element of vector = start index
        Second element of vector = end index
        """
        return 2

    def get_name(self) -> "str":
        return "Append input between two indexes to the end"

class ELFPDFShuffleMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        length = len(text)
        if length == 0: return text
        start = int.from_bytes(input[0].tobytes()[2:4], "little") % len(text)
        end = int.from_bytes(input[1].tobytes()[2:4], "little") % len(text)
        if len(text) >= 10000: return text

        if end < start:
            shuffled = bytearray(text[end:start])
            random.shuffle(shuffled)
            return text[:end] + bytes(shuffled) + text[start:]
        else:
            shuffled = bytearray(text[start:end])
            random.shuffle(shuffled)
            return text[:start] + bytes(shuffled) + text[end:]

    def get_dimension(self) -> "int":
        """
        First element of vector = start index
        Second element of vector = end index
        """
        return 2
    
    def get_name(self) -> "str":
        return "Shuffle input between two indexes"

class ELFPDFRepeatMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        length = len(text)
        if length == 0: return text
        start = int.from_bytes(input[0].tobytes()[2:4], "little") % len(text)
        end = int.from_bytes(input[1].tobytes()[2:4], "little") % len(text)

        multiplier = int.from_bytes(input[2].tobytes()[2:4], "little")
        multiplier = min(multiplier, 5000) # Cap at 5k

        if len(text) * multiplier >= 10000: return text

        if end < start:
            return text[:end] + text[end:start] * multiplier + text[start:]
        else:
            return text[:start] + text[start:end] * multiplier + text[end:]

    def get_dimension(self) -> "int":
        """
        First element of vector = start index
        Second element of vector = end index
        Second element of vector = number to repeat
        """
        return 3
    
    def get_name(self) -> "str":
        return "Repeat input between two indexes"
