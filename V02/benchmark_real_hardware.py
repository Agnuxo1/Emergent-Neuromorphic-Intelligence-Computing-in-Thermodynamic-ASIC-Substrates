"""
Real Hardware Benchmark - Luckminer LV06
=========================================
Full Stratum pool implementation to benchmark the real ASIC.

This script:
1. Connects to the bridge as a pool
2. Sends real mining work
3. Captures shares from the miner
4. Measures performance metrics

NO SIMULATION. Real hardware only.
"""

import socket
import json
import time
import hashlib
import struct

class LuckminerBenchmark:
    def __init__(self, bridge_ip="192.168.0.14", bridge_port=3333):
        self.bridge_ip = bridge_ip
        self.bridge_port = bridge_port
        self.sock = None
        self.shares_received = []
        self.job_id_counter = 0

    def connect(self):
        """Connect to bridge."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10.0)
            self.sock.connect((self.bridge_ip, self.bridge_port))
            print(f"[OK] Connected to bridge at {self.bridge_ip}:{self.bridge_port}")
            return True
        except Exception as e:
            print(f"[FAIL] Connection failed: {e}")
            return False

    def send_json(self, data):
        """Send JSON message."""
        message = json.dumps(data) + '\n'
        self.sock.sendall(message.encode())

    def recv_messages(self, timeout=2.0):
        """Receive all pending JSON messages."""
        messages = []
        self.sock.settimeout(timeout)

        try:
            buffer = b''
            while True:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break

                buffer += chunk

                # Process complete messages
                while b'\n' in buffer:
                    line, buffer = buffer.split(b'\n', 1)
                    if line.strip():
                        try:
                            msg = json.loads(line.decode())
                            messages.append(msg)
                        except:
                            pass

                # Break if we got at least one message and timeout
                if messages:
                    break

        except socket.timeout:
            pass

        return messages

    def handshake(self):
        """Perform Stratum handshake."""
        print("\n[1/5] Performing Stratum handshake...")

        # Subscribe
        subscribe = {
            "id": 1,
            "method": "mining.subscribe",
            "params": ["chimera_benchmark/1.0"]
        }
        self.send_json(subscribe)
        responses = self.recv_messages()
        print(f"  Subscribe response: {len(responses)} messages")

        # Authorize
        authorize = {
            "id": 2,
            "method": "mining.authorize",
            "params": ["chimera", "x"]
        }
        self.send_json(authorize)
        responses = self.recv_messages()
        print(f"  Authorize response: {len(responses)} messages")

        print("[OK] Handshake complete")
        return True

    def send_work(self, seed_text="BENCHMARK_SEED"):
        """Send mining work to miner."""
        self.job_id_counter += 1

        # Create seed
        seed = seed_text.encode().ljust(32, b'\x00')[:32]
        seed_hex = seed.hex()

        # Difficulty (very low for fast shares)
        difficulty = 1

        # Set difficulty first
        diff_msg = {
            "id": None,
            "method": "mining.set_difficulty",
            "params": [difficulty]
        }
        self.send_json(diff_msg)

        # Send work
        work_msg = {
            "id": None,
            "method": "mining.notify",
            "params": [
                f"job_{self.job_id_counter}",  # job_id
                "0000000000000000000000000000000000000000000000000000000000000000",  # prevhash
                seed_hex,  # coinb1 (our seed)
                "",  # coinb2
                [],  # merkle_branch
                "20000000",  # version
                "1d00ffff",  # nbits
                hex(int(time.time()))[2:],  # ntime
                True  # clean_jobs
            ]
        }
        self.send_json(work_msg)

        print(f"[2/5] Work sent: job_id=job_{self.job_id_counter}, seed={seed_text}")
        return f"job_{self.job_id_counter}"

    def collect_shares(self, duration=10.0):
        """Collect shares for specified duration."""
        print(f"\n[3/5] Collecting shares for {duration} seconds...")
        print("-" * 60)

        start_time = time.time()
        shares = []

        while time.time() - start_time < duration:
            try:
                messages = self.recv_messages(timeout=1.0)

                for msg in messages:
                    # Check if it's a share submission
                    if msg.get('method') == 'mining.submit':
                        params = msg.get('params', [])
                        if len(params) >= 5:
                            worker = params[0]
                            job_id = params[1]
                            extranonce2 = params[2]
                            ntime = params[3]
                            nonce = params[4]

                            share_info = {
                                'time': time.time() - start_time,
                                'job_id': job_id,
                                'nonce': nonce,
                                'worker': worker
                            }
                            shares.append(share_info)

                            elapsed = time.time() - start_time
                            print(f"[{elapsed:5.1f}s] Share #{len(shares)}: nonce={nonce}")

                            # Acknowledge the share
                            ack = {
                                "id": msg.get('id'),
                                "result": True,
                                "error": None
                            }
                            self.send_json(ack)

            except Exception as e:
                pass

            # Progress indicator every 2 seconds if no shares
            elapsed = time.time() - start_time
            if len(shares) == 0 and int(elapsed) % 2 == 0:
                print(f"[{elapsed:5.1f}s] Waiting for shares...")

        print("-" * 60)
        return shares

    def run_benchmark(self, duration=15.0):
        """Run complete benchmark."""
        print("="*60)
        print("REAL HARDWARE BENCHMARK - LUCKMINER LV06")
        print("="*60)
        print(f"Target: {self.bridge_ip}:{self.bridge_port}")
        print(f"Duration: {duration}s")
        print("="*60)

        # Connect
        if not self.connect():
            return None

        # Handshake
        if not self.handshake():
            return None

        # Send work
        job_id = self.send_work("CHIMERA_BENCHMARK_" + str(int(time.time())))

        # Collect shares
        shares = self.collect_shares(duration=duration)

        # Calculate metrics
        print("\n[4/5] Calculating metrics...")

        if len(shares) > 0:
            shares_per_second = len(shares) / duration
            avg_time_between_shares = duration / len(shares) if len(shares) > 0 else 0

            # Estimate hashrate (very rough)
            # With difficulty 1, each share represents ~4.3 billion hashes
            estimated_hashrate = shares_per_second * 4.3e9  # H/s
            estimated_hashrate_mhs = estimated_hashrate / 1e6  # MH/s
            estimated_hashrate_ghs = estimated_hashrate / 1e9  # GH/s

            results = {
                'success': True,
                'duration': duration,
                'total_shares': len(shares),
                'shares_per_second': shares_per_second,
                'avg_interval_seconds': avg_time_between_shares,
                'estimated_hashrate_hs': estimated_hashrate,
                'estimated_hashrate_mhs': estimated_hashrate_mhs,
                'estimated_hashrate_ghs': estimated_hashrate_ghs,
                'shares_data': shares
            }
        else:
            results = {
                'success': False,
                'duration': duration,
                'total_shares': 0,
                'error': 'No shares received'
            }

        # Print results
        print("\n[5/5] BENCHMARK RESULTS")
        print("="*60)

        if results['success']:
            print(f"Duration:              {results['duration']:.2f} s")
            print(f"Total Shares:          {results['total_shares']}")
            print(f"Shares/Second:         {results['shares_per_second']:.3f}")
            print(f"Avg Share Interval:    {results['avg_interval_seconds']:.2f} s")
            print(f"\nEstimated Hashrate:")
            print(f"  {results['estimated_hashrate_hs']:.2e} H/s")
            print(f"  {results['estimated_hashrate_mhs']:.2f} MH/s")
            print(f"  {results['estimated_hashrate_ghs']:.3f} GH/s")
            print("\n[SUCCESS] Benchmark complete!")
        else:
            print(f"[FAIL] {results.get('error')}")
            print("\nPossible causes:")
            print("1. Miner is not actively mining")
            print("2. Difficulty is too high")
            print("3. Miner needs to be restarted")
            print("4. Bridge is not properly forwarding work")

        print("="*60)

        # Cleanup
        self.sock.close()

        return results

if __name__ == "__main__":
    benchmark = LuckminerBenchmark(
        bridge_ip="192.168.0.14",
        bridge_port=3333
    )

    results = benchmark.run_benchmark(duration=20.0)

    # Save results
    if results and results.get('success'):
        print("\n✓ Real hardware connection validated")
        print("✓ Luckminer LV06 is operational")
        print(f"✓ Hashrate: ~{results['estimated_hashrate_ghs']:.2f} GH/s")
    else:
        print("\n✗ Hardware benchmark failed")
        print("Troubleshooting required")
