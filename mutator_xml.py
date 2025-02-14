import copy
from mutator_base import BaseMutator
import numpy as np
from format_finder import try_xml

# https://docs.python.org/3/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET

# Returns a new xml with the tag lengths being multiplied
# by the number from 'input'.
class XMLOverFlowMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        repeat = min(int.from_bytes(input[0].tobytes()[2:5], "little") % len(text), 10000)
        xmlTemplate="""
        {tag1}
            {input1}
            {input2}
        {tag2}
        """
        if len(xmlTemplate) * repeat < 10000:
            return xmlTemplate.format(tag1=("<tag>"*repeat), input1=("<input>" * repeat), input2=("</input>" * repeat), tag2=("</tag>" * repeat)).encode()

        return text
    """
    First element of vector, number of repetitions of the Entities in the xml.
    """
    def get_dimension(self) -> "int":
        return 1

    def get_name(self) -> "str":
        return "Repeated tag in xml"

# Changes all of the attributes for all tags to the set character
# mulitplied by the number from 'input'
class XMLAttributeMutator():
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        repeat = min(int.from_bytes(input[0].tobytes()[2:5], "little") % len(text), 10000)

        
        if len(text) * repeat > 10000:
            return text

        if not try_xml(text):
            return text

        tree = ET.fromstring(text)

        for element in tree.iter():
            element.attrib = {"<tag>": "</tag>" * repeat}


        return ET.tostring(tree)
    
    """
    First element of vector, number of repititions of the attribute added to the xml.
    """
    def get_dimension(self) -> "int":
        return 1

    def get_name(self) -> "str":
        return "Change attributes for tags in xml"


# Changes all of the 'href' attributes to the set character, by the
# number of 'input'
class XMLhrefAttributeMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        repeat = min(int.from_bytes(input[0].tobytes()[2:5], "little") % len(text), 10000)

        if len(text) * repeat > 10000:
            return text

        if not try_xml(text):
            return text

        tree = ET.fromstring(text)
        for element in tree.iter():
            if 'href' in element.attrib:
                element.attrib['href'] = "https://COMP6447rox.wtf" * repeat

        return ET.tostring(tree).decode()
    
    """
    First element of vector, number of repititions of the attribute added to the xml.
    """
    def get_dimension(self) -> "int":
        return 1

    def get_name(self) -> "str":
        return "Change 'href' attributes in xml"


# Modifies all of the tags, except the root tag to the set character,
# mulitplied by the number of 'input'
class XMLTagMutator():
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        repeat = min(int.from_bytes(input[0].tobytes()[2:5], "little") % len(text), 10000)

        if len(text) * repeat > 10000:
            return text

        if not try_xml(text):
            return text

        tree = ET.fromstring(text)
        tags_list = XMLTagMutator.get_XMLTags(text)
        for tag in tags_list:
            for elem in tree.findall(tag.tag):
                elem.tag = "<tag>" * repeat
        return ET.tostring(tree)

    # Returns a list of all tags in the xml file.
    def get_XMLTags(sample_text):
        xmlTree = ET.fromstring(sample_text)
        tags_list = []
        for tag in xmlTree.iter():
            tags_list.append(tag)

        return tags_list
    
    """
    First element of vector, number of repititions of the tag added to the xml.
    """
    def get_dimension(self) -> "int":
        return 1

    def get_name(self) -> "str":
        return "Change tag names in xml"


# Modifies the Root tag by the number of times from the 'input'
class XMLRootTagMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        repeat = min(int.from_bytes(input[0].tobytes()[2:5], "little") % len(text), 10000)

        if not try_xml(text):
            return text

        root = XMLRootTagMutator.get_RootTag(text)

        if len(text) + ("<tag>" * repeat) > 10000:
            return text
        
        tree = ET.fromstring(text)
        for elem in tree.iter():
            if elem.tag == root.tag:
                elem.tag = "<tag>" * repeat
        
        tree.append(root)
        return ET.tostring(tree)

    #returns the root tag.
    def get_RootTag(sample_text):
        tree = ET.ElementTree(ET.fromstring(sample_text))
        root = tree.getroot()
        return root

    """
    First element of vector, number of repititions of the Root tag added to the xml.
    """
    def get_dimension(self) -> "int":
        return 1

    def get_name(self) -> "str":
        return "Repeat root tag in xml"
    
# Add's children (New elements) to the xml by appending the tree to itself
# by the number of times from the 'input'.
class XMLChildrenMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        repeat = min(int.from_bytes(input[0].tobytes()[2:5], "little") % len(text), 10000)
        
        if len(text) * repeat > 10000:
            return text

        if not try_xml(text):
            return text
        
        tree = ET.fromstring(text)
        new_tree = copy.deepcopy(tree)
        for i in range(0, repeat):
            tree.append(new_tree)

        return ET.tostring(tree)

    """
    First element of vector, number of repititions for the number the tree replicate added to the xml.
    """
    def get_dimension(self) -> "int":
        return 1

    def get_name(self) -> "str":
        return "Repeat the tree's children in xml"
