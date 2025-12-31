import pandas as pd
import prince
import matplotlib
matplotlib.use('Agg') # Utiliser un backend non-interactif pour éviter les erreurs Tkinter
import matplotlib.pyplot as plt

# 1. Charger les données
df = pd.read_csv("HealthInsurance.csv")

# 2. Sélection des variables pour l'ACM
# On ne garde que les variables qualitatives
# On exclut 'rownames' qui semble être un identifiant
df_acm = df.select_dtypes(include=['object', 'category'])

print(f"Analyse sur {df_acm.shape[0]} individus et {df_acm.shape[1]} variables.")
print("Variables :", df_acm.columns.tolist())

# 3. Réalisation de l'ACM
mca = prince.MCA(
    n_components=2,
    n_iter=3,
    copy=True,
    check_input=True,
    engine='sklearn',
    random_state=42
)

mca = mca.fit(df_acm)

# 4. Résultats : Valeurs propres (Inertie)
print("\n--- 1. Inertie (Valeurs Propres) ---")
print(mca.eigenvalues_summary)

# Calcul des corrections (Benzecri et Greenacre) pour le rapport
J = df_acm.shape[1] # Nombre de variables (9)
K = sum(df_acm[col].nunique() for col in df_acm.columns) # Nombre total de modalités
lambda_bar = 1 / J

print(f"\n--- Corrections d'Inertie ---")
print(f"Nombre de variables J = {J}")
print(f"Nombre total de modalités K = {K}")
print(f"Inertie moyenne (Seuil de Benzecri) lambda_bar = 1/{J} = {lambda_bar:.4f}")

eigenvalues = mca.eigenvalues_
print("\nValeurs propres brutes :")
for i, val in enumerate(eigenvalues):
    print(f"Axe {i+1}: {val:.4f}")

# 5. Résultats : Coordonnées des colonnes (Modalités)
# On affiche les coordonnées sur les 2 premiers axes pour aider à l'interprétation
coords = mca.column_coordinates(df_acm)
print("\n--- 2. Coordonnées des modalités (Axes 1 et 2) ---")
print(coords.sort_values(by=0)) # Trié par l'axe 1 pour voir les oppositions

# 6. Visualisation (Manuelle avec Matplotlib)
plt.figure(figsize=(12, 12))
ax = plt.gca()

# Récupération des coordonnées
x = coords[0]
y = coords[1]
labels = coords.index

# Tracé des points
ax.scatter(x, y, c='blue', marker='o', label='Modalités')

# Ajout des étiquettes
for i, label in enumerate(labels):
    ax.text(x[i]+0.02, y[i]+0.02, label, fontsize=9)

# Lignes des axes
plt.axhline(0, color='grey', linestyle='--', linewidth=0.8)
plt.axvline(0, color='grey', linestyle='--', linewidth=0.8)

# Titres et labels
plt.xlabel("Axe 1")
plt.ylabel("Axe 2")
plt.title("ACM - Carte des modalités (Health Insurance)")
plt.grid(True, alpha=0.3)

plt.savefig("acm_resultats.png")
print("\nGraphique sauvegardé sous 'acm_resultats.png'")
