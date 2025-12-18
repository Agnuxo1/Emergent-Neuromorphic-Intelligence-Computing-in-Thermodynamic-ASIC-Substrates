import numpy as np
from typing import Callable

class ChaosEngine:
    """
    Implements Quantum Scrambling Dynamics (OTOC - Out-of-Time-Order Correlators).
    
    Theory:
    Intelligence is correlated with the ability to 'scramble' information.
    We measure this by simulating two parallel universes:
    1. Universe A: The original seed.
    2. Universe B: The original seed + 1 bit flip (The Butterfly).
    
    The OTOC is related to the Hamming Distance between the states of A and B over time.
    High Scrambling = Efficient Information Mixing (Liquid/Chaotic Phase).
    Low Scrambling = Frozen/Ordered Phase.
    """
    
    @staticmethod
    def calculate_otoc(simulator_func: Callable[[bytes], bytes], base_seed: bytes) -> float:
        """
        Calculates the immediate divergence (Lyapunov Exponent proxy) for a single step.
        
        Args:
            simulator_func: Function that takes bytes and returns bytes (The Physical Work).
            base_seed: The input state.
            
        Returns:
            float: Normalized Scrambling Rate [0.0 - 1.0].
                   0.0 = No divergence (Order).
                   0.5 = Perfect Scrambling (Random/Chaos).
        """
        # 1. Trajectory A (Original)
        # We need the simulator to return a single representative hash or state
        # For the S9, this is the 'best nonce' or just the first result
        hash_a = simulator_func(base_seed)
        
        # 2. Trajectory B (Perturbed)
        # Flip the last bit of the seed
        seed_array = bytearray(base_seed)
        seed_array[-1] ^= 1 
        seed_b = bytes(seed_array)
        
        hash_b = simulator_func(seed_b)
        
        if not hash_a or not hash_b:
            return 0.0
            
        # 3. Measure Hamming Distance
        # OTOC(t) ~ 1 - Commutator(V, W)
        # Here we use normalized Hamming distance as the metric for divergence
        return ChaosEngine._hamming_distance(hash_a, hash_b)

    @staticmethod
    def _hamming_distance(b1: bytes, b2: bytes) -> float:
        """Computes normalized Hamming distance between two byte strings."""
        # XOR the bytes
        xored = int.from_bytes(b1, 'big') ^ int.from_bytes(b2, 'big')
        
        # Count set bits
        set_bits = bin(xored).count('1')
        
        # Normalize by total bits (256 for SHA-256)
        return set_bits / 256.0
