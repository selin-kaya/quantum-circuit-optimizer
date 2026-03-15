from qiskit import QuantumCircuit
from qcopt import optimize_circuit

def test_optimizer_2q_count():
    qc = QuantumCircuit(2)
    qc.h(0); qc.h(0)
    qc.cx(0, 1)
    qc.x(1); qc.x(1)
    qc.cx(0, 1)

    res = optimize_circuit(qc, optimization_level=3, basis_gates=["u3", "cx"])
    assert res.after.size <= res.before.size