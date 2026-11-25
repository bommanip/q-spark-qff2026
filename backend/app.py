
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

import math
import secrets


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
            return jsonify({"error": "Choose H or X gate."}), 400

        if not 1 <= shots <= 10000:
            return jsonify({"error": "Shots must be between 1 and 10000."}), 400

        circuit = QuantumCircuit(1, 1)

        if gate == "h":
            circuit.h(0)
        else:
            circuit.x(0)

        circuit.measure(0, 0)

        result = simulator.run(circuit, shots=shots).result()
        counts = result.get_counts()

        return jsonify({
            "gate": gate.upper(),
            "shots": shots,
            "counts": counts,
            "circuit": str(circuit.draw(output="text"))
        })

    except (ValueError, TypeError):
        return jsonify({"error": "Please enter valid circuit settings."}), 400

    except Exception:
        return jsonify({"error": "The quantum simulation could not be completed."}), 500


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
            return jsonify({"error": "Shots must be between 1 and 10000."}), 400

        circuit = QuantumCircuit(2, 2)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure([0, 1], [0, 1])

        result = simulator.run(circuit, shots=shots).result()
        counts = result.get_counts()

        return jsonify({
            "experiment": "Bell State Entanglement",
            "shots": shots,
            "counts": counts,
            "circuit": str(circuit.draw(output="text")),
            "explanation": (
                "The two qubits are entangled. Their measurement "
                "results are correlated: both are usually 0 or both are 1."
            )
        })

    except (ValueError, TypeError):
        return jsonify({"error": "Please enter valid experiment settings."}), 400

    except Exception:
        return jsonify({"error": "The entanglement simulation could not be completed."}), 500


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
            return jsonify({"error": "Shots must be between 1 and 10000."}), 400

        if experiment == "x":
            circuit = QuantumCircuit(1, 1)
            circuit.x(0)
            circuit.measure(0, 0)
            explanation = "The X gate flips the qubit from |0> to |1>. The expected measurement result is 1."

        elif experiment == "z":
            circuit = QuantumCircuit(1, 1)
            circuit.h(0)
            circuit.z(0)
            circuit.h(0)
            circuit.measure(0, 0)
            explanation = "The Z gate changes the phase of the qubit. The H gates allow us to observe this phase change through interference. The expected result is 1."

        elif experiment == "cnot":
            circuit = QuantumCircuit(2, 2)
            circuit.x(0)
            circuit.cx(0, 1)
            circuit.measure([0, 1], [0, 1])
            explanation = "The control qubit starts at 1. The CNOT gate flips the target qubit. The expected measurement result is 11."

        elif experiment == "combined":
            circuit = QuantumCircuit(1, 1)
            circuit.h(0)
            circuit.x(0)
            circuit.h(0)
            circuit.measure(0, 0)
            explanation = "The H, X and H gates are applied in sequence. The expected result is 0."

        else:
            return jsonify({"error": "Choose x, z, cnot or combined."}), 400

        result = simulator.run(circuit, shots=shots).result()
        counts = result.get_counts()

        return jsonify({
            "experiment": experiment,
            "shots": shots,
            "counts": counts,
            "circuit": str(circuit.draw(output="text")),
            "explanation": explanation
        })

    except (ValueError, TypeError):
        return jsonify({"error": "Please enter valid experiment settings."}), 400

    except Exception:
        return jsonify({"error": "The experiment could not be completed."}), 500


# ==========================================
# SHARED GROVER'S SEARCH ENGINE
# ==========================================

def execute_grover(marked_state, shots):
    """
    Runs a two-qubit Grover search.

    Four possible states:
    00 = top-left
    01 = top-right
    10 = bottom-left
    11 = bottom-right

    The selected marked state is amplified
    using one Grover iteration.
    """

    circuit = QuantumCircuit(2, 2)

    # Step 1: Create equal superposition.
    circuit.h([0, 1])

    # Step 2: Oracle.
    # Convert the chosen target into |11>
    # so that CZ marks the required state.

    if marked_state[1] == "0":
        circuit.x(0)

    if marked_state[0] == "0":
        circuit.x(1)

    circuit.cz(0, 1)

    # Undo the temporary X gates.
    if marked_state[0] == "0":
        circuit.x(1)

    if marked_state[1] == "0":
        circuit.x(0)

    # Step 3: Grover diffusion operator.
    circuit.h([0, 1])
    circuit.x([0, 1])
    circuit.cz(0, 1)
    circuit.x([0, 1])
    circuit.h([0, 1])

    # Step 4: Measure.
    circuit.measure([0, 1], [0, 1])

    # Step 5: Run simulation.
    result = simulator.run(circuit, shots=shots).result()
    counts = result.get_counts()

    success_count = counts.get(marked_state, 0)
    success_percentage = round((success_count / shots) * 100, 2)

    return {
        "counts": counts,
        "marked_state": marked_state,
        "success_count": success_count,
        "success_percentage": success_percentage,
        "circuit": str(circuit.draw(output="text"))
    }


