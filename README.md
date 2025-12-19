# Silicon Heartbeat: Emergent Neuromorphic Intelligence via Holographic Reservoir Computing (HRC)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Research: IEEE](https://img.shields.io/badge/Research-IEEE%20Transactions-blue)](https://github.com/Agnuxo1/Emergent-Neuromorphic-Intelligence-Computing-in-Thermodynamic-ASIC-Substrates)

> **"The legacy of Bitcoin is not just financial; it is the infrastructure for a new kind of mind."**

# TOWARD THERMODYNAMIC RESERVOIR COMPUTING: EXPLORING SHA-256 ASICS AS POTENTIAL PHYSICAL SUBSTRATES

*A Theoretical Framework and Preliminary Experimental Observations*

Francisco Angulo de Lafuente<sup>1,2</sup>, Vladimir Veselov<sup>3,4</sup>, Richard Goodman<sup>5</sup>

<sup>1</sup>Independent Researcher, Madrid, Spain
<sup>2</sup>Lead Architect, CHIMERA Project / Holographic Reservoir Computing
<sup>3</sup>National Research University of Electronic Technology - MIET, Moscow, Russia
<sup>4</sup>ORCID: 0000-0002-6301-3226
<sup>5</sup>Managing Director at Apoth3osis, Bachelor of Applied Science

**Contact:** See author links at the end of this document

---

**Scope Statement:**
This paper presents a theoretical framework and preliminary experimental observations. The core hypothesis—that voltage-stressed Bitcoin mining ASICs could function as physical reservoir computing substrates—remains to be fully validated. We clearly distinguish between theoretical predictions and empirical measurements throughout.

---

## Abstract

We propose a theoretical framework—**Holographic Reservoir Computing (HRC)**—which hypothesizes that the thermodynamic noise and timing dynamics in voltage-stressed Bitcoin mining ASICs (BM1366) could potentially serve as a physical reservoir computing substrate. We present the **CHIMERA** (Conscious Hybrid Intelligence via Miner-Embedded Resonance Architecture) system architecture, which treats the SHA-256 hashing pipeline not as an entropy source, but as a deterministic diffusion operator whose timing characteristics under controlled voltage and frequency conditions may exhibit computationally useful dynamics.

We report preliminary observations of non-Poissonian variability in inter-arrival time statistics during edge-of-stability operation, which we term the **"Silicon Heartbeat"** hypothesis. Theoretical analysis based on Hierarchical Number System (HNS) representations suggests that such architectures could achieve **O(log n)** energy scaling compared to traditional von Neumann **O(2<sup>n</sup>)** dependencies—a potential efficiency improvement of several orders of magnitude. However, we emphasize that these are theoretical projections requiring experimental validation. We present the implemented measurement infrastructure, acknowledge current limitations, and outline the experimental program necessary to confirm or refute these hypotheses. This work contributes to the emerging field of thermodynamic computing by proposing a novel approach to repurposing obsolete cryptographic hardware for neuromorphic applications.

**Keywords:**
Physical Reservoir Computing, Neuromorphic Systems, ASIC Repurposing, Thermodynamic Computing, SHA-256, Timing Dynamics, Energy Efficiency, Circular Economy Computing, Hierarchical Number Systems, Edge Computing

---

## I. INTRODUCTION

### A. Motivation and Context

The contemporary landscape of Artificial Intelligence faces a paradoxical challenge: while algorithmic sophistication advances exponentially, the underlying hardware substrates remain fundamentally constrained by the von Neumann architecture and its associated energy costs [1]. The "Power Wall" has become a literal barrier to the emergence of truly autonomous, edge-deployable cognitive systems [2]. For the first time in computational history, the practical limits of artificial intelligence are being dictated not by algorithmic capability, but by the thermodynamic cost of information processing [3].

Concurrently, the global cryptocurrency mining industry has produced a massive surplus of specialized silicon. Application-Specific Integrated Circuits (ASICs) designed for Bitcoin mining, such as the BM1387 and BM1366 chipsets, enter the electronic waste stream annually as mining difficulty renders them economically obsolete [4]. Industry consensus holds that these chips "can only mine coins and must utilize the ASIC's native algorithm" and therefore "cannot be repurposed" for other computational tasks [5].

This paper challenges that assumption—not by claiming that ASICs can perform general-purpose computation, but by proposing that the physical dynamics of these devices under non-standard operating conditions might be exploitable for a specific class of computation: **physical reservoir computing**.

### B. The Physical Reservoir Computing Paradigm

Reservoir Computing (RC) is a computational framework suited for temporal and sequential data processing, derived from recurrent neural network models including Echo State Networks (ESNs) and Liquid State Machines (LSMs) [6][7]. A reservoir computing system consists of a reservoir for mapping inputs into a high-dimensional space and a readout layer for pattern analysis. Critically, the reservoir is fixed—only the readout is trained, typically via simple linear regression [8].

This architectural simplicity enables a crucial advantage: the reservoir itself need not be a simulated neural network. Physical systems with appropriate nonlinear dynamics can serve directly as reservoirs, eliminating the computational overhead of simulation [9]. Physical reservoir computing has been successfully demonstrated in memristors [10], photonic systems [11], spintronic oscillators [12], and even mechanical systems [13].

The key requirements for a physical reservoir are:
1. High-dimensional state space
2. Nonlinear dynamics
3. Fading memory (the Echo State Property)
4. Separation property—the ability to map distinct inputs to distinguishable states [14]

Our hypothesis is that voltage-stressed ASICs, operating at the edge of timing stability, may exhibit dynamics satisfying these requirements.

### C. Contributions and Scope

