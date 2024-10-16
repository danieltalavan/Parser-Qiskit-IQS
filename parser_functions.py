### Necessary imports

import re
from qiskit import transpile

def cod_qasm(qc):
    """
    Description: Converts a Qiskit circuit to QASM code.
    Input: Circuit to analyze. (Type: QuantumCircuit)
    Output: Equivalent QASM code. (Type: string)
    """
    transpiled_qc = transpile(qc, basis_gates=['rx', 'cx', 'x', 'h', 'ry', 'cy', 'y', 'rz', 'cz', 'z'])
    code = transpiled_qc.qasm()

    return code


def create_qasm_file(filename, qasm_code):
    """
    Description: Generates a .qasm file from the provided information. Additionally, displays a success message upon completion.
    Input: - Name/path of the file to be generated. (Type: string)
           - QASM code containing the circuit information. (Type: string)
    Output: -
    """
    with open(filename, "w") as file:
        file.write(qasm_code)

    print(f"The string has been saved in the file '{filename}'.")


def import_qasm(filename):
    """
    Description: Retrieves the circuit information from a .qasm file. This function is the inverse of create_qasm_file().
    Input: Name/path of the file to import. (Type: string)
    Output: Imported circuit in QASM code. (Type: string)
    """
    with open(filename, "r") as file:
        content = file.read()
    return content


def qasm_to_list(qasm_code):
    """
    Description: Removes information from the code not related to the gates used. Suppresses initialization and retains qubit count.
    Input: QASM code. (Type: string)
    Output: - List with each line of QASM code. (Type: list)
            - Number of qubits used by the circuit. (Type: int)
    """
    qasm_lines = qasm_code.splitlines()
    n_qubits = qasm_lines[2].split("qreg q[")[1].split("]")[0]  # Better done with regex

    qasm_lines = qasm_lines[3:]
    gate_list = []
    for line in qasm_lines:
        gate = convert_gate(line, "psi")
        gate_list.append(gate)
    
    return gate_list, n_qubits


def convert_gate(line, register):
    """
    Description: Converts a QASM command line to its Intel-QS equivalent.
    Input: - QASM gate command, specifying the type of gate and the qubit(s) it applies to. (Type: string)
           - Name of the quantum register or circuit in Intel-QS. (Type: string)
    Output: Intel-QS equivalent of the QASM gate command. (Type: string)
    """
    words = line.split()
    parts = words[0].split("(")

    if len(words[0]) > 2:
        angle = parts[1].replace("pi", "M_PI")
        qubits = re.findall(r'\[(.*?)\]', words[1])[0]
        command = f"{register}.ApplyRotation{parts[0][1].upper()}({qubits}, {angle});"
    else:
        if len(words[0]) == 2:
            qubits = ",".join(re.findall(r'q\[(\d+)\]', words[1]))
            command = f"{register}.ApplyCPauli{words[0][1].upper()}({qubits});"
        elif len(words[0]) == 1:
            qubits = re.findall(r'\[(.*?)\]', words[1])[0]
            if words[0] != "h":
                command = f"{register}.ApplyPauli{words[0].upper()}({qubits});"
            else:
                command = f"{register}.ApplyHadamard({qubits});"

    return command


def init_qasm():
    """
    Description: Internal function (not explicitly used by the user). Initializes the file from another one in the working directory called "inicio.qasm".
    Input: -
    Output: Necessary lines of code for library functionality. (Type: list)
    """
    with open("inicio.qasm", "r") as file:
        init_content = file.read()
    init_content = init_content.split("&&&")
    return init_content


def create_cpp(filename, gate_list):
    """
    Description: Generates the final .cpp code, which can be compiled and executed. The code includes necessary information to initialize the Intel-QS library and the circuit to study.
    Input: - Name/path of the file to generate. (Type: string)
           - Circuit gates expressed as Intel-QS commands. (Type: list)
    Output: -
    """
    circuit = gate_list[0]
    n_qubits = gate_list[1]

    init_code = init_qasm()
    init_code[0] += f"{n_qubits};"
    
    gates = "\n\n"
    for gate in circuit:
        gates += f"{gate}\n"
    
    init_code[2] += gates
    
    cpp_code = ""
    for section in init_code:
        cpp_code += section
        
    with open(filename, "w") as file:
        file.write(cpp_code)

    print(f"The string has been saved in the file '{filename}'.")


def translate_from_qasm(qasm_code, cpp_filename="qasm.cpp"):
    """
    Description: Creates the .cpp file from the provided QASM code.
    Input: - QASM code. (Type: string)
    Output: -
    """
    gate_list = qasm_to_list(qasm_code)
    create_cpp(cpp_filename, gate_list)


def translate_from_qiskit(qiskit_circuit, cpp_filename="qasm.cpp"):
    """
    Description: Creates the .cpp file from the provided Qiskit circuit.
    Input: - Qiskit circuit. (Type: QuantumCircuit)
    Output: -
    """
    qasm_code = cod_qasm(qiskit_circuit)
    translate_from_qasm(qasm_code, cpp_filename)
