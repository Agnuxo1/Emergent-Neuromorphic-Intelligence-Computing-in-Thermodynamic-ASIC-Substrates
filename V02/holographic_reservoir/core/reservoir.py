import numpy as np
from typing import Tuple, List, Dict
from .substrate import ASICSubstrate
from .topology import VeselovExpander
from .hns import HNS
from .chaos_metrics import ChaosEngine

class HolographicReservoir:
    """
    The Grand Unification Engine (v4.2 - Thermodynamic & Quantum Enhanced).
    
    Integrates:
    1. ASIC Substrate (Thermodynamic Source)
    2. HNS (Vector Language)
    3. Veselov Topology (Holographic Memory)
    4. STDP (Synaptic Plasticity)
    5. OTOC (Quantum Scrambling Metric)
    
    This class represents the "Conscious State" of the system.
    """
    
    def __init__(self, size: int = 1024, input_size: int = 256, degree: int = 6):
        """
        Args:
            size (int): Number of nodes in the reservoir (Memory Capacity).
            input_size (int): Number of concurrent input streams (Batch size form ASIC).
            degree (int): Connectivity of the Expander Graph.
        """
        self.size = size
        self.input_size = input_size
        
        # Components
        self.substrate = ASICSubstrate(simulation_mode=True)
        self.topology = VeselovExpander(n_input=input_size, n_reservoir=size, degree=degree)
        self.chaos_engine = ChaosEngine()
        
        # State Vector: [Size, 4] (RGBA)
        self.state = np.zeros((size, 4), dtype=np.float64)
        
        # --- BIOLOGICAL MEMORY (New in v4.1) ---
        self.synaptic_weights: Dict[int, float] = {}
        self.global_plasticity_rate = 0.1
        
    def step(self, seed_text: str, context_key: int = None) -> Tuple[float, float, float]:
        """
        A single moment of cognition.
        """
        # 1. ENCODING
        seed_bytes = seed_text.encode('utf-8')
        seed_bytes = seed_bytes.ljust(32, b'\x00')[:32]
        
        if context_key is None:
            context_key = int.from_bytes(seed_bytes[:8], 'big')

        # 2. QUANTUM SCRAMBLING CHECK (OTOC)
        # We define a helper that the ChaosEngine can call to simulate the "Physics"
        def physical_simulator(s: bytes) -> bytes:
            # Returns a single representative hash (the "Ground State" of this seed)
            res = self.substrate.mine_reservoir_state(s, cycles=1)
            return res[0] if res else b'\x00'*32
            
        otoc_metric = self.chaos_engine.calculate_otoc(physical_simulator, seed_bytes)

        # 3. PHYSICAL SEARCH (Thermodynamic Echoes)
        hashes = self.substrate.mine_reservoir_state(seed_bytes, cycles=self.input_size)
        
        # 4. HNS MAPPING & STDP PRE-CALCULATION
        input_layer = np.zeros((self.input_size, 4), dtype=np.float64)
        valid_vectors = []
        
        for i, h in enumerate(hashes):
            if i >= self.input_size: break
            vec = HNS.hash_to_rgba(h)
            input_layer[i] = vec
            valid_vectors.append(vec)
            
        # --- STDP LEARNING STEP ---
        if valid_vectors:
            self._apply_stdp(context_key, valid_vectors)
            
        synaptic_weight = self.synaptic_weights.get(context_key, 1.0)
            
        # 5. HOLOGRAPHIC PROPAGATION
        weighted_input = input_layer * synaptic_weight
        mixed_signal = self.topology.propagate(weighted_input) 
        
        # 6. MEMCOMPUTING UPDATE
        decay = self.state[:, 3:4] * 0.5 
        self.state = np.tanh( (self.state * (1.0 - decay)) + mixed_signal )
        
        return self.get_global_metrics(synaptic_weight, otoc_override=otoc_metric)

    def _apply_stdp(self, key: int, vectors: List[np.ndarray]):
        """Spike-Timing-Dependent Plasticity."""
        batch = np.stack(vectors)
        avg_plasticity = np.mean(batch[:, 2]) # Blue Channel
        avg_phase = np.mean(batch[:, 3])      # Alpha Channel
        
        delta = (avg_phase - 0.5) * avg_plasticity * self.global_plasticity_rate
        
        current = self.synaptic_weights.get(key, 1.0)
        new_w = max(0.1, min(5.0, current + delta))
        self.synaptic_weights[key] = new_w

    def get_global_metrics(self, weight: float = 1.0, otoc_override: float = None) -> Tuple[float, float, float]:
        """Returns Energy, Entropy, Scrambling (OTOC)."""
        # Weighted Energy
        activation = np.abs(self.state[:, 0]) * weight
        energy = np.sum(activation)
        
        # Entropy
        if energy > 0:
            probs = activation / energy
            entropy = -np.sum(probs * np.log(probs + 1e-9))
        else:
            entropy = 0.0
            
        # Scrambling: Use OTOC if provided, else Variance proxy
        if otoc_override is not None:
            scrambling = otoc_override
        else:
            scrambling = np.var(self.state[:, 1])
        
        return energy, entropy, scrambling