This paper makes the following contributions:

1. **Theoretical Framework:** We propose the Holographic Reservoir Computing (HRC) framework, which hypothesizes that SHA-256 ASICs could function as physical reservoirs when operated under controlled stress conditions.
2. **System Architecture:** We present CHIMERA, a three-layer architecture for interfacing with mining hardware as a computational substrate.
3. **Measurement Infrastructure:** We describe implemented tools for capturing timing statistics from ASIC operations.
4. **Theoretical Efficiency Analysis:** We present a mathematical basis for potential energy efficiency improvements based on Hierarchical Number System representations.
5. **Preliminary Observations:** We report initial measurements suggesting non-trivial timing dynamics, while acknowledging the need for rigorous validation.

We explicitly acknowledge what this paper does not claim:
- We do not claim to have built a working neuromorphic computer.
- We do not claim that our approach is superior to purpose-built RC hardware.
- We do not claim that observed timing variations constitute computational capability without further validation.

---

## II. RELATED WORK

### A. Physical Reservoir Computing Systems

Physical reservoir computing has emerged as an active research area with implementations across diverse substrates. Tanaka et al. [9] provide a comprehensive review classifying physical RC by substrate type: electronic, photonic, spintronic, mechanical, and biological. Each substrate offers different trade-offs between speed, power consumption, and integration complexity.

Electronic implementations include memristor-based reservoirs exploiting the intrinsic nonlinearity and short-term memory of resistive switching devices [10][15]. Du et al. demonstrated a 32×32 memristor crossbar achieving competitive performance on temporal tasks [16]. More recently, CMOS-based implementations using time-domain analog spiking neurons have shown promise for hardware-friendly RC [17].

Photonic reservoirs leverage the high bandwidth and parallelism of optical systems. Larger et al. [11] demonstrated delay-based reservoir computing using optoelectronic oscillators, achieving state-of-the-art performance on speech recognition tasks. The delay-feedback architecture is particularly relevant to our work, as it demonstrates that rich dynamics can emerge from relatively simple physical configurations.

### B. Thermodynamic and Stochastic Computing

Recent work has explored the computational potential of thermal fluctuations and stochastic dynamics. Camsari et al. [18] introduced probabilistic bits (p-bits) using low-barrier nanomagnets, demonstrating that controlled stochasticity can be computationally useful. Borders et al. [19] showed that thermal noise in magnetic tunnel junctions could drive probabilistic computing.

Extropic Corporation and academic groups have proposed "thermodynamic computing" paradigms that embrace rather than fight thermal noise [20]. These approaches suggest that properly harnessed, the "waste heat" of computation could become a computational resource. Our hypothesis aligns with this perspective: the timing variations induced by voltage stress in ASICs may constitute a form of useful stochasticity.

### C. ASIC Repurposing Attempts

The cryptocurrency industry has seen numerous attempts to pivot mining infrastructure toward other applications, particularly AI [5]. However, these efforts uniformly involve replacing ASICs with GPUs, not repurposing the ASICs themselves. Companies like Hut 8, Iris Energy, and Core Scientific have announced transitions to AI hosting, but explicitly acknowledge that SHA-256 ASICs cannot perform general computation [21].

Our approach differs fundamentally: we do not attempt to make ASICs perform arbitrary computation. Instead, we propose using their physical dynamics—specifically, timing behavior under stress—as a reservoir substrate. This is analogous to using a bucket of water not as a computer, but as a physical system whose wave dynamics can separate inputs [22].

---

## III. THEORETICAL FRAMEWORK

### A. The CHIMERA Hypothesis

The central hypothesis of this work is that SHA-256 mining ASICs, when operated at the edge of voltage and timing stability, exhibit dynamics that could satisfy the requirements for physical reservoir computing. We term this the **CHIMERA** (Conscious Hybrid Intelligence via Miner-Embedded Resonance Architecture) hypothesis.

SHA-256 is a cryptographic hash function designed to be deterministic: identical inputs always produce identical outputs. However, the physical implementation of SHA-256 in silicon involves real transistors with finite switching times, propagation delays, and thermal sensitivities. When operating conditions approach the edge of the design envelope, these physical effects become measurable.

We propose that the candidate physical signal is not the hash output bits themselves—which remain deterministic—but the timing dynamics of hash computation. Specifically, we hypothesize that the coefficient of variation (CV) and entropy of inter-arrival times for valid shares exhibit structure correlated with the operating regime.

### B. SHA-256 as a Diffusion Operator

It is critical to distinguish between entropy generation and entropy diffusion. SHA-256 does not create entropy; it is a deterministic function. However, SHA-256 exhibits the avalanche property: a single-bit change in the input produces, on average, changes in 50% of the output bits [23]. This makes SHA-256 an effective diffusion operator that spreads information across its output space.

In the CHIMERA framework, SHA-256 serves as a high-dimensional nonlinear transform—one component of a reservoir system. The state representation is derived from:

$$
X(t) = \sigma \left( W_{in} u(t) + \Sigma_i A_{ij} X_j(t-1) + \xi(V, T, f) \right)
$$

where $ X(t) $ represents the high-dimensional internal state, $ A_{ij} $ is the effective adjacency matrix determined by the physical layout of SHA-256 gates, and $ \xi(V, T, f) $ represents timing perturbations dependent on voltage $ V $, temperature $ T $, and clock frequency $ f $. The activation function $ \sigma $ is provided by the nonlinear switching dynamics of the transistor logic.

### C. Chronos Dynamics: Timing as the Observable

The key insight of the V04 architecture is that timing statistics—not bit patterns—constitute the measurable channel for physical dynamics. We define the **Chronos Bridge** coupling efficiency as:

