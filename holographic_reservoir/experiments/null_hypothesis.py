import sys
import os
import time
import numpy as np
import random

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.np_solver import NPSolver

def random_solver(numbers, target, max_epochs=1000):
    """Pure random guessing control."""
    numbers = np.array(numbers)
    start_time = time.time()
    for _ in range(max_epochs):
        # Randomly select a subset mask
        mask = np.random.choice([True, False], size=len(numbers))
        current_sum = np.sum(numbers[mask])
        if current_sum == target:
            return True, time.time() - start_time
    return False, time.time() - start_time

def run_null_hypothesis_test():
    print("--- NULL HYPOTHESIS TEST: RESERVOIR VS RANDOM CHANCE ---")
    
    # Problem Set (medium difficulty)
    numbers = [23, 45, -12, 88, 34, 19, 9, -4, 102, 5, 12, 67, -22, 1, 15, 77, -50, 20]
    target = 100
    
    print(f"Problem: Subset Sum. Set Size: {len(numbers)}. Target: {target}")
    
    n_trials = 10
    chimera_wins = 0
    random_wins = 0
    chimera_times = []
    random_times = []
    
    print(f"\nRunning {n_trials} trials...")
    
    for i in range(n_trials):
        print(f"Trial {i+1}...", end=" ")
        
        # 1. Run CHIMERA (Hardware Mode)
        # We need to manually initialize the reservoir passed to solver if we want custom control
        # But NPSolver doesn't take 'simulation_mode' in init in the current file view?
        # WAIT! We patched NPSolver earlier to take simulation_mode=False hardcoded.
        # Let's double check. Yes, Step 559.
        # So invoking NPSolver() defaults to Hardware.
        solver = NPSolver(numbers, target)
        res_c = solver.solve(max_epochs=2000)
        
        # 2. Run Random
        # To be fair, Random gets same number of "function evaluations" (epochs)
        success_r, time_r = random_solver(numbers, target, max_epochs=2000)
        
        # Collect Data
        if res_c['success']: 
            chimera_wins += 1
            chimera_times.append(res_c['time'])
            
        if success_r:
            random_wins += 1
            random_times.append(time_r)
            
        print(f"DONE. | Chimera: {'OK' if res_c['success'] else 'FAIL'} ({res_c['time']:.3f}s) | Random: {'OK' if success_r else 'FAIL'} ({time_r:.3f}s)")

    print("\n--- RESULTS SUMMARY ---")
    print(f"CHIMERA Success Rate: {chimera_wins}/{n_trials} ({(chimera_wins/n_trials)*100}%)")
    print(f"RANDOM Success Rate:  {random_wins}/{n_trials} ({(random_wins/n_trials)*100}%)")
    
    avg_c = np.mean(chimera_times) if chimera_times else float('inf')
    avg_r = np.mean(random_times) if random_times else float('inf')
    
    print(f"Avg Time (CHIMERA): {avg_c:.4f}s")
    print(f"Avg Time (RANDOM):  {avg_r:.4f}s")
    
    if chimera_wins > random_wins or (chimera_wins == random_wins and avg_c < avg_r):
        print("\nCONCLUSION: PHYSICAL ADVANTAGE DETECTED.")
        print(f"The Thermodynamic Substrate outperformed Random Chance by {((chimera_wins - random_wins)/n_trials)*100:.1f}%.")
        print("This validates the 'Broken Cage' hypothesis.")
    else:
        print("\nCONCLUSION: FAILURE. No physical advantage observed.")
        print("The system performed equal to or worse than random chance.")
        print("Hardware entropy did not provide 'better' chaotic search.")

if __name__ == "__main__":
    # Suppress internal prints of solver for clean output
    # actually let's keep them to see progress or just run
    run_null_hypothesis_test()
