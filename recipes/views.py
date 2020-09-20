import csv
import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from .forms import RecipeForm
from .models import Amount, Favorite, Follow, Ingredient, Recipe, Tag, ToShop
from .utils import filter_by_tags, get_ingredients

User = get_user_model()


def index(request):
    """Главная страничка с рецептами"""

    headline = 'Рецепты'   # заголовок страницы
    index = True  # для синей черточки в наве

    all_tags = Tag.objects.all()
    paginator, page = filter_by_tags(request, 'index', request.user)

    return render(request, 'index.html', {
        'page': page,
        'paginator': paginator,
        'headline': headline,
        'index': index,
        'all_tags': all_tags, })


@login_required
def new_recipe(request):
    """Форма создания рецепта"""

    headline = 'Создание рецепта'
    new_recipe = True

    if request.method == 'POST':
        form = RecipeForm(
            request.POST,
            files=request.FILES or None)

        ingredients = get_ingredients(request)

        if not ingredients:
            form.add_error(
                None, 'В рецепте должен быть хотя бы один ингредиент')

        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            for name, units in ingredients.items():
                ingredient = Ingredient.objects.get(name=name)
                amount = Amount(
                    units=units,
                    ingredient=ingredient,
                    recipe=recipe)
                amount.save()

            form.save_m2m()
            return redirect(recipe_view, recipe_id=recipe.id)

    else:
        form = RecipeForm(files=request.FILES or None)

    return render(request, 'recipe_create_edit.html', {
        'form': form,
        'headline': headline,
        'new_recipe': new_recipe, })


@login_required
def recipe_edit(request, recipe_id):
    """Форма редактирования рецепта"""

    headline = 'Редактирование рецепта'
    recipe_edit = True

    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.user != recipe.author:
        return redirect(recipe_view, recipe_id=recipe_id)

    if request.method == "POST":
        form = RecipeForm(
            request.POST,
            files=request.FILES or None,
            instance=recipe)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            recipe.amount_set.all().delete()  # перезаписываем все что было :)

            ingredients = get_ingredients(request)

            for name, units in ingredients.items():
                ingredient = Ingredient.objects.get(name=name)
                amount = Amount(
                    units=units,
                    ingredient=ingredient,
                    recipe=recipe)
                amount.save()

            form.save_m2m()
            return redirect(recipe_view, recipe_id=recipe_id)

    form = RecipeForm(
                request.POST or None,
                files=request.FILES or None,
                instance=recipe)
    return render(request, 'recipe_create_edit.html', {
        'form': form,
        'recipe_edit': recipe_edit,
        'headline': headline, })


@login_required
def recipe_delete(request, recipe_id):
    """Удаление рецепта по кнопке"""

    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
    return redirect(index)


def recipe_view(request, recipe_id):
    """Просмотр отдельного рецепта"""

    recipe = get_object_or_404(Recipe, id=recipe_id)

    return render(
        request, 'recipe_single.html',
        {'recipe': recipe, })


@login_required
def follow_index(request):
    """Страница "Мои подписки" с рецептами авторов,
    на которых подписан текущий пользователь"""

    headline = 'Мои подписки'
    follow_index = True

    favorite_authors = request.user.follower.all()

    paginator = Paginator(favorite_authors, 9)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'follow.html', {
        'page': page,
        'paginator': paginator,
        'headline': headline,
        'follow_index': follow_index, })


@login_required
def favourites(request):
    """Страница рецептов, добавленных пользователем в избранное"""

    headline = 'Избранное'
    favourites = True

    all_tags = Tag.objects.all()

    paginator, page = filter_by_tags(request, 'favourites', request.user)

    return render(request, 'index.html', {
        'page': page,
        'paginator': paginator,
        'all_tags': all_tags,
        'headline': headline,
        'favourites': favourites, })


@login_required
def shoping_list(request):
    """Список покупок"""

    headline = 'Список покупок'
    shoping_list_index = True

    recipes_to_shop = request.user.shoper.all()

    return render(request, 'shop_list.html', {
        'recipes_to_shop': recipes_to_shop,
        'headline': headline,
        'shoping_list_index': shoping_list_index,
        'shoping_list': recipes_to_shop, })


def profile(request, username):
    """Страничка-профиль пользователя"""

    profile = get_object_or_404(
                    User,
                    username=username)

    headline = profile.username
    index = True

    all_tags = Tag.objects.all()

    follow = False
    if request.user.is_authenticated and Follow.objects.filter(
            user=request.user, author=profile).exists():
        follow = True

    paginator, page = filter_by_tags(request, 'profile', profile)

    return render(request, 'profile.html', {
        'headline': headline,
        'profile': profile,
        'page': page,
        'paginator': paginator,
        'follow': follow,
        'index': index,
        'all_tags': all_tags, })


class Purchases(View):
    """Работает с js, добавляет рецепт в список покупок/удаляет из него"""

    def post(self, request):
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        ToShop.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse({'success': 'true'})

    def delete(self, request, recipe_id):
        count, _ = ToShop.objects.filter(
            user=request.user,
            recipe=recipe_id
            ).all().delete()
        return JsonResponse({'success': 'true' if count > 0 else 'false'})


class Favorites(View):
    """Работает с js, добавляет рецепт в избранное/удаляет из него"""

    def post(self, request):
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        Favorite.objects.get_or_create(
            user=request.user, recipe=recipe)
        return JsonResponse({'success': 'true'})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)

        count, _ = Favorite.objects.filter(
            user=request.user,
            recipe=recipe).all().delete()
        return JsonResponse({'success': 'true' if count > 0 else 'false'})


class Subscribe(View):
    """Работает с js, добавляет пользователя
    в "Мои подписки"/удаляет из него"""

    def post(self, request):
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, id=author_id)
        if request.user != author:
            Follow.objects.get_or_create(user=request.user, author=author)
            return JsonResponse({'success': 'true'})
        return JsonResponse({'success': 'false'})

    def delete(self, request, author_of_recipe):
        author = get_object_or_404(User, id=author_of_recipe)
        count, _ = Follow.objects.filter(
            user=request.user, author=author
            ).all().delete()
        return JsonResponse({'success': 'true' if count > 0 else 'false'})


class Ingredients(View):
    """Работает с js, возвращает на сайт список ингредиентов по началу слова"""

    def get(self, request):
        text = request.GET.get('query')

        suggest = Ingredient.objects.filter(
            name__istartswith=text).annotate(
                title=F('name'), dimension=F('measurement_unit')
                ).values('title', 'dimension').order_by('title')

        return JsonResponse(list(suggest), safe=False)


@login_required
def print_shoping_list(request):

    recipes_to_shop = Recipe.objects.filter(
        recipe_to_shop__user=request.user).all()
    ingredient_list = recipes_to_shop.annotate(
        title=F('amount__ingredient__name'),
        units=F('amount__ingredient__measurement_unit')
        ).values('title', 'units').order_by('title').annotate(
            total=Sum('amount__units'))  # все равно order_by не работает

    response = HttpResponse(content_type='text/txt')
    response['Content-Disposition'] = 'attachment; filename="shoping_list.txt"'

    writer = csv.writer(response)

    writer.writerow([f'Список покупок: {request.user.username}'])
    writer.writerow([])

    for ingredient in ingredient_list:
        if ingredient['title']:
            name = ingredient['title']
            dimension = ingredient['units']
            total = ingredient['total']
            writer.writerow([f'{name} - {total} {dimension}'])

    return response
