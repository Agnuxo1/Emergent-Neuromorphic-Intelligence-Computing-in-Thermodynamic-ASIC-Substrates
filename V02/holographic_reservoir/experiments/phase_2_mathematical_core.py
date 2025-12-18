"""
Phase II Validation: The Mathematical Core
===========================================
Following ROADMAP_FINAL.md Section 4, Phase II

Tests:
- Task 2.1: HNSDecoder (Hash -> Vector RGBA)
- Task 2.2: VeselovExpander (Bipartite Topology)
- Task 2.3: ChaosEngine (OTOC Calculation)

Author: CHIMERA Project
Date: December 2025
"""

import sys
import os
import time
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.hns import HNS
from core.topology import VeselovExpander
from core.chaos_metrics import ChaosEngine
from core.substrate import ASICSubstrate

def test_hns_decoder():
    """
    Test 2.1: HNS Decoder (Hash -> Vector)
    Verify that hash_to_rgba produces valid 4D vectors with proper statistics.
    """
    print("\n" + "="*70)
    print("TEST 2.1: HNS DECODER (Hash -> RGBA Vector)")
    print("="*70)

    # Generate test hashes
    substrate = ASICSubstrate(simulation_mode=True)
    test_seed = b"HNS_TEST_SEED_2025"

    print(f"Generating 1000 test hashes...")
    hashes = substrate.mine_reservoir_state(test_seed, cycles=1000)

    # Convert to vectors
    print("Converting hashes to RGBA vectors...")
    vectors = []
    for h in hashes:
        vec = HNS.hash_to_rgba(h)
        vectors.append(vec)

    vectors_np = np.array(vectors)

    # Statistical Analysis
    print("\n--- VECTOR STATISTICS ---")
    print(f"Shape: {vectors_np.shape}")
    print(f"Data Type: {vectors_np.dtype}")

    channels = ['R (Energy)', 'G (Gradient)', 'B (Plasticity)', 'A (Phase)']
    print(f"\n{'Channel':<18} | {'Mean':<10} | {'Std Dev':<10} | {'Min':<10} | {'Max':<10}")
    print("-" * 70)

    for i, name in enumerate(channels):
        vals = vectors_np[:, i]
        mean_val = np.mean(vals)
        std_val = np.std(vals)
        min_val = np.min(vals)
        max_val = np.max(vals)
        print(f"{name:<18} | {mean_val:.6f} | {std_val:.6f} | {min_val:.6f} | {max_val:.6f}")

    # Expected values for uniform distribution [0, 1]
    expected_mean = 0.5
    expected_std = 1.0 / np.sqrt(12)  # ~0.288675

    print(f"\n--- EXPECTED VALUES (Uniform Random) ---")
    print(f"Mean: {expected_mean:.6f}")
    print(f"Std Dev: {expected_std:.6f}")

    # Check if values are within acceptable range
    mean_check = all(0.45 < np.mean(vectors_np[:, i]) < 0.55 for i in range(4))
    std_check = all(0.25 < np.std(vectors_np[:, i]) < 0.35 for i in range(4))
    range_check = (0.0 <= vectors_np.min()) and (vectors_np.max() <= 1.0)

    # Sample vectors
    print("\n--- SAMPLE VECTORS (First 5) ---")
    for i in range(min(5, len(vectors))):
        print(f"[{i}] {HNS.vector_to_string(vectors[i])}")

    print("\n--- VALIDATION ---")
    print(f"Mean in range [0.45, 0.55]:  {mean_check}")
    print(f"Std Dev in range [0.25, 0.35]: {std_check}")
    print(f"Values in range [0.0, 1.0]:  {range_check}")

    if mean_check and std_check and range_check:
        print("\n[OK] PASSED: HNS Decoder working correctly")
        print("Interpretation: Hash -> Vector mapping preserves uniform distribution")
        return True
    else:
        print("\n[FAIL] FAILED: HNS Decoder statistics out of range")
        return False

