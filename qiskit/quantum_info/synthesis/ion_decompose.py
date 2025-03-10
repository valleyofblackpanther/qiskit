# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Decomposition methods for trapped-ion basis gates RXXGate, RXGate, RYGate.
"""

from __future__ import annotations
import numpy as np

from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.library.standard_gates.ry import RYGate
from qiskit.circuit.library.standard_gates.rx import RXGate
from qiskit.circuit.library.standard_gates.rxx import RXXGate
from qiskit.utils.deprecation import deprecate_func


@deprecate_func(since="0.46.0")
def cnot_rxx_decompose(plus_ry: bool = True, plus_rxx: bool = True):
    """Decomposition of CNOT gate.

    NOTE: this differs to CNOT by a global phase.
    The matrix returned is given by exp(1j * pi/4) * CNOT

    Args:
        plus_ry (bool): positive initial RY rotation
        plus_rxx (bool): positive RXX rotation.

    Returns:
        QuantumCircuit: The decomposed circuit for CNOT gate (up to
        global phase).
    """
    # Convert boolean args to +/- 1 signs
    if plus_ry:
        sgn_ry = 1
    else:
        sgn_ry = -1
    if plus_rxx:
        sgn_rxx = 1
    else:
        sgn_rxx = -1
    circuit = QuantumCircuit(2, global_phase=-sgn_ry * sgn_rxx * np.pi / 4)
    circuit.append(RYGate(sgn_ry * np.pi / 2), [0])
    circuit.append(RXXGate(sgn_rxx * np.pi / 2), [0, 1])
    circuit.append(RXGate(-sgn_rxx * np.pi / 2), [0])
    circuit.append(RXGate(-sgn_rxx * sgn_ry * np.pi / 2), [1])
    circuit.append(RYGate(-sgn_ry * np.pi / 2), [0])
    return circuit
