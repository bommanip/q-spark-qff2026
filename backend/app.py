
import base64
import io
import math
import threading
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from flask import Flask, jsonify, request
from flask_cors import CORS

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


# ==========================================
# APP CONFIGURATION
# ==========================================

frontend = Path(__file__).resolve().parents[1] / "frontend"
app = Flask(__name__, static_folder=frontend, static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 4096
CORS(app)

simulator = AerSimulator()
plot_lock = threading.Lock()


# ==========================================
# VISUALIZATION HELPERS
# ==========================================

def figure_to_base64(fig):
    buffer = io.BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=150,
        bbox_inches="tight",
        facecolor="#ffffff"
    )

    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode("utf-8")

    plt.close(fig)

    return "data:image/png;base64," + encoded


def generate_circuit_image(circuit):
    try:
        with plot_lock:
            fig = circuit.draw(
                output="mpl",
                fold=-1
            )

            return figure_to_base64(fig)

    except Exception as error:
        print("Circuit image error:", error)
        return None


def generate_histogram_image(counts, title="Measurement Results"):
    try:
        with plot_lock:
            labels = list(counts.keys())
            values = list(counts.values())

            fig, ax = plt.subplots(figsize=(8, 4))

            bars = ax.bar(
                labels,
                values,
                color="#7657E8",
                edgecolor="#4C35A5",
                linewidth=1.2
            )

            ax.set_title(title, fontsize=14, fontweight="bold")
            ax.set_xlabel("Measurement Outcome")
            ax.set_ylabel("Number of Measurements")
            ax.grid(axis="y", alpha=0.25)

            for bar, value in zip(bars, values):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    str(value),
                    ha="center",
                    va="bottom"
                )

            fig.tight_layout()

            return figure_to_base64(fig)

    except Exception as error:
        print("Histogram image error:", error)
        return None


def add_visualizations(response, circuit, counts, chart_title):
    response["circuit_image"] = generate_circuit_image(circuit)

    response["histogram_image"] = generate_histogram_image(
        counts,
        chart_title
    )

    return response


# ==========================================
# GENERAL HELPERS
# ==========================================

def run_circuit(circuit, shots=1024):
    compiled = circuit.copy()

    result = simulator.run(
        compiled,
        shots=shots
    ).result()

    return result.get_counts()


def validate_shots(value, default=1024):
    try:
        shots = int(value)
    except (TypeError, ValueError):
        shots = default

    return max(1, min(shots, 10000))


# ==========================================
# GROVER ALGORITHM HELPER
# ==========================================

def execute_grover(marked_state, shots=1024):

    circuit = QuantumCircuit(2, 2)

    # Initial superposition
    circuit.h([0, 1])

    # Qiskit displays bit 0 at the right end of each measurement string.
    zero_qubits = [qubit for qubit, bit in enumerate(reversed(marked_state)) if bit == "0"]
    for qubit in zero_qubits:
        circuit.x(qubit)
    circuit.cz(0, 1)
    for qubit in zero_qubits:
        circuit.x(qubit)

    # Diffusion operator
    circuit.h([0, 1])
    circuit.x([0, 1])
    circuit.h(1)
    circuit.cx(0, 1)
    circuit.h(1)
    circuit.x([0, 1])
    circuit.h([0, 1])

    # Measurement
    circuit.measure([0, 1], [0, 1])

    counts = run_circuit(circuit, shots)

    return {
        "counts": counts,
        "circuit": str(circuit),
        "circuit_object": circuit
    }


# ==========================================
# HOME
# ==========================================

@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.get("/health")
def home():

    return jsonify({
        "message": "Welcome to Q-Spark!",
        "status": "Quantum simulator is ready."
    })


# ==========================================
# MODULE 1 - BASIC QUANTUM CIRCUITS
# ==========================================

@app.route("/run-circuit", methods=["POST"])
def run_basic_circuit():

    data = request.get_json(silent=True) or {}

    gate = str(data.get("gate", "H")).upper()
    shots = validate_shots(data.get("shots", 1024))

    circuit = QuantumCircuit(1, 1)

    if gate == "X":
        circuit.x(0)
    else:
        circuit.h(0)

    circuit.measure(0, 0)

    counts = run_circuit(circuit, shots)

    response = {
        "experiment": "Basic Quantum Circuit",
        "gate": gate,
        "shots": shots,
        "counts": counts,
        "circuit": str(circuit),
        "explanation": (
            "The Hadamard gate creates a superposition."
            if gate == "H"
            else "The Pauli-X gate flips the qubit from 0 to 1."
        )
    }

    return jsonify(add_visualizations(
        response,
        circuit,
        counts,
        "Basic Circuit Measurement Results"
    ))


# ==========================================
# MODULE 2 - ENTANGLEMENT
# ==========================================

