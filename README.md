# QRC_hackathon_Paris_2025
Contains the project presented at the Qiskit Fall Fest Paris-Saclay 2025 for the Quandela - track 2 hackathon
# Quantum Reservoir Computing (QRC) for Swaption Price Forecasting

This project implements a **Quantum Reservoir Computing (QRC)** model, based on a Transverse-Field Ising Hamiltonian, to predict the principal components (PC) of financial swaption prices. The QRC is applied to a time-series forecasting problem with an autoregressive structure, following the methodology described in the reference paper: [arXiv:2505.13933](https://arxiv.org/abs/2505.13933).

---

## Project Structure

The repository is structured around two core files:

1.  `hackathon_Paris_2025.ipynb`: The primary Jupyter Notebook detailing the entire workflow, from data loading, pre-processing (PCA and $\mathbf{[0, 2\pi]}$ normalization), QRC circuit execution, Ridge Regression readout training, and final comparison against the classical baseline.
2.  `Generate_QRC_circuit.py`: An auxiliary Python module containing the reusable functions necessary to build and parametrize the quantum reservoir circuit.

---

## Core Module: `Generate_QRC_circuit.py`

This module defines the architectural backbone of the Quantum Reservoir (QR), using an all-to-all coupling scheme between input and hidden qubits.

### Key Functions

| Function Name | Description |
| :--- | :--- |
| **`build_QRC_layer`** | Constructs a single time step (layer) of the reservoir. It applies **Angle Encoding** ($\mathbf{R}\_Y$) of input features and simulates the fixed **Ising Hamiltonian evolution** (via $\mathbf{R}\_Z$ local fields and $\mathbf{R}\_{XX}$ coupling). |
| **`build_QRC_circuit`** | Assembles the complete QRC circuit by stacking multiple layers (`num_layers`) and manages the quantum registers (input/hidden qubits). Crucially, it applies a **reset operation** to the input qubits after each layer to maintain the reservoir's state between time steps. |

---

## Quantum Backend and Noise Management

The project is designed to evaluate QRC performance under realistic quantum computing conditions. The notebook allows the user to switch between different execution modes:

### 1. Simulated Backend (with Noise)
When selecting a Qiskit Aer simulator (set "simulator = True"), the code loads and integrate a **Simulated Noise Model** derived from a real least-busy quantum device. This simulates real-world hardware imperfections (decoherence, gate errors, readout errors), allowing the assessment of the QRC model's robustness under realistic, albeit simulated, conditions. **Notice that no errore mitigation/suppression techniques are implemented in this case**: directly comment the noise-implementing lines of code to avoid noise action.

### 2. Real Hardware Backend (with Mitigation)
For execution on an actual quantum device, set "simulator = False" -> the workflow incorporates crucial noise handling techniques to improve result fidelity:
* **Gate twirling**
* **Dynamical decoupling**

---

## Getting Started

### Prerequisites
1.  **Python 3.x**
2.  **Required Libraries:** Install the necessary packages:
    ```bash
    pip install qiskit qiskit-aer numpy pandas scikit-learn matplotlib
    ```
    *(For real hardware access, `qiskit-ibm-runtime` is also required.)*

### Execution Steps
1.  **Clone the repository:**
    ```bash
    git clone [YOUR_REPOSITORY_URL]
    cd [YOUR_REPOSITORY_NAME]
    ```
2.  **Open the notebook:** Launch `hackathon_Paris_2025.ipynb` in a Jupyter environment.
3.  **Data Loading:** Ensure the financial dataset (e.g., `Dataset_Simulated_Price_swaption.xlsx`) is available in the specified path.
4.  **Configuration:** In the backend selection cell, configure your user-defined parameters ($n_2, \nu, t$ and backend choice (Simulator or Real Device).
5.  **Run All:** Execute all cells sequentially. The notebook performs:
    * PCA and data encoding.
    * Autoregressive Feature ($\mathbf{X}$) and Target ($\mathbf{Y}$) construction.
    * QRC execution to obtain quantum features ($\mathbf{R}$).
    * Training of **QRC Readout** ($\mathbf{Ridge}$ on $\mathbf{R}$).
    * Training of **GB Baseline** ($\mathbf{GB}$ on $\mathbf{X}$) for end-to-end comparison.
    * Final Mean Squared Error (MSE) comparison and inverse transformation of results to original price scale.

---

## Comparison Goal

The project's main objective is an **end-to-end comparison** of performance between the QRC model and a strong classical baseline:

| Model | Feature Input | Model Complexity |
| :--- | :--- | :--- |
| **QRC (Full Flow)** | Classical $\mathbf{X}$ (9 features) | Fixed Quantum Dynamics + Linear Readout |
| **GB Baseline** | Classical $\mathbf{X}$ (9 features) | Non-Linear Gradient Boosting |

The final MSE comparison determines if the QRC approach provides a viable alternative or advantage for financial time-series prediction.
