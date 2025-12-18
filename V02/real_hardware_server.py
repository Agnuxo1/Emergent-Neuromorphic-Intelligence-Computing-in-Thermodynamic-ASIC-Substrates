"""
Real Hardware Server - Direct ASIC Control
===========================================
Complete Stratum pool server to control Luckminer LV06.

This server:
- Acts as a real mining pool
- Accepts connections from Luckminer
- Sends custom work (seeds)
- Captures real shares (hashes)
- Measures performance

Author: CHIMERA Project
Date: December 2025
"""

import socket
import json
import threading
import time
import hashlib
from collections import deque

class RealHardwareServer:
    def __init__(self, host="192.168.0.14", port=3333):
        self.host = host
        self.port = port
        self.running = False
        self.connections = []
        self.shares_received = deque(maxlen=1000)
        self.share_count = 0
        self.start_time = time.time()
        self.job_id = 0

    def handle_connection(self, conn, addr):
        """Handle miner connection."""
        print(f"\n[CONNECTION] Miner connected from {addr}")
        self.connections.append((conn, addr))

        try:
            buffer = b''
            while self.running:
                data = conn.recv(4096)
                if not data:
                    break

                buffer += data

                # Process JSON messages
                while b'\n' in buffer:
                    line, buffer = buffer.split(b'\n', 1)
                    if line.strip():
                        try:
                            msg = json.loads(line.decode())
                            self.process_message(msg, conn, addr)
                        except Exception as e:
                            print(f"[ERROR] Parse failed: {e}")

        except Exception as e:
            print(f"[ERROR] Connection error: {e}")
        finally:
            conn.close()
            if (conn, addr) in self.connections:
                self.connections.remove((conn, addr))
            print(f"[DISCONNECT] Miner disconnected: {addr}")

    def process_message(self, msg, conn, addr):
        """Process Stratum message."""
        method = msg.get('method')
        msg_id = msg.get('id')

        if method == 'mining.subscribe':
            # Miner subscribes
            response = {
                "id": msg_id,
                "result": [[["mining.set_difficulty", "1"], ["mining.notify", "1"]], "08000002", 4],
                "error": None
            }
            self.send_json(conn, response)
            print(f"[SUBSCRIBE] Miner {addr} subscribed")

        elif method == 'mining.authorize':
            # Miner authorizes
            user = msg.get('params', ['unknown'])[0]
            response = {"id": msg_id, "result": True, "error": None}
            self.send_json(conn, response)
            print(f"[AUTHORIZE] Worker: {user}")

            # Immediately send work
            print(f"[WORK] Sending initial work to {addr}...")
            self.send_work(conn)

        elif method == 'mining.submit':
            # SHARE RECEIVED!
            params = msg.get('params', [])
            if len(params) >= 5:
                worker = params[0]
                job_id = params[1]
                extranonce2 = params[2]
                ntime = params[3]
                nonce = params[4]

                self.share_count += 1
                elapsed = time.time() - self.start_time

                share_data = {
                    'time': time.time(),
                    'worker': worker,
                    'job_id': job_id,
                    'nonce': nonce,
                    'elapsed': elapsed
                }
                self.shares_received.append(share_data)

                print(f"[SHARE #{self.share_count}] nonce={nonce} ({elapsed:.1f}s)")

                # Acknowledge
                response = {"id": msg_id, "result": True, "error": None}
                self.send_json(conn, response)

                # Send new work immediately
                self.send_work(conn)

    def send_json(self, conn, data):
        """Send JSON message."""
        message = json.dumps(data) + '\n'
        conn.sendall(message.encode())

    def send_work(self, conn):
        """Send mining work."""
        self.job_id += 1

        # Create seed
        seed_text = f"CHIMERA_SEED_{self.job_id}_{int(time.time())}"
        seed = seed_text.encode().ljust(32, b'\x00')[:32]
        seed_hex = seed.hex()

        # Extremely low difficulty for USB miner
        diff_msg = {
            "id": None,
            "method": "mining.set_difficulty",
            "params": [0.00001]  # Ultra-low difficulty for LV06
        }
        self.send_json(conn, diff_msg)

        # Send work
        work_msg = {
            "id": None,
            "method": "mining.notify",
            "params": [
                f"job_{self.job_id}",
                "0000000000000000000000000000000000000000000000000000000000000000",
                seed_hex,
                "",
                [],
                "20000000",
                "207fffff",  # nbits (maximum easy target)
                hex(int(time.time()))[2:],
                True
            ]
        }
        self.send_json(conn, work_msg)

    def get_stats(self):
        """Get current statistics."""
        elapsed = time.time() - self.start_time
        shares_per_sec = self.share_count / elapsed if elapsed > 0 else 0
        shares_per_min = shares_per_sec * 60

        return {
            'uptime': elapsed,
            'total_shares': self.share_count,
            'shares_per_sec': shares_per_sec,
            'shares_per_min': shares_per_min,
            'active_connections': len(self.connections)
        }

    def start(self):
        """Start the server."""
        self.running = True
        self.start_time = time.time()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            sock.bind((self.host, self.port))
            sock.listen(5)

            print("="*60)
            print("REAL HARDWARE SERVER - LUCKMINER LV06")
            print("="*60)
            print(f"Listening on {self.host}:{self.port}")
            print("Waiting for miner connections...")
            print("="*60)

            while self.running:
                conn, addr = sock.accept()
                thread = threading.Thread(target=self.handle_connection, args=(conn, addr))
                thread.daemon = True
                thread.start()

        except Exception as e:
            print(f"[ERROR] Server error: {e}")
        finally:
            sock.close()

    def stop(self):
        """Stop the server."""
        self.running = False

