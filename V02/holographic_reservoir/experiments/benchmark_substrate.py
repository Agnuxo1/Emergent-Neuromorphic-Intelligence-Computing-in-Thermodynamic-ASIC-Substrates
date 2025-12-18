import sys
import os
import time
import numpy as np

# Add parent directory to path to allow importing core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.substrate import ASICSubstrate
from core.hns import HNS

def benchmark():
    print("--- CHIMERA SUBSTRATE BENCHMARK (Simulation Mode) ---")
    
    substrate = ASICSubstrate(simulation_mode=True)
    
    # 1. Speed Test
    print("\n[TEST 1] Speed Verification...")
    start_time = time.time()
    n_cycles = 100000
    seed = b"BenchmarkSeed123"
    results = substrate.mine_reservoir_state(seed, cycles=n_cycles)
    end_time = time.time()
    
    duration = end_time - start_time
    hashes_per_second = n_cycles / duration
    
    print(f"Cycles: {n_cycles}")
    print(f"Duration: {duration:.4f}s")
    print(f"Speed: {hashes_per_second:.2f} Hash/s")
    
    # 2. Entropy / HNS Distribution Test
    print("\n[TEST 2] Entropy & HNS Mapping Distribution...")
    # Convert first 1000 hashes to vectors
    vectors = []
    for h in results[:1000]:
        vectors.append(HNS.hash_to_rgba(h))
    
    vectors_np = np.array(vectors)
    
    # Check stats for each channel (R, G, B, A)
    channels = ['R (Energy)', 'G (Gradient)', 'B (Plasticity)', 'A (Phase)']
    print(f"{'Channel':<15} | {'Mean':<10} | {'Std Dev':<10} | {'Min':<10} | {'Max':<10}")
    print("-" * 65)
    for i, name in enumerate(channels):
        vals = vectors_np[:, i]
        print(f"{name:<15} | {np.mean(vals):.6f} | {np.std(vals):.6f} | {np.min(vals):.6f} | {np.max(vals):.6f}")
        
    # Validation: Mean should be close to 0.5, Std Dev close to 1/sqrt(12) ~= 0.288 for uniform dist
    print("\nExpected Mean for Uniform Random: 0.500000")
    print("Expected StdDev for Uniform Random: 0.288675")
    
    print("\n--- BENCHMARK COMPLETE ---")

if __name__ == "__main__":
    benchmark()
