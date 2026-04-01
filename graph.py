import matplotlib.pyplot as plt
import sys
import time
from numpy import polyfit, log

sys.setrecursionlimit(10**6)


def wlcs(s1, s2, weights):
    m = len(s1)
    n = len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + weights.get(s1[i - 1], 0)
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


tests = [f"test{i}.txt" for i in range(1, 11)]

products = []
times = []

for test in tests:
    with open(f"tests/{test}") as f:
        lines = f.read().strip().split("\n")

    K = int(lines[0])
    weights = {}
    for i in range(1, K + 1):
        parts = lines[i].split()
        weights[parts[0]] = int(parts[1])

    A = lines[-2].strip()
    B = lines[-1].strip()

    times_run = []
    for _ in range(5):
        start = time.perf_counter()
        result = wlcs(A, B, weights)
        elapsed = time.perf_counter() - start
        times_run.append(elapsed)
    avg_time = min(times_run)

    products.append(len(A) * len(B))
    times.append(avg_time)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.scatter(products, times, color="blue", s=100, zorder=5)
ax1.plot(products, times, "b--", alpha=0.5)
ax1.set_xlabel("m x n ", fontsize=12)
ax1.set_ylabel("Runtime (s)", fontsize=12)
ax1.set_title("Runtime vs m x n", fontsize=14)
ax1.grid(True, alpha=0.3)

for i, (prod, t) in enumerate(zip(products, times)):
    ax1.annotate(f"test{i + 1}", (prod, t), textcoords="offset points", xytext=(5, 5), fontsize=9)

ax2.loglog(products, times, "ro-", markersize=10, linewidth=2)
ax2.set_xlabel("m x n Log Scale", fontsize=12)
ax2.set_ylabel("Runtime (s) - Log Scale", fontsize=12)
ax2.set_title("Log-Log Plot (Slope confirms O(mxn))", fontsize=14)
ax2.grid(True, alpha=0.3, which="both")


slope, intercept = polyfit(log(products), log(times), 1)
ax2.text(0.05,0.95,f"Slope ~ {slope:.2f}",transform=ax2.transAxes,fontsize=12,verticalalignment="top",bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

plt.tight_layout()
plt.savefig("graph.png", dpi=150, bbox_inches="tight")
plt.close()

print("Graph saved")
