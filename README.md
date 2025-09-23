# Sistema-de-gestion-

Sosa: aca comentemos lo que vamos a ir haciendo, tenemos que empezar a trabajr con git. Empece a trabajar en otra rama (rama sosa)
Antes de empezar a codear hagamos:

git pull origin main

codigos para crear una rama es el siguiente:

git checkout main
git pull origin main
git checkout -b sosa

cuando terminemos de hacer algo y queremos hacer commit al main hacemos:
git checkout main
git pull origin main
git merge sosa
git push origin main

siempre mantener nuestras ramas actualizadas con:
git checkout sosa
git merge main
