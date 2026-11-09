# Task 01: Strong Scaling vs. Weak Scaling Foundations

## Foundational Assumptions
- **Amdahl (1967) - Strong Scaling**: Assumes a **fixed problem size**. As processor count $P$ approaches infinity, the execution time of the parallelizable portion approaches zero, but the total execution time is strictly bottlenecked by the sequential portion ($s$). This is "fixed-size" scaling.
- **Gustafson (1988) - Weak Scaling**: Assumes a **fixed execution time**. As processor count $P$ scales toward infinity, the problem size increases proportionally. The time spent on the parallel portion remains constant, while the overall problem size and parallel work expand. This is "fixed-time" scaling.

## Divergence
Amdahl's law is pessimistic about massive parallelism because it assumes the workload is static. Gustafson's law is optimistic, recognizing that in reality, users scale up the problem size (e.g., higher resolution grids, more particles) when they have more computing power available, effectively shrinking the proportion of time spent on serial bottlenecks.
