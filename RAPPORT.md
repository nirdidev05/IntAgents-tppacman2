# RAPPORT

## Partie 1: Value Iteration

### Question 1

*Préciser le détail du calcul de la politique gloutonne pour les 3 premières itérations de Value Iteration dans l'environnement BookGrid avec les paramètres par défaut*

**Paramètres :** γ = 0.9, noise = 0.2, livingReward = 0
**Modèle stochastique :** T(s, a, s_voulu) = 0.8 ; T(s, a, s_perp) = 0.1 × 2
**Récompenses :** R((3,2), exit, TERMINAL) = +1 ; R((3,1), exit, TERMINAL) = −1 ; R = 0 sinon

**Layout BookGrid** (colonne, ligne) :

```
(0,2)  (1,2)  (2,2)  [+1]=(3,2)
(0,1)  [mur]  (2,1)  [-1]=(3,1)
(0,0)  (1,0)  (2,0)   (3,0)
```

La politique gloutonne à l'itération k est :
**π_k(s) = argmax_a Σ_{s'} T(s,a,s') · [R(s,a,s') + γ · V_k(s')]**

---

#### Itération 0 (initialisation)

V_0(s) = 0 pour tout s.
Politique : arbitraire (toutes les Q-valeurs sont nulles).

---

#### Itération 1 : calcul de V_1 à partir de V_0

Pour tout état non-terminal :
V_1(s) = max_a Σ_{s'} T(s,a,s') · [R(s,a,s') + 0.9 · V_0(s')]

Comme V_0 = 0 partout, seuls les états disposant d'une récompense immédiate obtiennent une valeur non nulle.

**État (3,2)** — seule action : exit → TERMINAL avec R = +1 :
V_1(3,2) = 1 × (+1 + 0.9 × 0) = **1.00**

**État (3,1)** — seule action : exit → TERMINAL avec R = −1 :
V_1(3,1) = 1 × (−1 + 0.9 × 0) = **−1.00**

**Tous les autres états** — R = 0 partout et V_0 = 0 :
V_1(s) = 0.00

**Politique gloutonne π_1** — calculée avec V_1 :
Q((2,2), east, V_1) = 0.8·(0.9·1.00) + 0.1·(0.9·0) + 0.1·(0.9·0) = **0.72** → π_1(2,2) = east
Q((2,1), north, V_1) = 0.8·(0.9·0) + 0.1·(0.9·0) + 0.1·(0.9·(−1)) = **−0.09** → à comparer aux autres actions
Pour les états avec V_1 = 0 partout dans leur voisinage : Q = 0 pour toutes les actions → politique arbitraire.

---

#### Itération 2 : calcul de V_2 à partir de V_1

**État (2,2)** — actions depuis (2,2) avec noise=0.2 :

