# Voxel Pandemia

## Posons le problème

Ce script python vise à résoudre le problème suivant :

Considérons un cube de largeur N, composer lui-même de cube de largeur 1.
La Voxel Pandemia se traduit par la transformaiton à l'instant 0 d'un cube en un cube contaminé
à une position initial x, y et z. Pour les t+1 suivants la contamination suit la rgèle suivante :

Pour chaque cube contaminé à un instant, tout les cubes saints en contact avec celui-ci par une face seront contaminé
à l'instant t+1. La pandémie se termine lorsque tout les cubes ont été contaminé.

L'objectif est donc de concevoir un alogrithme permettant connaître l'évolution du virus pour toutes les positions de départs possibles.

## Solution proposée

Afin de résoudre ce problème, l'idée la plus simple et de regarder en 2 dimensions.
On constate rapidement un propagation du virus avec une forme de losange et à la notion même d'instant t et t+1
du problème nous pousse à donner une solution dont le calcul nécessite de prendre en compte les instants précédants.
On peut donc facilement concevoir un alogrithme basique prenant en entrée un état A de la population de cube à un instant t et retournant
un état B correspondant à la population à l'instant t+1.

La proposition d'un tel algoritme était l'idée de départ et s'optimise assez facilement tout d'abord en prenant en compte les axes de symétrie du cube, et la possibilité de regarder à un instant t uniquement les cubes contaminés.

Mais dans mon cas j'ai souhaité prendre une approche différente. En effet, on s'arrête facilement à la réduction du problème 3D en un problème 2D. J'ai donc pour ma part continuer la réduction en prenant le problème en 1 dimension et dans ce cas plusieurs choses apparaissent :

- Tout d'abord on voit que pour une ligne donnée à un instant t avec une position de départ x. Il n'existe que 3 possibilités d'évolutions entre un instant t et t+1. Soit la maladie se propage des 2 côtés, soit de un seul en fonction de la position de départ, soit finalement aucune propagation car plus de case à contaminer. Prédire donc le nombre de case contaminé à un instant t est donc possible avec seulement la position de départ et la taille de la ligne. Nous permettant donc de nous détacher de la notion d'état précédant exprimée plus haut.
- Ensuite lorsque l'on pense en 1D et que l'on repart en 2D on remarque également que au final l'état des lignes à côté de la ligne de départ possède en réalité le même état que celle de départ avec tout simplement un décalage de jour correspondant à la distance entre les 2. A partir de là il est donc possible de prédire le nombre de contaminé à un instant t avec la position x/y de départ de la contamination seulement avec la taille de la grille carré en appliquant juste un décalage de jour entre les différentes lignes relativement à la ligne de départ (x).
- Finalement on se rend aussi compte que certaine ligne dans le cas en 2D sont inactivent après une certaine date. En effet après avoir été contaminé totalement une ligne ne produit plus de nouveau contaminé et il est possible d'éviter de calculer ces lignes inutiles en proposant un décalage dans notre parcours de lignes à partir du certaine date. Cette même date peut être identifié comme le temps nécessaire à contaminer une ligne entière et qui s'exprime par la taille d'une ligne moins la position x et y de départ. Cela permet donc d'éviter de prendre en compte certaines lignes une fois contaminé. Et donc d'effectuer les calculs en partant de la ligne de départ de l'infection et de simplement la propager dans la direction en y appliquant un décalage pour éviter d'effectuer un calcul sur des lignes inutilement.

Une fois ces constats réalisé et testé en 2D. On se rend compte que le passage de la 2D à la 3D peut s'effectuer de la même façon que de la 1D à la 2D. En effet, le phénomène de date relative à la position initiale s'exporte au niveau des tranches du cubes et permet donc de reproduire la même technique.

## Résultats et discussions

L'algorithme en lui même possède une compléxité inférieur à O(n**2) pour donner le nombre d'infecter à un instant t. Mais l'avantage comparé à l'idée initiale basé sur des états, est que cette méthode permet d'avoir le nombre exact de nouveaux infectés à un instant t sans avoir besoin de connaître les états précédants à l'exception de la position de départ de la contamination, cette même propriété a aussi l'avantage de permettre la parrallélisation de la simulation, à partir d'une position initiale x,y,z il est possible de connaître la durée de l'épidémie; correspondant en réalité à une distance de manhattan en 3D en le point de départ et le point le plus éloigné de celui-ci (coin du cube). On peut tout à fait parralléliser l'alogithme de façon à traiter des ensembles de jours par processus. Cet algorithme s'avérera donc plus performants dans le cas de question préçise basé sur la prédiction à un instant future.

L'alogoritme proposer répond à la solution général des différentes possibilités d'évolution du virus en fonction de la position de départ et de la taille du cube. La réponse donnée içi s'exprime par la translation (position initiale) et la séquence d'infection qui en résulte (nombre d'infecté supplémentaire à un instant t), ces 2 informations correspondent à la signature du développement de la pandémie, pour une translation x,y,z, une pandémie produira toujours la même séquence d'infection peu importe la permutation entre x, y et z (par exemple 0 1 0 donnera la même séquence que 1 0 0), cela étant dû à la symétrie de la problématique. Mais l'algorithme est suiffisament bien conçus pour permettre d'autres possibilités. Comme effectuer des simulations entres des dates préçisent. Le programme peut donc s'adapter à des besoins en ayant résolu une problématique plus générale.

## Perspectives

L'idée de base en 1D s'exprime facilement par une fonction. Et je pense qu'il est tout à fait possible s'exprimer la solution dans les dimensions supérieures de la même façon sans avoir à effectuer d'itération sur les tranches/lignes du cube.
