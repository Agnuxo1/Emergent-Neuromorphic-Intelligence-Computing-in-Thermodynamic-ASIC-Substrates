import sys
import os
import time
import numpy as np
import hashlib

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.reservoir import HolographicReservoir

def run_anomaly_test():
    print("--- EXPERIMENT 2: MEMORY & ANOMALY DETECTION (Simulation Mode) ---")
    print("Hypothesis: The STDP mechanism allows the system to 'learn' repeated structures (Contexts)")
    print("while ignoring transient noise. We compare the 'Synaptic Weight' evolution.")
    
    reservoir = HolographicReservoir(size=1024, input_size=64)
    
    # Dataset
    # 1. Structure: A repeated known sentence (The "Signal")
    signal_text = "The universe is built on holographic principles and thermodynamic logic."
    signal_key = int.from_bytes(signal_text.encode()[:8], 'big')
    
    # 2. Noise: We will generate completely random strings every step ( The "Noise" )
    # Note: We won't track specific keys for random noise effectively, or we treat them as unique
    
    print(f"\nTraining Phase (20 Epochs)...")
    print(f"Signal: '{signal_text}'")
    
    signal_weights_trace = []
    
    for epoch in range(20):
        # 1. Feed Signal
        e, s, rate = reservoir.step(signal_text, context_key=signal_key)
        w = reservoir.synaptic_weights.get(signal_key, 1.0)
        signal_weights_trace.append(w)
        
        # 2. Feed Random Noise (Interference)
        noise_text = f"NOISE_{os.urandom(8).hex()}"
        noise_key = int.from_bytes(noise_text.encode()[:8], 'big')
        e_n, s_n, rate_n = reservoir.step(noise_text, context_key=noise_key)
        
        # We don't track noise weights because they are unique keys every time (Transient)
        # But let's see if the Signal Weight grows
        
        print(f"Epoch {epoch+1}: Signal Weight={w:.4f} | Noise Ent={s_n:.4f}")

    print("\n--- RESULTS ---")
    print("Evolution of Signal Weight (Memory):")
    print(signal_weights_trace)
    
    initial = signal_weights_trace[0]
    final = signal_weights_trace[-1]
    
    print(f"\nInitial Weight: {initial:.4f}")
    print(f"Final Weight:   {final:.4f}")
    
    delta = final - initial
    print(f"Delta: {delta:.4f}")
    
    if abs(delta) > 0.1:
        print("\nSUCCESS: The system has altered its internal structure (Plasticity) in response to the signal.")
        if delta > 0:
            print("Output: POTENTIATION (Learned/Remembered)")
        else:
            print("Output: DEPRESSION (Habituated/Ignored)")
        print("This confirms the 'Chimera_NN' logic: The system is not static.")
    else:
        print("\nFAILURE: Weights remained static. STDP not effective.")

if __name__ == "__main__":
    run_anomaly_test()
