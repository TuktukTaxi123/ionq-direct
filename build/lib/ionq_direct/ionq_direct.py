import json
import pennylane as qml
from pennylane.tape import QuantumTape
import requests
import ast

class CreateCircuit():
    """
    Creates a quantum circuit in the IonQ format given a pennylane circuit.
    """
    # TODO: Implement native gates

    def __init__(self, qnode, params, shots=1000, native=False, 
                 filename='circuit.json', circuit_name='circuit', api_key=''):
        qnode(*[params])
        """
        Args:
            qnode (qml.QNode): Circuit with a default qubit qnode dev.
            params (list): Parameters the circuit takes.
            shots (int): Number of shots to use in simulation.
            native (bool): Choose whether to use native gates or not
            filename (str): File to save the job submission to.
            circuit_name (str): Name of the circuit.
            api_key (str): API key.
        """
        self._submission = None
        self.qtape = qnode.qtape
        self.ionq_circuit = []
        self.shots = shots
        self.filename = filename
        self.circuit_name = circuit_name
        self.api_key = api_key
        self.job = {}

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
            
    def set_shots(self, shots):
        """
        Set the number of shots to use in simulation.
        
        Args:
            shots (int): Number of shots.
        """
        self.shots = shots
        print("Shots set to", self.shots)
    
    def set_filename(self, filename):
        """
        Set the filename to save the job submission to.

        Args:
            filename (str): Filename.
        """
        self.filename = filename
        print("Filename set to", self.filename)
    
    def set_circuit_name(self, circuit_name):
        """
        Set the name of the circuit.
        
        Args:
            circuit_name (str): Name of the circuit.
            Name can be used to identify the circuit in the IonQ dashboard.
        """
        self.circuit_name = circuit_name
        print("Circuit name set to", self.circuit_name)

    def set_api_key(self, api_key):
        """
        Set the API key to use for submitting the job.
        
        Args:
            api_key (str): API key.
        """
        self.api_key = api_key
        print("API key set")

    def save_job(self):
        """
        Save the job submission to a file. 
        The job submission is saved in JSON format accepted by IonQ.
        """
        if self.job == {}:
            raise Exception("Job not created yet")

        with open(self.filename, "w") as f:
            json.dump(self.job, f, indent=2)
        
        print(f"Job submission saved to {self.filename}")

    def submit_job(self):
        """
        Submit the job to the IonQ API.
        
        Returns:
            dict: Job information result.
        """
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

    def set_native(self, native):
        """
        Set whether to use native gates or not.
        
        Args:
            native (bool): True if native gates are to be used.
            TODO: Implement native gate support. Currently not supported
        """
        if native == True:
            raise Exception("Native gates not implemented yet")
        self.native = native
        print("Native set to", self.native)

class QPUSubmission(CreateCircuit):
    """
    Submits a job to the IonQ QPU.
    """

    def __init__(self, qnode, params, shots=1000, native=False, 
                 filename='circuit.json', circuit_name='circuit', api_key='', target='qpu.aria-1', debiasing=True):
        """
        Args:
            See `CreateCircuit()` for non-qpu specific arguments.
            Target (str): Target device to run the job on.
                - Valid devices:
                    -`qpu.aria-1`
                    -`qpu.aria-2`
                    -`qpu.forte`
            Debiasing (bool): Whether to use error mitigation or not.
        
        Note: Sharpening is a post processing error mitigation technique that is called
        during job retreival. Debiasing must be enabled for sharpening to be used.
        """
        super().__init__(qnode, params, shots, native, filename, circuit_name, api_key)
        self.debiasing = debiasing
        self.target = target
    
    def set_debiasing(self, debiasing):
        """
        Set whether to use Debiasing or not.
        """
        self.debiasing = debiasing
        print("Debiasing set to", self.debiasing)
    
    def set_target(self, target):
        """
        Set the target device to run the job on.

        Valid devices:
            -`qpu.aria-1`
            -`qpu.aria-2`
            -`qpu.forte`
        """
        self.target = target
        print("Target set to", self.target)

    def create_job(self):
        """
        Create the job submission.
        """
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

class SimulatorSubmission(CreateCircuit):

    def __init__(self, qnode, params, shots=1000, native=False, 
                 filename='circuit.json', circuit_name='circuit', api_key='', noise_model = 'ideal'):
        super().__init__(qnode, params, shots, native, filename, circuit_name, api_key)

        self.target = 'simulator'
        self.noise_model = noise_model
    
    def set_noise_model(self, noise_model):
        self.noise_model = noise_model
        print("Target set to", self.target)

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