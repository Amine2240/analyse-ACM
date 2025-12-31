import pandas as pd

# 1. Charger le tableau
try:
    df = pd.read_csv("HealthInsurance.csv")
    print("Fichier chargé avec succès.\n")
except FileNotFoundError:
    print("Erreur : Le fichier 'HealthInsurance.csv' est introuvable.")
    exit()

# 2. Vérification des contraintes de l'énoncé

# A. Nombre d'individus (> 200)
n_individus = len(df)
print(f"--- Contrainte 1 : Nombre d'individus ---")
print(f"Nombre de lignes : {n_individus}")
if n_individus >= 200:
    print(" OK (> 200)")
else:
    print(" Pas assez d'individus")

# B. Types de variables (4 Quali, 1 Quanti)
# On considère 'object' et 'category' comme qualitatif, et 'int64'/'float64' comme quantitatif
vars_quali = df.select_dtypes(include=['object', 'category']).columns.tolist()
vars_quanti = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

print(f"\n--- Contrainte 2 : Types de variables ---")
print(f"Variables Qualitatives ({len(vars_quali)}) : {vars_quali}")
print(f"Variables Quantitatives ({len(vars_quanti)}) : {vars_quanti}")

if len(vars_quali) >= 4 and len(vars_quanti) >= 1:
    print("OK (Au moins 4 Quali et 1 Quanti)")
else:
    print("Manque de variables (Vérifie les types)")

# C. Nombre de modalités (> 2 pour au moins 2 variables)
print(f"\n--- Contrainte 3 : Nombre de modalités ---")
count_sup_2 = 0
for col in vars_quali:
    n_mod = df[col].nunique()
    print(f" - {col} : {n_mod} modalités")
    if n_mod > 2:
        count_sup_2 += 1

if count_sup_2 >= 2:
    print(f"OK ({count_sup_2} variables ont plus de 2 modalités)")
else:
    print("Pas assez de diversité dans les modalités")

# Aperçu final
print("\n--- Aperçu des données ---")
print(df.head())
