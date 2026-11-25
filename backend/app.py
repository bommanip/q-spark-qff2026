
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


frontend = Path(__file__).resolve().parents[1] / "frontend"
app = Flask(__name__, static_folder=frontend, static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 4096
CORS(app)

simulator = AerSimulator()


# ==========================================
# HOME
# ==========================================

@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.get("/health")
def health():
    return jsonify({
        "message": "Welcome to QubitQuest!",
        "status": "Quantum simulator is ready."
    })


# ==========================================
# MODULE 2: H GATE
# ==========================================

@app.post("/api/run-circuit")
@app.route("/run-circuit", methods=["POST"])
def run_circuit():

    data = request.get_json(silent=True) or {}

    try:
        gate = data.get("gate", "h").lower()
        shots = int(data.get("shots", 1024))

        if gate not in ["h", "x"]:
            return jsonify({
                "error": "Choose H or X gate."
            }), 400

        if not 1 <= shots <= 10000:
            return jsonify({
                "error": "Shots must be between 1 and 10000."
            }), 400

        circuit = QuantumCircuit(1, 1)

        if gate == "h":
            circuit.h(0)
        else:
            circuit.x(0)

        circuit.measure(0, 0)

        result = simulator.run(
            circuit,
            shots=shots
        ).result()

        counts = result.get_counts()

        return jsonify({
            "gate": gate.upper(),
            "shots": shots,
            "counts": counts,
            "circuit": str(circuit.draw(output="text"))
        })

    except (ValueError, TypeError):
        return jsonify({
            "error": "Please enter valid circuit settings."
        }), 400

    except Exception:
        return jsonify({
            "error": "The quantum simulation could not be completed."
        }), 500


# ==========================================
# MODULE 2: BELL STATE ENTANGLEMENT
# ==========================================

@app.post("/api/run-entanglement")
@app.route("/run-entanglement", methods=["POST"])
def run_entanglement():

    data = request.get_json(silent=True) or {}

    try:
        shots = int(data.get("shots", 1024))

        if not 1 <= shots <= 10000:
            return jsonify({
                "error": "Shots must be between 1 and 10000."
            }), 400

        circuit = QuantumCircuit(2, 2)

        circuit.h(0)
        circuit.cx(0, 1)

        circuit.measure([0, 1], [0, 1])

        result = simulator.run(
            circuit,
            shots=shots
        ).result()

        counts = result.get_counts()

        return jsonify({
            "experiment": "Bell State Entanglement",
            "shots": shots,
            "counts": counts,
            "circuit": str(circuit.draw(output="text")),
            "explanation": (
                "The two qubits are entangled. "
                "Their measurement results are correlated: "
                "both are usually 0 or both are 1."
            )
        })

    except (ValueError, TypeError):
        return jsonify({
            "error": "Please enter valid experiment settings."
        }), 400

    except Exception:
        return jsonify({
            "error": "The entanglement simulation could not be completed."
        }), 500


# ==========================================
# MODULE 3: QUANTUM GATES
# ==========================================

@app.post("/api/run-module3")
@app.route("/run-module3", methods=["POST"])
def run_module3():

    data = request.get_json(silent=True) or {}

    try:
        experiment = data.get("experiment", "").lower()
        shots = int(data.get("shots", 1024))

        if not 1 <= shots <= 10000:
            return jsonify({
                "error": "Shots must be between 1 and 10000."
            }), 400

        # X GATE
        if experiment == "x":

            circuit = QuantumCircuit(1, 1)

            circuit.x(0)
            circuit.measure(0, 0)

            explanation = (
                "The X gate flips the qubit from |0> to |1>. "
                "The expected measurement result is 1."
            )

        # Z GATE: H -> Z -> H
        elif experiment == "z":

            circuit = QuantumCircuit(1, 1)

            circuit.h(0)
            circuit.z(0)
            circuit.h(0)

            circuit.measure(0, 0)

            explanation = (
                "The Z gate changes the phase of the qubit. "
                "The H gates allow us to observe this phase change "
                "through interference. The expected result is 1."
            )

        # CNOT GATE
        elif experiment == "cnot":

            circuit = QuantumCircuit(2, 2)

            circuit.x(0)
            circuit.cx(0, 1)

            circuit.measure([0, 1], [0, 1])

            explanation = (
                "The control qubit starts at 1. "
                "The CNOT gate flips the target qubit. "
                "The expected measurement result is 11."
            )

        # COMBINED GATES: H -> X -> H
        elif experiment == "combined":

            circuit = QuantumCircuit(1, 1)

            circuit.h(0)
            circuit.x(0)
            circuit.h(0)

            circuit.measure(0, 0)

            explanation = (
                "The H, X and H gates are applied in sequence. "
                "The X gate leaves the equal superposition unchanged, "
                "and the final H gate returns the qubit to |0>. "
                "The expected measurement result is 0."
            )

        else:

            return jsonify({
                "error": "Choose x, z, cnot or combined."
            }), 400

        result = simulator.run(
            circuit,
            shots=shots
        ).result()

        counts = result.get_counts()

        return jsonify({
            "experiment": experiment,
            "shots": shots,
            "counts": counts,
            "circuit": str(circuit.draw(output="text")),
            "explanation": explanation
        })

    except (ValueError, TypeError):
        return jsonify({
            "error": "Please enter valid experiment settings."
        }), 400

    except Exception:
        return jsonify({
            "error": "The experiment could not be completed."
        }), 500


# ==========================================
# MODULE 4: GROVER'S SEARCH ALGORITHM
# ==========================================

@app.post("/api/run-grover")
@app.route("/run-grover", methods=["POST"])
def run_grover():

    data = request.get_json(silent=True) or {}

    try:
        shots = int(data.get("shots", 1024))

        if not 1 <= shots <= 10000:
            return jsonify({
                "error": "Shots must be between 1 and 10000."
            }), 400

        # Create a two-qubit circuit
        # with two classical measurement bits.

        circuit = QuantumCircuit(2, 2)

        # STEP 1: Create equal superposition.

        circuit.h([0, 1])

        # STEP 2: Oracle.
        # Mark the answer |11> by changing its phase.

        circuit.cz(0, 1)

        # STEP 3: Grover diffusion operator.

        circuit.h([0, 1])
        circuit.x([0, 1])

        circuit.cz(0, 1)

        circuit.x([0, 1])
        circuit.h([0, 1])

        # STEP 4: Measure both qubits.

        circuit.measure([0, 1], [0, 1])

        # Run the actual Qiskit simulation.

        result = simulator.run(
            circuit,
            shots=shots
        ).result()

        counts = result.get_counts()

        return jsonify({
            "experiment": "Grover's Search Algorithm",
            "shots": shots,
            "counts": counts,
            "marked_state": "11",
            "circuit": str(circuit.draw(output="text")),
            "explanation": (
                "Grover's algorithm starts by creating an equal "
                "superposition of four possible answers: 00, 01, "
                "10 and 11. The oracle marks 11. The diffusion "
                "operator amplifies the probability of the marked "
                "answer. After one Grover iteration, measuring "
                "the two qubits returns 11 with certainty in "
                "an ideal simulation."
            )
        })

    except (ValueError, TypeError):
        return jsonify({
            "error": "Please enter valid experiment settings."
        }), 400

    except Exception:
        return jsonify({
            "error": "Grover's simulation could not be completed."
        }), 500


# ==========================================
# START FLASK SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )
