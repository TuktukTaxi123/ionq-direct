import json
import pennylane as qml
from pennylane.tape import QuantumTape
import requests
import ast

class CreateCircuit():
    """
    Creates a quantum circuit in the IonQ format given a pennylane circuit.

    Args:
        qnode (qml.qnode): Quantum circuit function with attributed default qubit qnode
        params (list): List of parameters needed by qnode
        native (bool): If True, use native gates from the qnode, otherwise use the default gates
    """
    # TODO: Implement native gates

    def __init__(self, qnode, params, native=False):
        qnode(*[params])

        self._submission = None
        self.qtape = qnode.qtape
        self.ionq_circuit = []

        for op in self.qtape.operations:
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
                    self.ionq_circuit.append({"gate": "xx", "targets": [op.wires[0], op.wires[1]], "rotation": op.parameters[0]})
                elif op.name == "IsingYY":
                    self.ionq_circuit.append({"gate": "yy", "targets": [op.wires[0], op.wires[1]], "rotation": op.parameters[0]})
                elif op.name == "IsingZZ":
                    self.ionq_circuit.append({"gate": "zz", "targets": [op.wires[0], op.wires[1]], "rotation": op.parameters[0]})
                # two qubit gates in pennylane-ionq package (same as Ising variants above)
                elif op.name == "XX":
                    self.ionq_circuit.append({"gate": "xx", "targets": [op.wires[0], op.wires[1]], "rotation": op.parameters[0]})
                elif op.name == "YY":
                    self.ionq_circuit.append({"gate": "yy", "targets": [op.wires[0], op.wires[1]], "rotation": op.parameters[0]})
                elif op.name == "ZZ":
                    self.ionq_circuit.append({"gate": "zz", "targets": [op.wires[0], op.wires[1]], "rotation": op.parameters[0]})
            else:
                raise Exception("Native gates not implemented yet")

class QPUSubmission(CreateCircuit):

    def __init__(self, qnode, params, native=False, debiasing=True, shots=1000, 
                 filename='circuit.json', circuit_name='circuit', api_key='', target='qpu.aria-1'):
        super().__init__(qnode, params, native)
        self.debiasing = debiasing
        self.circuit_name = circuit_name
        self.target = target
        self.shots = shots
        self.job = {}

        self.api_key = api_key
        self.filename = filename
        self.post_url = 'https://api.ionq.co/v0.3/jobs'


    def set_shots(self, shots):
        self.shots = shots
        print("Shots set to", self.shots)
    
    def set_debiasing(self, debiasing):
        self.debiasing = debiasing
        print("Debiasing set to", self.debiasing)
    
    def set_filename(self, filename):
        self.filename = filename
        print("Filename set to", self.filename)
    
    def set_circuit_name(self, circuit_name):
        self.circuit_name = circuit_name
        print("Circuit name set to", self.circuit_name)
    
    def set_api_key(self, api_key):
        self.api_key = api_key
        print("API key set")
    
    def set_target(self, target):
        self.target = target
        print("Target set to", self.target)
    
    def set_native(self, native):
        if native == True:
            raise Exception("Native gates not implemented yet")
        self.native = native
        print("Native set to", self.native)
    
    def set_filename(self, filename):
        self.filename = filename
        print("Filename set to", self.filename)

    def create_job(self):
        self.job = {
            "name": self.circuit_name,
            "shots": self.shots,
            "target": self.target,
            "error_mitigation": {
                "debias": self.debiasing,
            },
            "input": {
                "qubits": len(self.qtape.wires),
                "circuit": self.ionq_circuit
            }
        }
    
    def save_job(self):
        if self.job == {}:
            raise Exception("Job not created yet")

        with open(self.filename, "w") as f:
            json.dump(self.job, f, indent=2)
        
        print(f"Job submission saved to {self.filename}")

    def submit_job(self):
        if self.job == {}:
            raise Exception("Job not created yet")
        if self.api_key == '':
            raise Exception("API key not set")

        url = "https://api.ionq.co/v0.3/jobs"
        headers = {
            "Authorization": f"apiKey {self.api_key}",
            "Content-Type": "application/json"
        }
        file_path = f'{self.filename}'
        with open(file_path, 'r') as file:
            data = file.read()
        
        job_result = requests.post(url, headers=headers, data=data)
        return ast.literal_eval(job_result.text)

class SimulatorSubmission(CreateCircuit):

    def __init__(self, qnode, params, native=False, shots=1000, 
                 filename='circuit.json', circuit_name='circuit', api_key='', noise_model = 'ideal'):
        super().__init__(qnode, params, native)
        self.circuit_name = circuit_name
        self.target = 'simulator'
        self.shots = shots
        self.job = {}

        self.api_key = api_key
        self.filename = filename
        self.post_url = 'https://api.ionq.co/v0.3/jobs'
        self.noise_model = noise_model

    def set_shots(self, shots):
        self.shots = shots
        print("Shots set to", self.shots)
    
    def set_debiasing(self, debiasing):
        self.debiasing = debiasing
        print("Debiasing set to", self.debiasing)
    
    def set_filename(self, filename):
        self.filename = filename
        print("Filename set to", self.filename)
    
    def set_circuit_name(self, circuit_name):
        self.circuit_name = circuit_name
        print("Circuit name set to", self.circuit_name)
    
    def set_api_key(self, api_key):
        self.api_key = api_key
        print("API key set")
    
    def set_target(self, target):
        self.target = target
        print("Target set to", self.target)
    
    def set_native(self, native):
        if native == True:
            raise Exception("Native gates not implemented yet")
        self.native = native
        print("Native set to", self.native)
    
    def set_filename(self, filename):
        self.filename = filename
        print("Filename set to", self.filename)

    def create_job(self):
        self.job = {
            "name": self.circuit_name,
            "shots": self.shots,
            "target": self.target,
            "noise": {
                "model": self.noise_model
            },
            "input": {
                "qubits": len(self.qtape.wires),
                "circuit": self.ionq_circuit
            }
        }
    
    def save_job(self):
        if self.job == {}:
            raise Exception("Job not created yet")

        with open(self.filename, "w") as f:
            json.dump(self.job, f, indent=2)
        
        print(f"Job submission saved to {self.filename}")
    
    def submit_job(self):
        if self.job == {}:
            raise Exception("Job not created yet")
        if self.api_key == '':
            raise Exception("API key not set")

        url = "https://api.ionq.co/v0.3/jobs"
        headers = {
            "Authorization": f"apiKey {self.api_key}",
            "Content-Type": "application/json"
        }
        file_path = f'{self.filename}'
        with open(file_path, 'r') as file:
            data = file.read()
        
        job_result = requests.post(url, headers=headers, data=data)
        return ast.literal_eval(job_result.text)