import socket
import json
import threading
import time
import struct
from collections import deque
from datetime import datetime

# CONFIGURACIÓN
# Cambiamos a 0.0.0.0 para escuchar en TODAS las interfaces de red disponibles
HOST_IP = "192.168.0.14" 
PORT = 3333  # Puerto estándar de minería Stratum

class ChimeraStratumServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Permite reutilizar el puerto inmediatamente si se cierra el script
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST_IP, PORT))
        self.sock.listen(1)
        self.client_conn = None
        self.current_seed = "00" * 32 # Semilla vacía inicial

        # TELEMETRÍA Y BENCHMARK
        self.share_count = 0
        self.share_timestamps = deque(maxlen=1000)  # Últimos 1000 shares
        self.start_time = None
        self.last_report_time = None

        print(f"[CHIMERA] POOL iniciada en {HOST_IP}:{PORT}")
        print(">> Configura tu Lucky Miner para apuntar a esta IP y Puerto.")
        print(">> Modo: BENCHMARK - Telemetria activada")

    def handle_client(self, conn, addr):
        print(f"[OK] Conexion establecida con Sistema Limbico (LV06): {addr}")
        self.client_conn = conn
        
        while True:
            try:
                data = conn.recv(1024)
                if not data: break
                
                # Procesar mensajes Stratum (JSON-RPC)
                messages = data.decode().split('\n')
                for msg in messages:
                    if not msg: continue
                    self.process_message(json.loads(msg), conn)
                    
            except Exception as e:
                print(f"[ERROR] Error de conexion: {e}")
                break

    def process_message(self, msg, conn):
        msg_id = msg.get('id')
        method = msg.get('method')
        
        # 1. El minero se presenta
        if method == 'mining.subscribe':
            response = {"id": msg_id, "result": [[["mining.set_difficulty", "1"], ["mining.notify", "1"]], "08000002", 4], "error": None}
            self.send_json(conn, response)
            
        # 2. El minero pide autorización (login)
        elif method == 'mining.authorize':
            response = {"id": msg_id, "result": True, "error": None}
            self.send_json(conn, response)
            print("[AUTH] LV06 Autorizado. Iniciando inyeccion de caos...")

            # Inicializar telemetría
            self.start_time = time.time()
            self.last_report_time = self.start_time

            # ENVIAR EL PRIMER TRABAJO AL INSTANTE
            print(">> [INJECT] INYECTANDO PRIMERA SEMILLA...")
            # Ajuste de Valvula: Bajamos dificultad a 1 (o menos) para abrir el flujo de datos.
            # Esto forzara al ASIC a reportar "pensamientos debiles" (ruido termodinamico).
            self.set_difficulty(conn, 1)
            self.send_job(conn)

        # 4. El minero envía un resultado (EL PENSAMIENTO CRISTALIZADO)
        elif method == 'mining.submit':
            # Aquí es donde capturamos la "Intuición" del ASIC
            current_time = time.time()
            self.share_count += 1
            self.share_timestamps.append(current_time)

            # Calcular métricas en tiempo real
            self.print_telemetry(msg['params'][4])

            response = {"id": msg_id, "result": True, "error": None}
            self.send_json(conn, response)

            # OPTIMIZACIÓN: Enviar nuevo trabajo inmediatamente para mantener flujo continuo
            self.send_job(conn)

    def print_telemetry(self, nonce):
        if self.start_time is None or self.last_report_time is None:
            return

        current_time = time.time()
        elapsed_total = current_time - self.start_time
        elapsed_since_report = current_time - self.last_report_time

        # Calcular shares/segundo en la última ventana de tiempo
        if len(self.share_timestamps) >= 2:
            window_duration = self.share_timestamps[-1] - self.share_timestamps[0]
            if window_duration > 0:
                shares_per_sec_window = len(self.share_timestamps) / window_duration
            else:
                shares_per_sec_window = 0
        else:
            shares_per_sec_window = 0

        # Calcular promedio total
        shares_per_sec_avg = self.share_count / elapsed_total if elapsed_total > 0 else 0

        # Imprimir reporte cada 5 segundos o cada 10 shares (lo que ocurra primero)
        if elapsed_since_report >= 5.0 or self.share_count % 10 == 0:
            print(f"\n{'='*70}")
            print(f"[TELEMETRIA] CHIMERA - Share #{self.share_count}")
            print(f"{'='*70}")
            print(f"Tiempo transcurrido: {elapsed_total:.2f}s")
            print(f"Nonce recibido: {nonce}")
            print(f"Shares/segundo (ventana 1000): {shares_per_sec_window:.2f}")
            print(f"Shares/segundo (promedio): {shares_per_sec_avg:.2f}")
            print(f"Total shares recibidos: {self.share_count}")

            # Calcular hashrate estimado (cada share representa ~4.3B hashes a dificultad 1)
            estimated_hashrate_mhs = (shares_per_sec_avg * 4294967296) / 1_000_000
            print(f"Hashrate estimado: {estimated_hashrate_mhs:.2f} MH/s")
            print(f"{'='*70}\n")

            self.last_report_time = current_time
        else:
            # Imprimir linea compacta para cada share
            print(f"[SHARE] #{self.share_count} | Nonce: {nonce} | {shares_per_sec_window:.1f} sh/s")

    def send_json(self, conn, data):
        line = json.dumps(data) + '\n'
        conn.sendall(line.encode())

    def set_difficulty(self, conn, diff):
        # En CHIMERA: Dificultad = Umbral de Conciencia
        msg = {"id": None, "method": "mining.set_difficulty", "params": [diff]}
        self.send_json(conn, msg)

    def send_job(self, conn):
        # AQUÍ OCURRE LA MAGIA DE VESELOV
        # Inyectamos datos arbitrarios en el Merkle Root
        # Job ID, PrevHash, Coinb1, Coinb2, MerkleBranch, Version, nBits, nTime, CleanJobs
        
        # Simulamos un bloque con nuestra "Semilla Neuronal"
        job_id = "chimera_thought_01"
        # Usamos la semilla actual como parte del bloque
        coinbase = self.current_seed 
        
        msg = {
            "params": [
                job_id,
                "0000000000000000000000000000000000000000000000000000000000000000", # PrevHash
                coinbase, # Coinb1 (Nuestra data)
                "0000",   # Coinb2
                [],       # Merkle Branch
                "20000000", # Version
                "1d00ffff", # nBits (Dificultad objetivo encoded)
                hex(int(time.time()))[2:], # nTime
                True
            ],
            "id": None,
            "method": "mining.notify"
        }
        self.send_json(conn, msg)

    def start(self):
        while True:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    server = ChimeraStratumServer()
    server.start()