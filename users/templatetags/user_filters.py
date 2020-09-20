from urllib.parse import urlencode  # noqa

from django import template

from recipes.models import Follow, ToShop, User, Favorite  # noqa

register = template.Library()


@register.filter
def addclass(field, css):
    """Фильтр для добавления класса к полю в шаблоне"""
    return field.as_widget(attrs={"class": css})


@register.filter
def format_count(word, count):
    """Фильтр для склонения слова 'рецепт' по числу"""
    count = count - 3  # в шаблоне нам нужно кол-во оставшихся рецептов минус 3

    remainder_ten = count % 10
    remainder_hundred = count % 100
    if remainder_ten == 0:
        word += 'ов'
    elif remainder_ten == 1 and remainder_hundred != 11:
        word += ''
    elif remainder_ten < 5 and remainder_hundred not in [11, 12, 13, 14]:
        word += 'а'
    else:
        word += 'ов'
    return word


@register.filter
def get_filter_values(value):
    return value.getlist('filters')


@register.filter
def get_filter_link(request, tag):
    new_request = request.GET.copy()  # копируем реквест

    if tag.slug in request.GET.getlist('filters'):  # кошмар какой
        filters = new_request.getlist('filters')
        filters.remove(tag.slug)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.slug)

    return new_request.urlencode()


@register.simple_tag
def url_replace(request, field, value):
    """Используется для сохранения GET-параметров при пагинации"""

    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.filter
def is_recipe_favorited(recipe, user):
    return Favorite.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def is_recipe_shoped(recipe, user):
    return ToShop.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def is_author_followed(author, user):
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter
def count_recipes_shoped(request, user_id):
    """Считает количество покупок для синего счетчика"""
    toshop = ToShop.objects.filter(user=user_id).count()
    return toshop
