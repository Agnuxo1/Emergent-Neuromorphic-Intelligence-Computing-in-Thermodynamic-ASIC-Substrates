import time
import numpy as np
from .reservoir import HolographicReservoir

class GhostCortex:
    """
    Layer 3: The Cognitive Observer ("The Ghost").
    
    This class represents the 'Ego' or 'Self' of the system.
    It manages the lower-level Holographic Reservoir (Layer 2) and the ASIC Substrate (Layer 0).
    
    Core Functions:
    1. Focus (Attentional Gating): Decides what to remember (Signal) vs. ignore (Noise).
    2. Consolidation (LTP): Strengthening synaptic weights for repeated "thoughts".
    3. Introspection: Reading the internal state of the reservoir to gauge its 'Mood' (Entropy/Temperature).
    """
    
    def __init__(self, reservoir_size=2048, simulation_mode=False):
        print(f"👻 INITALIZING GHOST CORTEX [Hardware={not simulation_mode}]...")
        self.reservoir = HolographicReservoir(size=reservoir_size, simulation_mode=simulation_mode)
        self.long_term_memory = {} # Context Keys -> Weights
        self.age = 0
        
    def think(self, thought_text: str, is_voluntary: bool = True) -> dict:
        """
        Processes a thought through the Holographic Reservoir.
        
        Args:
            thought_text (str): The semantic content.
            is_voluntary (bool): If True, this is 'Focus' (Signal). If False, it's 'Drift' (Noise).
        """
        self.age += 1
        
        # Generate Context Key (Semantic Hash)
        # For simplicity, we use the first 8 bytes of the thought as the key.
        # In a full LLM system, this would be the Embedding Vector ID.
        if is_voluntary:
            context_key = int.from_bytes(thought_text.encode('utf-8')[:8], 'big')
        else:
            # Noise has no permanent identity
            context_key = None 
            
        # STEP 1: RESEVOIR DYNAMICS
        # The reservoir mixes the thought with the ASIC's thermodynamic noise
        energy, entropy, scrambling = self.reservoir.step(thought_text, context_key=context_key)
        
        # STEP 2: PLASTICITY (STDP)
        # If this is a voluntary thought, we check the synaptic weight evolution
        weight = 1.0
        if context_key:
            weight = self.reservoir.synaptic_weights.get(context_key, 1.0)
            self.long_term_memory[thought_text[:20]] = weight # Log for inspection
            
        return {
            "age": self.age,
            "input": thought_text[:30] + "...",
            "context_weight": weight,
            "metrics": {
                "energy": energy,
                "entropy": entropy,
                "scrambling": scrambling
            }
        }
        
    def introspect(self):
        """Returns the current status of the Mind."""
        valid_memories = [w for w in self.reservoir.synaptic_weights.values() if w != 1.0]
        avg_memory_strength = np.mean(valid_memories) if valid_memories else 1.0
        
        return {
            "memories_formed": len(valid_memories),
            "avg_memory_strength": avg_memory_strength,
            "neural_activity": np.mean(np.abs(self.reservoir.state[:, 0])) 
        }