# ==========================================
# MODULE 4: ORIGINAL GROVER'S SEARCH
# ==========================================

@app.post("/api/run-grover")
@app.route("/run-grover", methods=["POST"])
def run_grover():
    data = request.get_json(silent=True) or {}

    try:
        shots = int(data.get("shots", 1024))

        if not 1 <= shots <= 10000:
            return jsonify({"error": "Shots must be between 1 and 10000."}), 400

        # Preserve the original default marked state.
        experiment = execute_grover("11", shots)

        return jsonify({
            "experiment": "Grover's Search Algorithm",
            "shots": shots,
            "counts": experiment["counts"],
            "marked_state": experiment["marked_state"],
            "circuit": experiment["circuit"],
            "explanation": (
                "Grover's algorithm creates an equal superposition "
                "of four possible answers. The oracle marks 11. "
                "The diffusion operator amplifies the marked answer. "
                "One iteration returns 11 with certainty in an ideal simulation."
            )
        })

    except (ValueError, TypeError):
        return jsonify({"error": "Please enter valid experiment settings."}), 400

    except Exception:
        return jsonify({"error": "Grover's simulation could not be completed."}), 500


# ==========================================
# ARCADE GAME 1: COIN LAB
# ==========================================

@app.route("/run-coin-lab", methods=["POST"])
def run_coin_lab():
    data = request.get_json(silent=True) or {}

    try:
        tilt = float(data.get("tilt_degrees", 90))
        shots = int(data.get("shots", 1024))

        if not 0 <= tilt <= 180:
            return jsonify({"error": "Tilt must be between 0 and 180 degrees."}), 400

        if not 1 <= shots <= 10000:
            return jsonify({"error": "Shots must be between 1 and 10000."}), 400

        angle = math.radians(tilt)

        circuit = QuantumCircuit(1, 1)
        circuit.ry(angle, 0)
        circuit.measure(0, 0)

        result = simulator.run(circuit, shots=shots).result()
        counts = result.get_counts()

        heads_count = counts.get("0", 0)
        tails_count = counts.get("1", 0)

        heads_probability = math.cos(angle / 2) ** 2
        tails_probability = math.sin(angle / 2) ** 2

        return jsonify({
            "experiment": "Coin Lab",
            "tilt_degrees": tilt,
            "shots": shots,
            "counts": {
                "heads": heads_count,
                "tails": tails_count
            },
            "probabilities": {
                "heads": round(heads_probability * 100, 2),
                "tails": round(tails_probability * 100, 2)
            },
            "observed_percentages": {
                "heads": round((heads_count / shots) * 100, 2),
                "tails": round((tails_count / shots) * 100, 2)
            },
            "circuit": str(circuit.draw(output="text")),
            "explanation": (
                "The RY gate rotates the qubit by the selected angle. "
                "Measurement produces one outcome per shot. "
                "Observed percentages may vary from theoretical probabilities."
            )
        })

    except (ValueError, TypeError):
        return jsonify({"error": "Please enter a valid tilt and shot count."}), 400

    except Exception:
        return jsonify({"error": "The Coin Lab simulation could not be completed."}), 500


# ==========================================
# ARCADE GAME 2: LINKED DICE
# ==========================================

