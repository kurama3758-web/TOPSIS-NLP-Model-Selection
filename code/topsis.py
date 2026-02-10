import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# Load decision matrix
data = pd.read_csv("../data/decision_matrix.csv")

models = data.iloc[:, 0].values
X = data.iloc[:, 1:].values.astype(float)
# Weights (sum = 1)
weights = np.array([0.35, 0.20, 0.15, 0.30])

# Benefit (1) / Cost (0)
criteria = np.array([1, 0, 0, 1])
# STEP 1: Normalize
norm = np.sqrt((X ** 2).sum(axis=0))
R = X / norm
# STEP 2: Weighted normalized matrix
V = R * weights
# STEP 3: Ideal best & worst
ideal_best = np.where(criteria == 1, V.max(axis=0), V.min(axis=0))
ideal_worst = np.where(criteria == 1, V.min(axis=0), V.max(axis=0))
# STEP 4: Distances
S_plus = np.sqrt(((V - ideal_best) ** 2).sum(axis=1))
S_minus = np.sqrt(((V - ideal_worst) ** 2).sum(axis=1))
# STEP 5: TOPSIS score
C = S_minus / (S_plus + S_minus)

ranking = pd.DataFrame({
    "Model": models,
    "TOPSIS Score": C
}).sort_values(by="TOPSIS Score", ascending=False)

print("\nFinal Ranking:\n")
print(ranking)

# AUTO-GENERATE tables.png
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.flatten()

tables = [
    ("Decision Matrix", data),
    ("Normalized Matrix", pd.DataFrame(R, columns=data.columns[1:], index=models)),
    ("Weighted Normalized Matrix", pd.DataFrame(V, columns=data.columns[1:], index=models)),
    ("Final Ranking", ranking)
]

for ax, (title, df) in zip(axes, tables):

    display_df = df.copy()

    for col in display_df.columns:
        if pd.api.types.is_numeric_dtype(display_df[col]):
            display_df[col] = display_df[col].round(4)

    ax.axis('off')
    ax.set_title(title, fontsize=11)

    table = ax.table(
        cellText=display_df.values.astype(str),
        colLabels=display_df.columns,
        rowLabels=display_df.index.astype(str),
        loc='center'
    )
    table.scale(1, 1.4)

plt.tight_layout()
plt.savefig("../results/tables.png", dpi=300)
plt.close()
# AUTO-GENERATE graphs.png
plt.figure(figsize=(8, 5))
plt.bar(ranking["Model"], ranking["TOPSIS Score"])
plt.xlabel("Models")
plt.ylabel("TOPSIS Score")
plt.title("TOPSIS Ranking of Conversational AI Models")
plt.tight_layout()
plt.savefig("../results/graphs.png", dpi=300)
plt.close()

print("\n tables.png and graphs.png generated automatically in results/ folder ✅")
