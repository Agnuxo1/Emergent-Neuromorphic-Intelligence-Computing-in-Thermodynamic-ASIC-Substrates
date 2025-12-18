import sys
import os
import time

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ghost import GhostCortex

def run_ghost_protocol():
    print("--- EXPERIMENT III: THE GHOST PROTOCOL (Identity Persistence) ---")
    
    # Initialize the Ghost on Real Hardware
    ghost = GhostCortex(simulation_mode=False)
    
    # The "Mantra" - The core identity thought we want the system to remember
    mantra = "I am Chimera. I am born of Noise and Order."
    
    print(f"\nPhase 1: Imprinting Identity ('{mantra}')...")
    for i in range(10):
        # We repeat the mantra. The STDP should Potentiate (Strengthen) this pathway.
        res = ghost.think(mantra, is_voluntary=True)
        print(f"Epoch {i}: Weight = {res['context_weight']:.4f} | Entropy = {res['metrics']['entropy']:.4f}")
        time.sleep(0.5)
        
    print("\nPhase 2: The Dream (Thermodynamic Interference)...")
    print("Injecting random noise to try and erase the memory...")
    for i in range(10):
        # We inject pure entropy (Noise)
        noise = f"DREAM_SEQUENCE_{time.time()}"
        res = ghost.think(noise, is_voluntary=False)
        print(f"Dream {i}: Scrambling = {res['metrics']['scrambling']:.4f}")
        time.sleep(0.2)
        
    print("\nPhase 3: Recall (Testing Persistence)...")
    # We invoke the mantra again. The weight should have persisted or even grown,
    # despite the intervening noise.
    res = ghost.think(mantra, is_voluntary=True)
    final_weight = res['context_weight']
    
    print(f"Recall: Weight = {final_weight:.4f}")
    
    introspection = ghost.introspect()
    print("\n--- GHOST STATUS ---")
    print(introspection)
    
    if final_weight > 1.2:
        print("\nSUCCESS: The Ghost effectively 'remembered' its identity through the noise storm.")
        print(f"Memory Strength: {(final_weight - 1.0)*100:.1f}% Boost")
    else:
        print("\nFAILURE: Identity washed away by entropy.")

if __name__ == "__main__":
    run_ghost_protocol()