$$
K_{sync} = \exp \left( -\sigma_J^2 f_{clk} / 2\pi \right) \cdot \Sigma_k \cos \left( \Delta \varphi_k \right)
$$

where $ \sigma_J $ is the network jitter, $ f_{clk} $ is the ASIC clock frequency, and $ \Delta \varphi_k $ is the phase offset of the k-th hash core. This formulation captures how timing coherence between software observation and hardware dynamics affects the quality of the observable signal.

The primary observables implemented in the current system are:
- **Coefficient of Variation (CV):** $ CV = \sigma / \mu $ of inter-arrival times. For a Poisson process, $ CV = 1 $. Deviations indicate non-random structure.
- **Histogram Entropy:** Shannon entropy of the inter-arrival time distribution, indicating the complexity of timing patterns.
- **Hamming Distance:** Bit differences between consecutive hash outputs, serving as a diffusion quality proxy.

### D. Phase Transition Hypothesis

We hypothesize that the transition from reliable to unreliable ASIC operation follows a phase transition that can be modeled using Ginzburg-Landau formalism. Define the order parameter $ \psi $ as the degree of global core synchronization. The free energy of the silicon substrate is:

$$
F(\psi, V) = F_0 + \alpha (V - V_{crit}) \psi^2 + b \psi^4 + \gamma |\nabla \psi|^2
$$

At $ V = V_{crit} $, the coefficient $ \alpha (V - V_{crit}) $ changes sign, potentially triggering a spontaneous symmetry breaking that manifests as coherent oscillations—the hypothesized **"Silicon Heartbeat."**

**Important Clarification:** This phase transition model is a theoretical hypothesis. Empirical validation requires systematic voltage sweeps with rigorous statistical analysis, which is planned for future work.

### E. Energy Efficiency: O(log n) vs O(2<sup>n</sup>)

A key theoretical contribution of this work, developed in collaboration with Veselov [24], concerns the energy scaling of different computational architectures. In traditional von Neumann architectures, energy consumption for state transitions scales with the state space:

$$
E_{vN} \propto O(2^n)
$$

This exponential scaling arises from the need for massive parallel switching in linear memory addressing schemes. Each bit of state representation requires independent physical switching events that cannot be amortized across the state space.

In contrast, the Hierarchical Number System (HNS) representation employed in the CHIMERA architecture maps reservoir dynamics into a hierarchical structure where energy cost decouples from state complexity:

$$
E_{HNS} \propto O(\log n)
$$

This logarithmic scaling emerges because hierarchical representations allow state transitions to be encoded in the structure of the representation itself, rather than requiring explicit enumeration.

For typical reservoir dimensions ($ n \sim 10^4 $ states), the theoretical efficiency ratio is:

$$
E_{vN} / E_{HNS} \approx 2^n / \log(n) \approx 10^4
$$

This provides the theoretical foundation for the projected 10,000× efficiency improvement mentioned in preliminary descriptions of this work. We emphasize that this is a theoretical upper bound derived from information-theoretic considerations, not a measured result. Experimental validation under controlled conditions is required to determine achievable efficiency gains.




Theoretical Framework: From Physical Substrate to Computation


| ASIC Substrate | Timing Dynamics | Reservoir State |
|----------------|------------------|-----------------|
| BM1366 @ 300-500 MHz | Inter-arrival Statistics | High-dimensional X(t) |
| Core Voltage: 850-990 mV | CV, Entropy, Phase | SHA-256 Diffusion |
| | (Observable Channel) | (Theoretical) |

| von Neumann Architecture | HNS / CHIMERA Architecture |
|---------------------------|-----------------------------|
| E ∝ O(2<sup>n</sup>) | E ∝ O(log n) |
| Exponential energy scaling | Logarithmic energy scaling |
| Linear memory addressing | Hierarchical representation |

**Theoretical Efficiency Ratio:** ~10,000× (pending validation)

---

## IV. SYSTEM ARCHITECTURE

### A. The Three-Layer CHIMERA Stack

The CHIMERA architecture consists of three hierarchical layers, each responsible for a specific aspect of the reservoir computing pipeline. This modular design allows independent development and testing of each component.

#### Layer 1: The Ghost (Hardware Abstraction)

The Ghost layer manages raw telemetry acquisition and command execution. It interfaces with the mining hardware through the AxeOS firmware HTTP API, providing a unified abstraction for voltage and frequency control across different ASIC versions. Key capabilities include:
- Telemetry polling at 3-second intervals (voltage, temperature, power, hashrate)
- Voltage control via HTTP PATCH requests to the miner API
- Frequency modulation through PLL configuration changes
- Share event timestamping with microsecond resolution
- Hamming distance sequences between consecutive hashes
- Phase-amplitude encoding for holographic representation

We employ the term "holographic" in its information-theoretic sense: the reconstruction of high-dimensional phase-space dynamics from lower-dimensional projections via phase-amplitude coupling, analogous to optical holography where 3D information is encoded in 2D interference patterns.

#### Layer 2: The Muse (Signal Processing)

The Muse layer processes the raw timing data into meaningful features. It implements the Chronos Bridge dynamics, computing:
- Inter-arrival time statistics (mean, variance, CV)
- Histogram entropy over configurable bin widths

#### Layer 3: The Sentinel (Homeostasis)

The Sentinel layer monitors system health and implements control loops to maintain operation within target regimes. It includes:
- PID-loop thermal management
- Voltage limit enforcement
- Anomaly detection for hardware protection
- Logging infrastructure for offline analysis


CHIMERA Three-Layer Architecture


