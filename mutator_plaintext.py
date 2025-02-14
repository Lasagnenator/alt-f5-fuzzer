import numpy as np
from mutator_base import BaseMutator

class RepeatMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        repeat = int.from_bytes(input[0].tobytes()[2:4], "little")
        repeat = min(repeat, 5000) # Cap at 5k
        if len(text) * repeat > 10000: return text
        return text * repeat

    def get_dimension(self) -> "int":
        """
        First element of vector = number to repeat
        """
        return 1

    def get_name(self) -> "str":
        return "Repeated input"

class SubstringMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        length = len(text)
        if length == 0: return text
        start = int.from_bytes(input[0].tobytes()[2:7], "little") % length
        end = int.from_bytes(input[1].tobytes()[2:7], "little") % length
        start, end = min(start, end), max(start, end)
        return text[start:end]

    def get_dimension(self) -> "int":
        """
        First element of vector = starting index
        Second element of vector = end index
        """
        return 2
    
    def get_name(self) -> "str":
        return "Substring of input"

class BitFlipMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        if len(text) == 0: return text
        byte_idx = int.from_bytes(input[0].tobytes()[2:7], "big") % len(text)
        bit = int.from_bytes(input[1].tobytes()[2:7], "big") % 8
        new = bytearray(text)
        new[byte_idx] = new[byte_idx] ^ (1 << bit)
        return bytes(new)

    def get_dimension(self) -> "int":
        """
        First element of vector = which byte to flip
        Second element of vector = which bit inside that byte to flip
        """
        return 2
    
    def get_name(self) -> "str":
        return "Random bit flip on input"

class ByteFlipMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        if len(text) == 0: return text
        byte_idx = int.from_bytes(input[0].tobytes()[2:7], "big") % len(text)
        new = bytearray(text)
        new[byte_idx] = new[byte_idx] ^ 0xff
        return bytes(new)

    def get_dimension(self) -> "int":
        """
        First element of vector = which byte to flip
        """
        return 1

    def get_name(self) -> "str":
        return "Random byte flip on input"