def test_veselov_expander():
    """
    Test 2.2: Veselov Expander (Bipartite Topology)
    Verify that the expander graph properly mixes information.
    """
    print("\n" + "="*70)
    print("TEST 2.2: VESELOV EXPANDER (Bipartite Topology)")
    print("="*70)

    # Initialize topology
    n_input = 256
    n_reservoir = 1024
    degree = 6

    print(f"Configuration:")
    print(f"  Input Nodes: {n_input}")
    print(f"  Reservoir Nodes: {n_reservoir}")
    print(f"  Degree (connections per node): {degree}")

    print("\nBuilding topology...")
    expander = VeselovExpander(n_input=n_input, n_reservoir=n_reservoir, degree=degree)

    print(f"Adjacency Matrix Shape: {expander.adj_matrix.shape}")
    print(f"Matrix Sparsity: {np.count_nonzero(expander.adj_matrix) / expander.adj_matrix.size * 100:.2f}%")
    print(f"Expected Sparsity: {degree / n_reservoir * 100:.2f}%")

    # Test propagation with a simple input
    print("\n--- PROPAGATION TEST ---")

    # Create a sparse input (single hot vector in 4 channels)
    test_input = np.zeros((n_input, 4))
    test_input[0, :] = [1.0, 0.5, 0.3, 0.2]  # Single active node

    print(f"Input Shape: {test_input.shape}")
    print(f"Input Active Nodes: 1/{n_input}")

    # Propagate
    start = time.time()
    output = expander.propagate(test_input)
    end = time.time()

    print(f"\nOutput Shape: {output.shape}")
    print(f"Propagation Time: {(end-start)*1000:.3f} ms")

    # Analyze output
    print("\n--- OUTPUT ANALYSIS ---")
    for i, channel in enumerate(['R', 'G', 'B', 'A']):
        channel_data = output[:, i]
        active_nodes = np.count_nonzero(channel_data > 0.01)
        mean_activation = np.mean(np.abs(channel_data))
        max_activation = np.max(np.abs(channel_data))

        print(f"Channel {channel}: Active={active_nodes}/{n_reservoir} ({active_nodes/n_reservoir*100:.1f}%), "
              f"Mean={mean_activation:.4f}, Max={max_activation:.4f}")

    # Validation: A single input should activate multiple reservoir nodes (mixing property)
    total_active = np.count_nonzero(np.any(output > 0.01, axis=1))
    expected_active = degree  # At least 'degree' nodes should be active

    print(f"\n--- MIXING VALIDATION ---")
    print(f"Total Active Reservoir Nodes: {total_active}")
    print(f"Expected (>= degree): >= {expected_active}")

    # Test global mixing with full random input
    print("\n--- GLOBAL MIXING TEST ---")
    random_input = np.random.rand(n_input, 4)
    output_full = expander.propagate(random_input)

    coverage = np.count_nonzero(np.any(output_full > 0.01, axis=1))
    print(f"Full Random Input -> Active Nodes: {coverage}/{n_reservoir} ({coverage/n_reservoir*100:.1f}%)")

    # More realistic thresholds:
    # - Single input should activate at least 'degree' nodes
    # - Full random input should activate at least 70% of reservoir (considering saturation/tanh)
    if total_active >= expected_active and coverage > n_reservoir * 0.70:
        print("\n[OK] PASSED: Veselov Expander properly mixes information")
        print("Interpretation: Single inputs propagate to multiple nodes (Holographic Property)")
        print(f"Coverage {coverage/n_reservoir*100:.1f}% > 70% threshold (Good for bipartite expander)")
        return True
    else:
        print("\n[FAIL] FAILED: Insufficient mixing detected")
        print(f"Single input activation: {total_active} >= {expected_active} ? {'OK' if total_active >= expected_active else 'FAIL'}")
        print(f"Full coverage: {coverage/n_reservoir*100:.1f}% > 70% ? {'OK' if coverage > n_reservoir * 0.70 else 'FAIL'}")
        return False

