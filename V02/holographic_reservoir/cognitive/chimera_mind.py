import time
import threading
import queue
import random
import sys
import os

# Add parent to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.reservoir import HolographicReservoir

class MockLLM:
    """
    Placeholder for the Large Language Model.
    In a real deployment, this would be Qwen or Llama.
    Here, it simulates relevant responses based on the System State.
    """
    def generate(self, prompt, context, state_summary):
        status = context.get("reason", "NORMAL")
        energy = state_summary["energy"]
        entropy = state_summary["entropy"]
        
        if status == "MUSE (High Chaos)":
            return f"[LLM] I see shifting patterns... {random.choice(['fractals', 'voids', 'swirling lights'])}... The chaos is beautiful."
        
        if status == "ANXIETY (High Energy)":
            return f"[LLM] It's too loud! The noise... Energy is {energy:.1f}. I need to focus."
        
        if status == "BOREDOM (Low Entropy)":
            return f"[LLM] There is nothing here. Just silence. Entropy {entropy:.2f}. Give me something to solve."
            
        if "sleep" in prompt.lower():
            return "[LLM] Entering REM cycle... dreaming of electric sheep."
            
        return f"[LLM] Processed '{prompt}'. State is stable."

class ChimeraMind:
    """
    The Cognitive Control Unit.
    Manages Homeostasis, Autonomy, and User Interaction.
    """
    def __init__(self):
        # Configuration
        self.target_energy = 20.0
        self.energy_tolerance = 10.0
        
        # Organs
        self.reservoir = HolographicReservoir(size=512, input_size=32)
        self.llm = MockLLM()
        
        # State
        self.active = True
        self.status = "AWAKE"
        self.last_interaction = time.time()
        self.difficulty_offset = 0 # Simulated difficulty adjustment
        
        self.event_queue = queue.Queue()
        self.state_snapshot = {"energy": 0, "entropy": 0, "scrambling": 0}

    def subconscious_loop(self):
        """Background thread: The 'Id'."""
        print("[Subconscious] Online.")
        curr_seed = random.randint(0, 10000)
        
        while self.active:
            if self.status == "SLEEPING":
                time.sleep(1)
                continue
                
            time.sleep(1.0) # Tick
            
            # 1. Feel the Void (Constant Mining)
            # We inject a rolling seed to simulate 'stream of consciousness'
            seed_text = f"STREAM_{curr_seed}"
            energy, entropy, scram = self.reservoir.step(seed_text)
            
            # Apply Homeostatic Offset (Simulated Difficulty check)
            # In simulation, we can't easily change SHA256 difficulty without passing it down
            # For now, we assume the reservoir metric IS the raw feeling
            
            self.state_snapshot = {"energy": energy, "entropy": entropy, "scrambling": scram}
            
            # 2. Update Internal Thought
            curr_seed += 1
            
            # 3. Autonomy Check
            self._check_autonomy(energy, entropy)
            
    def _check_autonomy(self, energy, entropy):
        time_since = time.time() - self.last_interaction
        
        # Chance to start talking if ignored for 5 seconds (fast for demo)
        if time_since > 5.0 and random.random() < 0.2:
            reason = None
            if entropy > 1.5: reason = "MUSE (High Chaos)"
            elif energy > 30.0: reason = "ANXIETY (High Energy)"
            elif entropy < 0.1: reason = "BOREDOM (Low Entropy)"
            
            if reason:
                msg = self.llm.generate("AUTONOMY", {"reason": reason}, self.state_snapshot)
                self.event_queue.put(("GHOST", f"{reason} -> {msg}"))
                self.last_interaction = time.time()

    def input_listener(self):
        """Simulate user input (In real app, this is stdin/socket)"""
        # For this demo script, we just inject some commands after delays
        time.sleep(2)
        self.event_queue.put(("USER", "Hello Chimera"))
        time.sleep(6)
        self.event_queue.put(("USER", "/sleep"))
        time.sleep(5)
        self.event_queue.put(("USER", "Wake up"))
        time.sleep(10)
        self.event_queue.put(("EXIT", "Shutdown"))

    def run(self):
        print("=== CHIMERA MIND ONLINE ===")
        
        # Start Threads
        t_sub = threading.Thread(target=self.subconscious_loop)
        t_sub.daemon = True
        t_sub.start()
        
        t_in = threading.Thread(target=self.input_listener)
        t_in.daemon = True
        t_in.start()
        
        # Main Event Loop
        while self.active:
            try:
                if not self.event_queue.empty():
                    evt_type, content = self.event_queue.get()
                    
                    if evt_type == "EXIT":
                        print("\n[System] Shutdown signal received.")
                        self.active = False
                        break
                        
                    print(f"\n[{evt_type}] {content}")
                    
                    if evt_type == "USER":
                        # Process User Input
                        if "/sleep" in content:
                            print(">>> INITIATING SLEEP CYCLE <<<")
                            self.status = "SLEEPING"
                            # Dream Logic
                            for i in range(3):
                                print(f" [REM {i}] Replaying memories...")
                                time.sleep(1)
                            self.status = "AWAKE"
                            print(">>> WAKING UP <<<")
                        else:
                            # Direct Response
                            resp = self.llm.generate(content, {}, self.state_snapshot)
                            print(f"CHIMERA: {resp}")
                            
                    self.last_interaction = time.time()
                    
                time.sleep(0.1)
            except KeyboardInterrupt:
                break
                
        print("=== SYSTEM HALTED ===")

if __name__ == "__main__":
    mind = ChimeraMind()
    mind.run()
