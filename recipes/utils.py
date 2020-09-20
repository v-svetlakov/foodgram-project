from django.core.paginator import Paginator
from django.db.models import Q

from .models import Recipe


def filter_by_tags(request, view, user):
    """Фильтрует выдачу по выбранным на страничке тегам,
    добавляет пагинацию"""

    filters = request.GET.getlist('filters')

    filters_by_views = {
        'index': Q(),
        'favourites': Q(favorited_recipe__user=request.user),
        'profile': Q(author=user),
    }

    recipe_list = Recipe.taged.filter_for_tags(
        filters).filter(filters_by_views[view]).distinct()

    paginator = Paginator(recipe_list, 9)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return paginator, page


def get_ingredients(request):
    """Используем в форме создания и редактирования рецептов,
    чтобы вытащить из POST запроса ингредиенты"""

    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]
            if value_ingredient.isdecimal():
                ingredients[request.POST[key]] = request.POST[
                    'valueIngredient_' + value_ingredient]
    return ingredients
