import json
import pennylane as qml
from pennylane.tape import QuantumTape

class DirectSubmission():
    def __init__(self, qnode, params, circuit_label, debiasing, shots, filename):
        self._submission = None
        self.qtape = qnode.qtape
        self.ionq_circuit = []

class DirectSubmissionSimulator():
    def __init__(self, qnode, params, circuit_label, debiasing, shots, filename):
        self._submission = None
        self.qtape = qnode.qtape
        self.ionq_circuit = []
