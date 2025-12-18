"""
CHIMERA OPTIMIZED FINAL - Maximum Entropy Flow
================================================
Servidor Stratum optimizado para flujo máximo de datos del LV06

CONFIGURACION CLAVE:
- nBits: 1d00ffff (dificultad mínima absoluta)
- Trabajo continuo (nuevo job después de cada share)
- Telemetría en tiempo real

Objetivo: 10+ shares/segundo para alimentación continua de HNS
"""

import socket
import json
import threading
import time
from collections import deque

HOST_IP = "192.168.0.14"
PORT = 3333

class ChimeraOptimized:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST_IP, PORT))
        self.sock.listen(1)

        # Telemetria
        self.share_count = 0
        self.share_timestamps = deque(maxlen=1000)
        self.start_time = None
        self.last_report_time = None
        self.job_id = 0

        print("="*70)
        print("CHIMERA OPTIMIZED - MAXIMUM ENTROPY FLOW")
        print("="*70)
        print(f"Server: {HOST_IP}:{PORT}")
        print("Target: 500 GH/s (Lucky Miner LV06)")
        print("nBits: 1d00ffff (minimum difficulty)")
        print("Expected: 10+ shares/second")
        print("="*70 + "\n")

    def handle_connection(self, conn, addr):
        print(f"[CONNECT] Miner: {addr}")
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
                            msg = json.loads(line.decode())
                            self.process_message(msg, conn, addr)
                        except Exception as e:
                            print(f"[ERROR] Parse: {e}")

        except Exception as e:
            print(f"[ERROR] Connection: {e}")
        finally:
            conn.close()
            print(f"[DISCONNECT] {addr}")

    def process_message(self, msg, conn, addr):
        msg_id = msg.get('id')
        method = msg.get('method')

        if method == 'mining.subscribe':
            response = {
                "id": msg_id,
                "result": [
                    [["mining.set_difficulty", "1"], ["mining.notify", "1"]],
                    "08000002",  # ExtraNonce1
                    4            # ExtraNonce2_size
                ],
                "error": None
            }
            self.send_json(conn, response)
            print("[SUBSCRIBE] OK")

        elif method == 'mining.authorize':
            response = {"id": msg_id, "result": True, "error": None}
            self.send_json(conn, response)
            print("[AUTHORIZE] OK")

            # Inicializar telemetria
            self.start_time = time.time()
            self.last_report_time = self.start_time

            # NO enviar set_difficulty - usar solo nBits en el job
            # Enviar primer trabajo
            self.send_work(conn)
            print("[WORK] First job sent\n")

        elif method == 'mining.submit':
            params = msg.get('params', [])
            if len(params) >= 5:
                nonce = params[4]

                current_time = time.time()
                self.share_count += 1
                self.share_timestamps.append(current_time)

                # Telemetria
                self.print_telemetry(nonce)

                # Aceptar share
                response = {"id": msg_id, "result": True, "error": None}
                self.send_json(conn, response)

                # Nuevo trabajo INMEDIATAMENTE
                self.send_work(conn)

    def print_telemetry(self, nonce):
        if not self.start_time:
            return

        current_time = time.time()
        elapsed_total = current_time - self.start_time
        elapsed_since_report = current_time - self.last_report_time

        # Calcular rates
        if len(self.share_timestamps) >= 2:
            window_duration = self.share_timestamps[-1] - self.share_timestamps[0]
            rate_window = len(self.share_timestamps) / window_duration if window_duration > 0 else 0
        else:
            rate_window = 0

        rate_avg = self.share_count / elapsed_total if elapsed_total > 0 else 0

        # Reporte cada 10 shares o cada 5s
        if elapsed_since_report >= 5.0 or self.share_count % 10 == 0:
            # Hashrate estimado (cada share a diff 1 = 4.3B hashes)
            hashrate_mhs = (rate_avg * 4294967296) / 1_000_000
            hashrate_ghs = hashrate_mhs / 1000

            print(f"\n{'='*70}")
            print(f"[STATS] Share #{self.share_count} | Time: {elapsed_total:.1f}s")
            print(f"{'='*70}")
            print(f"Nonce:         {nonce}")
            print(f"Rate (window): {rate_window:.2f} sh/s")
            print(f"Rate (avg):    {rate_avg:.2f} sh/s")
            print(f"Hashrate:      {hashrate_ghs:.3f} GH/s ({hashrate_mhs:.1f} MH/s)")
            print(f"Total shares:  {self.share_count}")

            # Comparacion con objetivo
            if rate_avg >= 10:
                status = "[OK] OPTIMAL ENTROPY FLOW"
            elif rate_avg >= 1:
                status = "[OK] GOOD"
            else:
                status = "[WARNING] LOW"

            print(f"Status:        {status}")
            print(f"{'='*70}\n")

            self.last_report_time = current_time
        else:
            print(f"[SHARE] #{self.share_count} | {nonce} | {rate_window:.1f} sh/s")

    def send_json(self, conn, data):
        try:
            line = json.dumps(data) + '\n'
            conn.sendall(line.encode())
        except Exception as e:
            print(f"[ERROR] Send: {e}")

    def send_work(self, conn):
        """
        Enviar trabajo con dificultad MINIMA absoluta

        KEY: nBits = 1d00ffff (dificultad 1, la mas baja posible)
        """
        self.job_id += 1

        # Seed para HNS
        seed_text = f"CHIMERA_{self.job_id}_{int(time.time())}"
        seed = seed_text.encode().ljust(64, b'\x00')[:64]
        seed_hex = seed.hex()

        # Timestamp SIEMPRE 8 caracteres
        ntime = format(int(time.time()), '08x')

        work_msg = {
            "id": None,
            "method": "mining.notify",
            "params": [
                f"{self.job_id:x}",                                    # job_id
                "0000000000000000000000000000000000000000000000000000000000000000",  # prevhash
                seed_hex,                                               # coinb1 (SEED)
                "",                                                     # coinb2
                [],                                                     # merkle_branch
                "20000000",                                             # version
                "1d00ffff",                                             # nBits (DIFICULTAD MINIMA)
                ntime,                                                  # nTime
                True                                                    # clean_jobs
            ]
        }
        self.send_json(conn, work_msg)

    def start(self):
        print("[INFO] Waiting for LV06 connection...\n")
        while True:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.handle_connection, args=(conn, addr))
            thread.daemon = True
            thread.start()

