import socket
import struct
import hashlib
import threading
import time

# Configuration matches driver-chimera.c
HOST = '127.0.0.1'
PORT = 4028

def sha256d(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def virtual_miner_thread(connection, address):
    try:
        data = connection.recv(1024)
        if not data: return
        
        # Unpack Request: 8 UINTS (Seed) + 1 UINT (Bits) + 1 UINT (ID)
        # Total 10 * 4 = 40 bytes
        if len(data) < 40:
            print(f"[VirtualS9] Error: Pkt too small ({len(data)})")
            return
            
        unpacked = struct.unpack('<8I II', data[:40])
        seed_ints = unpacked[:8]
        target_bits = unpacked[8] # e.g. 0x1d00ffff
        req_id = unpacked[9]
        
        # Reconstruct Seed Bytes
        seed_bytes = b''.join([struct.pack('<I', x) for x in seed_ints])
        
        # print(f"[VirtualS9] Mining Job {req_id} Received. Target={hex(target_bits)}")
        
        # PERFORMS WORK (The Simulation)
        # We try to find 1 valid nonce to behave like the real thing
        # Real S9 finds many, we simulated finding 1 for the protocol test
        
        # Create Header
        header_prefix = b'\x00'*4 + b'\x00'*32 + seed_bytes + b'\x00'*4 + struct.pack('<I', target_bits)
        
        found_nonce = 0
        found_hash = b'\x00'*32
        
        # Quick Scan (Fake Work)
        for nonce in range(1000):
            h = sha256d(header_prefix + struct.pack('<I', nonce))
            # Just return the first one for speed, or check difficulty
            # For this 'Protocol Test', we just return a hash.
            found_hash = h
            found_nonce = nonce
            break # Instant return
            
        # Pack Response: ID, Nonce, Hash[8]
        # 1 + 1 + 8 = 10 UINTS = 40 bytes
        
        hash_ints = struct.unpack('<8I', found_hash)
        
        resp_fmt = '<I I 8I'
        response = struct.pack(resp_fmt, req_id, found_nonce, *hash_ints)
        
        connection.sendall(response)
        
    except Exception as e:
        print(f"[VirtualS9] Error: {e}")
    finally:
        connection.close()

def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"=== VIRTUAL ANTMINER S9 ONLINE ({HOST}:{PORT}) ===")
    print("Emulating 'driver-chimera.c' Protocol...")
    
    while True:
        conn, addr = sock.accept()
        t = threading.Thread(target=virtual_miner_thread, args=(conn, addr))
        t.start()

if __name__ == "__main__":
    run_server()
