# Voxel Pandemia

## Posons le problème

Ce script python vise à résoudre le problème suivant :

Considérons un cube de largeur N, composé lui-même de cube de largeur 1.
La Voxel Pandemia se traduit par la transformation à l'instant 0 d'un cube en un cube contaminé
à une position initial x, y et z. Pour les t+1 suivants la contamination suit la règle suivante :

Pour chaque cube contaminé à un instant, tous les cubes saints en contact avec celui-ci par une face seront contaminés
à l'instant t+1. La pandémie se termine lorsque tout les cubes ont été contaminé.

L'objectif est donc de concevoir un algorithme permettant connaître l'évolution du virus pour toutes les positions de départs possibles.

## Solution proposée

Afin de résoudre ce problème, l'idée la plus simple et de regarder en 2 dimensions.
On constate rapidement une propagation du virus avec une forme de losange et à la notion même d'instant t et t+1
du problème nous pousse à donner une solution dont le calcul nécessite de prendre en compte les instants précédents.
On peut donc facilement concevoir un algorithme basique prenant en entrée un état A de la population de cube à un instant t et retournant
un état B correspondant à la population à l'instant t+1.

La proposition d'un tel algorithme était l'idée de départ et s'optimise assez facilement tout d'abord en prenant en compte les axes de symétrie du cube, et la possibilité de regarder à un instant t uniquement les cubes contaminés.

Mais dans mon cas j'ai souhaité prendre une approche différente. En effet, on s'arrête facilement à la réduction du problème 3D en un problème 2D. J'ai donc pour ma part continuer la réduction en prenant le problème en 1 dimension et dans ce cas plusieurs choses apparaissent :

- Tout d'abord on voit que pour une ligne donnée à un instant t avec une position de départ x. Il n'existe que 3 possibilités d'évolution entre un instant t et t+1. Soit la maladie se propage des 2 côtés, soit d'un seul en fonction de la position de départ, soit finalement aucune propagation car plus de case à contaminer. Prédire donc le nombre de case contaminé à un instant t est donc possible avec seulement la position de départ et la taille de la ligne. Nous permettant donc de nous détacher de la notion d'état précédent exprimée plus haut.
- Ensuite lorsque l'on pense en 1D et que l'on repart en 2D on remarque également qu'au final l'état des lignes à côté de la ligne de départ possède en réalité le même état que celle de départ avec tout simplement un décalage de jour correspondant à la distance entre les 2. À partir de là il est donc possible de prédire le nombre de contaminé à un instant t avec la position x/y de départ de la contamination seulement avec la taille de la grille carré en appliquant juste un décalage de jour entre les différentes lignes relativement à la ligne de départ (x).
- Finalement on se rend aussi compte que certaine ligne dans le cas en 2D sont inactives après une certaine date. En effet après avoir été contaminé totalement une ligne ne produit plus de nouveau contaminé et il est possible d'éviter de calculer ces lignes inutiles en proposant un décalage dans notre parcours de lignes à partir d'une certaine date. Cette même date peut être identifiée comme le temps nécessaire à contaminer une ligne entière et qui s'exprime par la taille d'une ligne moins la position x et y de départ. Cela permet donc d'éviter de prendre en compte certaines lignes une fois contaminées. Et donc d'effectuer les calculs en partant de la ligne de départ de l'infection et de simplement la propager dans la direction en y appliquant un décalage pour éviter d'effectuer un calcul sur des lignes inutilement.

Une fois ces constats réalisé et testé en 2D. On se rend compte que le passage de la 2D à la 3D peut s'effectuer de la même façon que de la 1D à la 2D. En effet, le phénomène de date relative à la position initiale s'exporte au niveau des tranches du cube et permet donc de reproduire la même technique. Une dernière optimisation proposée est l'utilisation de memoization. En effet, chaque tranche du cube correspond à la même tranche initiale avec une composition décaler de t temps, correspondant à la distance entre la tranche départ et les autres. De ce fait il est possible de mémoriser le nombre d'infecter à instant t pour la tranche de départ, et une fois atteinte par les autres avec le décalage, il suffit de récupérer l'information stockée précédemment. Cette mémorisation à un coup, celle-ci peut même être réduite, mais dans mon cas j'ai préféré maximiser la performance de temps puisque je suppose qu'un groupe de scientifique possédera surement plus de RAM dans leurs machines que de temps consacrait à attendre.

