import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data_full = {
    "Drive": {
        "Djikstra": {"distance": 5477.17, "time": 0.0608, "memory": 974.75},
        "AStar": {"distance": 5477.17, "time": 0.0525, "memory": 439.98},
        "Bellman Ford": {"distance": 5477.17, "time": 4.823, "memory": 972.38}
    },
    "Walk": {
        "Djikstra": {"distance": 5354.60, "time": 0.937, "memory": 8512.24},
        "AStar": {"distance": 5354.60, "time": 0.581, "memory": 3748.74},
        "Bellman Ford": {"distance": float("inf"), "time": None, "memory": 11134.99}
    },
    "Bike": {
        "Djikstra": {"distance": 5462.37, "time": 0.212, "memory": 4041.01},
        "AStar": {"distance": 5462.37, "time": 0.167, "memory": 875.34},
        "Bellman Ford": {"distance": 5462.37, "time": 30.30, "memory": 4041.01}
    }
}

df_full = pd.DataFrame([
    {"mode": mode, "algorithm": algo, **data_full[mode][algo]}
    for mode in data_full
    for algo in data_full[mode]
])

df_full['distance'] = df_full['distance'].replace(np.inf, np.nan)

width = 0.25
x = np.arange(len(df_full['algorithm'].unique()))

fig_time, ax_time = plt.subplots(figsize=(7, 6))
for i, mode in enumerate(df_full['mode'].unique()):
    subset = df_full[df_full['mode'] == mode]
    ax_time.bar(x + i * width, subset['time'], width, label=mode.capitalize())
ax_time.set_title("Execution Time (Comparing Modes and Algorithms)")
ax_time.set_xticks(x + width)
ax_time.set_xticklabels(df_full['algorithm'].unique())
ax_time.set_ylabel("Time (s)")
ax_time.set_yscale('log')
ax_time.legend()
ax_time.grid(True, linestyle="--", alpha=0.5)
fig_memory, ax_memory = plt.subplots(figsize=(7, 6))
for i, mode in enumerate(df_full['mode'].unique()):
    subset = df_full[df_full['mode'] == mode]
    ax_memory.bar(x + i * width, subset['memory'], width, label=mode.capitalize())
ax_memory.set_title("Peak Memory Usage (Comparing Modes and Algorithms)")
ax_memory.set_xticks(x + width)
ax_memory.set_xticklabels(df_full['algorithm'].unique())
ax_memory.set_ylabel("Memory (KB)")
ax_memory.legend()
ax_memory.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()