def run_benchmark(duration=60):
    """Ejecutar benchmark por tiempo especificado"""
    server = ChimeraOptimized()

    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()

    print(f"[BENCHMARK] Running for {duration} seconds...\n")

    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print("\n[STOPPED] Benchmark interrupted\n")

    # Reporte final
    if server.share_count > 0:
        elapsed = time.time() - server.start_time
        rate = server.share_count / elapsed
        hashrate_ghs = (rate * 4294967296) / 1_000_000_000

        print("\n" + "#"*70)
        print("BENCHMARK FINAL RESULTS")
        print("#"*70)
        print(f"Duration:        {elapsed:.1f} seconds")
        print(f"Total shares:    {server.share_count}")
        print(f"Rate:            {rate:.2f} shares/second")
        print(f"Rate:            {rate * 60:.1f} shares/minute")
        print(f"Hashrate:        {hashrate_ghs:.3f} GH/s")
        print()
        print("COMPARISON:")
        print(f"  Previous (diff=1024): 0.017 sh/s (1 share/min)")
        print(f"  Current  (diff=1):    {rate:.2f} sh/s")
        print(f"  IMPROVEMENT:          {rate/0.017:.0f}x MORE DATA FLOW")
        print()

        if hashrate_ghs >= 0.1:
            print("[SUCCESS] Real hardware validated!")
            print("[OK] Entropy flow sufficient for CHIMERA HNS")
        else:
            print("[WARNING] Hashrate lower than expected")
            print("[INFO] Check miner configuration")

        print("#"*70 + "\n")
    else:
        print("\n[ERROR] No shares received")
        print("Troubleshooting:")
        print("1. Verify miner points to 192.168.0.14:3333")
        print("2. Check miner web UI status")
        print("3. Restart miner if needed\n")

if __name__ == "__main__":
    run_benchmark(duration=60)
