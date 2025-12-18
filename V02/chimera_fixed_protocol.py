"""
CHIMERA STRATUM SERVER - PROTOCOLO CORREGIDO
Implementación Stratum compatible con BM1387 (LV06, Antminer S9)
"""

import socket
import json
import threading
import time
import struct
from collections import deque

HOST_IP = "192.168.0.14"
PORT = 3333

class ChimeraStratum:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST_IP, PORT))
        self.sock.listen(1)
        self.client_conn = None

        # Telemetría
        self.share_count = 0
        self.share_timestamps = deque(maxlen=1000)
        self.start_time = None
        self.last_report_time = None

        # Job counter
        self.job_counter = 0

        print(f"[CHIMERA] Stratum server on {HOST_IP}:{PORT}")
        print("[CONFIG] Difficulty = 1")
        print("[PROTOCOL] Fixed BM1387-compatible format")
        print("="*70)

    def handle_client(self, conn, addr):
        print(f"[OK] Miner connected: {addr}")
        self.client_conn = conn

        buffer = ""
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break

                buffer += data.decode('utf-8', errors='ignore')

                # Process complete JSON messages
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.strip():
                        try:
                            msg = json.loads(line)
                            self.process_message(msg, conn)
                        except json.JSONDecodeError as e:
                            print(f"[ERROR] JSON decode: {e}")

            except Exception as e:
                print(f"[ERROR] Connection: {e}")
                break

        print("[INFO] Miner disconnected")

    def process_message(self, msg, conn):
        msg_id = msg.get('id')
        method = msg.get('method')

        if method == 'mining.subscribe':
            # Respuesta estándar con ExtraNonce1 y ExtraNonce2_size
            response = {
                "id": msg_id,
                "result": [
                    [
                        ["mining.set_difficulty", "1"],
                        ["mining.notify", "1"]
                    ],
                    "08000002",  # ExtraNonce1 (4 bytes en hex)
                    4            # ExtraNonce2_size (4 bytes)
                ],
                "error": None
            }
            self.send_json(conn, response)
            print("[SUBSCRIBE] Miner subscribed")

        elif method == 'mining.authorize':
            response = {"id": msg_id, "result": True, "error": None}
            self.send_json(conn, response)
            print("[AUTH] Miner authorized")

            # Inicializar telemetría
            self.start_time = time.time()
            self.last_report_time = self.start_time

            # Enviar dificultad mínima
            self.set_difficulty(conn, 1)

            # Enviar primer trabajo VÁLIDO
            self.send_job(conn)
            print("[INJECT] First job sent with diff=1\n")

        elif method == 'mining.submit':
            # Share recibido del minero
            params = msg.get('params', [])
            if len(params) >= 5:
                worker, job_id, extranonce2, ntime, nonce = params[:5]

                current_time = time.time()
                self.share_count += 1
                self.share_timestamps.append(current_time)

                # Telemetría
                self.print_telemetry(nonce)

                # Aceptar share
                response = {"id": msg_id, "result": True, "error": None}
                self.send_json(conn, response)

                # Enviar nuevo trabajo inmediatamente
                self.send_job(conn)
            else:
                print(f"[ERROR] Invalid submit format: {params}")
                response = {"id": msg_id, "result": False, "error": (21, "Invalid params", None)}
                self.send_json(conn, response)

        elif method == 'mining.extranonce.subscribe':
            response = {"id": msg_id, "result": True, "error": None}
            self.send_json(conn, response)

        else:
            print(f"[WARN] Unknown method: {method}")

    def print_telemetry(self, nonce):
        if self.start_time is None or self.last_report_time is None:
            return

        current_time = time.time()
        elapsed_total = current_time - self.start_time
        elapsed_since_report = current_time - self.last_report_time

        # Calcular rates
        if len(self.share_timestamps) >= 2:
            window_duration = self.share_timestamps[-1] - self.share_timestamps[0]
            shares_per_sec_window = len(self.share_timestamps) / window_duration if window_duration > 0 else 0
        else:
            shares_per_sec_window = 0

        shares_per_sec_avg = self.share_count / elapsed_total if elapsed_total > 0 else 0

        # Reporte periódico
        if elapsed_since_report >= 5.0 or self.share_count % 10 == 0:
            hashrate_mhs = (shares_per_sec_avg * 4294967296) / 1_000_000
            hashrate_ghs = hashrate_mhs / 1000

            print(f"\n{'='*70}")
            print(f"[TELEMETRIA] Share #{self.share_count}")
            print(f"{'='*70}")
            print(f"Tiempo:           {elapsed_total:.1f}s")
            print(f"Nonce:            {nonce}")
            print(f"Rate (ventana):   {shares_per_sec_window:.2f} sh/s")
            print(f"Rate (promedio):  {shares_per_sec_avg:.2f} sh/s")
            print(f"Hashrate:         {hashrate_ghs:.2f} GH/s ({hashrate_mhs:.0f} MH/s)")
            print(f"Total shares:     {self.share_count}")
            print(f"{'='*70}\n")

            self.last_report_time = current_time
        else:
            print(f"[SHARE] #{self.share_count} | {nonce} | {shares_per_sec_window:.1f} sh/s")

    def send_json(self, conn, data):
        try:
            line = json.dumps(data) + '\n'
            conn.sendall(line.encode('utf-8'))
        except Exception as e:
            print(f"[ERROR] Send failed: {e}")

    def set_difficulty(self, conn, diff):
        msg = {
            "id": None,
            "method": "mining.set_difficulty",
            "params": [diff]
        }
        self.send_json(conn, msg)

    def send_job(self, conn):
        """
        Enviar trabajo en formato Stratum estándar compatible con BM1387

        mining.notify params:
        [0] job_id
        [1] prevhash (32 bytes hex, little-endian)
        [2] coinb1 (coinbase part 1)
        [3] coinb2 (coinbase part 2)
        [4] merkle_branch (array of merkle hashes)
        [5] version (4 bytes hex)
        [6] nbits (4 bytes hex - difficulty target)
        [7] ntime (4 bytes hex - unix timestamp)
        [8] clean_jobs (boolean)
        """

        self.job_counter += 1
        job_id = f"{self.job_counter:x}"

        # Timestamp actual en formato correcto (8 caracteres hex)
        ntime = format(int(time.time()), '08x')

        # Crear coinbase transaction válida
        # Formato mínimo para que el ASIC pueda procesar
        # Version (01000000) + input + output + locktime
        coinb1 = "01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff2703"
        # Height en coinbase (block 1) + extranonce placeholder
        coinb1 += "0101"

        # Coinb2: resto de coinbase + outputs
        coinb2 = "ffffffff0100f2052a01000000434104"
        coinb2 += "678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000"

        msg = {
            "params": [
                job_id,                                                                                  # job_id
                "0000000000000000000000000000000000000000000000000000000000000000",                    # prevhash
                coinb1,                                                                                 # coinb1
                coinb2,                                                                                 # coinb2
                [],                                                                                     # merkle_branch
                "20000000",                                                                             # version
                "1d00ffff",                                                                             # nbits (diff 1)
                ntime,                                                                                  # ntime
                True                                                                                    # clean_jobs
            ],
            "id": None,
            "method": "mining.notify"
        }
        self.send_json(conn, msg)

    def start(self):
        print("[INFO] Waiting for connections...\n")
        while True:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()

if __name__ == "__main__":
    server = ChimeraStratum()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[STOPPED] Server stopped")