## Résultats et discussions

L'avantage comparé à l'idée initiale basée sur des états, est que cette méthode permet d'avoir le nombre exact de nouveau infecté à un instant t sans avoir besoin de connaître les états précédents à l'exception de la position de départ de la contamination, cette même propriété a aussi l'avantage de permettre la parallélisation de la simulation, à partir d'une position initiale x,y,z il est possible de connaître la durée de l'épidémie; correspondant en réalité à une distance de Manhattan en 3D en le point de départ et le point le plus éloigné de celui-ci (coin du cube). On peut tout à fait paralléliser l'algorithme de façon à traiter des ensembles de jours par processus.

L'algorithme proposé répond au problème général des différentes possibilités d'évolution du virus en fonction de la position de départ et de la taille du cube. La réponse donnée ici s'exprime par la translation (position initiale) et la séquence d'infection qui en résulte (nombre d'infecté supplémentaire à un instant t), ces 2 informations correspondent à la signature du développement de la pandémie, pour une translation x,y,z, une pandémie produira toujours la même séquence d'infection peu importe la permutation entre x, y et z (par exemple 0 1 0 donnera la même séquence que 1 0 0), cela étant dû à la symétrie de la problématique. Mais l'algorithme est suffismament bien conçus pour permettre d'autres possibilités. Comme effectuer des simulations entre des dates précises. Le programme peut donc s'adapter à des besoins en ayant résolu une problématique plus générale.

## Perspectives

L'idée de base en 1D s'exprime facilement par une fonction. Et je pense qu'il est tout à fait possible s'exprimer la solution dans les dimensions supérieures de la même façon sans avoir à effectuer d'itération sur les tranches/lignes du cube. De plus le concept de "translation temporelle" entre les lignes/tranches peut rendre possible le développement d'une visualisation d'un instant t sans avoir à calculer les instants précédents.

## Utilisation

Ce programme a été écrit et doit être lancé avec python 3.

Tout d'abord cloné et naviguer dans le répertoire du projet : 

````bash
git clone https://github.com/CuadrosNicolas/Voxel-Pandemia
cd Voxel-Pandemia
````

Ensuite vous pouvez simplement lancer le programme avec la commande suivante :

````bash
python3 main.py
````

Le programme affichera finalement dans la console des tableaux correspondant aux différentes possibilités du virus en fonction de la position de départ. La taille du cube choisi pour la simulation de base est 5, celle-ci peut être changée par le biais du fichier "config.json". Le paramètre "limitOne" permet également de limiter le calcul à uniquement la première translaiton (0,0,0) correspondant au cas nécessitant le plus de temps pour infecter la totalité du cube.

## Benchmark

Ce repo possède le script "benchmark.py" afin de comparer les performances entre une implémentation classique décrite au départ (avec l'utilisation d'état précédant) et la version actuelle. le benchmark nécessite d'être sous UNIX et d'avoir la librarie numpy d'installer. Une fois cela vérifié, vous pouvez lancer le benchmark avec la commande suivante :

````bash
python3 benchmark.py
````

exec_base correspond à l'implémentation classique et exec_main à la version actuelle.

## Implémentation en Go

Une implémentation en Go de l'algorithme est également disponible sous le dossier golang/main. Une implémentation de la version basique est également disponible sous le dossier golang/base. Ces 2 programmes s'appuient sur le fichier de configuration golang/conf.json et pour fonctionner correctement doivent être lancés depuis le dossier golang.

Par exemple si vous êtes dans le dossier du repository : 

````bash
cd golang
go run main/main.go -v
````

Le "-v" permet d'afficher les résultats et pas juste le temps écoulé. 

Le benchmark utiliser pour l'implémentation en Python est également disponible. Comparé à la version en Python, la version en Golang est bien plus rapide notamment grâce à l'utilisation des goroutines.
