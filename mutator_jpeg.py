from PIL import Image
import io
import numpy as np
from mutator_base import BaseMutator
from format_finder import try_jpg

class JPEGSizeMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        width = int.from_bytes(input[0].tobytes()[2:4], "little")
        height = int.from_bytes(input[1].tobytes()[2:4], "little")

        if not try_jpg(text):
            return text

        image = Image.open(io.BytesIO(text))

        width = (input[0] * 2 - 1) * width
        height = (input[1] * 2 - 1) * height
        try:
            image.size = tuple(image.size[0] * width, image.size[1] * height)
        except:
            return text

        mutated = io.BytesIO()
        image.save(mutated, format="JPEG")

        mutated.seek(0)
        return mutated.read()
        
    def get_dimension(self) -> "int":
        """
        First element of vector = the width of the new filename
        Second element of vector = the height of the new filename
        """
        return 2

    def get_name(self) -> "str":
        return "Multiplier for size mutator"

class JPEGWidthMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        width = int.from_bytes(input[0].tobytes()[2:4], "little")

        if not try_jpg(text):
            return text

        image = Image.open(io.BytesIO(text))

        width = (input[0] * 2 - 1) * width
        try:
            image.width *= width
        except:
            return text

        mutated = io.BytesIO()
        image.save(mutated, format="JPEG")

        mutated.seek(0)
        return mutated.read()
        
    def get_dimension(self) -> "int":
        """
        First element of vector = the width of the new filename
        """
        return 1

    def get_name(self) -> "str":
        return "Multiplier for width mutator"

class JPEGHeightMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        height = int.from_bytes(input[0].tobytes()[2:4], "little")

        if not try_jpg(text):
            return text

        image = Image.open(io.BytesIO(text))

        height = (input[0] * 2 - 1) * height
        try:
            image.height *= height
        except:
            return text

        mutated = io.BytesIO()
        image.save(mutated, format="JPEG")

        mutated.seek(0)
        return mutated.read()
        
    def get_dimension(self) -> "int":
        """
        First element of vector = the height of the new filename
        """
        return 1

    def get_name(self) -> "str":
        return "Multiplier for height mutator"

class JPEGMetadataBitFlipMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        if not try_jpg(text):
            return text
        
        index = text.index(b"\xff\xda")
        byte_idx = int.from_bytes(input[0].tobytes()[2:7], "big") % index
        bit = int.from_bytes(input[1].tobytes()[2:7], "big") % 8
        new = bytearray(text)
        new[byte_idx] = new[byte_idx] ^ (1 << bit)
        return bytes(new)
        
    def get_dimension(self) -> "int":
        """
        First element of vector = the byte to change
        Second element of vector = the bit to flip
        """
        return 2

    def get_name(self) -> "str":
        return "Metadata Bit flipper"

class JPEGMetadataByteFlipMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        if not try_jpg(text):
            return text

        index = text.index(b"\xff\xda")
        if len(text) == 0: return text
        byte_idx = int.from_bytes(input[0].tobytes()[2:7], "big") % index
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

def extend_str(string: str, length: int) -> str:
    if string == "":
        return ""
    new_str = []
    i = 0
    while (True):
        for char in string:
            if i >= length:
                return ''.join(new_str)
            new_str.append(char)
            i += 1
