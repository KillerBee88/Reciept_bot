from django.contrib import admin
from .models import Recipe, Subscription, Categories, Client, LikeDislike, UserCategoryView


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_category')

    def get_category(self, obj):
        return obj.category.category

    get_category.short_description = 'Category'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('client', 'subscription_is_active')


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'username', 'name')


@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ('client', 'recipe', 'action')


@admin.register(UserCategoryView)
class UserCategoryViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'views_left', 'date')



