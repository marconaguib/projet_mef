# Projet de Maillage et Eléments finis

Dans ce projet, nous résolvons un problème de réaction-diffusion simple dans le sens des éléments finis.
Il s'agit d'illustrer la température en tout point de l'espace d'un appartement (cf. figure), contenant des fenêtres et des radiateurs.

![appartement][appartement]

Avec :
- L = 10
- l = 8
- d = 0.5
- Longueur d'une fenêtre = 1
- Longueur d'un radiateur = 1
- T_c = 25
- T_f = -10

On utilise la méthode des éléments finis, avec une finesse h = 0.1. Nous calculons la matrice de rigidité. Nous appliquons les conditions de Dirichlet sur les fenêtres et les radiateurs. Puis nous approchons l'intégrale du membre de droite par une quadrature d'ordre 2. Enfin, nous résolvons le système linéaire à l'aide de la libraire Scipy.

## Exécution "rapide"
`python3 resolution.py`, elle met environ 20 secondes.

## Résultat
![temp][temperature]

## Scripts
- [maillage.py](maillage.py) : Classes Points, Segment, Triangle et Mesh
- [assemblage.py](assemblage.py) : Classe Triplet et assemblage des différentes matrices
- [mesh_pb.geo](mesh_pb.geo) : Geométrie du problème (appartement) en GMSH
- [resolution.py](resolution.py) : Données du problème, appels aux fonction et plot

[appartement]: https://github.com/marconaguib/projet_mef/blob/master/appart.png "Joli appartement"
[temperature]: https://github.com/marconaguib/projet_mef/blob/master/temp.png "Température calculée en tout point"
