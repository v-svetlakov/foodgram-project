from django.contrib import admin

from .models import Ingredient, Recipe, Amount, Follow, Tag, Favorite, ToShop


class AmountInLine(admin.TabularInline):
    model = Amount
    extra = 1


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'style', 'slug', 'id')
    search_fields = ('name', )


class RecipeAdmin(admin.ModelAdmin):

    def count_favorited(self, obj):
        count = Favorite.objects.filter(recipe=obj).count()
        if 0 < count <= 3:
            stars = count * '\N{GLOWING STAR}'
            return f'{count} {stars}'  # это звездочки в админке
        if count > 3:
            stars = 3 * '\N{GLOWING STAR}'
            return f'{count} {stars}'
        return count

    count_favorited.short_description = 'Добавления в избранное'

    list_display = ('name', 'author', 'pub_date', 'count_favorited')
    search_fields = ('name', )
    filter_horizontal = ('tag', )
    list_filter = ('tag', 'pub_date', 'author', )
    autocomplete_fields = ('ingredients', )
    inlines = (AmountInLine, )
    readonly_fields = ('count_favorited', )


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


class AmountAdmin(admin.ModelAdmin):
    fields = ('ingredient', 'recipe', 'units')
    search_fields = ('ingredient', 'recipe')


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Amount, AmountAdmin)
admin.site.register(Follow)
admin.site.register(Favorite)
admin.site.register(ToShop)
