## As-tu envisagé d'autres techniques de résolution pour cet exercice?

Il aurais été possible de le traiter dans une approche plus
fonctionelle.

Des fonctions "action" qui prennent des ressources(foo, bar, foobar,
second, euros) en paramêtre et retourne une ressource.

- créer tous les foos puis tous les bars pour créer assez de foobar
  pour avoir assez d'euros pour acheter un worker, (avec une marge due
  au random). rince/repeat jusqu'a avoir assez de workers pour que le
  jeux s'arrète.

- rendre chaques workers responsable de la création d'un autre worker
 (27 foo, 9 bar...)



## Est-il possible de traiter des temps qui ne sont pas des valeurs entières? Est-il
nécessaire de réaliser des changement profonds sur l’archi ou le code?

Il est possible de traiter des valeurs qui ne sont pas
entières. D'ailleurs le programme le permet déjà.

```python
class REQUIREMENTS:
    """
    here you get the cost of each activity.
    If you want to play with the application it's the right place to start
    """
    create_foo = {"seconds": 1.5}
    create_bar = {"seconds": check_bar_price}
    create_foobar = {"seconds": 2.3, "foos": 1.2, "bars": 1.2}
    sell_foobar = {"seconds": 10.5, "foobars": 5.4}
    buy_worker = {"euros": 3.5, "foos": 6.3}
    change_activity = {"seconds": 5.4}
```

```shell
python3 run.py
>>> run: 461, {'foos': 27.700000000000067, 'bars': 16.800000000000033, 'foobars': 0.5999999999999925, 'euros': 10.5, 'workers': 29, 'seconds': 166.3743690533461}
run: 462, {'foos': 34.40000000000006, 'bars': 16.800000000000033, 'foobars': 0.5999999999999925, 'euros': 7.0, 'workers': 30, 'seconds': 30.074369053346068}
```
## Seconde entière

D’ailleurs, le temps de fabrication d’un bar est aléatoire, entre 0.5 et 2 secondes.
L’implémentation actuelle prend effectivement une valeur aléatoire, mais du fait du
fonctionnement “discret” à la seconde près, les temps sont systématiquement
arrondis à la seconde supérieure.


Comme les workers consomment des secondes comme s'il s'agissais d'une
ressource, quand ils consomment une quantité non entière de seconde,
le reste est gardé dans le "pool" du worker et peut être employé
ulterieurement.

cf le nombre de secondes restante dans l'exemple plus haut, calculé en
faisant :

```
sum([worker.seconds for worker in self.workers])
```

## As-tu pensé à d’autres stratégies? à des moyens d’optimiser une
   stratégie?

L'implémentation est en effet très naïve. Pour avoir de meilleurs
résultats il faut prendre le problème à la source. Que veux t'on ?
Créer 30 workers. Donc on veux le plus rapidement possible de nouveaux
workers pour avoir plus de force de travail.

Comme changer d'activité prend du temps, il faut en changer le moins
possible.

Il ne me semble pas intéressant de vendre moins de 5 foobar puisque le
temps de vente est fixe.

Il faut donc récolter assez de ressources pour en vendre 5.

On peut mettre le premier robot à la création de foo ( 7 foos pour
créer 5 foobar en prenant en compte les 40% de perte, plus 30 pour
acheter un nouveau robot)
Le second robot peut créer des bars dont le temps de création est
aléatoire (5). Il aura dans tous les cas fini avant le premier robot.

Il peut ensuite venir donner un coup de main pour les derniers foos à
créer.

Le second robot peut ensuite fabriquer des foobar pendant que le
premier continue a créer des foos.

Ensuite, sachant qu'il faut 37 secondes en moyenne pour créer assez de
foo pour un nouveau robot et en moyenne 6.25 secondes pour créer assez
de bar, il faut ~6 robots qui créés des foo pour un qui créé des bar.

On peut laisser un robot crééer des foobars et les vendre.

En ajoutant un peu de logique dans la méthode `run` du manager on
devrais pouvoir valider cette stratégie.


## Le décorateur validate est centrale dans l’implémentation. Il est
   dommage de pas l’avoir testé de façon unitaire

En effet. Pour rester dans le temps imparti j'ai préféré faire des
tests d'intégrations qui valident le fonctionnement général et me
permettent d'avancer rapidement mais pour livrer un produit fini un
test unitaire du décorateur aurai été indispensable.


## EXEC_SPEED aurait pu être défini avec l’instruction os.getenv('EXEC_SPEED', 1) pour
permettre de surcharger sa valeur avec une variable d’environnement sans nécessairement
modifier code.

Je n'utilise pas `EXEC_SPEED` Seulement un naif:

```python
        for worker in self.workers:
            worker.seconds += 1
```

Mais

```python
        for worker in self.workers:
            worker.seconds += os.getenv('EXEC_SPEED', 1)
```

Est une bonne solution pour rendre le programme plus configurable. Il
faudrais alors faire la même chose pour REQUIREMENTS afin de
configurer toutes les rêgles du jeu dans un .env

## En lieu et place de ta fonction log(), tu aurais pu utiliser le module
[logging](<https://docs.python.org/3.8/library/logging.html>) de la
librairie standard.

Si j'avais utilisé des logs en effet s'aurait été la meilleur chose à
faire. J'ai utilisé un bête "print(manager)" que j'aurais pu remplacer
par un `sys.stdout.write` qui aurait été plus propre.


## ListAvailableTask[random.randint(0,len(ListAvailableTask)-1)] aurait pu s’écrire plus
simplement avec
[random.choice()](<https://docs.python.org/3.8/library/random.html?#random.choice>) :
random.choice(ListAvailableTask)


Je plaide non coupable :) Je n'utilise que `random.random` et
`random.uniform`. si j'avais voulu que les temps d'executions ne soit
que des pas de demi secondes, j'aurais pu utiliser
`random.choice([0.5, 1, 1.5, 2.0])`


## Remarque mineure : ton code mixe un petit peu plusieurs styles pour tes variables/attributs
de classe ; On trouve par exemple :
○ self.queue_foo , self.robot_counter , self._previous_task respectent la PEP8 pour les
noms de variables
○ ListAvailableTask serait plutôt un nom de classe, pas une variable
○ nextTask, getOneBar, getOneFoo sont en camelCase, qui n’est pas recommandé
dans la PEP8.

Je plaide non coupable :) ce ne sont pas mes noms de
fonction/méthodes. ni celles en snake_case ne celles en CamelCase

En revanche, je me suis permis d'écrire `class REQUIREMENTS` vu le
fonctionnement un peu particulier de cette classe et qu'elle ressemble
a un settings django (les habitudes ont la vie dure ;) )


## Nous aurions aimé en savoir davantage sur des choix d’architecture et sur le fonctionnement du
programme dans le README. Et peut-être aussi y ajouter une section pour les limitations actuelles
et les pistes d’amélioration que tu aurais aimé exploiter si tu avais
eu plus de temps par exemple.


Je pensais l'avoir fait mais je serais ravi d'en discuter de vive voix
avec vous :)
