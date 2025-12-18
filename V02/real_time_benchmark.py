"""
BENCHMARK EN TIEMPO REAL con archivo de log
"""
import socket, json, threading, time, sys
from collections import deque

HOST, PORT = "192.168.0.14", 3333
LOG_FILE = "benchmark_live.log"

class RTBench:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))
        self.sock.listen(1)
        self.shares = 0
        self.times = deque(maxlen=1000)
        self.start = None
        self.log = open(LOG_FILE, 'w', buffering=1)
        self.log_and_print(f"[BENCHMARK] Server started on {HOST}:{PORT}")
        self.log_and_print("[CONFIG] Difficulty = 1")
        self.log_and_print("[INFO] Waiting for miner...")
        self.log_and_print("="*60)

    def log_and_print(self, msg):
        print(msg)
        self.log.write(msg + '\n')
        self.log.flush()

    def handle(self, c, a):
        self.log_and_print(f"[CONNECTED] {a}")
        while True:
            try:
                d = c.recv(1024)
                if not d: break
                for m in d.decode().split('\n'):
                    if m: self.proc(json.loads(m), c)
            except Exception as e:
                self.log_and_print(f"[ERROR] {e}")
                break

    def proc(self, m, c):
        i, me = m.get('id'), m.get('method')
        if me == 'mining.subscribe':
            c.sendall((json.dumps({"id":i,"result":[[["mining.set_difficulty","1"],["mining.notify","1"]],"08000002",4],"error":None})+'\n').encode())
        elif me == 'mining.authorize':
            c.sendall((json.dumps({"id":i,"result":True,"error":None})+'\n').encode())
            self.log_and_print("[AUTH] Miner authorized")
            self.log_and_print("[START] Data collection started\n")
            self.start = time.time()
            c.sendall((json.dumps({"id":None,"method":"mining.set_difficulty","params":[1]})+'\n').encode())
            self.job(c)
        elif me == 'mining.submit':
            t = time.time()
            self.shares += 1
            self.times.append(t)
            c.sendall((json.dumps({"id":i,"result":True,"error":None})+'\n').encode())

            if self.start:
                elapsed = t - self.start
                avg_rate = self.shares / elapsed

                if len(self.times) >= 2:
                    window = self.times[-1] - self.times[0]
                    win_rate = len(self.times) / window if window > 0 else 0
                else:
                    win_rate = 0

                if self.shares % 10 == 0:
                    hashrate_mhs = (avg_rate * 4294967296) / 1_000_000
                    self.log_and_print(f"\n{'='*60}")
                    self.log_and_print(f"[TELEMETRIA] Share #{self.shares}")
                    self.log_and_print(f"{'='*60}")
                    self.log_and_print(f"Tiempo:           {elapsed:.1f}s")
                    self.log_and_print(f"Tasa promedio:    {avg_rate:.2f} sh/s")
                    self.log_and_print(f"Tasa ventana:     {win_rate:.2f} sh/s")
                    self.log_and_print(f"Hashrate est.:    {hashrate_mhs:.2f} MH/s")
                    self.log_and_print(f"Total shares:     {self.shares}")
                    self.log_and_print(f"{'='*60}\n")
                else:
                    self.log_and_print(f"[SHARE] #{self.shares} | {win_rate:.1f} sh/s")

                if elapsed >= 60:
                    self.log_and_print(f"\n{'#'*60}")
                    self.log_and_print("RESULTADOS FINALES DEL BENCHMARK")
                    self.log_and_print(f"{'#'*60}")
                    self.log_and_print(f"Duracion:             {elapsed:.2f}s")
                    self.log_and_print(f"Total shares:         {self.shares}")
                    self.log_and_print(f"Tasa promedio:        {avg_rate:.2f} sh/s")
                    self.log_and_print(f"Hashrate estimado:    {hashrate_mhs:.2f} MH/s")
                    self.log_and_print(f"\n--- COMPARACION ---")
                    self.log_and_print(f"Anterior (diff=1024): 0.017 sh/s (1 share/minuto)")
                    self.log_and_print(f"Actual (diff=1):      {avg_rate:.2f} sh/s")
                    self.log_and_print(f"\n*** MEJORA: {avg_rate/0.017:.1f}x MAS FLUJO DE DATOS ***")
                    self.log_and_print(f"\n--- PROYECCION ---")
                    self.log_and_print(f"Shares por minuto:    {avg_rate * 60:.0f}")
                    self.log_and_print(f"Shares por hora:      {avg_rate * 3600:.0f}")
                    self.log_and_print(f"\n--- DIAGNOSTICO ---")
                    if avg_rate > 1.0:
                        self.log_and_print("[OK] FLUJO OPTIMO - Cuello de botella ELIMINADO")
                    elif avg_rate > 0.1:
                        self.log_and_print("[WARNING] Flujo aceptable pero mejorable")
                    else:
                        self.log_and_print("[ERROR] Flujo insuficiente")
                    self.log_and_print(f"{'#'*60}\n")
                    self.log.close()
                    sys.exit(0)

            self.job(c)

    def job(self, c):
        c.sendall((json.dumps({"params":["j","0"*64,"0"*64,"0000",[],"20000000","1d00ffff",hex(int(time.time()))[2:],True],"id":None,"method":"mining.notify"})+'\n').encode())

    def run(self):
        try:
            while True:
                c, a = self.sock.accept()
                threading.Thread(target=self.handle, args=(c,a), daemon=True).start()
        except KeyboardInterrupt:
            self.log_and_print("\n[STOPPED] Benchmark interrupted")
            self.log.close()

if __name__ == "__main__":
    RTBench().run()
