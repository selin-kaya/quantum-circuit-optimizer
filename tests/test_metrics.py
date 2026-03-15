from qiskit import QuantumCircuit
from qcopt.metrics import compute_metrics

def test_metrics_counts():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.z(1)

    m = compute_metrics(qc)
    assert m.width == 2
    assert m.num_2q == 1
    assert m.num_1q == 2