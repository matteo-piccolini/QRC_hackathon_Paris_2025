from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister, Parameter, ParameterVector

def build_QRC_layer(circ: QuantumCircuit, input_reg: QuantumRegister, hidden_reg: QuantumRegister, layer_params, H_params) -> None:
    # Angle encoding of features on input qubits - rotations aroun y-axis
    circ.barrier(input_reg, label = "encoding")
    for index, qubit in enumerate(input_reg):
        circ.ry(layer_params[index], qubit)
    
    # Hamiltonian evolution of the whole system (input + hidden qubits) with H_params[dt, nu, J]: local Z field
    circ.barrier(label = "evolution")
    all_qubits = list(input_reg) + list(hidden_reg)
    for k in all_qubits:
        circ.rz(2 * H_params[0] * H_params[1], k)
    
    # Hamiltonian evolution of the whole system with H_params[dt, nu, J]: XX coupling between input and hidden
    for input_qubit in input_reg:
        for hidden_qubit in hidden_reg:
            circ.rxx(2 * H_params[2] * H_params[0], input_qubit, hidden_qubit)
    

def build_QRC_circuit(num_layers: int, num_input: int, num_hidden: int, H_params) -> QuantumCircuit:
    # Define registers and create quantum circuit
    input_reg = QuantumRegister(num_input, "input")
    hidden_reg = QuantumRegister(num_hidden, "hidden")
    qc = QuantumCircuit(input_reg, hidden_reg, name = "reservoir")
    
    # Create vector of encoding parameters (one per input qubit, per layer) to be passed to the QRC circuit
    encoding_params = ParameterVector("theta", num_layers * num_input)
    
    # Iteratively assemble layers to create the circuit
    for layer in range(num_layers):
        start = layer * num_input
        layer_params = encoding_params[start: start + num_input]
        
        build_QRC_layer(qc, input_reg, hidden_reg, layer_params, H_params)
        
        # Reset input qubit after each layer but the last
        if layer < num_layers - 1:
            qc.barrier(input_reg, label = "reset input")
            for qubit in input_reg:
                qc.reset(qubit)
    
    # Measure all qubits
    qc.measure_all()
    
    return qc

