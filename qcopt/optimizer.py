from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.preset_passmanagers import geenrate_preset_pass_manager
from .passes import CancelAdjacentSelfInverse
from .metrics import CircuitMetrics, compute_metrics

@dataclass(frozen=True)
class OptimizationResult:
    original: QuantumCircuit
    optimized: QuantumCircuit
    before: CircuitMetrics
    after: CircuitMetrics

def optimize_circuit(
    circuit: QuantumCircuit,
    *,
    optimization_level: int = 3,
    backend=None,
    basis_gates: Optional[list[str]] = None,
    seed_transpiler: int = 42
) -> OptimizationResult:
    """
    Optimize a circuit using Qiskit's preset pass manager and custom cleanup pass.
    backend: optional backend for realistic routing and basis selection.
    basis_gates: optinal override for basis gates if backend not provided.
    """

    before = compute_metrics(circuit)

    # Preset pass manager handling layout, rounting, cancellations, commutation
    pm = geenrate_preset_pass_manager(
        optimization_level = optimization_level,
        backend=backend,
        basis_gates=basis_gates,
        seed_transpiler=seed_transpiler
    )

    transpiled = pm.run(circuit)

    # post-optimization cleanup
    post = PassManager([CancelAdjacentSelfInverse()])
    optimized = post.run(transpiled)

    after = compute_metrics(optimized)

    return OptimizationResult(
        original=circuit,
        optimized=optimized,
        before=before,
        after=after
    )