from numpy import ndarray
from mutator_base import BaseMutator

def combine(base: bytes, mutators: "list[tuple[BaseMutator, ndarray]]") -> bytes:
    """
    Chain mutators together and produce a single output.
    """
    if isinstance(base, str):
        base = base.encode()
    for mut, vec in mutators:
        base = mut.get_mutation(base, vec)
        if isinstance(base, str):
            base = base.encode()
    return base

def apply(text: bytes, mutators: "list[BaseMutator]", vec: ndarray) -> bytes:
    """
    Chain the given mutators with the overall vector.
    """
    start = 0
    output = []
    for m in mutators:
        end = start + m.get_dimension()
        output.append((m, vec[start:end]))
        start = end
    return combine(text, output)

def get_dim(mutators: "list[BaseMutator]"):
    return sum(m.get_dimension() for m in mutators)

def get_name(mutators: "list[BaseMutator]"):
    return " -> ".join(m.get_name() for m in mutators)
