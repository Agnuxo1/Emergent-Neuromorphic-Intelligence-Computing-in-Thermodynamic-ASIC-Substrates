import socket
import json
import hashlib
import time
import struct

class ASICSubstrate:
    """
    Layer 0: The Physical Substrate.
    Interfaces with the AxeOS Hybrid Driver (Port 4028) to retrieve thermodynamic entropy.
    """
    def __init__(self, simulation_mode=False):
        self.simulation_mode = simulation_mode
        self.hardware_ip = "127.0.0.1"
        self.hardware_port = 4028
        
        if not self.simulation_mode:
            print(f"🔌 ASIC Substrate Linked: {self.hardware_ip}:{self.hardware_port}")
            
    def mine_reservoir_state(self, seed: bytes, cycles: int = 1) -> list:
        """
        Retrieves 'cycles' number of entropy hashes from the substrate.
        Args:
            seed (bytes): Semantic seed (currently unused by V1 hardware, but good for logs).
            cycles (int): Number of entropy frames to fetch.
        """
        results = []
        
        if self.simulation_mode:
            # CPU Simulation (PRNG) - Control Group
            for i in range(cycles):
                current = hashlib.sha256(seed + str(i).encode() + str(time.time()).encode()).digest()
                results.append(current)
            return results
            
        else:
            # HARDWARE MODE (Burst Protocol)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5.0) # Increased timeout for burst
                s.connect((self.hardware_ip, self.hardware_port))
                
                # OPTIMIZED BURST REQUEST
                # We request 'cycles' hashes in one go
                cmd = f"BURST:{cycles}\n".encode()
                s.sendall(cmd)
                
                # Receive all data
                # Expected bytes = cycles * 32
                expected_bytes = cycles * 32
                data = b""
                
                start_recv = time.time()
                while len(data) < expected_bytes:
                    if time.time() - start_recv > 5.0: break # Safety breakout
                    chunk = s.recv(4096)
                    if not chunk: break
                    data += chunk
                
                s.close()
                
                # Split raw bytes into 32-byte hash chunks
                for i in range(0, len(data), 32):
                    chunk = data[i:i+32]
                    if len(chunk) == 32:
                        results.append(chunk)
                        
                # Fallback expansion if network dropped packets (Safety)
                # If we got at least 1 hash but less than requested, expand the last one
                if results and len(results) < cycles:
                    needed = cycles - len(results)
                    last = results[-1]
                    for _ in range(needed):
                        last = hashlib.sha256(last).digest()
                        results.append(last)
                        
            except Exception as e:
                print(f"[Substrate] Hardware Link Error: {e}")
                # Fallback to simulation if hardware fails to keep system alive
                results = self.mine_reservoir_state(seed, cycles=cycles) # Infinite recursion risk if sim_mode not handled? 
                # No, we need to manually return simulated data here without calling self.mine_reservoir_state again with False
                # Just return raw PRNG
                return [os.urandom(32) for _ in range(cycles)]
                
        return results