def run_server_with_monitoring(duration=60):
    """Run server and monitor for specified duration."""
    server = RealHardwareServer()

    # Start server in thread
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()

    print(f"\nMonitoring for {duration} seconds...")
    print("Press Ctrl+C to stop early\n")

    try:
        start = time.time()
        last_share_count = 0

        while time.time() - start < duration:
            time.sleep(5)

            stats = server.get_stats()
            new_shares = stats['total_shares'] - last_share_count
            last_share_count = stats['total_shares']

            print(f"\n[{stats['uptime']:.0f}s] Stats:")
            print(f"  Connections: {stats['active_connections']}")
            print(f"  Total Shares: {stats['total_shares']}")
            print(f"  Shares/min: {stats['shares_per_min']:.2f}")
            print(f"  Last 5s: +{new_shares} shares")

    except KeyboardInterrupt:
        print("\n\nStopping...")

    # Final report
    stats = server.get_stats()

    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    print(f"Duration:          {stats['uptime']:.1f} s")
    print(f"Total Shares:      {stats['total_shares']}")
    print(f"Shares/Second:     {stats['shares_per_sec']:.3f}")
    print(f"Shares/Minute:     {stats['shares_per_min']:.2f}")

    if stats['total_shares'] > 0:
        # Estimate hashrate
        # Difficulty 0.0001 means ~430,000 hashes per share
        hashes_per_share = 430000
        estimated_hashrate = stats['shares_per_sec'] * hashes_per_share
        estimated_mhs = estimated_hashrate / 1e6

        print(f"\nEstimated Hashrate:")
        print(f"  {estimated_hashrate:.2e} H/s")
        print(f"  {estimated_mhs:.2f} MH/s")
        print("\n[SUCCESS] Real hardware communication established!")
    else:
        print("\n[WARNING] No shares received")
        print("Check:")
        print("1. Miner configuration (should point to 192.168.0.14:3333)")
        print("2. Miner status in web UI")
        print("3. Network connectivity")

    print("="*60)

    server.stop()
    return stats

if __name__ == "__main__":
    stats = run_server_with_monitoring(duration=45)
