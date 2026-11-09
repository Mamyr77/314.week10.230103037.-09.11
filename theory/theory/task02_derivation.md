Let the total execution time on $P$ processors be normalized to 1:
$$s + p = 1$$
Where:
- $s$ is the fraction of time spent in serial execution on $P$ processors (denoted as $\alpha$ in the formulation).
- $p$ is the fraction of time spent in parallel execution on $P$ processors.

The equivalent serial execution time (if run on a single processor) would be:
$$T_{serial} = s + p \cdot P$$

The scaled speedup $S(P)$ is the ratio of the serial execution time to the parallel execution time:
$$S(P) = \frac{s + p \cdot P}{s + p}$$

Since we normalized $s + p = 1$, the denominator is 1:
$$S(P) = s + p \cdot P$$

We know that $p = 1 - s$. Substituting $p$:
$$S(P) = s + (1 - s) \cdot P$$
$$S(P) = s + P - s \cdot P$$
$$S(P) = P - s(P - 1)$$

Given that the serial fraction is denoted as $\alpha$ ($s = \alpha$):
$$S(P) = P - \alpha(P - 1)$$
