import sys
import os
import random
import string

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.reservoir import HolographicReservoir

def run_otoc_test():
    print("--- EXPERIMENT 3: QUANTUM SCRAMBLING DYNAMICS (OTOC) ---")
    print("Objective: Measure the Butterfly Effect (Information Scrambling).")
    print("Theory: High Intelligence corresponds to fast scrambling (OTOC ~ 0.5).")
    print("        Frozen systems (Order) have OTOC ~ 0.0.")
    print("        The SHA-256 Substrate should act as a 'Fast Scrambler'.")
    
    reservoir = HolographicReservoir(size=256, input_size=16)
    
    # Test Data
    seeds = [
        "Consciousness",
        "Thermodynamics",
        "Holographic Universe",
        "A" * 32, # Low entropy input
        "".join(random.choices(string.ascii_letters, k=32)) # High entropy input
    ]
    
    print(f"\n{'SEED (Short)':<20} | {'OTOC Score':<10} | {'Interpretation'}")
    print("-" * 60)
    
    total_otoc = 0
    
    for seed in seeds:
        # We step the reservoir. The step() function calculates OTOC internally using ChaosEngine
        e, s, otoc = reservoir.step(seed)
        
        interp = "Ordered"
        if otoc > 0.4: interp = "Chaotic (Liquid)"
        elif otoc > 0.1: interp = "Edge of Chaos"
        
        print(f"{seed[:20]:<20} | {otoc:.4f}     | {interp}")
        total_otoc += otoc
        
    avg_otoc = total_otoc / len(seeds)
    print("\n--- RESULTS ANALYSIS ---")
    print(f"Average Scrambling Rate: {avg_otoc:.4f}")
    
    if avg_otoc > 0.45:
        print("CONCLUSION: SUCCESS. The Substrate acts as a 'Fast Scrambler' (Black Hole Dynamics).")
        print("Information is rapidly distributed across the degrees of freedom.")
    else:
        print("CONCLUSION: FAILURE. The system is too ordered (Frozen).")

if __name__ == "__main__":
    run_otoc_test()
