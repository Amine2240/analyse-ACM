import pandas as pd
import prince

# Load Data
df = pd.read_csv("HealthInsurance.csv")
df_acm = df.select_dtypes(include=['object', 'category'])

# Fit MCA
mca = prince.MCA(n_components=2, engine='sklearn', random_state=42)
mca = mca.fit(df_acm)

# Get coordinates
coords = mca.column_coordinates(df_acm)
if hasattr(mca, 'column_contributions_'):
    contribs = mca.column_contributions_ * 100
else:
    # Fallback if attribute missing (older versions)
    # Just print coords to infer signs for known high contributors
    print("Contribs attribute missing, printing all coords")
    print(coords)
    exit()


# Filter for significant contributions (> 3.8%)
threshold = 100 / 26
print(f"Threshold: {threshold:.2f}%")

print("\n--- Dim 1 Significant ---")
dim1_sig = contribs[contribs[0] > threshold].sort_values(0, ascending=False)
for idx in dim1_sig.index:
    coord = coords.loc[idx, 0]
    sign = "(+)" if coord > 0 else "(-)"
    print(f"{idx}: {dim1_sig.loc[idx, 0]:.2f}% {sign}")

print("\n--- Dim 2 Significant ---")
dim2_sig = contribs[contribs[1] > threshold].sort_values(1, ascending=False)
for idx in dim2_sig.index:
    coord = coords.loc[idx, 1]
    sign = "(+)" if coord > 0 else "(-)"
    print(f"{idx}: {dim2_sig.loc[idx, 1]:.2f}% {sign}")
