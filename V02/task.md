# CHIMERA Task List

- [/] **Phase IV: Hardware Deployment (Lucky Miner / Antminer)**
    - [x] **Network Configuration**
        - [x] Identify Host IP (192.168.0.14)
        - [x] Configure Bridge Bind Address (0.0.0.0)
        - [/] Open Firewall Ports (3333) - *Pending User verification*
    - [ ] **Device Provisioning**
        - [ ] Configure Lucky Miner Settings (SSID, Password, Stratum IP)
        - [ ] Reboot Device
    - [ ] **Link Verification**
        - [ ] Establish TCP Connection (Miner -> Bridge)
        - [ ] Verify Stratum Handshake (subscribe/authorize)
        - [ ] Verify Job Dispatch (Seed Injection)
        - [ ] Verify Insight Reception (Nonce Submission)
    - [ ] **System Integration**
        - [ ] Connect Bridge Output to Reservoir (`substrate.py`)
        - [ ] Run Experiment 3 (Quantum Scrambling) on Live Hardware
