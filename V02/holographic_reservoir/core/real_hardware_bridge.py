"""
Real Hardware Bridge - Luckminer LV06 to CHIMERA
=================================================
This bridge receives Stratum protocol from the real miner and exposes
hashes to the CHIMERA substrate in real-time.

NO SIMULATION. Hardware only.

Architecture:
  Luckminer LV06 (192.168.0.15:random)
    -> Stratum TCP
    -> This Bridge (192.168.0.14:3333)
    -> Hash Queue
    -> Substrate API

Author: CHIMERA Project
Date: December 2025
"""

import socket
import json
import threading
import queue
import time
import hashlib
import struct
from collections import deque

class RealHardwareBridge:
    """
    Stratum pool server that captures real ASIC hashes.
    """

    def __init__(self, listen_ip="192.168.0.14", listen_port=3333):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.running = False

        # Hash queue for substrate to consume
        self.hash_queue = deque(maxlen=10000)  # Ring buffer
        self.share_counter = 0
        self.start_time = time.time()

        # Current seed being mined
        self.current_seed = b"00" * 32
        self.job_id = 0

        # Statistics
        self.stats = {
            'total_shares': 0,
            'shares_per_minute': 0,
            'connected_miners': 0,
            'uptime': 0
        }

    def handle_miner(self, conn, addr):
        """Handle incoming miner connection."""
        print(f"[Bridge] Miner connected: {addr}")
        self.stats['connected_miners'] += 1

        try:
            buffer = b''
            while self.running:
                data = conn.recv(4096)
                if not data:
                    break

                buffer += data

                # Process complete JSON messages
                while b'\n' in buffer:
                    line, buffer = buffer.split(b'\n', 1)
                    if line.strip():
                        try:
                            msg = json.loads(line.decode())
                            self.process_message(msg, conn, addr)
                        except Exception as e:
                            print(f"[Bridge] JSON parse error: {e}")

        except Exception as e:
            print(f"[Bridge] Connection error: {e}")
        finally:
            conn.close()
            self.stats['connected_miners'] -= 1
            print(f"[Bridge] Miner disconnected: {addr}")

    def process_message(self, msg, conn, addr):
        """Process Stratum message from miner."""
        msg_id = msg.get('id')
        method = msg.get('method')

        if method == 'mining.subscribe':
            # Miner subscribes
            response = {
                "id": msg_id,
                "result": [[["mining.set_difficulty", "1"], ["mining.notify", "1"]], "08000002", 4],
                "error": None
            }
            self.send_json(conn, response)
            print(f"[Bridge] Miner subscribed: {addr}")

        elif method == 'mining.authorize':
            # Miner authorizes
            response = {"id": msg_id, "result": True, "error": None}
            self.send_json(conn, response)
            print(f"[Bridge] Miner authorized: {addr}")

            # Send initial work
            self.set_difficulty(conn, 1)
            self.send_work(conn, self.current_seed)

        elif method == 'mining.submit':
            # MINER FOUND A SHARE! This is the gold.
            params = msg.get('params', [])
            if len(params) >= 5:
                worker = params[0]
                job_id = params[1]
                extranonce2 = params[2]
                ntime = params[3]
                nonce = params[4]

                print(f"[Bridge] SHARE from {addr}: nonce={nonce}")

                # Convert share to hash
                hash_result = self.share_to_hash(nonce, job_id)

                # Add to queue
                self.hash_queue.append(hash_result)
                self.share_counter += 1
                self.stats['total_shares'] += 1

                # Calculate shares/min
                elapsed = time.time() - self.start_time
                self.stats['shares_per_minute'] = (self.stats['total_shares'] / elapsed) * 60

                # Acknowledge
                response = {"id": msg_id, "result": True, "error": None}
                self.send_json(conn, response)

                # Optionally send new work immediately
                # self.send_work(conn, self.current_seed)

    def share_to_hash(self, nonce: str, job_id: str) -> bytes:
        """
        Convert a mining share (nonce) to a 32-byte hash.

        In real Bitcoin mining, the nonce is part of the block header.
        For CHIMERA, we hash: current_seed + nonce_bytes
        """
        try:
            # Convert hex nonce to bytes
            nonce_bytes = bytes.fromhex(nonce) if isinstance(nonce, str) else nonce

            # Combine seed + nonce
            combined = self.current_seed + nonce_bytes

            # Double SHA-256 (Bitcoin style)
            hash_result = hashlib.sha256(hashlib.sha256(combined).digest()).digest()

            return hash_result
        except Exception as e:
            print(f"[Bridge] Error converting share: {e}")
            # Return hash of seed only as fallback
            return hashlib.sha256(self.current_seed).digest()

    def send_json(self, conn, data):
        """Send JSON message to miner."""
        message = json.dumps(data) + '\n'
        conn.sendall(message.encode())

    def set_difficulty(self, conn, diff):
        """Send difficulty to miner."""
        msg = {"id": None, "method": "mining.set_difficulty", "params": [diff]}
        self.send_json(conn, msg)

    def send_work(self, conn, seed: bytes):
        """Send work (mining.notify) to miner with injected seed."""
        self.job_id += 1

        # Convert seed to hex for coinbase
        seed_hex = seed.hex() if isinstance(seed, bytes) else seed

        msg = {
            "id": None,
            "method": "mining.notify",
            "params": [
                f"chimera_{self.job_id}",
                "0000000000000000000000000000000000000000000000000000000000000000",  # prevhash
                seed_hex,  # coinb1 (OUR SEED)
                "",  # coinb2
                [],  # merkle_branch
                "20000000",  # version
                "1d00ffff",  # nbits (very low difficulty)
                hex(int(time.time()))[2:],  # ntime
                True  # clean_jobs
            ]
        }
        self.send_json(conn, msg)
        print(f"[Bridge] Sent work: job={self.job_id}, seed={seed_hex[:16]}...")

    def inject_seed(self, seed: bytes):
        """
        API for substrate: Inject new seed for miners to work on.
        This broadcasts new work to all connected miners.
        """
        if len(seed) != 32:
            seed = seed.ljust(32, b'\x00')[:32]

        self.current_seed = seed
        print(f"[Bridge] New seed injected: {seed.hex()[:16]}...")

        # We would broadcast to all connected miners here
        # For now, they'll get it on next work request

    def get_hashes(self, count: int = 100, timeout: float = 5.0) -> list:
        """
        API for substrate: Get hashes from queue.

        Args:
            count: Number of hashes to collect
            timeout: Max time to wait

        Returns:
            List of 32-byte hashes
        """
        print(f"[Bridge API] Collecting {count} hashes (timeout={timeout}s)...")
        start = time.time()
        results = []

        while len(results) < count and (time.time() - start) < timeout:
            if self.hash_queue:
                results.append(self.hash_queue.popleft())
            else:
                time.sleep(0.1)  # Wait for shares

        print(f"[Bridge API] Collected {len(results)} hashes in {time.time()-start:.2f}s")
        return results

    def get_stats(self):
        """Get bridge statistics."""
        self.stats['uptime'] = time.time() - self.start_time
        self.stats['queue_size'] = len(self.hash_queue)
        return self.stats

    def start(self):
        """Start the bridge server."""
        self.running = True

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            sock.bind((self.listen_ip, self.listen_port))
            sock.listen(5)
            print(f"[Bridge] Started on {self.listen_ip}:{self.listen_port}")
            print(f"[Bridge] Waiting for Lucky Miner LV06...")

            while self.running:
                conn, addr = sock.accept()
                thread = threading.Thread(target=self.handle_miner, args=(conn, addr))
                thread.daemon = True
                thread.start()

        except Exception as e:
            print(f"[Bridge] Server error: {e}")
        finally:
            sock.close()

    def stop(self):
        """Stop the bridge."""
        self.running = False
        print("[Bridge] Stopped")


if __name__ == "__main__":
    print("="*60)
    print("CHIMERA REAL HARDWARE BRIDGE")
    print("Lucky Miner LV06 -> Stratum -> CHIMERA")
    print("="*60)

    bridge = RealHardwareBridge(listen_ip="192.168.0.14", listen_port=3333)

    # Start in separate thread so we can test the API
    server_thread = threading.Thread(target=bridge.start)
    server_thread.daemon = True
    server_thread.start()

    print("\nBridge running. Press Ctrl+C to stop.")
    print("Monitoring shares...\n")

    try:
        while True:
            time.sleep(5)
            stats = bridge.get_stats()
            print(f"Stats: {stats['total_shares']} shares | "
                  f"{stats['shares_per_minute']:.1f} shares/min | "
                  f"Queue: {stats['queue_size']} | "
                  f"Miners: {stats['connected_miners']}")

    except KeyboardInterrupt:
        print("\nStopping bridge...")
        bridge.stop()
