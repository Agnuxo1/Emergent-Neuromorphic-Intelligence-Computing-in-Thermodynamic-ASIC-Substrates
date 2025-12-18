import sys
import os
import time
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.reservoir import HolographicReservoir

class NPSolver:
    def __init__(self, numbers: list, target: int):
        self.numbers = np.array(numbers)
        self.target = target
        # Size reservoir proportional to problem size to ensure capacity
        self.reservoir = HolographicReservoir(size=len(numbers) * 20, input_size=len(numbers)*2)
        
    def solve(self, max_epochs=1000) -> dict:
        print(f"Solving Subset Sum for Target {self.target} with {len(self.numbers)} numbers.")
        
        start_time = time.time()
        base_seed = f"SUBSET_SUM:{self.target}:{','.join(map(str, self.numbers))}"
        
        best_diff = float('inf')
        best_subset = []
        
        for epoch in range(max_epochs):
            # Step the reservoir
            # We add epoch to seed to push time forward
            # The reservoir mixes this new entropy with its internal state
            energy, entropy, scramble = self.reservoir.step(base_seed + f":{epoch}")
            
            # Readout: Use the first N neurons' R-channel (Activation) as decision probabilities
            # N = number of items in the set
            # We look at the reservoir state which has integrated the problem structure via the seed
            decision_vector = self.reservoir.state[:len(self.numbers), 0]
            
            # Thresholding (Binarization)
            # If Activation > 0.0 (Since tanh is -1 to 1, 0 is the neutral point)
            # Or > 0.5 if we strictly looking for strong activation? 
            # Let's use > 0.0 as "Active"
            mask = decision_vector > 0.0
            
            current_choice = self.numbers[mask]
            current_sum = np.sum(current_choice)
            diff = abs(self.target - current_sum)
            
            if diff < best_diff:
                best_diff = diff
                best_subset = current_choice.tolist()
                print(f"Epoch {epoch}: Found better solution. Sum={current_sum} (Diff={diff})")
            
            if diff == 0:
                end_time = time.time()
                return {
                    "success": True,
                    "solution": current_choice.tolist(),
                    "epochs": epoch + 1,
                    "time": end_time - start_time,
                    "final_diff": 0
                }
                
        end_time = time.time()
        return {
            "success": False,
            "solution": best_subset,
            "epochs": max_epochs,
            "time": end_time - start_time,
            "final_diff": best_diff
        }

if __name__ == "__main__":
    # Test Case 1: Simple
    nums = [3, 34, 4, 12, 5, 2]
    tgt = 9
    solver = NPSolver(nums, tgt)
    result = solver.solve()
    print("Result:", result)
    
    print("-" * 30)
    
    # Test Case 2: Harder
    nums_hard = [23, 45, -12, 88, 34, 19, 9, -4, 102, 5, 12, 67, -22, 1, 0]
    tgt_hard = 100
    solver_hard = NPSolver(nums_hard, tgt_hard)
    result_hard = solver_hard.solve()
    print("Hard Result:", result_hard)