| Action | Transitions (s', prob)            | Q((2,2), a, V_1)                              |
| ------ | --------------------------------- | --------------------------------------------- |
| east   | (3,2):0.8 ; (2,2):0.1 ; (2,1):0.1 | 0.8·0.9·1 + 0.1·0 + 0.1·0 =**0.72** |
| north  | (2,2):0.8 ; (1,2):0.1 ; (3,2):0.1 | 0 + 0 + 0.1·0.9·1 = 0.09                    |
| south  | (2,1):0.8 ; (1,2):0.1 ; (3,2):0.1 | 0 + 0 + 0.1·0.9·1 = 0.09                    |
| west   | (1,2):0.8 ; (2,2):0.1 ; (2,1):0.1 | 0 + 0 + 0 = 0                                 |

V_2(2,2) = max(0.72, 0.09, 0.09, 0) = **0.72**
Pour tous les autres états non-terminaux : V_2(s) = 0.00 (V_1 = 0 dans leur voisinage)

**Politique gloutonne π_2** — calculée avec V_2 :
Q((2,2), east, V_2) = 0.8·0.9·1 + 0.1·0.9·0.72 = 0.72 + 0.0648 = 0.7848 → π_2(2,2) = east
Q((1,2), east, V_2) = 0.8·0.9·0.72 + 0.1·0 + 0.1·0 = **0.5184** → π_2(1,2) = east
Q((2,1), north, V_2) = 0.8·0.9·0.72 + 0.1·0.9·0 + 0.1·0.9·(−1) = 0.5184 − 0.09 = **0.4284** → π_2(2,1) = north

---

#### Itération 3 : calcul de V_3 à partir de V_2

États avec V_2 ≠ 0 : (3,2)=1.00, (3,1)=−1.00, (2,2)=0.72

**État (2,2)** :
Q((2,2), east, V_2) = 0.8·0.9·1 + 0.1·0.9·0.72 + 0.1·0.9·0 = 0.72 + 0.0648 = **0.7848**
V_3(2,2) = **0.7848**

**État (1,2)** :
Q((1,2), east, V_2) = 0.8·0.9·0.72 + 0.1·0.9·0 + 0.1·0.9·0 = **0.5184**
V_3(1,2) = **0.5184**

**État (2,1)** :
Q((2,1), north, V_2) = 0.8·0.9·0.72 + 0.1·0.9·0 + 0.1·0.9·(−1) = 0.5184 − 0.09 = **0.4284**
V_3(2,1) = **0.4284**

**Politique gloutonne π_3** — calculée avec V_3 :

| État  | Meilleure action  | Q-valeur |
| ------ | ----------------- | -------- |
| (3,2)  | exit              | 1.00     |
| (3,1)  | exit              | −1.00   |
| (2,2)  | east              | 0.8292   |
| (1,2)  | east              | 0.6584   |
| (2,1)  | north             | 0.5136   |
| Autres | arbitraire (Q≈0) | —       |

Les valeurs obtenues correspondent exactement aux captures d'écran de l'interface graphique (`python gridworld.py -a value -i 3 -k 0 -v`).

### Question 2

*Modifier un seul des 2 paramètres (noise ou discount) pour obtenir une politique optimale qui permet à l'agent de traverser le pont (s'il n'était pas soumis au bruit). Préciser le paramètre modifié et sa valeur dans votre rapport et justifier votre choix.*

**Paramètre modifié : `noise = 0.0`** (valeur par défaut : 0.2)

**Commande :** `python gridworld.py -g BridgeGrid -a value --noise 0.0`

*(sans `-k`, Value Iteration converge par défaut avant que l'agent agisse)*

**Politique obtenue sur le pont :**
Tous les états de la ligne centrale (le pont) pointent vers `east` → l'agent traverse jusqu'à l'état absorbant +10.

**Justification :**

Le BridgeGrid est un couloir étroit (une seule ligne de largeur) bordé de deux falaises à −100.
Avec `noise = 0.2`, chaque action a 20 % de chances d'aller perpendiculairement (10 % gauche + 10 % droite), c'est-à-dire de tomber dans une falaise (−100). Le risque rend le coût espéré de traverser le pont trop élevé : l'agent préfère sortir par le +1 à gauche plutôt que de risquer −100 pour atteindre +10.

Avec `noise = 0.0`, l'environnement est **déterministe** : l'agent va exactement là où il le décide, sans risque de glisser. Le gain espéré de traverser le pont jusqu'à +10 devient alors supérieur à sortir immédiatement par +1, et la politique optimale devient : aller `east` sur tout le pont.

Modifier le `discount` seul ne suffit pas : quelle que soit sa valeur (0.9 à 1.0), tant que `noise = 0.2`, la pénalité espérée des falaises reste dominante et l'agent refuse de traverser.

### Question 3

*Modifier un seul des 3 paramètres (noise, discount, livingReward) pour obtenir les politiques optimales ci-dessous. Préciser pour chaque politique, le paramètre modifié et sa valeur dans votre rapport et justifier votre choix.*

1. qui suit un chemin risqué pour atteindre l’état absorbant de récompense +1 ;
2. qui suit un chemin risqué pour atteindre l’état absorbant de récompense +10 ;
3. qui suit un chemin sûr pour atteindre l’état absorbant de récompense +1 ;
4. qui évite les états absorbants

**Rappel :** les valeurs par défaut (noise=0.2, discount=0.9, livingReward=0) donnent une politique qui suit le **chemin sûr vers +10**.

**Layout DiscountGrid** (simplifié) :

```
Ligne 4 (haut) : (0,4) (1,4) (2,4) (3,4) (4,4)   ← chemin sûr
Ligne 3       : (0,3) [mur] (2,3) (3,3) (4,3)
Ligne 2       :              [+1]=(2,2)  [+10]=(4,2)
Ligne 1       : (0,1) (1,1) (2,1) (3,1) (4,1)   ← chemin risqué (près de la falaise)
Ligne 0       : [-10] [-10] [-10] [-10] [-10]     ← falaise (états absorbants négatifs)
```

---

#### Politique 1 : chemin risqué → +1

**Paramètre modifié : `livingReward = -2.0`**

**Commande :** `python gridworld.py -a value -g DiscountGrid --livingReward -2.0`

**Politique obtenue :** (0,1)→east → (1,1)→east → (2,1)→north → (2,2)→exit → **+1**

**Justification :** avec livingReward = −2, chaque pas coûte −2. L’agent veut sortir rapidement pour limiter les pénalités cumulées. Le +1 en (2,2) est plus proche (3 pas via la ligne 1) que le +10 en (4,2) (5 pas). L’agent préfère donc +1, même si la récompense est plus faible. Il passe par la ligne 1 (chemin risqué, proche de la falaise −10) car c’est le trajet le plus court : le chemin sûr par les lignes 3-4 prend beaucoup plus de pas, ce qui accumule plus de pénalités.

---

#### Politique 2 : chemin risqué → +10

**Paramètre modifié : `noise = 0.0`** (valeur par défaut : 0.2)

**Commande :** `python gridworld.py -a value -g DiscountGrid --noise 0.0`

**Politique obtenue :** (0,1)→east → (1,1)→east → (2,1)→east → (3,1)→east → (4,1)→north → (4,2)→exit → **+10**

**Justification :** avec noise = 0, l’environnement est déterministe. L’agent ne risque plus de glisser dans la falaise −10 en passant par la ligne 1. Le chemin risqué (ligne 1) est le plus court vers +10, et comme il n’y a plus de risque de chute, c’est le chemin optimal. Le +10 est préféré au +1 car γ = 0.9 ne le réduit que légèrement (10 × 0.9⁵ ≈ 5.9 > 1 × 0.9³ ≈ 0.73).

---

#### Politique 3 : chemin sûr → +1

**Paramètre modifié : `discount = 0.1`** (valeur par défaut : 0.9)

**Commande :** `python gridworld.py -a value -g DiscountGrid --discount 0.1`

**Politique obtenue :** (0,1)→north → (0,2)→north → (0,3)→north → (0,4)→east → (1,4)→east → (2,4)→south → (2,3)→south → (2,2)→exit → **+1**

**Justification :** avec γ = 0.1, l’agent est très myope et préfère les récompenses proches. Le +10 en (4,2) est loin (∼9 pas) et vaut seulement 10 × 0.1⁹ ≈ 0.005, tandis que le +1 en (2,2) via le chemin sûr (∼7 pas) vaut 1 × 0.1⁷ ≈ 0.000013 — les deux sont faibles, mais le +1 est relativement plus accessible. L’agent conserve le chemin sûr (lignes 3-4) car avec noise = 0.2, le chemin risqué (ligne 1) expose l’agent à la falaise −10, ce qui représente une perte catastrophique que même la myopie ne peut ignorer.

---

#### Politique 4 : éviter les états absorbants

**Paramètre modifié : `livingReward = 10.0`** (valeur par défaut : 0)

**Commande :** `python gridworld.py -a value -g DiscountGrid --livingReward 10.0`

**Politique obtenue :** l’agent ne sort jamais. Il boucle indéfiniment dans les cases non-terminales, récoltant +10 à chaque pas.

**Justification :** avec livingReward = +10, chaque pas rapporte +10. La somme des récompenses actualisées d’une boucle infinie est 10/(1−0.9) = 100, bien supérieure à n’importe quelle sortie (+10 ou +1). L’agent maximise son gain en restant en vie le plus longtemps possible. La politique pointe systématiquement loin des exits et de la falaise : vers les coins du plateau (north, west aux bords).

## Partie 2: QLearning tabulaire

### Question 4

*Précisez le détail du calcul des qvaleurs pour les 4 premiers épisodes.*

On utilise les paramètres par défaut du Q-learning sur le gridworld : α = 0.5, γ = 0.9.
Au départ, toutes les Q-valeurs sont initialisées à 0.

On rappelle la formule de mise à jour qu'on applique à chaque transition :
Q(s,a) ← (1−α)·Q(s,a) + α·[r + γ·max_b Q(s',b)]

Comme demandé dans le README, on fait jouer l'agent en mode manuel (`-m`) avec ces trajectoires :
- Épisodes 1 et 2 : on monte tout au nord puis on va à l'est → on arrive en (3,2) → exit avec récompense +1
- Épisodes 3 et 4 : on va tout à l'est puis on monte au nord → on arrive en (3,1) → exit avec récompense −1

---

#### Épisode 1 : (0,0)→N→(0,1)→N→(0,2)→E→(1,2)→E→(2,2)→E→(3,2)→exit→+1

Vu que toutes les Q-valeurs valent 0 au départ, à chaque étape on a max Q(s') = 0 et la récompense vaut 0 aussi, donc les mises à jour ne changent rien... sauf la toute dernière transition où on reçoit enfin r = +1 :

| Étape | s | a | s' | r | sample = r + γ·max Q(s') | Q(s,a) ← |
|-------|---|---|----|---|--------------------------|-----------|
| 1-5 | (0,0)→...→(2,2) | north/east | ... | 0 | 0 + 0.9×0 = 0 | reste à 0 |
| 6 | (3,2) | exit | TERMINAL | **+1** | 1 + 0.9×0 = 1 | 0.5×0 + 0.5×1 = **0.5** |

Après cet épisode, on a une seule Q-valeur non nulle : Q((3,2), exit) = **0.5**

---

#### Épisode 2 : même trajectoire

Cette fois c'est plus intéressant. Quand on arrive en (2,2) et qu'on fait east vers (3,2), le max Q((3,2)) n'est plus 0 mais 0.5 (grâce à l'épisode 1). Du coup la valeur se propage :

| Étape | s | a | s' | r | sample | Q(s,a) ← |
|-------|---|---|----|---|--------|-----------|
| 1-4 | (0,0)→...→(1,2) | ... | ... | 0 | 0 | reste à 0 |
| 5 | (2,2) | east | (3,2) | 0 | 0 + 0.9×**0.5** = 0.45 | 0.5×0 + 0.5×0.45 = **0.225** |
| 6 | (3,2) | exit | TERMINAL | +1 | 1 + 0.9×0 = 1 | 0.5×0.5 + 0.5×1 = **0.75** |

On voit ici un truc important : l'info de récompense se **propage en arrière**. Au 1er épisode, seul (3,2) avait appris quelque chose. Au 2e, c'est (2,2) qui récupère une Q-valeur parce qu'il sait maintenant que (3,2) a de la valeur.

Q-valeurs non nulles : Q((2,2), east) = **0.225**, Q((3,2), exit) = **0.75**

---

#### Épisode 3 : (0,0)→E→(1,0)→E→(2,0)→E→(3,0)→N→(3,1)→exit→−1

On change de chemin : on va vers l'est par le bas, et on tombe sur l'état −1. Même logique, toutes les Q-valeurs sur ce chemin sont à 0, seule la dernière transition change quelque chose :

| Étape | s | a | s' | r | sample | Q(s,a) ← |
|-------|---|---|----|---|--------|-----------|
| 1-4 | (0,0)→...→(3,0) | east/north | ... | 0 | 0 | reste à 0 |
| 5 | (3,1) | exit | TERMINAL | **−1** | −1 + 0.9×0 = −1 | 0.5×0 + 0.5×(−1) = **−0.5** |

Q-valeurs non nulles : Q((2,2), east) = 0.225, Q((3,1), exit) = **−0.5**, Q((3,2), exit) = 0.75

---

#### Épisode 4 : même trajectoire que l'épisode 3

Comme pour l'épisode 2, la 2e fois qu'on passe par ce chemin, l'info se propage d'un cran en arrière. (3,0) apprend que monter vers (3,1) c'est une mauvaise idée :

| Étape | s | a | s' | r | sample | Q(s,a) ← |
|-------|---|---|----|---|--------|-----------|
| 1-3 | (0,0)→...→(2,0) | east | ... | 0 | 0 | reste à 0 |
| 4 | (3,0) | north | (3,1) | 0 | 0 + 0.9×(−0.5) = **−0.45** | 0.5×0 + 0.5×(−0.45) = **−0.225** |
| 5 | (3,1) | exit | TERMINAL | −1 | −1 + 0 = −1 | 0.5×(−0.5) + 0.5×(−1) = **−0.75** |

Q-valeurs non nulles finales :

| Couple (s, a) | Q-valeur |
|---------------|----------|
| Q((2,2), east) | 0.225 |
| Q((3,2), exit) | 0.75 |
| Q((3,0), north) | −0.225 |
| Q((3,1), exit) | −0.75 |

Ce qu'on remarque, c'est qu'après 4 épisodes, seuls les états proches des terminaux ont des Q-valeurs non nulles. L'information se propage lentement : un état de plus par épisode. C'est très différent de Value Iteration qui met à jour tous les états d'un coup à chaque itération.

### Question 5

*Expliquer les différences entre le résultat obtenu avec epsilon à 0.1 et à 0.9.*

**Commandes :**
- `python gridworld.py -a q -k 100 --noise 0.0 -e 0.1 -q`
- `python gridworld.py -a q -k 100 --noise 0.0 -e 0.9 -q`

Avec **ε = 0.1**, l'agent ne prend une action aléatoire que 10% du temps. Dès qu'il a trouvé le bon chemin vers +1, il l'exploite presque systématiquement. Du coup le return moyen pendant l'entraînement est plutôt bon (~0.39), parce que l'agent suit la bonne politique 90% du temps.

Avec **ε = 0.9**, c'est l'inverse : l'agent fait n'importe quoi 90% du temps. Il explore énormément, ce qui fait qu'il se retrouve souvent dans l'état −1 ou qu'il erre dans la grille sans but. Le return moyen est du coup très faible (~0.015).

Ce qui est intéressant c'est que dans les deux cas, la politique apprise (les Q-valeurs) converge vers la même politique optimale. Avec ε = 0.9, l'agent a visité beaucoup plus de couples (s,a) différents grâce à l'exploration, mais ça ne lui a pas donné un avantage ici vu que la grille est petite.

En résumé : ε petit = bon return pendant l'entraînement mais risque de pas assez explorer, ε grand = return faible mais meilleure exploration. C'est le dilemme **exploration vs exploitation** qu'on a vu en cours. En pratique, une valeur intermédiaire (genre 0.1 à 0.3) est un bon compromis.

### Question 6

*Préciser comment est modélisé l'environnement robot crawler sous forme de MDP (état, action, récompense) ainsi que la dimension de S. Quel est le comportement attendu de l'agent s'il suit sa politique optimale ?*

**Commande :** `python crawler.py`

En regardant le code de `crawler.py`, on peut décrire le MDP du robot :

**États (S) :** chaque état correspond à une position (angleBras, angleMain). Les angles sont discrétisés :
- le bras a **9 positions** possibles (entre un angle min et max)
- la main a **13 positions** possibles

Donc au total on a **|S| = 9 × 13 = 117 états**.

**Actions (A) :** à chaque état, l'agent peut faire entre 2 et 4 actions :
- `arm-up` / `arm-down` : monter ou descendre l'angle du bras
- `hand-up` / `hand-down` : monter ou descendre l'angle de la main

Aux bords (quand le bras ou la main est à son angle min ou max), certaines actions ne sont pas disponibles.

**Récompense (R) :** c'est simplement le déplacement horizontal du robot : R = newX − oldX. Si le robot avance vers la droite, la récompense est positive ; s'il recule, elle est négative.

**Comportement optimal :** quand l'agent a appris sa politique optimale, on voit le robot qui rampe de manière fluide vers la droite. Il enchaîne un mouvement cyclique de bras et de main (un peu comme un mouvement de nage) qui maximise son avancement à chaque pas. C'est assez satisfaisant à regarder dans l'interface graphique.

### Question 7

*Expliquer les résultats obtenus et préciser dans le rapport les solutions que l'on peut mettre en place pour améliorer ces résultats.*

### Question 8

*Expliquer dans le rapport les features que vous avez implémentées et leurs rôles. Présenter et analyser les résultats obtenus.*
