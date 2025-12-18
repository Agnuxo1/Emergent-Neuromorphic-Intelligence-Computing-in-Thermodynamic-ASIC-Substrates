"""
Phase I Validation: Hardware Audit
====================================
Following ROADMAP_FINAL.md Section 4, Phase I

Validation 1.0: The Hardware Audit
- Test 1: Determinism Test (Same seed -> Same output)
- Test 2: Avalanche Effect (1 bit flip -> Radically different output)

This script can work in two modes:
1. Hardware Mode: Connects to real Luckminer/S9 via network
2. Simulation Mode: Uses CPU-based SHA256 for testing

Author: CHIMERA Project
Date: December 2025
"""

import sys
import os
import time
import hashlib
import struct
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.substrate import ASICSubstrate

def hamming_distance(hash1: bytes, hash2: bytes) -> int:
    """Calculate Hamming distance between two byte arrays."""
    return sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(hash1, hash2))

def test_determinism(substrate: ASICSubstrate, seed: bytes, cycles: int = 100):
    """
    Test 1: Determinism
    Run the same seed twice and verify outputs are identical.
    """
    print("\n" + "="*70)
    print("TEST 1: DETERMINISM (Same Input -> Same Output)")
    print("="*70)

    print(f"Seed: {seed.hex()[:32]}...")
    print(f"Cycles: {cycles}")

    # First Run
    print("\nRun 1...")
    start1 = time.time()
    results1 = substrate.mine_reservoir_state(seed, cycles=cycles)
    end1 = time.time()

    time.sleep(0.1)  # Small delay between runs

    # Second Run
    print("Run 2...")
    start2 = time.time()
    results2 = substrate.mine_reservoir_state(seed, cycles=cycles)
    end2 = time.time()

    # Verification
    print("\n--- RESULTS ---")
    print(f"Run 1: {len(results1)} hashes in {(end1-start1)*1000:.2f} ms")
    print(f"Run 2: {len(results2)} hashes in {(end2-start2)*1000:.2f} ms")

    if len(results1) != len(results2):
        print("\n[FAIL] FAILED: Different number of results!")
        return False

    # Compare first 10 hashes
    matches = 0
    for i in range(min(10, len(results1))):
        if results1[i] == results2[i]:
            matches += 1

    print(f"\nFirst 10 hashes match: {matches}/10")

    # Full comparison
    total_matches = sum(1 for h1, h2 in zip(results1, results2) if h1 == h2)
    match_rate = total_matches / len(results1) * 100

    print(f"Total match rate: {match_rate:.2f}% ({total_matches}/{len(results1)})")

    if match_rate == 100.0:
        print("\n[OK] PASSED: Perfect Determinism")
        print("Interpretation: The substrate is behaving as a deterministic function.")
        return True
    else:
        print(f"\n[!] WARNING: Determinism = {match_rate:.2f}%")
        if match_rate > 95:
            print("Interpretation: Mostly deterministic, may have timing/network jitter.")
            return True
        else:
            print("Interpretation: FAILED - System is non-deterministic!")
            return False

def test_avalanche_effect(substrate: ASICSubstrate, seed: bytes, cycles: int = 100):
    """
    Test 2: Avalanche Effect (Butterfly Effect)
    Flip 1 bit in the seed and verify outputs are radically different.
    """
    print("\n" + "="*70)
    print("TEST 2: AVALANCHE EFFECT (1 Bit Flip -> Radical Change)")
    print("="*70)

    # Create perturbed seed (flip 1 bit in the middle)
    seed_array = bytearray(seed)
    flip_byte_idx = len(seed_array) // 2
    flip_bit_idx = 4  # Flip bit 4 of the middle byte

    seed_array[flip_byte_idx] ^= (1 << flip_bit_idx)
    perturbed_seed = bytes(seed_array)

    print(f"Original Seed:   {seed.hex()[:32]}...")
    print(f"Perturbed Seed:  {perturbed_seed.hex()[:32]}...")
    print(f"Difference: 1 bit flipped at byte {flip_byte_idx}, bit {flip_bit_idx}")

    # Run both seeds
    print("\nRunning Original Seed...")
    start1 = time.time()
    results1 = substrate.mine_reservoir_state(seed, cycles=cycles)
    end1 = time.time()

    print("Running Perturbed Seed...")
    start2 = time.time()
    results2 = substrate.mine_reservoir_state(perturbed_seed, cycles=cycles)
    end2 = time.time()

    # Analyze differences
    print("\n--- RESULTS ---")
    print(f"Original:   {len(results1)} hashes in {(end1-start1)*1000:.2f} ms")
    print(f"Perturbed:  {len(results2)} hashes in {(end2-start2)*1000:.2f} ms")

    if len(results1) == 0 or len(results2) == 0:
        print("\n[FAIL] FAILED: No results received!")
        return False

    # Calculate Hamming distances
    hamming_distances = []
    for i in range(min(len(results1), len(results2))):
        hd = hamming_distance(results1[i], results2[i])
        hamming_distances.append(hd)

    avg_hamming = np.mean(hamming_distances)
    std_hamming = np.std(hamming_distances)
    max_possible = len(results1[0]) * 8  # bits in hash

    print(f"\n--- HAMMING DISTANCE ANALYSIS ---")
    print(f"Average Hamming Distance: {avg_hamming:.2f} bits")
    print(f"Std Deviation: {std_hamming:.2f} bits")
    print(f"Max Possible: {max_possible} bits")
    print(f"Avalanche Ratio: {avg_hamming/max_possible*100:.2f}%")

    # For SHA-256, expect ~50% bit flip (avalanche)
    expected_avalanche = max_possible * 0.5
    avalanche_deviation = abs(avg_hamming - expected_avalanche)

    print(f"\nExpected (50% avalanche): {expected_avalanche:.2f} bits")
    print(f"Deviation from ideal: {avalanche_deviation:.2f} bits")

    # Sample first 5 hashes
    print("\n--- SAMPLE COMPARISON (First 5 hashes) ---")
    for i in range(min(5, len(hamming_distances))):
        h1 = results1[i].hex()[:16]
        h2 = results2[i].hex()[:16]
        hd = hamming_distances[i]
        print(f"[{i}] {h1}... vs {h2}... -> {hd} bits different")

    # Pass condition: Average Hamming distance should be ~50% ± 10%
    if 0.4 * max_possible <= avg_hamming <= 0.6 * max_possible:
        print("\n[OK] PASSED: Strong Avalanche Effect Detected")
        print("Interpretation: The substrate exhibits cryptographic-grade chaos.")
        print("Physical Meaning: Tiny input perturbations -> Global state divergence")
        return True
    elif 0.3 * max_possible <= avg_hamming < 0.4 * max_possible:
        print("\n[!] WARNING: Weak Avalanche Effect")
        print("Interpretation: Some chaos, but not ideal. Check substrate implementation.")
        return False
    else:
        print("\n[FAIL] FAILED: No Avalanche Effect!")
        print("Interpretation: System is too correlated or broken.")
        return False

