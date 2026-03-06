from __future__ import annotations
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.convertes import circuit_to_dag, dag_to_circuit

SELF_INVERSE_1Q = {"x", "h", "z", "y"}

class CancelAdjacentSelfInverse(TransformationPass):
    
    def run(self, dag):
        qc = dag_to_circuit(dag)
        new = qc.copy_empty_like()

        # Track last gate per qubit. If same self inverse occurs twice in a row, cancel
        last = {i: None for i in range(qc.num_qubits)}

        for inst, qargs, carg in qc.data:
            if len(qargs) == 1:
                q = qc.find_bit(qargs[0]).index
                name = inst.name

                if name in SELF_INVERSE_1Q and last[q] == name:
                    # If it is last, rebuild by popping last instruction affecting q
                    # Otherwise, fall back to appending
                    if len(new.data) > 0:
                        prev_inst, prev_qargs, prev_cargs = new.data[-1]
                        prev_q = new.find_bit(prev_qargs[0]).index if len(prev_qargs) == 1 else None

                        if prev_q == q and prev_inst.name == name:
                            new.data.pop()
                            last[q] = None
                            continue
                
                new.append(inst, qargs, cargs)
                last[q] = name if name in SELF_INVERSE_1Q else None
            
            else:
                new.append(inst, qargs, cargs)
                for qa in qargs:
                    # Multi-qubit op breaks adjacency assumptions for involved qubits
                    last[new.find_bit(qa).index] = None
        
        return circuit_to_dag(new)



