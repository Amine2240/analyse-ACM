import pandas as pd
import prince
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 1. Load Data
df = pd.read_csv("HealthInsurance.csv")
df_acm = df.select_dtypes(include=['object', 'category'])

# 2. Fit MCA
mca = prince.MCA(n_components=10, engine='sklearn', random_state=42)
mca = mca.fit(df_acm)

# 3. Scree Plot
eigenvalues = mca.eigenvalues_
percentages = mca.percentage_of_variance_

plt.figure(figsize=(10, 6))
x = range(1, len(eigenvalues) + 1)
plt.bar(x, percentages, alpha=0.7, label='% Variance')
plt.plot(x, percentages, 'ro-', linewidth=2)
plt.xlabel('Dimensions')
plt.ylabel('Percentage of Explained Variance')
plt.title('Scree Plot (Éboulis des valeurs propres)')
plt.xticks(x)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

plt.savefig('scree_plot.png')
print("Scree plot saved to scree_plot.png")
