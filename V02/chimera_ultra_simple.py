"""
CHIMERA ULTRA-SIMPLE - Minimal Working Implementation
========================================================
La implementación MÁS simple posible para validar comunicación

Usa parámetros probados del real_hardware_server.py que SÍ recibió 1 share
"""

import socket
import json
import threading
import time

HOST = "192.168.0.14"
PORT = 3333

class UltraSimpleServer:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))
        self.sock.listen(5)
        self.share_count = 0
        self.start_time = time.time()
        self.job_id = 0

        print("="*60)
        print("CHIMERA ULTRA-SIMPLE SERVER")
        print("="*60)
        print(f"Listening: {HOST}:{PORT}")
        print("Using EXACT format from working real_hardware_server.py")
        print("nBits: 207fffff (from working code)")
        print("="*60 + "\n")

    def handle(self, conn, addr):
        print(f"[CONNECT] {addr}")
        buffer = b''

        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    break

                buffer += data

                while b'\n' in buffer:
                    line, buffer = buffer.split(b'\n', 1)
                    if line.strip():
                        try:
                            msg = json.loads(line)
                            self.proc(msg, conn, addr)
                        except:
                            pass

        except:
            pass
        finally:
            conn.close()

    def proc(self, msg, conn, addr):
        mid = msg.get('id')
        method = msg.get('method')

        if method == 'mining.subscribe':
            r = {"id": mid, "result": [[["mining.set_difficulty","1"],["mining.notify","1"]],"08000002",4], "error": None}
            self.send(conn, r)
            print(f"[SUBSCRIBE] {addr}")

        elif method == 'mining.authorize':
            r = {"id": mid, "result": True, "error": None}
            self.send(conn, r)
            print(f"[AUTHORIZE] {addr}")
            print(f"[WORK] Sending job...")
            self.send_work(conn)

        elif method == 'mining.submit':
            params = msg.get('params', [])
            if len(params) >= 5:
                nonce = params[4]
                self.share_count += 1
                elapsed = time.time() - self.start_time
                rate = self.share_count / elapsed

                print(f"\n>>> SHARE #{self.share_count} <<< nonce={nonce} | {elapsed:.1f}s | {rate:.2f} sh/s\n")

                # Accept
                r = {"id": mid, "result": True, "error": None}
                self.send(conn, r)

                # Send new work
                self.send_work(conn)

    def send(self, conn, data):
        try:
            conn.sendall((json.dumps(data) + '\n').encode())
        except:
            pass

    def send_work(self, conn):
        """
        FORMATO EXACTO del real_hardware_server.py que SÍ funcionó
        """
        self.job_id += 1

        # Seed (igual que el código que funcionó)
        seed_text = f"CHIMERA_SEED_{self.job_id}_{int(time.time())}"
        seed = seed_text.encode().ljust(32, b'\x00')[:32]
        seed_hex = seed.hex()

        # Usar EXACTAMENTE los mismos parámetros que funcionaron
        work = {
            "id": None,
            "method": "mining.notify",
            "params": [
                f"job_{self.job_id}",  # job_id
                "0000000000000000000000000000000000000000000000000000000000000000",  # prevhash
                seed_hex,              # coinb1 (SEED - funciona con 64 chars)
                "",                    # coinb2 (vacío - como el que funcionó)
                [],                    # merkle_branch
                "20000000",            # version
                "207fffff",            # nBits (EXACTO del código que funcionó)
                hex(int(time.time()))[2:],  # ntime
                True                   # clean_jobs
            ]
        }
        self.send(conn, work)

    def run(self):
        print("[INFO] Waiting for connections...\n")
        while True:
            conn, addr = self.sock.accept()
            t = threading.Thread(target=self.handle, args=(conn, addr), daemon=True)
            t.start()

if __name__ == "__main__":
    server = UltraSimpleServer()
    try:
        server.run()
    except KeyboardInterrupt:
        elapsed = time.time() - server.start_time
        print(f"\n\n{'='*60}")
        print("FINAL RESULTS")
        print("="*60)
        print(f"Duration:     {elapsed:.1f}s")
        print(f"Total shares: {server.share_count}")
        if server.share_count > 0:
            rate = server.share_count / elapsed
            print(f"Rate:         {rate:.3f} sh/s ({rate*60:.1f} sh/min)")
        print("="*60 + "\n")
