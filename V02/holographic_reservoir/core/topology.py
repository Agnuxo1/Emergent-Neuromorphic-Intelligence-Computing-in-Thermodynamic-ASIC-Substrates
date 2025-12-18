import networkx as nx
import numpy as np

class VeselovExpander:
    """
    Veselov Topology Manager.
    
    Implements a Bipartite Expander Graph for Holographic Information Mixing.
    This structure ensures that information injected into the system is rapidly
    scrambled and distributed across the entire reservoir state.
    
    Structure:
    - Input Layer (L): Sensory inputs (mapped input vectors)
    - Reservoir Layer (R): Hidden memory state
    - Edges: Random bipartite connections (Ramanujan Graph properties via random construction)
    """
    
    def __init__(self, n_input=256, n_reservoir=1024, degree=6):
        """
        Initialize the topological structure.
        
        Args:
            n_input: Number of input nodes.
            n_reservoir: Number of reservoir/memory nodes.
            degree: Connectivity degree (d). Number of connections per node.
        """
        self.n_input = n_input
        self.n_reservoir = n_reservoir
        self.degree = degree
        
        # Build the Adjacency Matrix
        # We use a random bipartite graph construction which is known to be a good expander.
        # Reference: Pinsker (1973) - Almost all random bipartite graphs are expanders.
        self.adj_matrix = self._build_topology()
        
    def _build_topology(self) -> np.ndarray:
        """Constructs the mixing matrix."""
        # We manually construct a sparse adjacency matrix for efficiency / clarity
        adj = np.zeros((self.n_input, self.n_reservoir), dtype=np.float32)
        
        rng = np.random.default_rng(42) # Fixed seed for Structural Determinism (Auditable)
        
        for i in range(self.n_input):
            # Each input node connects to 'degree' unique reservoir nodes
            targets = rng.choice(self.n_reservoir, size=self.degree, replace=False)
            # We set the weight used for mixing to 1.0 / sqrt(degree) to preserve variance
            # This is a standard initialization for neural reservoirs (Xavier/He like)
            weight = 1.0 / np.sqrt(self.degree) 
            adj[i, targets] = weight
            
        return adj
        
    def propagate(self, input_vectors: np.ndarray) -> np.ndarray:
        """
        Performs the 'Holographic Mixing' step.
        
        Args:
            input_vectors: Input state (Shape: [Batch, N_Input] or [N_Input])
            
        Returns:
            Projected state in Reservoir dimension (Shape: [Batch/1, N_Reservoir])
            
        Mechanism: 
        V_out = Tanh( V_in * Adj_Matrix )
        """
        # Linear Projection (Mixing)
        # Note: input_vectors should match n_input dimension
        # If input is (N_Input, 4) [RGBA], we mix each channel separately?
        # Veselov's notes imply global mixing.
        # Let's assume input_vectors is shape (N_Input, Channels) or just (N_Input).
        
        # If we are processing RGBA, we apply the topology to the spatial dimension,
        # preserving the channel dimension.
        
        raw_flow = np.dot(input_vectors.T, self.adj_matrix).T 
        # Result shape: (N_Reservoir, Channels) if input was (N_Input, Channels)
        
        # Non-linear activation (Physical Saturation)
        return np.tanh(raw_flow)
