from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit import Aer, execute
import numpy as np
import math

''''''

pts = np.array([[1, 1], [3, 3], [4, 4], [2, 2]])
x = pts[:, 0]
y = pts[:, 1]

print(list(x))
print(list(y))

qreg = QuantumRegister(3, 'qreg')
creg = ClassicalRegister(1, 'creg')
qc = QuantumCircuit(qreg, creg, name='qc')

backend = Aer.get_backend('qasm_simulator')

phi_vec = [(c + 1) * (math.pi/2) for c in list(x)]
theta_vec = [(c + 1) * (math.pi/2) for c in list(y)]

results_list = []

for i in range(1, 4):
    qc.h(qreg[2])

    qc.u3(theta_vec[0], phi_vec[0], 0, qreg[0])           
    qc.u3(theta_vec[i], phi_vec[i], 0, qreg[1]) 

    qc.cswap(qreg[2], qreg[0], qreg[1])
    qc.h(qreg[2])

    qc.measure(qreg[2], creg[0])

    qc.reset(qreg)

    job = execute(qc, backend=backend, shots=2048)
    result = job.result().get_counts(qc)
    print(result)
    results_list.append(result['1'])

print(results_list)

classes = ['33', '44', '22']
pred = classes[results_list.index(min(results_list))]

print(pred)