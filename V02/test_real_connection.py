"""
Test Real Hardware Connection
==============================
Connects to the existing chimera_wifi_bridge.py to verify
the Luckminer LV06 is sending data.

This will attempt to sniff/monitor the Stratum traffic.
"""

import socket
import json
import time

def monitor_stratum_traffic(duration=30):
    """
    Monitor the existing Stratum connection.
    We'll try to connect as a second client to see traffic.
    """
    print("="*60)
    print("REAL HARDWARE CONNECTION TEST")
    print("Monitoring Luckminer LV06 @ 192.168.0.15")
    print(f"Duration: {duration}s")
    print("="*60)

    try:
        # Try to connect to the bridge
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)

        print("\n[1/3] Attempting connection to bridge...")
        sock.connect(("192.168.0.14", 3333))
        print("[OK] Connected to bridge at 192.168.0.14:3333")

        # Send subscribe
        print("\n[2/3] Sending mining.subscribe...")
        subscribe_msg = {
            "id": 1,
            "method": "mining.subscribe",
            "params": ["test_monitor/1.0"]
        }
        sock.sendall((json.dumps(subscribe_msg) + '\n').encode())

        # Receive response
        buffer = b''
        start_time = time.time()
        message_count = 0

        print(f"\n[3/3] Monitoring traffic for {duration}s...")
        print("-"*60)

        while time.time() - start_time < duration:
            try:
                sock.settimeout(1.0)
                data = sock.recv(4096)

                if data:
                    buffer += data

                    # Process complete messages
                    while b'\n' in buffer:
                        line, buffer = buffer.split(b'\n', 1)
                        if line.strip():
                            try:
                                msg = json.loads(line.decode())
                                message_count += 1

                                # Print message info
                                method = msg.get('method', msg.get('result', 'unknown'))
                                print(f"[{time.time()-start_time:.1f}s] Message #{message_count}: {method}")

                                # If it's a mining.notify, show details
                                if msg.get('method') == 'mining.notify':
                                    params = msg.get('params', [])
                                    if len(params) > 0:
                                        job_id = params[0]
                                        print(f"  -> New work: job_id={job_id}")

                            except Exception as e:
                                print(f"  [Error parsing]: {e}")

            except socket.timeout:
                # No data, continue
                elapsed = time.time() - start_time
                if int(elapsed) % 5 == 0:
                    print(f"  [{elapsed:.0f}s] Waiting for messages...")

        print("-"*60)
        print(f"\nTest complete!")
        print(f"Total messages received: {message_count}")
        print(f"Messages per second: {message_count/duration:.2f}")

        sock.close()

        if message_count > 0:
            print("\n[SUCCESS] Hardware connection is ACTIVE!")
            print("The Luckminer LV06 is communicating with the bridge.")
            return True
        else:
            print("\n[WARNING] No messages received.")
            print("The bridge may not be sending work or miner is not responding.")
            return False

    except Exception as e:
        print(f"\n[FAIL] Connection test failed: {e}")
        print("\nPossible causes:")
        print("1. chimera_wifi_bridge.py is not running")
        print("2. Bridge is on different IP/port")
        print("3. Firewall blocking connection")
        return False

if __name__ == "__main__":
    success = monitor_stratum_traffic(duration=20)

    print("\n" + "="*60)
    if success:
        print("STATUS: READY FOR HARDWARE INTEGRATION")
    else:
        print("STATUS: TROUBLESHOOTING NEEDED")
    print("="*60)
