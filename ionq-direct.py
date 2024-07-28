import json
import pennylane as qml
from pennylane.tape import QuantumTape

class DirectSubmission():
    def __init__(self, qnode, params, circuit_label, debiasing, shots, filename, native=False):
        self._submission = None
        self.qtape = qnode.qtape
        self.ionq_circuit = []

        for op in qtape.operations:
            if native == False:
                # arbritrary single qubit rotations
                if op.name == "RX":
                    self.ionq_circuit.append({"gate": "rx", "target": op.wires[0], "rotation": op.parameters[0]})
                elif op.name == "RY":
                    self.ionq_circuit.append({"gate": "ry", "target": op.wires[0], "rotation": op.parameters[0]})
                elif op.name == "RZ":
                    self.ionq_circuit.append({"gate": "rz", "target": op.wires[0], "rotation": op.parameters[0]})
                # pauli gates
                elif op.name == "PauliX":
                    self.ionq_circuit.append({"gate": "x", "target": op.wires[0]})
                elif op.name == "PauliY":
                    self.ionq_circuit.append({"gate": "y", "target": op.wires[0]})
                elif op.name == "PauliZ":
                    self.ionq_circuit.append({"gate": "z", "target": op.wires[0]})
                # other single qubit gates
                elif op.name == "S":
                    self.ionq_circuit.append({"gate": "s", "target": op.wires[0]})
                elif op.name == "S.inv":
                    self.ionq_circuit.append({"gate": "si", "target": op.wires[0]})
                elif op.name == "T":
                    self.ionq_circuit.append({"gate": "t", "target": op.wires[0]})
                elif op.name == "T.inv":
                    self.ionq_circuit.append({"gate": "ti", "target": op.wires[0]})
                elif op.name == "SX":
                    self.ionq_circuit.append({"gate": "v", "target": op.wires[0]})
                elif op.name == "SX.inv":
                    self.ionq_circuit.append({"gate": "vi", "target": op.wires[0]})
                elif op.name == "Hadamard":
                    self.ionq_circuit.append({"gate": "h", "target": op.wires[0]})
                # two qubit gates
                elif op.name == "CNOT":
                    self.ionq_circuit.append({"gate": "cnot", "control": op.wires[0], "target": op.wires[1]})
                elif op.name == "SWAP":
                    self.ionq_circuit.append({"gate": "swap", "control": op.wires[0], "target": op.wires[1]})
                elif op.name == "IsingXX":
                    self.ionq_circuit.append({"gate": "xx", "control": op.wires[0], "target": op.wires[1], "rotation": op.parameters[0]})
                elif op.name == "IsingYY":
                    self.ionq_circuit.append({"gate": "yy", "control": op.wires[0], "target": op.wires[1], "rotation": op.parameters[0]})
                elif op.name == "IsingZZ":
                    self.ionq_circuit.append({"gate": "zz", "control": op.wires[0], "target": op.wires[1], "rotation": op.parameters[0]})
                # two qubit gates in pennylane-ionq package (same as Ising variants above)
                elif op.name == "XX":
                    self.ionq_circuit.append({"gate": "xx", "control": op.wires[0], "target": op.wires[1], "rotation": op.parameters[0]})
                elif op.name == "YY":
                    self.ionq_circuit.append({"gate": "yy", "control": op.wires[0], "target": op.wires[1], "rotation": op.parameters[0]})
                elif op.name == "ZZ":
                    self.ionq_circuit.append({"gate": "zz", "control": op.wires[0], "target": op.wires[1], "rotation": op.parameters[0]})

class DirectSubmissionSimulator():
    def __init__(self, qnode, params, circuit_label, debiasing, shots, filename):
        self._submission = None
        self.qtape = qnode.qtape
        self.ionq_circuit = []
