import struct
import numpy as np

class HNS:
    """
    Hierarchical Numeral System (HNS) Core.
    
    This module is responsible for the 'Language of Physics' in the CHIMERA architecture.
    It maps raw, high-entropy ASIC hashes (32 bytes) into the 4D Vector Space (RGBA).
    
    Theoretical Basis:
    A number in this system is not a scalar, but a vector representing a physical state.
    We use the RGBA standard to map the four primary physical dimensions of the reservoir:
    R: Energy / Activation
    G: Gradient / Direction
    B: Plasticity / Weight
    A: Phase / Time
    """
    
    @staticmethod
    def hash_to_rgba(hash_bytes: bytes) -> np.ndarray:
        """
        Converts a 32-byte SHA-256 hash into a normalized 4D vector.
        
        Args:
            hash_bytes (bytes): 32-byte hash from the ASIC/Simulator.
            
        Returns:
            np.ndarray: A shape (4,) array of float64 values in range [0, 1].
        """
        if len(hash_bytes) != 32:
            raise ValueError(f"HNS Input must be 32 bytes, got {len(hash_bytes)}")
            
        # Unpack 32 bytes into 4 unsigned 64-bit integers (>4Q = Big Endian, 4 Long Longs)
        # We use simple unpacking to get massive integers, then normalize.
        # This preserves the 'Avalanche Effect' of the hash in the resulting vector.
        chunks = struct.unpack(">4Q", hash_bytes)
        
        # We mod by 10^9 to get a clean fractional part, then divide.
        # Note: Using full 64-bit range is also valid, but Veselov's notes suggest
        # hierarchical mapping. Here we use a standard linear normalization for stability.
        # Max uint64 is ~1.8e19. We simply normalize to 0-1.
        
        vector = np.array([
            (chunks[0] / 18446744073709551615), # R: Activation Energy
            (chunks[1] / 18446744073709551615), # G: Vector Direction (Gradient)
            (chunks[2] / 18446744073709551615), # B: Plasticity
            (chunks[3] / 18446744073709551615)  # A: Phase (Wavefunction/Memory)
        ], dtype=np.float64)
        
        return vector

    @staticmethod
    def vector_to_string(vector: np.ndarray) -> str:
        """Debug helper to print vector state."""
        return f"R={vector[0]:.4f} | G={vector[1]:.4f} | B={vector[2]:.4f} | A={vector[3]:.4f}"