@app.route("/run-entanglement", methods=["POST"])
def run_entanglement():

    data = request.get_json(silent=True) or {}

    shots = validate_shots(data.get("shots", 1024))

    circuit = QuantumCircuit(2, 2)

    circuit.h(0)
    circuit.cx(0, 1)

    circuit.measure([0, 1], [0, 1])

    counts = run_circuit(circuit, shots)

    response = {
        "experiment": "Quantum Entanglement",
        "shots": shots,
        "counts": counts,
        "circuit": str(circuit),
        "explanation": (
            "The Hadamard gate creates superposition. "
            "The CNOT gate entangles the two qubits. "
            "Their measurement results are correlated."
        )
    }

    return jsonify(add_visualizations(
        response,
        circuit,
        counts,
        "Entanglement Measurement Results"
    ))


# ==========================================
# MODULE 3 - QUANTUM GATES
# ==========================================

@app.route("/run-module3", methods=["POST"])
def run_module3():

    data = request.get_json(silent=True) or {}

    gate = str(data.get("gate", "X")).upper()
    shots = validate_shots(data.get("shots", 1024))

    circuit = QuantumCircuit(2, 2)

    if gate == "X":
        circuit.x(0)

    elif gate == "Z":
        circuit.h(0)
        circuit.z(0)
        circuit.h(0)

    elif gate == "CNOT":
        circuit.x(0)
        circuit.cx(0, 1)

    elif gate == "H":
        circuit.h(0)

    else:
        circuit.h(0)
        circuit.x(0)
        circuit.h(0)

    circuit.measure([0, 1], [0, 1])

    counts = run_circuit(circuit, shots)

    response = {
        "experiment": "Quantum Gates",
        "gate": gate,
        "shots": shots,
        "counts": counts,
        "circuit": str(circuit),
        "explanation": (
            "This experiment demonstrates the action "
            "of the selected quantum gate."
        )
    }

    return jsonify(add_visualizations(
        response,
        circuit,
        counts,
        "Quantum Gate Measurement Results"
    ))


# ==========================================
# MODULE 4 - GROVER'S ALGORITHM
# ==========================================

@app.route("/run-grover", methods=["POST"])
def run_grover():

    data = request.get_json(silent=True) or {}

    marked_state = str(data.get("marked_state", "11"))

    if marked_state not in ["00", "01", "10", "11"]:
        return jsonify({
            "error": "Marked state must be 00, 01, 10 or 11."
        }), 400

    shots = validate_shots(data.get("shots", 1024))

    result = execute_grover(marked_state, shots)

    counts = result["counts"]
    circuit = result["circuit_object"]

    response = {
        "experiment": "Grover's Search Algorithm",
        "marked_state": marked_state,
        "shots": shots,
        "counts": counts,
        "circuit": result["circuit"],
        "explanation": (
            "Grover's algorithm uses an oracle to mark the target "
            "state and a diffusion operator to amplify its probability."
        )
    }

    return jsonify(add_visualizations(
        response,
        circuit,
        counts,
        "Grover Search Measurement Results"
    ))


# ==========================================
# COIN LAB
# ==========================================

@app.route("/run-coin-lab", methods=["POST"])
def run_coin_lab():

    data = request.get_json(silent=True) or {}

    try:
        tilt_degrees = float(data.get("tilt_degrees", 90))
    except (TypeError, ValueError):
        tilt_degrees = 90

    tilt_degrees = max(0, min(180, tilt_degrees))

    shots = validate_shots(data.get("shots", 1024))

    angle = math.radians(tilt_degrees)

    circuit = QuantumCircuit(1, 1)

    circuit.ry(angle, 0)
    circuit.measure(0, 0)

    counts = run_circuit(circuit, shots)

    heads = counts.get("0", 0)
    tails = counts.get("1", 0)

    heads_probability = math.cos(angle / 2) ** 2
    tails_probability = math.sin(angle / 2) ** 2

    response = {
        "experiment": "Quantum Coin Lab",
        "tilt_degrees": tilt_degrees,
        "shots": shots,
        "heads": heads,
        "tails": tails,
        "counts": counts,
        "heads_probability": round(heads_probability * 100, 2),
        "tails_probability": round(tails_probability * 100, 2),
        "circuit": str(circuit),
        "explanation": (
            "The Ry rotation changes the probability of measuring "
            "heads or tails. The measurement counts are sampled "
            "from the quantum simulator."
        )
    }

    return jsonify(add_visualizations(
        response,
        circuit,
        {
            "Heads": heads,
            "Tails": tails
        },
        "Quantum Coin Measurement Results"
    ))


# ==========================================
# LINKED DICE
# ==========================================

