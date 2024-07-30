# Pennylane IonQ Batch Job and Noisy Simulator Package 

This Python package allows you to construct circuits in pennylane and submit them to IonQ QPUs and Noisy Simulators.
Unlike the `pennylane-ionq` package, this package stores the job id of all jobs sent, allowing you to submit and retrieve batches of jobs easily.

## Features

- **Circuit Conversion**: Converts quantum circuits into IonQ-compatible JSON format.
- **Batch Submission**: Retrieves job ID of jobs sent to IonQ devices, allowing for easy batch submission and retreival
- **Noise Model Simulator Support**: Allows for easy use of IonQ Noisy Simulators, which is not present in the existing `pennylane-ionq` package
- **Native Gate Support**: Coming soon. Allows for direct native gate submission

## Installation and Requirements

- Clone this repository or download the `ionq_direct.py` file directly. No external dependencies beyond the standard Python libraries are required.
- Make a free account on the [IonQ Cloud Portal](cloud.ionq.com) to acquire an API key. This is required for noisy simulator runs.

## Usage

### Basic Example

```python
# Imports
from ionq_direct import SimulatorSubmission
dev = qml.device("default.qubit", wires=3)

# Build quantum circuit as per usual
@qml.qnode(dev)
def ansatz(rots):
    qml.RX(rots[0], wires = 0)
    qml.RX(rots[1], wires = 1)
    qml.RX(rots[2], wires = 2)
    qml.IsingXX(rots[3], wires = [0,1])
    qml.IsingXX(rots[4], wires = [1,2])
    return qml.state()

# Arguments to run quantum circuit
rots = [0.1,0.2,0.3,0.4,0.5]
filename = '/Users/documents/test_file.json' # file to store circuit
noise_model = 'aria-1'
shots=1000
api_key = 'API_KEY'

# Create a simulator job submission instance
simulator_job = SimulatorSubmission(qnode=ansatz,params=rots,filename=filename,
                                        api_key=api_key,shots=shots,noise_model=noise_model)

# Create the job
simulator_job.create_job()

# Save the job to the specified filename
simulator_job.save_job()
>> JSON file for job saved to /Users/documents/test_file.json

# Submit the job
simulator_job.submit_job()
>> {'id': 'job_id_string',
 'status': 'job_status',
 'request': request_number}
