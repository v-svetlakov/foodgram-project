from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('new/', views.new_recipe,
         name='new_recipe'),  # создание нового рецепта
    path('recipes/<int:recipe_id>/edit/', views.recipe_edit,
         name='recipe_edit'),
    path('recipes/<int:recipe_id>/edit/delete/', views.recipe_delete,
         name='recipe_delete'),

    path('follow/', views.follow_index,
         name='follow_index'),  # авторы, на которых подписан пользователь
    path('recipes/<int:recipe_id>/', views.recipe_view,
         name='recipe'),  # отдельный рецепт
    path('favourites/', views.favourites,
         name='favourites'),  # избранные рецепты
    path('shoping_list/', views.shoping_list,
         name='shoping_list'),  # список покупок
    path('shoping_list/print/', views.print_shoping_list,
         name='print_shoping_list'),  # распечатка списка покупок

    path('purchases/', views.Purchases.as_view(),
         name='add_purchase'),  # js добавление рецепта в покупки
    path('purchases/<int:recipe_id>/', views.Purchases.as_view(),
         name='delete_purchase'),  # js удаление рецепта из покупок
    path('favorites/', views.Favorites.as_view(),
         name='add_favorites'),  # js добавление рецепта в избранное
    path('favorites/<int:recipe_id>/', views.Favorites.as_view(),
         name='delete_favorites'),  # js удаление рецепта из избранного
    path('subscriptions/', views.Subscribe.as_view(),
         name='subscribe'),  # js добавление автора в подписки
    path('subscriptions/<int:author_of_recipe>/',
         views.Subscribe.as_view(),
         name='unsubscribe'),  # js удаление автора из подписок
    path('ingredients/', views.Ingredients.as_view(),
         name='ingredients'),  # js ингредиенты в форме

    path('<username>/', views.profile, name='profile'),  # профиль пользователя

]