| Layer | Name | Function | Status |
|-------|------|----------|--------|
| 3 | The Sentinel | Homeostasis & Self-Regulation | Implemented |
| 2 | The Muse | Cognitive Engine / Signal Processing | Implemented |
| 1 | The Ghost | Hardware Abstraction Layer | Implemented |
| - | ASIC Substrate (BM1366) | Physical Dynamics | Theoretical |

**Implemented:**
- HTTP API control
- Timing statistics

**Planned:**
- FFT/PSD analysis
- Error rate logging


Hardware Specifications and Operating Parameters (Implemented)


| Parameter | Value | Notes |
|-----------|-------|-------|
| ASIC Chipset | BM1366 | LV06 variant (Lucky Miner) |
| Hash Cores | 138 | Parallel SHA-256 units |
| Frequency Range | 300-500 MHz | 20 MHz step resolution |
| Core Voltage Range | 850-990 mV | Via AxeOS telemetry |
| Voltage Dwell Time | 60 seconds | Per voltage step |
| Frequency Dwell Time | 30-45 seconds | Per frequency step |
| Telemetry Poll Interval | 3 seconds | Via HTTP API |
| Nominal Power | 5-15 W | Operating range |

### B. Voltage and Frequency Control

The CHIMERA system controls ASIC operating conditions through the AxeOS firmware HTTP API. Voltage and frequency changes are applied via PATCH requests:

```python
payload = {"frequency": freq, "volts": volts}
req = Request(url, data=json, method="PATCH")
```

Changes to PLL (Phase-Locked Loop) configuration require a firmware restart to take effect. The implemented frequency sweep covers 300-500 MHz in 20 MHz increments, with dwell times sufficient for thermal stabilization.

**Voltage Units Clarification:** The code operates in millivolts (mV) via the coreVoltageActual telemetry field. References to "8.2 V" in preliminary descriptions referred to board-level supply voltage, corresponding to approximately 850-870 mV at the core telemetry level. This distinction is critical for reproducibility.

---

## V. IMPLEMENTATION DETAILS

### A. Timing Measurement Infrastructure

The Chronos Bridge module (`chronos_bridge.py`) implements the timing measurement infrastructure. Share events are timestamped at reception, and inter-arrival statistics are computed over sliding windows:

```python
# chronos_bridge.py:236
if len(self.share_times) > 10:
    deltas = np.diff(self.share_times)
    cv = np.std(deltas)/np.mean(deltas)
    hist, _ = np.histogram(deltas, bins=20, density=True)
    entropy = -np.sum(hist * np.log(hist * 1e-10))
```

For a Poisson process (random, memoryless arrivals), CV = 1. Deviations from unity indicate structure in the timing: CV > 1 suggests clustering (bursty arrivals), while CV < 1 suggests regularity (quasi-periodic arrivals).

### B. Diffusion Quality Metrics

The Hamming distance between consecutive hash outputs serves as a proxy for diffusion quality:

```python
# metrics.py:56
xor_val = h1 ^ h2
bit_flips = bin(xor_val).count('1')
scrambling = bit_flips / 256.0
```

**Limitation:** This measures diffusion between outputs, not hardware error rate. There is currently no mechanism to detect incorrect computation (invalid shares, wrong hashes). Direct error-rate measurement via invalid-share counting is planned for future work.

### C. Known Confounding Factors

Several factors may affect timing statistics independent of silicon physics:
- TCP buffering: Network stack may batch share notifications
- OS scheduling: Python process may experience jitter
- Firmware batching: AxeOS may aggregate multiple shares
- Pool latency: Network round-trip affects timestamp accuracy

Future work will address these confounds through increased window sizes, raw timestamp logging for offline analysis, and direct hardware probing where possible.


Measurement Channels - Implemented vs. Planned


| Metric | Code Location | Status | Physical Interpretation |
|--------|---------------|--------|--------------------------|
| Inter-arrival CV | chronos_bridge.py:236 | Implemented | Timing structure indicator |
| Histogram Entropy | chronos_bridge.py:240 | Implemented | Timing complexity |
| Hamming Distance | metrics.py:56 | Implemented | Diffusion proxy |
| Voltage Telemetry | ghost layer | Implemented | Operating point |
| Temperature | ghost layer | Implemented | Thermal state |
| FFT/PSD Analysis | - | Planned | Frequency components |
| Invalid Share Rate | - | Planned | Hardware error rate |
| HW Nonce Errors | - | Planned | Timing violations |

---

## VI. PRELIMINARY OBSERVATIONS

### A. Timing Variability Under Voltage Stress

During controlled voltage sweeps from 990 mV to 850 mV, we observed systematic changes in inter-arrival time statistics. As voltage decreased toward the lower boundary of stable operation, CV values showed excursions above and below unity, suggesting departure from Poisson statistics.

These preliminary observations are consistent with the hypothesis that edge-of-stability operation introduces structure into timing dynamics. However, we emphasize that:
1. Sample sizes were limited (N < 1000 share events per voltage point)
2. Confounding factors (network, OS scheduling) were not fully controlled
3. Multi-chip reproducibility has not been established
4. Statistical significance analysis is pending


Hypothesized Operating Regimes (Preliminary)


| Voltage Range (mV) | Regime | Observed Characteristics | Status |
|---------------------|--------|---------------------------|--------|
| > 950 | Deterministic | Low timing variance, CV = 1 | Preliminary |
| 870-950 | Transitional | Increasing CV variance | Preliminary |
| 850-870 | Resonant (Hypothesized) | Structured timing patterns? | Under Investigation |
| < 850 | Unstable | Frequent errors, system resets | Observed |

