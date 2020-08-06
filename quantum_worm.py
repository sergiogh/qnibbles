import numpy as np

# importing Qiskit
from qiskit import IBMQ, Aer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.quantum_info import Statevector


def random_position(qubits):
	return x,y

def random_walk(position):
	return new_position

def cnx(qc, *qubits):
    if len(qubits) > 3:
        last = qubits[-1]
        # A matrix: (made up of a  and Y rotation, lemma4.3)
        qc.crz(np.pi/2, qubits[-2], qubits[-1])
        qc.cu3(np.pi/2, 0, 0, qubits[-2],qubits[-1])

        # Control not gate
        cnx(qc,*qubits[:-2],qubits[-1])

        # B matrix (pposite angle)
        qc.cu3(-np.pi/2, 0, 0, qubits[-2], qubits[-1])

        # Control
        cnx(qc,*qubits[:-2],qubits[-1])

        # C matrix (final rotation)
        qc.crz(-np.pi/2,qubits[-2],qubits[-1])
    elif len(qubits) == 3:
        qc.ccx(*qubits)
    elif len(qubits) == 2:
        qc.cx(*qubits)


def quantumRandomStartingPoint(qubits):
	qc = QuantumCircuit(qubits)
	qc.h(range(qubits))
	qc.measure_all()

	backend = Aer.get_backend("qasm_simulator")
	result = execute(qc, backend=backend, shots=1).result()
	for r in result.get_counts():
		return getCoordinatesFromBinary(r)


def getCoordinatesFromBinary(binary_result):
	n = int(binary_result, 2)
	y = int(n / 16) + 1
	x = n - ((y - 1) * 16) + 1
	coordinates = {'x': x, 'y': y}
	return coordinates
