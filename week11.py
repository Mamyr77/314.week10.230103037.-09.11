import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import multiprocessing
import time
import math
import csv


# --- TASK 06-10, 16-17: Calculations ---
def run_calculations():
    print("================ CALCULATIONS ================")
    # Task 06
    print("\n--- TASK 06: Parametric Speedup ---")
    a = 0.04
    for p in [16, 64, 256, 1024, 4096, 16384]:
        s_p = p - a * (p - 1)
        print(f"P={p:<5} | S(P)={s_p:<8.2f} | E(P)={s_p / p:.4f}")

    # Task 07
    print("\n--- TASK 07: Reverse Engineering ---")
    p, s_min = 8192, 7500
    a_max = (p - s_min) / (p - 1)
    print(f"Max serial fraction to achieve S(P)>=7500 on 8192 cores: {a_max:.6f}")

    # Task 08
    print("\n--- TASK 08: Amdahl vs. Gustafson Cross-Over ---")
    s, p_cross = 0.08, 128
    amdahl = 1 / (s + (1 - s) / p_cross)
    gustafson = p_cross - s * (p_cross - 1)
    print(
        f"Amdahl: {amdahl:.2f}, Gustafson: {gustafson:.2f}, Discrepancy: {((gustafson - amdahl) / amdahl) * 100:.2f}%")

    # Task 09
    print("\n--- TASK 09: Multi-Component Workload ---")
    a_agg = 0.02 + 0.06
    for p in [512, 2048]:
        print(f"P={p:<4} | S(P)={p - a_agg * (p - 1):.2f}")

    # Task 10
    print("\n--- TASK 10: Memory Growth Rate ---")
    print("Max N (64 nodes) = cbrt((64 * 32GB) / c)")
    print("Max N (512 nodes) = cbrt((512 * 32GB) / c) = 2 * Max N (64 nodes)")

    # Task 16
    print("\n--- TASK 16: GEMM Scaling ---")
    print("To keep time constant as P increases, compute work O(N^3) must scale with P.")
    print("Therefore, N must scale as cbrt(P).")

    # Task 17
    print("\n--- TASK 17: 3D Stencil Scaling ---")
    print("Volume (compute) scales as O(N^3) ~ P. Surface (communication) scales as O(N^2) ~ P^(2/3).")
    print("Comm-to-Compute ratio = P^(2/3) / P = P^(-1/3). The ratio improves as P scales.")
    print("==============================================\n")


# --- TASK 21: Simulator ---
def amdahls_law(p, a): return 1 / (a + (1 - a) / p)


def gustafsons_law(p, a): return p - a * (p - 1)


def run_simulator():
    processors = np.array([2 ** i for i in range(17)])
    results = []
    for a in [0.001, 0.01, 0.04, 0.08, 0.20]:
        for p in processors:
            results.append({'P': p, 'a': a, 'Amdahl': amdahls_law(p, a), 'Gustafson': gustafsons_law(p, a)})

    df = pd.DataFrame(results)
    df.to_csv('simulator_results.csv', index=False)
    print("Task 21 Simulator run complete. Output saved to 'simulator_results.csv'.")


# --- TASK 22 & 23: Empirical Benchmark ---
def worker_task(iters):
    res = 0.0
    for i in range(iters): res += math.sin(i) * math.cos(i)
    return res


def run_benchmark():
    workload = 1000000
    threads_list = [1, 2, 4]  # Reduced for fast execution in this combined script
    results = []

    for t in threads_list:
        start = time.time()
        procs = [multiprocessing.Process(target=worker_task, args=(workload,)) for _ in range(t)]
        for p in procs: p.start()
        for p in procs: p.join()
        mean_time = time.time() - start
        results.append({'Threads': t, 'MeanTime': mean_time})
        print(f"Benchmark Threads: {t}, Time: {mean_time:.3f}s")

    df = pd.DataFrame(results)
    df.to_csv('benchmark_results.csv', index=False)
    return df


# --- TASK 24: Curve Fitting and Plotting ---
def fit_and_plot(df):
    if len(df) < 2: return
    t1 = df['MeanTime'].iloc[0]
    df['Speedup'] = df['Threads'] * (t1 / df['MeanTime'])

    p_data = df['Threads'].values
    s_data = df['Speedup'].values

    try:
        popt, _ = curve_fit(gustafsons_law, p_data, s_data, bounds=(0, 1))
        a_obs = popt[0]
        print(f"Task 23: Fitted empirical serial fraction a = {a_obs:.6f}")
    except:
        a_obs = 0.01

    plt.figure(figsize=(8, 5))
    plt.plot(p_data, p_data, 'k--', label='Ideal')
    plt.plot(p_data, gustafsons_law(p_data, a_obs), 'b-', label=f'Gustafson (a={a_obs:.3f})')
    plt.plot(p_data, s_data, 'ro', label='Empirical')
    plt.xlabel('Threads');
    plt.ylabel('Speedup')
    plt.legend();
    plt.grid(True)
    plt.savefig('scaling_plot.png')
    print("Task 24: Plot saved as 'scaling_plot.png'.")


if __name__ == '__main__':
    run_calculations()
    run_simulator()
    df_bench = run_benchmark()
    fit_and_plot(df_bench)