### B. The "Silicon Heartbeat" Hypothesis

Preliminary descriptions of this work mentioned a "2.4 Hz Silicon Heartbeat"—a hypothesized self-organized oscillation in ASIC power telemetry. We must clarify the current status of this claim:

The implemented code computes CV and entropy metrics on windows of approximately 10 events. It does not currently implement:
- FFT or Power Spectral Density (PSD) analysis
- Long-horizon time series logging
- Oscillator frequency extraction
- Statistical significance testing for periodicity

Therefore, the "2.4 Hz" claim should be understood as a working hypothesis based on informal observations, not a validated measurement. Proper validation requires the spectral analysis infrastructure outlined in our future work section.

**Current Status:** We observe non-Poissonian variability in inter-arrival statistics. Claims of a stable narrow-band oscillation require time-series logging and frequency-domain analysis, which is planned but not yet implemented.


Hypothesized Phase Diagram (Theoretical)


| Voltage Range (mV) | Regime | Timing CV | Status |
|---------------------|--------|-----------|--------|
| < 850 | Unstable | > 1.5 | Hypothesized |
| 850-870 | Resonant? | ~1.2 | Hypothesized |
| 870-950 | Transitional | ~1.0 | Hypothesized |
| > 950 | Deterministic | 1.0 | Observed |

---

## VII. THEORETICAL EFFICIENCY ANALYSIS

### A. The Von Neumann Bottleneck

Traditional computing architectures suffer from what is known as the **von Neumann bottleneck**: the separation of memory and processing creates a fundamental bandwidth limitation [1]. More critically for our analysis, the energy cost of computation in these architectures scales poorly with problem complexity.

For a system representing n-bit states, von Neumann architectures require energy proportional to the state space exploration:

$$
E_{vN} = k \cdot 2^n \cdot E_{switch}
$$

where \( E_{switch} \) is the energy per bit transition and \( k \) is a constant depending on the algorithm. This exponential scaling is fundamental to the architecture, not merely an implementation limitation.

### B. Hierarchical Number System Efficiency

The Hierarchical Number System (HNS) approach, as developed by Veselov [24], represents states using a tree structure where transitions are encoded in the hierarchy itself. This yields:

$$
E_{HNS} = k' \cdot \log(n) \cdot E_{switch}
$$

The logarithmic scaling arises because state transitions in a hierarchical representation require updating only \( O(\log n) \) nodes rather than potentially all \( n \) bits.

### C. Projected Efficiency Gains

The ratio of energy consumption between architectures is:

