# Foodgram

Сайт рецептов
Неавторизованный пользователь может просматривать рецепты. 
Авторизованный пользователь может писать свои рецепты, добавлять чужие рецепты в избранное, подписываться на других авторов рецептов и формировать список покупок.

## Начало работы
Зависимости:
```
pip install -r requirements.txt 
```

Ингредиенты для рецептов: файл ingredients.json
Миграция:
```
manage.py migrate recipes 0002
```

Теги для рецептов: файл tags.json
Миграция:
```
manage.py migrate recipes 0003
```

## Авторы

* **Vladimir Svetlakov** - *Initial work* - [svvladimir-ru](https://github.com/svvladimir-ru)