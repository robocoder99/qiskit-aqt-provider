from qiskit import *
from qiskit.providers.aqt import AQT

aqt = AQT.get_provider() # aqt is a provider

backend = aqt.get_backend('aqt_qasm_simulator') # backend is a job

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

#result is of type AQTJob 
#shots default is 1024
result = execute(qc, backend, shots=10)
result.print_dax()