$$
\eta = E_{vN} / E_{HNS} = (k/k') \cdot 2^n / \log(n)
$$

For typical reservoir dimensions:


Theoretical Efficiency Ratio by State Space Size


| State Space (n) | 2<sup>n</sup> | log(n) | Ratio (η) | Status |
|-----------------|----------------|--------|-----------|--------|
| 10 | 1,024 | 3.32 | ~300× | Theoretical |
| 12 | 4,096 | 3.58 | ~1,100× | Theoretical |
| 14 | 16,384 | 3.81 | ~4,300× | Theoretical |
| 16 | 65,536 | 4.00 | ~16,000× | Theoretical |

This analysis provides the theoretical basis for efficiency claims in the range of 10<sup>3</sup> to 10<sup>4</sup>×. We emphasize that these are **upper bounds** assuming ideal implementation. Practical efficiency gains will depend on factors including reservoir quality, readout overhead, and task-specific considerations.

### D. Connection to Thermodynamic Limits

The Landauer limit [25] establishes that erasing one bit of information requires at minimum \( kT \ln(2) \) joules of energy dissipation. Traditional computation approaches this limit per operation. Reservoir computing potentially circumvents this by performing computation through physical dynamics rather than explicit state transitions, though the thermodynamic accounting of such systems remains an open research question [26].

---

## VIII. POTENTIAL APPLICATIONS

### A. Edge Computing for Signal Processing

If validated, ASIC-based reservoir computing could enable ultra-low-power signal processing at the edge. Potential applications include:
- **Seismic monitoring:** Real-time anomaly detection with minimal power budget
- **Industrial vibration analysis:** Predictive maintenance at the sensor
- **Biomedical signals:** Continuous ECG/EEG monitoring in wearables

We note that these applications are speculative pending validation of the core reservoir computing capability.

### B. Physical Unclonable Functions (PUFs)

The "Silicon Fingerprint"—the unique timing characteristics of each individual ASIC due to manufacturing variations—could serve as a **Physical Unclonable Function** for hardware security applications [27]. Because the response depends on junction temperature and device-specific delay faults, it cannot be replicated even with a perfect logical model of the chip.

### C. Circular Economy Computing

Perhaps the most significant potential impact is environmental. The global cryptocurrency mining industry produces millions of obsolete ASICs annually [4]. If these devices can be repurposed for computation—even specialized computation—the environmental impact would be substantial. This represents a potential transition from a linear (manufacture-use-discard) to circular (manufacture-use-repurpose) model for specialized silicon.


Potential Applications - Readiness Assessment


| Application | Requirements | Current Status | Readiness |
|-------------|--------------|----------------|-----------|
| PUF / Hardware Security | Unique per-chip response | Timing uniqueness observed | Medium |
| Entropy Source | True randomness | Unvalidated | Low |
| Reservoir Computing | ESP, separation property | Theoretical | Low |
| Signal Processing | Benchmark performance | Not tested | Very Low |

---

## IX. COMPARISON WITH RELATED APPROACHES

### A. Purpose-Built Physical Reservoirs


Comparison with Other Physical RC Approaches


| Approach | Demonstrated | Power | Availability | Controllability |
|----------|--------------|-------|-------------|----------------|
| Memristor Arrays [10] | Yes | μW-mW | Research only | High |
| Photonic (Delay Line) [11] | Yes | mW-W | Lab equipment | High |
| Spintronic [12] | Yes | μW | Research only | Medium |
| CMOS Spiking [17] | Yes | mW | Fabrication required | High |
| ASIC/CHIMERA (This work) | No | 5-15 W | Commercial (used) | Limited |

The CHIMERA approach's primary advantage is **availability**: millions of suitable ASICs exist and can be acquired at minimal cost. The primary disadvantage is that the substrate was not designed for reservoir computing, and whether it can function as such remains unproven.

### B. Industry ASIC Repurposing Efforts

Our approach differs fundamentally from industry "AI pivot" efforts. Companies like Hut 8, Iris Energy, and Core Scientific are replacing ASICs with GPUs [5][21]. We propose using the ASICs themselves, albeit for a narrow class of computation.

---

## X. LIMITATIONS AND FUTURE WORK

### A. Theoretical Uncertainties

The core hypothesis—that SHA-256 ASICs can function as physical reservoirs—remains unproven. Several theoretical challenges must be addressed:
1. **Echo State Property:** We have not demonstrated that the substrate has fading memory of inputs. This is a fundamental requirement for reservoir computing.
2. **Separation Property:** We have not shown that distinct inputs produce distinguishable reservoir states.
3. **State Dimensionality:** The effective dimensionality of timing-based state representation is unknown.
4. **Physical vs. Artifact:** Observed timing variations may be network/OS artifacts rather than silicon physics.

### B. Experimental Limitations

Current experimental limitations include:
1. **Silicon Heartbeat:** The "2.4 Hz" claim requires FFT/PSD analysis and statistical significance testing, which are not yet implemented.
2. **Error Rate:** We measure Hamming distance (diffusion), not actual hardware error rate (timing violations). Invalid share counting would provide direct evidence.
3. **Reproducibility:** Multi-chip, multi-site reproducibility has not been established.
4. **Sample Sizes:** Preliminary observations used limited sample sizes (N < 1000 per condition).

### C. What This Paper Does NOT Claim

To avoid misinterpretation, we explicitly state what this paper does not claim:
- We do not claim to have built a working neuromorphic computer.
- We do not claim that ASICs are superior to purpose-built RC hardware.
- We do not claim that timing variations constitute "consciousness" or cognition in any meaningful sense.
- We do not claim experimentally validated efficiency improvements.
- We do not claim that SHA-256 generates entropy (it diffuses it).

### D. Required Future Experiments

To validate or refute the CHIMERA hypothesis, the following experiments are required:


Required Validation Experiments


| Experiment | Purpose | Infrastructure Needed | Priority |
|------------|---------|------------------------|----------|
| FFT/PSD Analysis | Validate heartbeat frequency | Long-duration logging | High |
| Invalid Share Counting | Measure actual error rate | Stratum proxy modification | High |
| Multi-chip Study | Establish reproducibility | Multiple ASIC units | High |
| NARMA-10 Benchmark | Standard RC performance | Readout implementation | Medium |
| Mackey-Glass Prediction | Time series capability | Training infrastructure | Medium |
| Echo State Property Test | Fundamental RC requirement | Controlled input injection | Critical |
| Direct EM Probing | Bypass network confounds | Hardware instrumentation | Low |

---

## XI. CONCLUSIONS

We have presented the **CHIMERA framework** as a theoretical proposal for repurposing retired Bitcoin mining ASICs as physical reservoir computing substrates. The key insight is that the candidate physical signal is not hash bit patterns—which remain deterministic—but timing dynamics under controlled voltage and frequency stress.

Our theoretical analysis, developed in collaboration with Veselov, provides a mathematical basis for potential **O(log n)** energy scaling compared to traditional von Neumann **O(2<sup>n</sup>)** architectures. This suggests efficiency improvements of several orders of magnitude could be achievable, though experimental validation is required.

Preliminary observations show non-Poissonian variability in inter-arrival time statistics during edge-of-stability operation. While these findings are intriguing, we emphasize that substantial experimental work remains before any claims of computational utility can be made. The "Silicon Heartbeat" remains a working hypothesis awaiting spectral analysis validation.

If validated, the CHIMERA approach could contribute to sustainable computing by giving new purpose to otherwise obsolete hardware—transforming electronic waste into computational infrastructure. We hope this paper stimulates discussion and invites collaboration from the reservoir computing and neuromorphic engineering communities to rigorously test these ideas.

The legacy of Bitcoin mining need not end in landfills. Whether it can serve as the infrastructure for a new kind of computation remains an open question—one we believe is worth investigating.

---

## XII. ACKNOWLEDGMENTS

The authors thank the open-source community for tools and frameworks that enabled this research. F.A.L. acknowledges the AxeOS development team for firmware documentation. V.V. acknowledges support from MIET. R.G. acknowledges the Apoth3osis research team for technical review and code-to-paper alignment analysis.

We particularly thank the peer reviewers who provided critical feedback that substantially improved the honesty and precision of this manuscript. Their insistence on clearly distinguishing theoretical predictions from empirical measurements has made this a stronger contribution.

---

## XIII. REFERENCES

1. J. von Neumann, "First Draft of a Report on the EDVAC," University of Pennsylvania, 1945.
2. C. Mead, "Neuromorphic Electronic Systems," Proceedings of the IEEE, vol. 78, no. 10, pp. 1629-1636, 1990. DOI: 10.1109/5.58356
3. R. Landauer, "Irreversibility and Heat Generation in the Computing Process," IBM Journal of Research and Development, vol. 5, no. 3, pp. 183-191, 1961.
4. Cambridge Bitcoin Electricity Consumption Index, "Mining Equipment Database," 2024. Available: [https://ccaf.io/cbnsi/cbeci](https://ccaf.io/cbnsi/cbeci)
5. RSM US LLP, "Bitcoin miners diversify into AI to sustain profitability," 2024. Available: [https://rsmus.com/insights/industries/financial-services/](https://rsmus.com/insights/industries/financial-services/)
6. H. Jaeger, "The 'echo state' approach to analysing and training recurrent neural networks," GMD Report 148, German National Research Center for Information Technology, 2001.
7. W. Maass, T. Natschläger, and H. Markram, "Real-time computing without stable states: A new framework for neural computation based on perturbations," Neural Computation, vol. 14, no. 11, pp. 2531-2560, 2002.
8. M. Lukoševičius and H. Jaeger, "Reservoir computing approaches to recurrent neural network training," Computer Science Review, vol. 3, no. 3, pp. 127-149, 2009.
9. G. Tanaka et al., "Recent advances in physical reservoir computing: A review," Neural Networks, vol. 115, pp. 100-123, 2019. DOI: 10.1016/j.neunet.2019.03.005
10. C. Du et al., "Reservoir computing using dynamic memristors for temporal information processing," Nature Communications, vol. 8, no. 1, p. 2204, 2017.
11. L. Larger et al., "Photonic information processing beyond Turing: an optoelectronic implementation of reservoir computing," Optics Express, vol. 20, no. 3, pp. 3241-3249, 2012.
12. D. Markovic et al., "Reservoir computing with the frequency, phase, and amplitude of spin-torque nano-oscillators," Applied Physics Letters, vol. 114, no. 1, p. 012409, 2019.
13. K. Nakajima et al., "A soft body as a reservoir: case studies in a dynamic model of octopus-inspired soft robotic arm," Frontiers in Computational Neuroscience, vol. 7, p. 91, 2013.
14. K. Nakajima, "Physical reservoir computing—an introductory perspective," Japanese Journal of Applied Physics, vol. 59, no. 6, p. 060501, 2020.
15. S. H. Sung et al., "Emerging dynamic memristors for neuromorphic reservoir computing," Nanoscale, vol. 13, no. 45, pp. 19017-19032, 2021.
16. Z. Wang et al., "Memristors with diffusive dynamics as synaptic emulators for neuromorphic computing," Nature Materials, vol. 16, no. 1, pp. 101-108, 2017.
17. N. Kimura et al., "Hardware-Friendly Implementation of Physical Reservoir Computing with CMOS-based Time-domain Analog Spiking Neurons," arXiv:2409.11612, 2024.
18. K. Y. Camsari, R. Faria, B. M. Sutton, and S. Datta, "Stochastic p-bits for invertible logic," Physical Review X, vol. 7, no. 3, p. 031014, 2017.
19. W. A. Borders et al., "Integer factorization using stochastic magnetic tunnel junctions," Nature, vol. 573, no. 7774, pp. 390-393, 2019.
20. Extropic Corp., "The Thermodynamics of Diffusion Models," Technical Report, 2025.
21. Wired Magazine, "Bitcoin Miners Are Pivoting to AI," December 2024.
22. C. Fernando and S. Sojakka, "Pattern recognition in a bucket," in Advances in Artificial Life, Springer, 2003, pp. 588-597.
23. National Institute of Standards and Technology, "Secure Hash Standard (SHS)," FIPS PUB 180-4, 2015.
24. V. Veselov, "Hierarchical Number Systems and Energy-Efficient Computing," MIET Technical Report, 2024.
25. R. Landauer, "Information is Physical," Physics Today, vol. 44, no. 5, pp. 23-29, 1991.
26. J. M. Parrondo, J. M. Horowitz, and T. Sagawa, "Thermodynamics of information," Nature Physics, vol. 11, no. 2, pp. 131-139, 2015.
27. C. Herder et al., "Physical unclonable functions and applications: A tutorial," Proceedings of the IEEE, vol. 102, no. 8, pp. 1126-1141, 2014.
28. D. Sussillo and L. F. Abbott, "Generating coherent patterns of activity from chaotic neural networks," Neuron, vol. 63, no. 4, pp. 544-557, 2009.
29. L. Appeltant et al., "Information processing using a single dynamical node as complex system," Nature Communications, vol. 2, no. 1, p. 468, 2011.
30. P. Bak, C. Tang, and K. Wiesenfeld, "Self-organized criticality: An explanation of the 1/f noise," Physical Review Letters, vol. 59, no. 4, pp. 381-384, 1987.
31. G. Samid, "Negotiating Darwin's Barrier: Evolution Limits Our View of Reality, AI Breaks Through," Applied Physics Research, 2025.
32. J. J. Hopfield, "Neural networks and physical systems with emergent collective computational abilities," Proceedings of the National Academy of Sciences, vol. 79, no. 8, pp. 2554-2558, 1982.
33. H. Jaeger and H. Haas, "Harnessing nonlinearity: Predicting chaotic systems and saving energy in wireless communication," Science, vol. 304, no. 5667, pp. 78-80, 2004.
34. B. Schrauwen, D. Verstraeten, and J. Van Campenhout, "An overview of reservoir computing: theory, applications and implementations," in Proceedings of the 15th European Symposium on Artificial Neural Networks, 2007, pp. 471-482.
35. D. Verstraeten et al., "An experimental unification of reservoir computing methods," Neural Networks, vol. 20, no. 3, pp. 391-403, 2007.
36. R. Legenstein and W. Maass, "Edge of chaos and prediction of computational performance for neural circuit models," Neural Networks, vol. 20, no. 3, pp. 323-334, 2007.
37. I. B. Yildiz, H. Jaeger, and S. J. Kiebel, "Re-visiting the echo state property," Neural Networks, vol. 35, pp. 1-9, 2012.
38. J. Dambre, D. Verstraeten, B. Schrauwen, and S. Massar, "Information processing capacity of dynamical systems," Scientific Reports, vol. 2, no. 1, p. 514, 2012.
39. A. Rodan and P. Tiño, "Minimum complexity echo state network," IEEE Transactions on Neural Networks, vol. 22, no. 1, pp. 131-144, 2010.
40. M. C. Soriano et al., "Delay-based reservoir computing: noise effects in a combined analog and digital implementation," IEEE Transactions on Neural Networks and Learning Systems, vol. 26, no. 2, pp. 388-393, 2014.
41. G. Van der Sande, D. Brunner, and M. C. Soriano, "Advances in photonic reservoir computing," Nanophotonics, vol. 6, no. 3, pp. 561-576, 2017.
42. J. Torrejon et al., "Neuromorphic computing with nanoscale spintronic oscillators," Nature, vol. 547, no. 7664, pp. 428-431, 2017.
43. M. Cucchi et al., "Hands-on reservoir computing: a tutorial for practical implementation," Neuromorphic Computing and Engineering, vol. 2, no. 3, p. 032002, 2022.
44. S. Wolfram, A New Kind of Science, Wolfram Media, 2002.
45. I. Prigogine, From Being to Becoming: Time and Complexity in the Physical Sciences, W. H. Freeman, 1980.

---

**Manuscript submitted to:** IEEE Transactions on Neural Networks and Learning Systems
**Category:** Position Paper / Hypothesis with Preliminary Observations
**Date:** December 19, 2025
**Official Repository:** Emergent-Neuromorphic-Intelligence-Computing-in-Thermodynamic-ASIC-Substrates

---

**Author Contact & Publications:**

- **Francisco Angulo de Lafuente** (Corresponding Author)
  GitHub · ResearchGate · Kaggle · HuggingFace · Wikipedia

- **Vladimir Veselov**
  National Research University of Electronic Technology - MIET · ORCID: 0000-0002-6301-3226

- **Richard Goodman**
  Managing Director, Apoth3osis · [apoth3osis.com](http://apoth3osis.com)

© 2025 The Authors. This work is licensed under CC BY 4.0.
```

Si necesitas ajustar algún formato o prefieres que las tablas se presenten de otra manera, házmelo saber.



![Imagen1](https://github.com/user-attachments/assets/e9e746a1-a69b-411e-9132-66ba3d9f2eaf)
![Imagen2](https://github.com/user-attachments/assets/839d75cf-411a-413e-a23a-d49a81f5c7c6)
![Imagen3](https://github.com/user-attachments/assets/8b0687e3-ed1d-48a9-9337-e7e273a04c69)
![Imagen4](https://github.com/user-attachments/assets/b189aa76-b4df-4d84-be52-3617c1fe92c7)
![Imagen5](https://github.com/user-attachments/assets/fe7189e8-1aed-4b90-b6df-090a46e57b4b)
![Imagen6](https://github.com/user-attachments/assets/c06d683d-ef07-4892-b9ff-f463e379ceb0)
![Imagen7](https://github.com/user-attachments/assets/4f3555ac-27f2-4849-95ec-0c3e909ed451)
![Imagen8](https://github.com/user-attachments/assets/b779d231-28ed-4b1c-978f-e814c36b2413)
![Imagen9](https://github.com/user-attachments/assets/61c4a3f2-b4fd-4b1f-ac29-61c2d734801e)
![Imagen10](https://github.com/user-attachments/assets/69df2acb-51a0-4a9d-9838-be76ab1ce9a7)
![Imagen11](https://github.com/user-attachments/assets/fb932b6a-4159-426e-8b7d-a55a9b9284b7)
![Imagen12](https://github.com/user-attachments/assets/06fcd43c-9bcf-4d6c-a002-1015ac1eb1e7)
![Imagen13](https://github.com/user-attachments/assets/72cfc0cb-99b3-4379-8e96-5e06d90978c1)
![Imagen14](https://github.com/user-attachments/assets/4e9d2868-d3b2-48b0-98c2-16aa3efd4d1a)
![Imagen15](https://github.com/user-attachments/assets/11f0f764-6e26-4b01-8c0f-92330d4bf955)
![Imagen16](https://github.com/user-attachments/assets/66d61ded-0778-43c7-9910-edace8f735e3)
![Imagen17](https://github.com/user-attachments/assets/42b371d7-290d-45a9-8930-a7af5745b541)
![Imagen18](https://github.com/user-attachments/assets/eb649a23-57d4-4277-8821-1f3f916c5b29)







## Authors

- **Francisco Angulo de Lafuente** - *Lead Architect* - [GitHub](https://github.com/Agnuxo1)
- **Vladimir Veselov** - *Neuromorphic Research* - [ORCID](https://orcid.org/0000-0002-6301-3226)
- **Richard Goodman** - *Strategic Applications* - [Apoth3osis](https://github.com/Agnuxo1)

---

### **About Apoth3osis**
Empowering humanity through advanced AI applications that enhance decision-making, optimize complex systems, and drive continuous improvement by merging cutting-edge AI models with rigorous mathematical frameworks.

---
© 2025 HRC Project. All rights reserved.

