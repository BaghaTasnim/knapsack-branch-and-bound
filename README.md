# TP Branch-and-Bound : Problème du Sac-à-Dos

**Auteur :** Tasnim BAGHA  
**Groupe :** 1  
**Cours :** Recherche Opérationnelle - 4ème année ingénieur


## Dépôt GitHub

Le code source complet, les instances de test et les résultats sont disponibles sur GitHub :  
[(https://github.com/BaghaTasnim/knapsack-branch-and-bound.git)](https://github.com/BaghaTasnim/knapsack-branch-and-bound.git)




## À propos

Ce projet implémente l'algorithme Branch-and-Bound pour résoudre le problème du sac-à-dos 0-1. C'est un travail que j'ai réalisé dans le cadre du cours de Recherche Opérationnelle. L'objectif était de développer une méthode exacte capable de trouver la solution optimale pour des instances de taille moyenne (jusqu'à 30 articles).

## Structure du projet

Voici comment j'ai organisé mon code :

```
TP_Branch_and_Bound/
├── src/
│   ├── __init__.py              # Package principal
│   ├── data_reader.py           # Lecture des fichiers d'instances
│   ├── greedy_algorithms.py     # Algorithmes gloutons (fractionnaire et entier)
│   ├── branch_and_bound.py      # Implémentation de B&B
│   └── main.py                  # Programme principal avec menu interactif
├── instances/
│   ├── instance_1.txt           # Instance simple (3 articles)
│   ├── instance_2.txt           # Instance moyenne (10 articles)
│   ├── instance_3.txt           # 15 articles
│   ├── instance_4.txt           # 20 articles
│   ├── instance_5.txt           # 25 articles
│   ├── instance_6.txt           # 30 articles
│   └── instance_7.txt           # Instance difficile (22 articles, ratios similaires)
├── results/                     # Graphiques et résultats générés
├── create_instances.py          # Script pour générer les instances de base
├── create_large_instances.py    # Script pour générer les instances 5, 6, 7
├── rapport_tasnim_bagha_g1.md   # Rapport de ce tp 
├── README.md                    # Ce fichier
└── requirements.txt             # Dépendances Python
```

## Installation

Pour faire tourner le programme, vous aurez besoin de Python 3.7 ou supérieur.

**1. Cloner ou télécharger le projet**

Si vous avez le fichier zip, extrayez-le. Sinon, clonez le dépôt.

**2. Installer les dépendances**

J'utilise numpy pour quelques calculs, matplotlib pour les graphiques, et tabulate pour l'affichage des tableaux :

```bash
pip install -r requirements.txt
```

Si pip n'est pas disponible, vous pouvez installer manuellement :
```bash
pip install numpy matplotlib tabulate
```

**3. Créer les instances de test**

Les instances sont déjà fournies dans le dossier `instances/`, mais si vous voulez les régénérer :

```bash
python create_instances.py
python create_large_instances.py
```

## Utilisation

### Lancer le programme en mode interactif

C'est la méthode que je recommande pour tester le programme :

```bash
cd src
python main.py
```

Vous verrez un menu avec 4 options :
1. Résoudre une instance spécifique
2. Comparer les performances avec/sans tri
3. Exécuter toutes les instances et générer les graphiques
4. Quitter

### Exemples d'utilisation en ligne de commande

**Résoudre une instance :**
```bash
cd src
python main.py ../instances/instance_1.txt
```

**Comparer avec et sans tri :**
```bash
python main.py --compare ../instances/instance_3.txt
```

**Exécuter toutes les instances :**
```bash
python main.py --all
```

## Format des instances

Les fichiers d'instance ont un format très simple :
```
W          # Capacité du conteneur
n          # Nombre d'articles
w1 v1      # Poids et valeur de chaque article
w2 v2
...
wn vn
```

Par exemple, `instance_1.txt` :
```
50
3
10 60
20 100
30 120
```

## Comment ça marche ?

Mon implémentation utilise trois algorithmes principaux :

### 1. Algorithme glouton fractionnaire
Cet algorithme résout la relaxation linéaire du problème (on peut prendre des fractions d'articles). Je l'utilise pour calculer les bornes supérieures dans l'arbre de recherche.

### 2. Algorithme glouton entier
Version entière du précédent. Il me permet d'obtenir rapidement une première solution réalisable qui sert de borne inférieure.

### 3. Branch-and-Bound
C'est l'algorithme principal. Il explore l'arbre des solutions de manière intelligente :
- Tri préalable des articles par ratio valeur/poids (optionnel)
- Exploration en profondeur d'abord (DFS)
- Calcul des bornes supérieures pour élaguer les branches non prometteuses
- À chaque nœud : décision de prendre ou non l'article suivant

L'algorithme garde trace du nombre de nœuds explorés et élagués, ce qui permet d'analyser son efficacité.

## Résultats obtenus

Voici un aperçu des résultats sur les 7 instances de test :

| Instance       | Articles | Valeur optimale | Nœuds explorés | Temps (s) |
|----------------|----------|-----------------|----------------|-----------|
| instance_1.txt | 3        | 220             | 8              | < 0.001   |
| instance_2.txt | 10       | 309             | 5              | < 0.001   |
| instance_3.txt | 15       | 1458            | 103            | < 0.001   |
| instance_4.txt | 20       | 4152            | 2174           | 0.017     |
| instance_5.txt | 25       | 1790            | 47             | 0.004     |
| instance_6.txt | 30       | 2427            | 44             | < 0.001   |
| instance_7.txt | 22       | 966             | 13390          | 0.056     |

L'instance 7 est particulièrement intéressante : bien qu'elle n'ait que 22 articles, elle est beaucoup plus difficile à résoudre car tous les articles ont des ratios valeur/poids très similaires (entre 1.8 et 2.5). Cela rend l'élagage moins efficace.

### Impact du tri

J'ai testé l'impact du tri des articles par ratio v/w décroissant. Les résultats sont mitigés :
- Pour certaines instances (3, 5, 6), le tri réduit drastiquement le nombre de nœuds (jusqu'à 89%)
- Pour d'autres (4, 7), le tri augmente le nombre de nœuds !

Cela m'a appris qu'il n'y a pas de stratégie universelle : l'efficacité dépend de la structure des données.

## Ce que j'ai appris

Ce TP m'a permis de :
- Comprendre en profondeur le fonctionnement de Branch-and-Bound
- Voir l'importance des bornes pour l'élagage
- Réaliser que les choix de conception (ordre de tri, stratégie d'exploration) ont un impact majeur
- Développer une analyse expérimentale rigoureuse

Les difficultés rencontrées :
- Gérer correctement l'élagage (s'assurer qu'on ne coupe pas de branches contenant l'optimum)
- Comprendre pourquoi certaines instances sont plus difficiles que d'autres
- Optimiser le code pour éviter les calculs redondants

## Améliorations possibles

Si j'avais plus de temps, j'aimerais :
- Implémenter d'autres stratégies d'exploration (Best-First, A*)
- Ajouter des prétraitements pour détecter les articles obligatoires
- Comparer avec d'autres méthodes (programmation dynamique, métaheuristiques)
- Paralléliser l'exploration des branches
- Tester sur des instances encore plus grandes

## Problèmes connus

- Pour instance_5, il y a un bug d'affichage du poids total (affiche -19 au lieu du poids réel)
- Pour instance_7, idem (affiche 20 au lieu de ~430)
- Le calcul du poids total semble ne pas prendre en compte tous les articles sélectionnés dans l'affichage

Ces bugs n'affectent pas la résolution elle-même (les solutions sont correctes), juste l'affichage.

## Dépendances

- **numpy** : Pour quelques opérations mathématiques
- **matplotlib** : Pour générer les graphiques comparatifs
- **tabulate** : Pour afficher les tableaux de résultats de façon propre


---

**Projet réalisé dans le cadre du cours de Recherche Opérationnelle**  
