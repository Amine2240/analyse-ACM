# Rapport d'Analyse des Données : Étude "Health Insurance" par ACM

**Binôme :** [Noms à compléter]  
**Date :** 28 Décembre 2025

---

## 1. Introduction et Objectifs

L'objectif de cette étude est d'explorer les relations entre les caractéristiques socio-démographiques, professionnelles et de santé d'une population de **8 802 individus**. 

Nous utilisons pour cela une **Analyse des Correspondances Multiples (ACM)**. Cette méthode factorielle est particulièrement adaptée car notre jeu de données est majoritairement composé de variables qualitatives (catégorielles). Elle nous permettra de résumer l'information, de visualiser les associations entre modalités et d'identifier des profils types d'individus.

## 2. Description des Données

Le jeu de données `HealthInsurance.csv` respecte les contraintes de l'étude :

* **Individus** : 8 802 observations.
* **Variables retenues pour l'ACM** : 9 variables qualitatives.
  * `health` (état de santé : yes/no)
  * `limit` (limitation de santé : yes/no)
  * `gender` (genre : male/female)
  * `insurance` (couverture assurance : yes/no)
  * `married` (statut marital : yes/no)
  *   `selfemp` (indépendant : yes/no)
  *   `region` (4 modalités : northeast, midwest, south, west)
  *   `ethnicity` (3 modalités : cauc, afam, other)
  *   `education` (7 modalités : none, highschool, bachelor, master, phd, ged, other)

Les variables quantitatives (`age`, `family`) n'ont pas été incluses directement dans l'ACM mais pourraient servir de variables illustratives ultérieurement.

## 3. Analyse de l'Inertie (Valeurs Propres)

### 3.1. Valeurs Propres Brutes

L'inertie totale représente la quantité d'information contenue dans le tableau de données.

| Axe (Composante) | Valeur Propre ($\lambda$) | % de Variance | % Cumulé |
| :--- | :--- | :--- | :--- |
| **Axe 1** | 0.1612 | **8.53%** | 8.53% |
| **Axe 2** | 0.1464 | **7.75%** | **16.29%** |

### 3.2. Correction de l'Inertie (Benzécri)

En ACM, les pourcentages d'inertie bruts sont souvent pessimistes (faibles) en raison du grand nombre de modalités. Pour mieux évaluer la part d'information expliquée, nous appliquons la correction de Benzécri.

**Paramètres :**
*   Nombre de variables $P = 9$
*   Inertie moyenne (seuil) $\bar{\lambda} = 1/P = 1/9 \approx 0.1111$

Seules les valeurs propres supérieures à ce seuil ($\lambda > 0.1111$) sont retenues pour l'interprétation.

**Formule de correction :**
$$ \tilde{\lambda} = \left( \frac{P}{P-1} (\lambda - \frac{1}{P}) \right)^2 $$

**Calculs :**

*   **Axe 1** ($\lambda_1 = 0.1612$) :
    $$ \tilde{\lambda}_1 = \left( \frac{9}{8} (0.1612 - 0.1111) \right)^2 \approx 0.00317 $$

*   **Axe 2** ($\lambda_2 = 0.1464$) :
    $$ \tilde{\lambda}_2 = \left( \frac{9}{8} (0.1464 - 0.1111) \right)^2 \approx 0.00157 $$

*   **Inertie Totale Corrigée** (somme des $\tilde{\lambda}$) : $\approx 0.00474$

**Pourcentages Corrigés :**

| Axe | % Inertie Corrigée | Interprétation |
| :--- | :--- | :--- |
| **Axe 1** | **66.9%** | L'axe 1 explique en réalité les deux tiers de l'information structurelle majeure. |
| **Axe 2** | **33.1%** | L'axe 2 explique le tiers restant. |

**Conclusion sur l'inertie** : Après correction, on constate que les deux premiers axes résument la quasi-totalité de l'information pertinente (au sens de Benzécri). L'interprétation du plan 1-2 est donc très robuste.

