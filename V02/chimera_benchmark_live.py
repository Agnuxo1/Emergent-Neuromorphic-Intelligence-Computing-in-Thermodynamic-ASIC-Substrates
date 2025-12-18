"""
CHIMERA LIVE BENCHMARK - Monitoreo en tiempo real
Ejecuta el servidor y captura métricas directamente en memoria
"""

import socket
import json
import threading
import time
from collections import deque
from datetime import datetime

# CONFIGURACIÓN
HOST_IP = "192.168.0.14"
PORT = 3333

class ChimeraBenchmarkServer:
    def __init__(self, duration_seconds=120):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST_IP, PORT))
        self.sock.listen(1)
        self.client_conn = None
        self.current_seed = "00" * 32

        # TELEMETRÍA
        self.share_count = 0
        self.share_timestamps = deque(maxlen=1000)
        self.start_time = None
        self.last_report_time = None
        self.benchmark_duration = duration_seconds
        self.running = True

        # Almacenar todos los reportes para análisis posterior
        self.all_reports = []

        print(f"[BENCHMARK] CHIMERA iniciado en {HOST_IP}:{PORT}")
        print(f"[CONFIG] Dificultad: 1 (minima)")
        print(f"[CONFIG] Duracion: {duration_seconds} segundos")
        print(f"[INFO] Esperando conexion del minero LV06...")
        print("="*70 + "\n")

    def handle_client(self, conn, addr):
        print(f"[OK] Minero conectado desde: {addr}")
        self.client_conn = conn

        while self.running:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                messages = data.decode().split('\n')
                for msg in messages:
                    if not msg:
                        continue
                    self.process_message(json.loads(msg), conn)

            except Exception as e:
                print(f"[ERROR] {e}")
                break

        print("[INFO] Conexion cerrada")

    def process_message(self, msg, conn):
        msg_id = msg.get('id')
        method = msg.get('method')

        if method == 'mining.subscribe':
            response = {"id": msg_id, "result": [[["mining.set_difficulty", "1"], ["mining.notify", "1"]], "08000002", 4], "error": None}
            self.send_json(conn, response)

        elif method == 'mining.authorize':
            response = {"id": msg_id, "result": True, "error": None}
            self.send_json(conn, response)
            print("[AUTH] Minero autorizado")
            print("[INJECT] Enviando primera semilla con dificultad=1\n")

            self.start_time = time.time()
            self.last_report_time = self.start_time

            self.set_difficulty(conn, 1)
            self.send_job(conn)

        elif method == 'mining.submit':
            current_time = time.time()
            self.share_count += 1
            self.share_timestamps.append(current_time)

            nonce = msg['params'][4]
            self.print_telemetry(nonce)

            response = {"id": msg_id, "result": True, "error": None}
            self.send_json(conn, response)

            self.send_job(conn)

            # Detener después de la duración especificada
            if self.start_time and (current_time - self.start_time) >= self.benchmark_duration:
                print(f"\n[BENCHMARK] Tiempo completado ({self.benchmark_duration}s)")
                self.running = False
                self.generate_final_report()

    def print_telemetry(self, nonce):
        if self.start_time is None or self.last_report_time is None:
            return

        current_time = time.time()
        elapsed_total = current_time - self.start_time
        elapsed_since_report = current_time - self.last_report_time

        if len(self.share_timestamps) >= 2:
            window_duration = self.share_timestamps[-1] - self.share_timestamps[0]
            shares_per_sec_window = len(self.share_timestamps) / window_duration if window_duration > 0 else 0
        else:
            shares_per_sec_window = 0

        shares_per_sec_avg = self.share_count / elapsed_total if elapsed_total > 0 else 0

        # Guardar datos para análisis
        report_data = {
            'timestamp': current_time,
            'share_num': self.share_count,
            'elapsed': elapsed_total,
            'window_rate': shares_per_sec_window,
            'avg_rate': shares_per_sec_avg,
            'nonce': nonce
        }

        if elapsed_since_report >= 5.0 or self.share_count % 10 == 0:
            self.all_reports.append(report_data)

            print(f"\n{'='*70}")
            print(f"[TELEMETRIA] Share #{self.share_count}")
            print(f"{'='*70}")
            print(f"Tiempo transcurrido: {elapsed_total:.2f}s")
            print(f"Nonce: {nonce}")
            print(f"Shares/s (ventana): {shares_per_sec_window:.2f}")
            print(f"Shares/s (promedio): {shares_per_sec_avg:.2f}")
            print(f"Total shares: {self.share_count}")

            estimated_hashrate_mhs = (shares_per_sec_avg * 4294967296) / 1_000_000
            print(f"Hashrate estimado: {estimated_hashrate_mhs:.2f} MH/s")
            print(f"{'='*70}\n")

            self.last_report_time = current_time
        else:
            print(f"[SHARE] #{self.share_count} | {nonce} | {shares_per_sec_window:.1f} sh/s")

    def generate_final_report(self):
        """Genera reporte final del benchmark"""
        print("\n" + "="*70)
        print("REPORTE FINAL DEL BENCHMARK")
        print("="*70)

        if not self.all_reports:
            print("[ERROR] No hay datos suficientes para generar reporte")
            return

        last = self.all_reports[-1]

        print(f"\nDuracion total: {last['elapsed']:.2f} segundos")
        print(f"Total de shares recibidos: {last['share_num']}")
        print(f"Tasa promedio: {last['avg_rate']:.2f} shares/segundo")
        print(f"Hashrate estimado: {(last['avg_rate'] * 4294967296 / 1_000_000):.2f} MH/s")

        print(f"\n{'='*70}")
        print("COMPARACION CON CONFIGURACION ANTERIOR")
        print(f"{'='*70}")
        print("Configuracion anterior (diff=1024): ~0.017 shares/s (1 share/min)")
        print(f"Configuracion actual (diff=1):     {last['avg_rate']:.2f} shares/s")

        if last['avg_rate'] > 0:
            improvement = last['avg_rate'] / 0.017
            print(f"\nMEJORA: {improvement:.1f}x mas flujo de datos")

        print(f"\n{'='*70}")
        print("PROYECCION")
        print(f"{'='*70}")
        print(f"Shares por minuto: {last['avg_rate'] * 60:.0f}")
        print(f"Shares por hora: {last['avg_rate'] * 3600:.0f}")

        print(f"\n{'='*70}")
        print("DIAGNOSTICO")
        print(f"{'='*70}")
        if last['avg_rate'] > 1.0:
            print("[OK] Flujo de entropia OPTIMO para CHIMERA")
            print("[OK] El cuello de botella ha sido ELIMINADO")
        elif last['avg_rate'] > 0.1:
            print("[WARNING] Flujo aceptable pero mejorable")
        else:
            print("[ERROR] Flujo insuficiente")

        print("="*70 + "\n")

        # Guardar reporte a archivo
        with open('benchmark_results.txt', 'w') as f:
            f.write(f"CHIMERA BENCHMARK RESULTS\n")
            f.write(f"{'='*70}\n")
            f.write(f"Fecha: {datetime.now()}\n")
            f.write(f"Duracion: {last['elapsed']:.2f}s\n")
            f.write(f"Total shares: {last['share_num']}\n")
            f.write(f"Tasa promedio: {last['avg_rate']:.2f} sh/s\n")
            f.write(f"Mejora vs diff=1024: {last['avg_rate'] / 0.017:.1f}x\n")

        print("[INFO] Resultados guardados en benchmark_results.txt")

    def send_json(self, conn, data):
        line = json.dumps(data) + '\n'
        conn.sendall(line.encode())

    def set_difficulty(self, conn, diff):
        msg = {"id": None, "method": "mining.set_difficulty", "params": [diff]}
        self.send_json(conn, msg)

    def send_job(self, conn):
        job_id = "chimera_thought"
        coinbase = self.current_seed

        msg = {
            "params": [
                job_id,
                "0000000000000000000000000000000000000000000000000000000000000000",
                coinbase,
                "0000",
                [],
                "20000000",
                "1d00ffff",
                hex(int(time.time()))[2:],
                True
            ],
            "id": None,
            "method": "mining.notify"
        }
        self.send_json(conn, msg)

    def start(self):
        while self.running:
            try:
                self.sock.settimeout(1.0)
                conn, addr = self.sock.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"[ERROR] {e}")
                break

        print("[INFO] Servidor detenido")
        self.sock.close()

if __name__ == "__main__":
    # Ejecutar benchmark por 90 segundos
    server = ChimeraBenchmarkServer(duration_seconds=90)
    server.start()
