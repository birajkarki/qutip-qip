from qutip_qip.decompositions.general_decompositions import (check_input,
check_input_shape, convert_qobj_gate_to_array)

from qutip_qip.decompositions.single_decompositions import (_ZYZ_rotation, _ZXZ_rotation, _rotation_matrices_dictionary, decompose_to_rotation_matrices, ABC_decomposition)
from qutip.qobj import Qobj
from qutip_qip.operations import *
from qutip_qip.circuit import QubitCircuit, Gate
from numpy import pi
import numpy as np

def decomposed_gates_to_circuit(decomposed_gate,num_of_qubits):
    """This function takes the input from a decomposition function and creates
    a circuit diagram.
    """
    # as decomposed_gate contains information about targets/control, there's no
    # additional input of target here.
    # In addition, there's no check if the gates are valid for number of qubits
    # because this is done in a decomposition function before output.
    if isinstance(decomposed_gate,tuple) == True:
        q_circuit = QubitCircuit(num_of_qubits, reverse_states=False)
        for i in decomposed_gate:
            q_circuit.add_gate(i)
        return(q_circuit)
    else:
        raise TypeError("Input is not a tuple of gates.")

def matrix_of_decomposed_gates(quantum_circuit):
    """Evaluates all the gates in the circuit. 
    """
    if isinstance(quantum_circuit, QubitCircuit) == True:
        gate_list = quantum_circuit.propagators()
        matrix_of_all_gates = gate_sequence_product(gate_list)
        return(matrix_of_all_gates)
    else:
        raise TypeError("Input is not of type QubitCircuit.")