## 4. Interprétation des Axes Factoriels

L'analyse des coordonnées des modalités (voir graphique `acm_resultats.png`) permet de donner un sens aux axes.

### 4.1. Axe 1 : Le gradient "Statut Socio-Économique & Santé"

Cet axe horizontal est le plus structurant (66.9% de l'inertie corrigée). Il oppose clairement deux situations :

*   **Côté Négatif (Gauche)** : On trouve les modalités associées à un niveau d'éducation élevé et une situation stable.
    *   `education__master` (-0.99), `education__bachelor` (-0.51)
    *   `insurance__yes` (-0.35) (Assuré)
    *   `married__yes` (-0.26)

*   **Côté Positif (Droite)** : On trouve les indicateurs de précarité sociale et sanitaire.
    *   `education__none` (+1.55) (Aucun diplôme), `education__ged` (+0.64)
    *   `insurance__no` (+1.39) (Non assuré)
    *   `health__no` (+0.96) (Mauvaise santé)
    *   `ethnicity__afam` (+0.54) (Afro-américain)

**Synthèse Axe 1** : Il discrimine les individus selon leur **capital social et sanitaire**. Il oppose les populations favorisées et assurées aux populations plus vulnérables.

### 4.2. Axe 2 : Distinction "Statut Professionnel & Démographie"

Cet axe vertical apporte une nuance supplémentaire (33.1% de l'inertie corrigée) :

*   **Côté Positif (Haut)** : Il isole un profil très spécifique.
    *   `education__phd` (+1.97) (Doctorat)
    *   `selfemp__yes` (+1.26) (Travailleurs indépendants)
    *   `ethnicity__other` (+1.16)

*   **Côté Négatif (Bas)** : Il regroupe des caractéristiques démographiques plus générales.
    *   `ethnicity__afam` (-1.61)
    *   `married__no` (-0.60) (Célibataire)
    *   `gender__female` (-0.41) (Femme)

**Synthèse Axe 2** : Cet axe semble isoler les **travailleurs indépendants hautement qualifiés** (souvent des profils atypiques dans les données de santé) par rapport au reste de la population, notamment les femmes célibataires issues de minorités.

## 5. Conclusion

L'Analyse des Correspondances Multiples a permis de structurer l'information contenue dans la base `HealthInsurance`. 

1.  **Hiérarchie des facteurs** : Le facteur principal (Axe 1) est socio-économique. Il montre que l'absence de diplôme est le vecteur principal de la précarité (absence d'assurance et mauvaise santé).
2.  **Profils types** :
    *   **Type A (Gauche)** : Individus mariés, éduqués (Master/Bachelor), assurés.
    *   **Type B (Droite)** : Individus sans diplôme, non assurés, en mauvaise santé.
    *   **Type C (Haut)** : Indépendants avec un très haut niveau d'étude (PhD).

Cette analyse suggère que les politiques de santé publique devraient cibler prioritairement les populations à faible niveau d'éducation, qui cumulent les risques de non-assurance et de mauvaise santé.

---
## Annexe : Code Python utilisé

Le code source complet et les fichiers du projet sont disponibles sur le dépôt GitHub suivant :  
**[https://github.com/Amine2240/analyse-ACM](https://github.com/Amine2240/analyse-ACM)**

### Aperçu du script principal (`preparation.py`)

```python
import pandas as pd
import prince
import matplotlib.pyplot as plt

# 1. Chargement
df = pd.read_csv("HealthInsurance.csv")
df_acm = df.select_dtypes(include=['object', 'category'])

# 2. ACM
mca = prince.MCA(n_components=2, engine='sklearn')
mca = mca.fit(df_acm)

# 3. Résultats
print(mca.eigenvalues_summary)
coords = mca.column_coordinates(df_acm)

# 4. Graphique
mca.plot(df_acm)
plt.show()
```
