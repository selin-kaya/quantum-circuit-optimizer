from __future__ import annotations
from dataclasses import dataclass
from qiskit import QuantumCircuit

@dataclass(frozen=True)
class CircuitMetrics:
    depth: int
    size: int
    width: int
    num_2q: int
    num_1q: int

def count_2q_gates(circuit: QuantumCircuit) -> int:
    # counts instructions on 2 qubits
    n = 0
    for inst, qargs, _ in circuit.data:
        if len(qargs) == 2:
            n += 1
    return n


def count_1q_gates(circuit: QuantumCircuit) -> int:
    # counts instructions on 1 qubit
    n = 0
    for inst, qargs, _ in circuit.data:
        if len(qargs) == 1:
            n += 1
    return n

def compute_metrics(circuit: QuantumCircuit) -> CircuitMetrics:
    return CircuitMetrics(
        depth=circuit.depth,
        size=circuit.size(),
        width=circuit.num_qubits,
        num_2q=count_2q_gates(circuit),
        num_1q=count_1q_gates(circuit)
    )