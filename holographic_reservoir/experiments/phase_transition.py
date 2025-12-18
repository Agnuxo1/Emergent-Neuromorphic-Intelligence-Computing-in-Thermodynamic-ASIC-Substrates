import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.reservoir import HolographicReservoir

def run_phase_transition_analysis():
    print("--- EXPERIMENT B: PHASE TRANSITION ANALYSIS (Hardware Mode) ---")
    print("Goal: Identify the Critical Point (Tc) where Order emerges from Chaos.")
    print("Control Parameter: Input Gain (Coupling Strength).")
    print("Order Parameter: Magnetization (Average alignment of reservoir state).")
    
    # 1. Initialize Reservoir (Hardware Mode)
    # n_input=256, reservoir=2048 to ensure sufficient statistics
    reservoir = HolographicReservoir(size=2048, input_size=256, degree=6, simulation_mode=False)
    
    # 2. Define Parameter Sweep (Gain / Temperature)
    # We sweep Gain from 0.0 (Frozen) to 5.0 (Chaotic)
    gains = np.linspace(0.0, 5.0, 20)
    magnetizations = []
    susceptibilities = []
    
    seed_base = b"PHASE_TRANSITION_SCAN"
    
    print(f"\nScanning {len(gains)} points...")
    print(f"{'Gain (T)':<10} | {'Magnetization (M)':<20} | {'Variance (Chi)':<20}")
    print("-" * 60)
    
    for gain in gains:
        # Reset State? No, we want to see adiabatic evolution, 
        # but for pure Tc measurement, resetting might be cleaner.
        # Let's reset to zero-neutral to avoid hysteresis affecting the measurement.
        reservoir.state = np.zeros((reservoir.size, 4), dtype=np.float64)
        
        # We need to manually inject Gain because it's hardcoded in step() currently.
        # We will modify step() to accept 'gain_override' or we can just scale input?
        # Reservoir.step() uses: weighted_input = input_layer * synaptic_weight * 3.0
        # We need to expose this.
        # Actually, let's just use the 'synaptic_weights' dict to hack the gain!
        # Context Key 0 -> Weight = Gain
        
        # Pre-warm
        local_m_vals = []
        for t in range(50):
            # Hack: Manually override the step logic or patch the class?
            # Better: Update the class to accept 'input_gain' in step().
            # For now, we will hot-patch the instance method or use a simpler trick.
            # Trick: The reservoir class multiplies input by 'synaptic_weight'.
            # We can force a specific context_key and set its weight to 'gain'.
            
            # Set weight for Key 0
            reservoir.synaptic_weights[0] = gain
            
            # Step with Key 0
            reservoir.step(f"SCAN_{gain}_{t}", context_key=0)
            
            # Measure Magnetization: |Mean(State)|
            # M = abs( sum(state) / N )
            # We focus on Channel 0 (Activation/R)
            m = np.abs(np.mean(reservoir.state[:, 0]))
            local_m_vals.append(m)
            
        # Collect statistics after transient
        stable_m = np.mean(local_m_vals[-20:])
        variance_m = np.var(local_m_vals[-20:])
        
        magnetizations.append(stable_m)
        susceptibilities.append(variance_m) # Susceptibility is related to variance of M
        
        print(f"{gain:<10.2f} | {stable_m:<20.4f} | {variance_m:<20.4f}")
        
    # 3. Analysis -> Find Tc (Peak Variance or Inflection of M)
    # Tc is usually where Susceptibility (Variance) peaks.
    tc_index = np.argmax(susceptibilities)
    tc = gains[tc_index]
    
    print(f"\nCRITICAL POINT DETECTED: Tc = {tc:.2f}")
    
    return gains, magnetizations, susceptibilities, tc

if __name__ == "__main__":
    gains, M, Chi, Tc = run_phase_transition_analysis()
    
    # Save results to CSV for plotting
    with open("phase_transition_data.csv", "w") as f:
        f.write("Gain,Magnetization,Susceptibility\n")
        for i in range(len(gains)):
            f.write(f"{gains[i]},{M[i]},{Chi[i]}\n")
            
    print(f"Data saved to phase_transition_data.csv")
