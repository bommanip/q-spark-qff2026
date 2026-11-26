"""Compare one blind guess with Q-Spark's two-qubit treasure circuit."""

from random import Random

from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

from backend.app import execute_grover

SHOTS = 1024
SEED = 2026


def main():
    random = Random(SEED)
    noise = NoiseModel()
    noise.add_all_qubit_quantum_error(depolarizing_error(0.02, 2), ["cx", "cz"])
    noisy_simulator = AerSimulator(noise_model=noise, seed_simulator=SEED)
    totals = [0, 0, 0]
    print("| Target | Random guess | Ideal Aer | Noisy Aer | Circuit depth |")
    print("| --- | ---: | ---: | ---: | ---: |")
    for target in ("00", "01", "10", "11"):
        classical = sum(random.randrange(4) == int(target, 2) for _ in range(SHOTS))
        ideal = execute_grover(target, shots=SHOTS)
        circuit = ideal["circuit_object"]
        noisy = noisy_simulator.run(circuit, shots=SHOTS).result().get_counts()
        hits = [classical, ideal["counts"].get(target, 0), noisy.get(target, 0)]
        assert hits[1] == SHOTS, (target, ideal["counts"])
        totals = [total + count for total, count in zip(totals, hits)]
        print(f"| `{target}` | " + " | ".join(map(str, hits)) + f" | {circuit.depth()} |")
    print("| **Total** | " + " | ".join(f"**{hits}/{4 * SHOTS} ({hits / (4 * SHOTS):.2%})**" for hits in totals) + " | — |")


if __name__ == "__main__":
    main()
