Python code for the paper "Reaction Networks Resemble Low-Dimensional Regular Lattices". Included is code to generate networks and analyze them.

The generation codes can create Erdős–Rényi (ER) networks, bipartite random (BR) networks, 
regular lattices networks with non-periodic boundary conditions (LNP) and periodic boundary conditions (LP), 
Watts–Strogatz (WS) networks, and modified regular lattices networks (LNP-R and LP-R), which generalize the WS 
construction to higher dimensions by adding random shortcuts with probability $p_r$ to the LNP and LP networks, respectively.

The analysis code calculates basic properties (number of nodes $n$, number of edges $e$, and density $\rho$), 
local properties (average node degree $\overline{k}$ and average square clustering coefficient $\overline{C_4}$), 
metric properties (diameter $D$ and average shortest-path length $\overline{l}$), and global properties (fractal dimension
$d_{\text{f}}$ and average growth exponent $\overline{\xi}$). 