def test_chaos_engine():
    """
    Test 2.3: Chaos Engine (OTOC Calculation)
    Verify that OTOC correctly measures scrambling/divergence.
    """
    print("\n" + "="*70)
    print("TEST 2.3: CHAOS ENGINE (OTOC - Scrambling Metrics)")
    print("="*70)

    # Create a simulator function wrapper
    substrate = ASICSubstrate(simulation_mode=True)

    def simulator_func(seed: bytes) -> bytes:
        """Wrapper for substrate that returns single hash."""
        results = substrate.mine_reservoir_state(seed, cycles=1)
        return results[0] if results else b'\x00'*32

    # Test OTOC with different seeds
    print("Testing OTOC calculation with different seeds...")

    test_seeds = [
        b"CHAOS_TEST_SEED_1",
        b"CHAOS_TEST_SEED_2",
        b"CHAOS_TEST_SEED_3",
        b"DIFFERENT_ENTROPY_SOURCE"
    ]

    print("\n--- OTOC MEASUREMENTS ---")
    otoc_scores = []

    for i, seed in enumerate(test_seeds):
        seed_padded = seed.ljust(32, b'\x00')[:32]

        start = time.time()
        otoc = ChaosEngine.calculate_otoc(simulator_func, seed_padded)
        end = time.time()

        otoc_scores.append(otoc)
        print(f"Seed {i+1}: OTOC = {otoc:.4f} (computed in {(end-start)*1000:.2f} ms)")

    # Statistics
    mean_otoc = np.mean(otoc_scores)
    std_otoc = np.std(otoc_scores)

    print(f"\n--- STATISTICS ---")
    print(f"Mean OTOC: {mean_otoc:.4f}")
    print(f"Std Dev: {std_otoc:.4f}")
    print(f"Min: {min(otoc_scores):.4f}")
    print(f"Max: {max(otoc_scores):.4f}")

    print(f"\n--- INTERPRETATION ---")
    print(f"Expected Range: [0.4, 0.6] (Cryptographic Scrambling)")

    if mean_otoc < 0.3:
        interpretation = "LOW: System in Ordered/Frozen Phase"
        status = "Warning"
    elif 0.3 <= mean_otoc < 0.4:
        interpretation = "MEDIUM-LOW: Weak Scrambling"
        status = "Warning"
    elif 0.4 <= mean_otoc <= 0.6:
        interpretation = "OPTIMAL: Strong Cryptographic Scrambling"
        status = "OK"
    elif 0.6 < mean_otoc <= 0.7:
        interpretation = "MEDIUM-HIGH: Very Strong Scrambling"
        status = "OK"
    else:
        interpretation = "HIGH: Maximum Chaos (May need cooling)"
        status = "Warning"

    print(f"Mean OTOC = {mean_otoc:.4f} -> {interpretation}")

    # Test determinism: same seed should give same OTOC
    print("\n--- DETERMINISM TEST ---")
    seed_fixed = b"DETERMINISM_TEST_SEED_FIXED!"
    otoc1 = ChaosEngine.calculate_otoc(simulator_func, seed_fixed)
    otoc2 = ChaosEngine.calculate_otoc(simulator_func, seed_fixed)

    print(f"OTOC Run 1: {otoc1:.6f}")
    print(f"OTOC Run 2: {otoc2:.6f}")
    print(f"Match: {otoc1 == otoc2}")

    if status == "OK" and otoc1 == otoc2:
        print("\n[OK] PASSED: Chaos Engine working correctly")
        print("Interpretation: OTOC properly measures scrambling with deterministic behavior")
        return True
    else:
        print(f"\n[{status}] {'PASSED' if status == 'OK' else 'WARNING'}: OTOC out of optimal range or non-deterministic")
        return status == "OK"

def run_phase_2_validation():
    """
    Complete Phase II Mathematical Core Validation Suite.
    """
    print("="*70)
    print("       CHIMERA PROJECT - PHASE II MATHEMATICAL CORE")
    print("       Following ROADMAP_FINAL.md Section 4, Phase II")
    print("="*70)

    results = {
        'hns_decoder': False,
        'veselov_expander': False,
        'chaos_engine': False
    }

    try:
        # Test 2.1: HNS Decoder
        results['hns_decoder'] = test_hns_decoder()

        # Test 2.2: Veselov Expander
        results['veselov_expander'] = test_veselov_expander()

        # Test 2.3: Chaos Engine
        results['chaos_engine'] = test_chaos_engine()

    except Exception as e:
        print(f"\n[ERROR] CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Final Report
    print("\n" + "="*70)
    print("PHASE II VALIDATION SUMMARY")
    print("="*70)
    print(f"Test 2.1 (HNS Decoder):       {'[OK] PASSED' if results['hns_decoder'] else '[FAIL] FAILED'}")
    print(f"Test 2.2 (Veselov Expander):  {'[OK] PASSED' if results['veselov_expander'] else '[FAIL] FAILED'}")
    print(f"Test 2.3 (Chaos Engine):      {'[OK] PASSED' if results['chaos_engine'] else '[FAIL] FAILED'}")

    all_passed = all(results.values())

    if all_passed:
        print("\n[+] PHASE II VALIDATION: COMPLETE")
        print("\nREADINESS STATUS: [OK] READY FOR PHASE III")
        print("Next Step: Integrate Cognitive Loop (LLM + Reservoir)")
        print("See: ROADMAP_FINAL.md Section 4, Phase III")
    else:
        print("\n[!] PHASE II VALIDATION: INCOMPLETE")
        print("\nREADINESS STATUS: [FAIL] NOT READY")
        print("Action Required: Fix failed components before proceeding")

    print("\n" + "="*70)

    return all_passed

if __name__ == "__main__":
    success = run_phase_2_validation()
    sys.exit(0 if success else 1)
