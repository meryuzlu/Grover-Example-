from qiskit_aer import AerSimulator
from qiskit import transpile
from qiskit.visualization import plot_histogram
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import WeightedAdder
import matplotlib.pyplot as plt


def oracle(set,target):
    add=WeightedAdder(4,set)

    n_control=add.num_control_qubits
    n_sum=add.num_sum_qubits
    n_work=add.num_carry_qubits
    q = QuantumRegister(4, "q")
    s = QuantumRegister(n_sum, "s")
    w = QuantumRegister(n_work, "w")
    c = QuantumRegister(n_control, "c")
    a= QuantumRegister(1,"a")


    qc=QuantumCircuit(q,s,w,c,a)


    adder_gate=add.to_gate(label="Sum")
    qc.append(adder_gate, q[:]+s[:]+w[:]+c[:])
    target_bits=format(target,f"0{n_sum}b")[::-1]
    for i, bit in enumerate (target_bits):
        if bit=="0":
            qc.x(s[i])
    qc.mcx(s[:],a[0])
    qc.z(a[0])
    qc.mcx(s[:], a[0])
    for i, bit in enumerate (target_bits):
        if bit=="0":
            qc.x(s[i])
    qc.append(adder_gate.inverse(), q[:]+s[:]+w[:]+c[:])





    return qc


#add=WeightedAdder(3,[2,3,5])
#print(add.num_qubits)
#print(add.num_sum_qubits)
#print(add.num_carry_qubits)
#print(add.num_control_qubits)

oracle_circuit = oracle([2,3,5,7], 7)
oracle_gate = oracle_circuit.to_gate(label="Oracle")

creg=ClassicalRegister(4)
grover_circuit = QuantumCircuit(*oracle_circuit.qregs,creg)

# initial superposition
grover_circuit.h([0,1,2,3])

# oracle
grover_circuit.append(oracle_gate, range(oracle_circuit.num_qubits))

# diffuser
grover_circuit.h([0,1,2,3])
grover_circuit.x([0,1,2,3])
grover_circuit.h(3)
grover_circuit.mcx([0,1,2],3)
grover_circuit.h(3)
grover_circuit.x([0,1,2,3])
grover_circuit.h([0,1,2,3])

grover_circuit.measure([0,1,2,3],creg)

sim=AerSimulator()
compiled=transpile(grover_circuit,sim)
result=sim.run(compiled,shots=1024).result()
counts=result.get_counts()

print(counts)



plot_histogram(counts)
plt.show()


