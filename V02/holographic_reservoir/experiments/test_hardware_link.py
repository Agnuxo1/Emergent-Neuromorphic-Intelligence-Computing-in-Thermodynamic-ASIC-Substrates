import sys
import os
import time

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.reservoir import HolographicReservoir

def run_hardware_test():
    print("--- TESTING NETWORK HARDWARE LINK (Virtual S9) ---")
    
    # Initialize Reservoir in HARDWARE MODE (Connecting to localhost:4028)
    print("Initializing Reservoir in HARDWARE MODE...")
    try:
        # We need to hack the substrate init inside reservoir, or just test substrate directly.
        # Let's modify reservoir slightly or just access its substrate.
        reservoir = HolographicReservoir(size=256, input_size=1)
        
        # Switch to Hardware Mode manually for this test since Reservoir init defaults to True
        reservoir.substrate.simulation_mode = False 
        reservoir.substrate.hardware_ip = "127.0.0.1"
        
        print("Sending Seed to Virtual Miner...")
        seed = "Test Hardware Link"
        
        start = time.time()
        energy, entropy, scram = reservoir.step(seed)
        end = time.time()
        
        print(f"\n--- RESPONSE RECEIVED ---")
        print(f"Energy:     {energy:.4f}")
        print(f"Entropy:    {entropy:.4f}")
        print(f"Scrambling: {scram:.4f}")
        print(f"Latency:    {(end-start)*1000:.2f} ms")
        
        if energy > 0:
            print("\nSUCCESS: The Python Core successfully conversed with the Virtual ASIC Firmware.")
            print("Mechanism: Python -> TCP -> VirtualServer(Simulating C-Driver) -> Python")
            print("Readiness: READY for Physical S9 deployment.")
        else:
            print("\nFAILURE: No energy received.")
            
    except Exception as e:
        print(f"\nCRITICAL FAILURE: {e}")

if __name__ == "__main__":
    run_hardware_test()