@app.route("/run-linked-dice", methods=["POST"])
def run_linked_dice():

    data = request.get_json(silent=True) or {}

    mode = str(data.get("mode", "independent")).lower()

    if mode not in ["independent", "entangled"]:
        return jsonify({
            "error": "Mode must be independent or entangled."
        }), 400

    shots = validate_shots(data.get("shots", 1024))

    circuit = QuantumCircuit(6, 6)

    if mode == "independent":
        circuit.h(range(6))

    else:
        circuit.h([0, 1, 2])
        circuit.cx(0, 3)
        circuit.cx(1, 4)
        circuit.cx(2, 5)

    circuit.measure(range(6), range(6))

    result = simulator.run(
        circuit,
        shots=shots * 3
    ).result()

    raw_counts = result.get_counts()

    # Separate distributions for the two dice
    die_one_counts = {}
    die_two_counts = {}

    pair_counts = {}

    matching_rolls = 0
    accepted_shots = 0

    for binary, frequency in raw_counts.items():

        value = int(binary.replace(" ", ""), 2)

        # First die uses qubits 0, 1, 2
        first_die = value & 7

        # Second die uses qubits 3, 4, 5
        second_die = (value >> 3) & 7

        # Reject invalid values (6 and 7)
        if first_die >= 6 or second_die >= 6:
            continue

        # Convert binary values 0-5 into dice faces 1-6
        first_die += 1
        second_die += 1

        pair = f"{first_die}-{second_die}"

        pair_counts[pair] = (
            pair_counts.get(pair, 0) + frequency
        )

        die_one_counts[first_die] = (
            die_one_counts.get(first_die, 0) + frequency
        )

        die_two_counts[second_die] = (
            die_two_counts.get(second_die, 0) + frequency
        )

        accepted_shots += frequency

        if first_die == second_die:
            matching_rolls += frequency

    if accepted_shots == 0:
        return jsonify({
            "error": "No valid dice results were generated. Please retry."
        }), 500

    # Each die gets its own six-face distribution
    die_one_distribution = {
        str(number): die_one_counts.get(number, 0)
        for number in range(1, 7)
    }

    die_two_distribution = {
        str(number): die_two_counts.get(number, 0)
        for number in range(1, 7)
    }

    # Preserve the previous combined/legacy distribution field
    dice_distribution = die_one_distribution.copy()

    # Exact structure expected by the Linked Dice frontend
    dice = {
        "die_one": die_one_distribution,
        "die_two": die_two_distribution
    }

    response = {
        "experiment": "Linked Quantum Dice",
        "mode": mode,
        "shots": accepted_shots,
        "accepted_shots": accepted_shots,
        "raw_shots": shots * 3,

        "dice": dice,
        "dice_distribution": dice_distribution,

        "pair_counts": pair_counts,

        "matching_rolls": matching_rolls,

        "matching_percentage": round(
            matching_rolls / accepted_shots * 100,
            2
        ),

        "circuit": str(circuit),

        "explanation": (
            "Independent mode applies Hadamard gates to all six qubits. "
            "Entangled mode creates correlated qubit pairs using CNOT gates. "
            "Each die has its own measurement distribution. "
            "Invalid binary values are rejected so each die has six faces."
        )
    }

    return jsonify(add_visualizations(
        response,
        circuit,
        pair_counts,
        "Linked Dice Pair Measurement Results"
    ))


# ==========================================
# QUANTUM TREASURE HUNT
# ==========================================

@app.route("/run-treasure-hunt", methods=["POST"])
def run_treasure_hunt():

    data = request.get_json(silent=True) or {}

    marked_state = str(data.get("marked_state", "11"))

    if marked_state not in ["00", "01", "10", "11"]:
        return jsonify({
            "error": "Choose a valid treasure location."
        }), 400

    shots = validate_shots(data.get("shots", 1024))

    result = execute_grover(marked_state, shots)

    counts = result["counts"]
    circuit = result["circuit_object"]

    locations = {
        "00": "Top Left",
        "01": "Top Right",
        "10": "Bottom Left",
        "11": "Bottom Right"
    }

    successful_searches = counts.get(marked_state, 0)

    response = {
        "experiment": "Quantum Treasure Hunt",
        "marked_state": marked_state,
        "treasure_location": locations[marked_state],
        "treasure_index": int(marked_state, 2),
        "shots": shots,
        "counts": counts,
        "success_percentage": round(
            successful_searches / shots * 100,
            2
        ),
        "circuit": result["circuit"],
        "explanation": (
            "Grover's algorithm searches four possible locations. "
            "The oracle marks the selected location, and the diffusion "
            "operator amplifies its probability."
        )
    }

    return jsonify(add_visualizations(
        response,
        circuit,
        counts,
        "Treasure Hunt Search Results"
    ))


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        port=8056
    )
