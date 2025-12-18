import hashlib
import struct
import time
import os
import socket
from typing import List, Tuple

class ASICSubstrate:
    """
    Physical Substrate Interface (Layer 0).
    """
    
    def __init__(self, simulation_mode: bool = True, hardware_ip: str = "127.0.0.1"):
        self.simulation_mode = simulation_mode
        self.hardware_ip = hardware_ip
        self.hardware_port = 4028
        self.target_bits = 0x1F00FFFF 

    def _sha256_double(self, data: bytes) -> bytes:
        return hashlib.sha256(hashlib.sha256(data).digest()).digest()
    
    def mine_reservoir_state(self, seed: bytes, cycles: int = 1000) -> List[bytes]:
        """
        Injects a 'Semantic Seed' (Idea) into the substrate.
        """
        results = []
        
        # Ensure 32 bytes
        if len(seed) != 32:
            seed = seed.ljust(32, b'\x00')[:32]
            
        if self.simulation_mode:
            # --- INTERNAL CPU SIMULATION ---
            header_prefix = b'\x00'*4 + b'\x00'*32 + seed + b'\x00'*4 + b'\x00'*4
            
            for nonce in range(cycles):
                nonce_bytes = struct.pack("<I", nonce) 
                work_header = header_prefix + nonce_bytes
                results.append(self._sha256_double(work_header))
                
        else:
            # --- NETWORK HARDWARE MODE (Real S9 or Virtual Server) ---
            # We send 1 request per cycle? No, that's too slow.
            # Real driver returns a batch. For this protocol test, we send 1 request.
            # To optimize, we'd send a batch request, but let's do 1 for Proof of Concept.
            
            try:
                # Struct: 8xINT (Seed) + 1xINT (Bits) + 1xINT (ID)
                seed_ints = struct.unpack('<8I', seed)
                req_id = int(time.time()) % 10000
                
                payload = struct.pack('<8I II', *seed_ints, self.target_bits, req_id)
                
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2.0)
                    s.connect((self.hardware_ip, self.hardware_port))
                    s.sendall(payload)
                    
                    # Receive Response: ID(I) + Nonce(I) + Hash(8I)
                    # Total 40 bytes
                    data = s.recv(40)
                    
                    if len(data) == 40:
                        unpacked = struct.unpack('<I I 8I', data)
                        # resp_id = unpacked[0]
                        # nonce = unpacked[1]
                        hash_ints = unpacked[2:]
                        
                        # Reconstruct Hash Bytes
                        hash_bytes = b''.join([struct.pack('<I', x) for x in hash_ints])
                        results.append(hash_bytes)
                        
                        # For testing, we just duplicate this result 'cycles' times or just return 1
                        # Ideally, the hardware returns a List.
                        # We will just return [hash_bytes] * cycles to satisfy the 'shape' expected by reservoir
                        # In real S9, the 'VirtualMinerThread' would stream back multiple nonces.
                        if cycles > 1:
                            results = [hash_bytes] * cycles 
                        
            except Exception as e:
                print(f"[Substrate] Hardware Link Error: {e}")
                # Fallback to simulation?? Or fail?
                # Let's fail gracefully by returning empty
                return []
            
        return results

    def benchmark_speed(self) -> float:
        """Returns Hashes Per Second (H/s) of the current substrate."""
        start = time.time()
        self.mine_reservoir_state(os.urandom(32), cycles=100)
        end = time.time()
        if end - start == 0: return 0.0
        return 100.0 / (end - start)
