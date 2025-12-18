"""
BENCHMARK RAPIDO - Muestra resultados directamente en consola
Ejecuta por 60 segundos y muestra estadisticas
"""
import socket, json, threading, time
from collections import deque

HOST, PORT = "192.168.0.14", 3333

class QuickBench:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))
        self.sock.listen(1)
        self.shares = 0
        self.times = deque(maxlen=1000)
        self.start = None
        print(f"[BENCHMARK] Listening on {HOST}:{PORT}")
        print("[INFO] Waiting for miner connection...")
        print("[CONFIG] Difficulty = 1")
        print("="*60)

    def handle(self, c, a):
        print(f"[CONNECTED] {a}")
        while True:
            try:
                d = c.recv(1024)
                if not d: break
                for m in d.decode().split('\n'):
                    if m: self.proc(json.loads(m), c)
            except: break

    def proc(self, m, c):
        i, me = m.get('id'), m.get('method')
        if me == 'mining.subscribe':
            c.sendall((json.dumps({"id":i,"result":[[["mining.set_difficulty","1"],["mining.notify","1"]],"08000002",4],"error":None})+'\n').encode())
        elif me == 'mining.authorize':
            c.sendall((json.dumps({"id":i,"result":True,"error":None})+'\n').encode())
            print("[AUTH] Miner authorized")
            print("[START] Beginning data collection...\n")
            self.start = time.time()
            c.sendall((json.dumps({"id":None,"method":"mining.set_difficulty","params":[1]})+'\n').encode())
            self.job(c)
        elif me == 'mining.submit':
            t = time.time()
            self.shares += 1
            self.times.append(t)
            c.sendall((json.dumps({"id":i,"result":True,"error":None})+'\n').encode())

            # Calculate metrics
            if self.start:
                elapsed = t - self.start
                avg_rate = self.shares / elapsed

                if len(self.times) >= 2:
                    window = self.times[-1] - self.times[0]
                    win_rate = len(self.times) / window if window > 0 else 0
                else:
                    win_rate = 0

                # Print every 10 shares
                if self.shares % 10 == 0:
                    hashrate_mhs = (avg_rate * 4294967296) / 1_000_000
                    print(f"\n{'='*60}")
                    print(f"[STATS] Share #{self.shares}")
                    print(f"{'='*60}")
                    print(f"Time elapsed:     {elapsed:.1f}s")
                    print(f"Avg rate:         {avg_rate:.2f} sh/s")
                    print(f"Window rate:      {win_rate:.2f} sh/s")
                    print(f"Est. hashrate:    {hashrate_mhs:.2f} MH/s")
                    print(f"Total shares:     {self.shares}")
                    print(f"{'='*60}\n")
                else:
                    print(f"[SHARE] #{self.shares} | {win_rate:.1f} sh/s")

                # Stop after 60s
                if elapsed >= 60:
                    print(f"\n{'#'*60}")
                    print("FINAL BENCHMARK RESULTS")
                    print(f"{'#'*60}")
                    print(f"Duration:         {elapsed:.2f}s")
                    print(f"Total shares:     {self.shares}")
                    print(f"Average rate:     {avg_rate:.2f} sh/s")
                    print(f"Est. hashrate:    {hashrate_mhs:.2f} MH/s")
                    print(f"\nCOMPARISON:")
                    print(f"Previous (diff=1024):  0.017 sh/s (1 share/min)")
                    print(f"Current (diff=1):      {avg_rate:.2f} sh/s")
                    print(f"IMPROVEMENT:           {avg_rate/0.017:.1f}x MORE DATA FLOW")
                    print(f"{'#'*60}\n")
                    exit(0)

            self.job(c)

    def job(self, c):
        c.sendall((json.dumps({"params":["job1","0"*64,"0"*64,"0000",[],"20000000","1d00ffff",hex(int(time.time()))[2:],True],"id":None,"method":"mining.notify"})+'\n').encode())

    def run(self):
        while True:
            c, a = self.sock.accept()
            threading.Thread(target=self.handle, args=(c,a), daemon=True).start()

if __name__ == "__main__":
    QuickBench().run()
