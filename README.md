# Foodgram

Сайт рецептов
Неавторизованный пользователь может просматривать рецепты. 
Авторизованный пользователь может писать свои рецепты, добавлять чужие рецепты в избранное, подписываться на других авторов рецептов и формировать список покупок.

Подписки на автора пока только через админку.
Рецепты в базу не добавлены, по этому при добавлении рецепта пишет ошибку, но если перейти на главную страничку пост будет.

### Требования


[Python](https://www.python.org/downloads/) v3.7 +  для запуска.
[Docker](https://www.docker.com/)
Установите зависимости.
```sh
$ sudo apt update
$ sudo apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common -y
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository \
$ "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
$ (lsb_release -cs) \
$ stable"
$ sudo apt update
$ sudo apt install docker-ce -y
```

После установки docker выполнить команду в командной строке:
```sh
$ docker-compose up
```

После сборки образа:
```sh
$ sudo docker exec -it <CONTAINER ID> python manage.py collectstatic
$ sudo docker exec -it <CONTAINER ID> python manage.py makemigrations
$ sudo docker exec -it <CONTAINER ID> python manage.py migrate
$ sudo docker exec -it <CONTAINER ID> python manage.py createsuperuser
$ sudo docker exec -it <CONTAINER ID> python manage.py loaddata fixtures.json
```

## Авторы

* **Vladimir Svetlakov** - *Initial work* - [svvladimir-ru](https://github.com/svvladimir-ru)

* [foodgram](http://www.foogramtest.ml/)
