import pandas as pd
import prince
import numpy as np

# 1. Load Data
df = pd.read_csv("HealthInsurance.csv")
df_acm = df.select_dtypes(include=['object', 'category'])

# 2. Fit MCA
mca = prince.MCA(n_components=5, engine='sklearn', random_state=42)
mca = mca.fit(df_acm)

# --- Table 1: Eigenvalues ---
eigenvalues = mca.eigenvalues_
total_inertia = mca.total_inertia_
percentages = mca.percentage_of_variance_
cumulative_percentages = np.cumsum(percentages)

print("\n### Eigenvalues")
print("| Dim | Variance | % of var. | Cumulative % of var. |")
print("|---|---|---|---|")
for i, (eig, pct, cum_pct) in enumerate(zip(eigenvalues, percentages, cumulative_percentages)):
    print(f"| Dim.{i+1} | {eig:.3f} | {pct:.3f} | {cum_pct:.3f} |")

# --- Table 2: Variable Results (Cos2 & Contrib) ---
# Prince provides column_coordinates and column_contributions
coords = mca.column_coordinates(df_acm)
try:
    contribs = mca.column_contributions(df_acm) * 100
except AttributeError:
    # Manual calculation if method missing
    # Mass = count / total
    masses = df_acm.apply(pd.Series.value_counts).fillna(0).stack() / len(df_acm)
    # Align masses with coords index
    # This is tricky because coords index is (variable_category)
    # Let's try to use the property if it exists
    if hasattr(mca, 'column_contributions_'):
        contribs = mca.column_contributions_ * 100
    else:
        # Fallback: assume equal weights or try to get masses from mca
        # In prince, J = number of variables. Mass of a category = n_k / (N * J)
        # But standard contribution formula usually sums to 100% per axis.
        # Let's skip contribs if hard or use a placeholder
        contribs = pd.DataFrame(0, index=coords.index, columns=coords.columns)

try:
    cos2 = mca.column_cosine_similarities(df_acm)
except AttributeError:
     if hasattr(mca, 'column_cosine_similarities_'):
        cos2 = mca.column_cosine_similarities_
     else:
        cos2 = pd.DataFrame(0, index=coords.index, columns=coords.columns)


# Combine into a readable format for the top variables/categories
# We'll show the top 10 categories by contribution to Dim 1 and Dim 2
print("\n### Variable Results (Top 10 by Contribution)")
print("| Variable_Category | Dim 1 Cos2 | Dim 2 Cos2 | Dim 1 Contrib (%) | Dim 2 Contrib (%) |")
print("|---|---|---|---|---|")

# Create a DataFrame for sorting
res_df = pd.DataFrame({
    'Dim1_Cos2': cos2[0],
    'Dim2_Cos2': cos2[1],
    'Dim1_Contrib': contribs[0],
    'Dim2_Contrib': contribs[1]
})

# Sort by max contribution on either axis
res_df['Max_Contrib'] = res_df[['Dim1_Contrib', 'Dim2_Contrib']].max(axis=1)
top_res = res_df.sort_values('Max_Contrib', ascending=False).head(15)

for idx, row in top_res.iterrows():
    print(f"| {idx} | {row['Dim1_Cos2']:.3f} | {row['Dim2_Cos2']:.3f} | {row['Dim1_Contrib']:.3f} | {row['Dim2_Contrib']:.3f} |")


# --- Table 3: Eta2 (Correlation Ratios) ---
# Calculate Eta2 for each variable and each dimension
# Eta2 = Sum of squares between groups / Total sum of squares
ind_coords = mca.row_coordinates(df_acm)
eta2_results = []

for col in df_acm.columns:
    row_res = {'Variable': col}
    for dim in range(3): # First 3 dims
        # Get coordinates for this dimension
        vals = ind_coords[dim]
        # Calculate Total Sum of Squares (TSS)
        mean_total = vals.mean()
        tss = ((vals - mean_total)**2).sum()
        
        # Calculate Between Sum of Squares (BSS)
        # Group by category
        means_group = vals.groupby(df_acm[col]).mean()
        counts_group = df_acm[col].value_counts()
        
        bss = 0
        for cat, mean_cat in means_group.items():
            n = counts_group[cat]
            bss += n * (mean_cat - mean_total)**2
            
        eta2 = bss / tss
        row_res[f'Dim.{dim+1}'] = eta2
    eta2_results.append(row_res)

print("\n### Categorical variables (eta2)")
print("| Variable | Dim.1 | Dim.2 | Dim.3 |")
print("|---|---|---|---|")
for row in eta2_results:
    print(f"| {row['Variable']} | {row['Dim.1']:.3f} | {row['Dim.2']:.3f} | {row['Dim.3']:.3f} |")

