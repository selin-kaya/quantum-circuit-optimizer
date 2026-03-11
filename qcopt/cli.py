from __future__ import annotations
import argparse
from pathlib import Path 
from qiskit import QuantumCircuit
from .optimizer import optimize_circuit

def load_circuit(path: Path) -> QuantumCircuit:
    if path.suffix.lower() in {".qasm"}:
        return QuantumCircuit.from_qasm_file(str(path))
    raise ValueError("Please provide a .qasm file.")

def main():
    p = argparse.ArgumentParser(prog="qcopt", description="Quantum Circuit Optimizer (Qiskit)")
    p.add_argument("input", type=str, help="Path to input circuit (.qasm)")
    p.add_argument("--level", type=int, default=3, choices=[0, 1, 2, 3], help="Qiskit optimization level")
    p.add_argument("--out", type=str, default=None, help="Output path to save optimized circuit (.qasm)")
    p.add_argument("--basis", type=str, default=None, help="Comma-separated basis gates")
    
    args = p.parse_args()

    qc = load_circuit(Path(args.input))
    basis = [g.strip() for g in args.basis.split(", ")] if args.basis else None
    
    res = optimize_circuit(qc, optimization_level=args.level, basis_gates=basis)

    b, a = res.before, res.after
    print("Metrics")
    print(f"Before: depth={b.depth}, size={b.size}, 1q={b.num_1q}, 2q={b.num_2q}")
    print(f"After: depth={a.depth}, size={a.size}, 1q={a.num_1q}, 2q={a.num_2q}")

    if args.out:
        out = Path(args.out)
        out.write_text(res.optimized.qasm())
        print(f"Saved optimized circuit to: {out}")