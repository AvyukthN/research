from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit import Aer, execute
import numpy as np
import math
import matplotlib.pyplot as plt

''''''

c_2538 = 0
c_10055 = 0
c_310 = 0

iters = 1

for j in range(iters):
    pts = np.array([[1, 1], [25, 38], [100, 55], [3, 10]])
    x = pts[:, 0]
    y = pts[:, 1]

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
         
        if i == 1:
            print(qc)

        qc.reset(qreg)

        job = execute(qc, backend=backend, shots=2048)
        result = job.result().get_counts(qc)
        results_list.append(result['1'])

    classes = ['25-38', '100-55', '3-10']
    pred = classes[results_list.index(min(results_list))]

    if pred == '25-38':
        c_2538 += 1
    if pred == '100-55':
        c_10055 += 1
    if pred == '3-10':
        c_310 += 1

plt.bar(["c_2538", "c_10055", "c_310"], [c_2538, c_10055, c_310])
plt.savefig('./preds.png')
plt.show()