@app.route("/run-linked-dice", methods=["POST"])
def run_linked_dice():
    data = request.get_json(silent=True) or {}

    try:
        mode = data.get("mode", "independent").lower()
        shots = int(data.get("shots", 1024))

        if mode not in ["independent", "entangled"]:
            return jsonify({
                "error": "Choose independent or entangled mode."
            }), 400

        if not 1 <= shots <= 10000:
            return jsonify({
                "error": "Shots must be between 1 and 10000."
            }), 400

        # Each die uses 3 qubits.
        # Binary outcomes 000 to 101 represent faces 1 to 6.
        # Outcomes 110 and 111 are rejected.

        if mode == "independent":
            circuit = QuantumCircuit(6, 6)
            circuit.h([0, 1, 2, 3, 4, 5])

            explanation = (
                "Each die is created using three independent qubits. "
                "Both dice have six equally likely valid outcomes. "
                "Their results are independent, so matching numbers "
                "occur by chance."
            )

        else:
            circuit = QuantumCircuit(6, 6)

            circuit.h(0)
            circuit.h(1)
            circuit.h(2)

            circuit.cx(0, 3)
            circuit.cx(1, 4)
            circuit.cx(2, 5)

            explanation = (
                "Three Bell pairs connect the corresponding qubits "
                "of the two dice. Their three-bit measurement values "
                "are perfectly correlated. After invalid outcomes are "
                "rejected, both fair six-sided dice show the same number."
            )

        circuit.measure([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5])

        pair_counts = {}
        first_die_counts = {str(i): 0 for i in range(1, 7)}
        second_die_counts = {str(i): 0 for i in range(1, 7)}

        accepted = 0
        raw_shots = 0
        max_raw_shots = shots * 20 + 10000

        while accepted < shots and raw_shots < max_raw_shots:

            remaining = shots - accepted
            batch_size = min(max(remaining * 2, 256), 10000)

            result = simulator.run(
                circuit,
                shots=batch_size
            ).result()

            counts = result.get_counts()
            raw_shots += batch_size

            for bitstring, frequency in counts.items():

                bits = bitstring.replace(" ", "")

                first_value = int(bits[-3:], 2)
                second_value = int(bits[:3], 2)

                if first_value >= 6 or second_value >= 6:
                    continue

                first_die = first_value + 1
                second_die = second_value + 1

                usable = min(frequency, shots - accepted)

                if usable <= 0:
                    continue

                pair = f"{first_die}-{second_die}"

                pair_counts[pair] = pair_counts.get(pair, 0) + usable

                first_die_counts[str(first_die)] += usable
                second_die_counts[str(second_die)] += usable

                accepted += usable

                if accepted >= shots:
                    break

        if accepted < shots:
            return jsonify({
                "error": "Could not collect enough valid dice rolls. Please try again."
            }), 500

        matching = sum(
            count for pair, count in pair_counts.items()
            if pair.split("-")[0] == pair.split("-")[1]
        )

        matching_percentage = round((matching / shots) * 100, 2)

        return jsonify({
            "experiment": "Linked Dice",
            "mode": mode,
            "shots": shots,
            "accepted_shots": accepted,
            "raw_shots": raw_shots,
            "dice": {
                "die_one": first_die_counts,
                "die_two": second_die_counts
            },
            "pair_counts": pair_counts,
            "matching_rolls": matching,
            "matching_percentage": matching_percentage,
            "circuit": str(circuit.draw(output="text")),
            "explanation": explanation
        })

    except (ValueError, TypeError):
        return jsonify({
            "error": "Please enter valid Linked Dice settings."
        }), 400

    except Exception:
        return jsonify({
            "error": "The Linked Dice simulation could not be completed."
        }), 500


# ==========================================
# ARCADE GAME 3: QUANTUM TREASURE HUNT
# ==========================================

@app.route("/run-treasure-hunt", methods=["POST"])
def run_treasure_hunt():
    data = request.get_json(silent=True) or {}

    try:
        shots = int(data.get("shots", 1024))

        if not 1 <= shots <= 10000:
            return jsonify({
                "error": "Shots must be between 1 and 10000."
            }), 400

        # Four possible treasure locations.
        locations = {
            "00": "top-left",
            "01": "top-right",
            "10": "bottom-left",
            "11": "bottom-right"
        }

        # A random treasure is hidden when no target is supplied.
        # The frontend can also supply a marked_state for a chosen challenge.
        marked_state = data.get("marked_state")

        if marked_state is None:
            marked_state = secrets.choice(list(locations.keys()))

        if not isinstance(marked_state, str) or marked_state not in locations:
            return jsonify({
                "error": "Invalid treasure location. Choose 00, 01, 10 or 11."
            }), 400

        # Run Grover's algorithm for the hidden treasure.
        experiment = execute_grover(marked_state, shots)

        return jsonify({
            "experiment": "Quantum Treasure Hunt",
            "algorithm": "Grover's Search Algorithm",
            "shots": shots,
            "counts": experiment["counts"],
            "marked_state": experiment["marked_state"],
            "treasure_location": locations[marked_state],
            "treasure_index": int(marked_state, 2),
            "success_count": experiment["success_count"],
            "success_percentage": experiment["success_percentage"],
            "circuit": experiment["circuit"],
            "explanation": (
                "Four possible treasure locations are prepared in "
                "equal superposition. The quantum oracle marks the "
                "hidden treasure location. Grover's diffusion operator "
                "amplifies the probability of the marked location. "
                "One Grover iteration finds the marked location with "
                "certainty in an ideal two-qubit simulation."
            )
        })

    except (ValueError, TypeError):
        return jsonify({
            "error": "Please enter valid Treasure Hunt settings."
        }), 400

    except Exception:
        return jsonify({
            "error": "The Treasure Hunt simulation could not be completed."
        }), 500


# ==========================================
# START FLASK SERVER
# ==========================================

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