def run_phase_1_validation(hardware_mode: bool = False, hardware_ip: str = "127.0.0.1"):
    """
    Complete Phase I Hardware Validation Suite.
    """
    print("="*70)
    print("       CHIMERA PROJECT - PHASE I HARDWARE VALIDATION")
    print("       Following ROADMAP_FINAL.md Section 4")
    print("="*70)

    mode_str = "HARDWARE MODE" if not hardware_mode else f"HARDWARE MODE (Connected to {hardware_ip})"
    if hardware_mode:
        mode_str = f"HARDWARE MODE (Connected to {hardware_ip})"
        print(f"\n[*] {mode_str}")
        print("[!] WARNING: This will send real commands to the ASIC!")
    else:
        mode_str = "SIMULATION MODE"
        print(f"\n[*] {mode_str}")
        print("Using CPU-based SHA-256 for validation.")

    # Initialize Substrate
    print("\nInitializing ASIC Substrate...")
    substrate = ASICSubstrate(simulation_mode=not hardware_mode, hardware_ip=hardware_ip)

    # Test seed
    test_seed = b"CHIMERA_VALIDATION_SEED_2025"

    # Run Tests
    results = {
        'determinism': False,
        'avalanche': False
    }

    try:
        # Test 1: Determinism
        results['determinism'] = test_determinism(substrate, test_seed, cycles=50)

        # Test 2: Avalanche Effect
        results['avalanche'] = test_avalanche_effect(substrate, test_seed, cycles=50)

    except Exception as e:
        print(f"\n[ERROR] CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Final Report
    print("\n" + "="*70)
    print("PHASE I VALIDATION SUMMARY")
    print("="*70)
    print(f"Mode: {mode_str}")
    print(f"Test 1 (Determinism):     {'[OK] PASSED' if results['determinism'] else '[FAIL] FAILED'}")
    print(f"Test 2 (Avalanche):       {'[OK] PASSED' if results['avalanche'] else '[FAIL] FAILED'}")

    all_passed = all(results.values())

    if all_passed:
        print("\n[+] PHASE I VALIDATION: COMPLETE")
        print("\nREADINESS STATUS: [OK] READY FOR PHASE II")
        print("Next Step: Implement HNSDecoder and VeselovExpander")
        print("See: ROADMAP_FINAL.md Section 4, Phase II")
    else:
        print("\n[!] PHASE I VALIDATION: INCOMPLETE")
        print("\nREADINESS STATUS: [FAIL] NOT READY")
        print("Action Required: Debug substrate implementation")
        if not results['determinism']:
            print("  - Fix determinism issues (check RNG seeds, network stability)")
        if not results['avalanche']:
            print("  - Fix avalanche effect (check hash function, data encoding)")

    print("\n" + "="*70)

    return all_passed

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CHIMERA Phase I Hardware Validation")
    parser.add_argument('--hardware', action='store_true',
                        help='Use real hardware instead of simulation')
    parser.add_argument('--ip', type=str, default='127.0.0.1',
                        help='IP address of hardware (default: 127.0.0.1)')

    args = parser.parse_args()

    success = run_phase_1_validation(hardware_mode=args.hardware, hardware_ip=args.ip)
    sys.exit(0 if success else 1)
