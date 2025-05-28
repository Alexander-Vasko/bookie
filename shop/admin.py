from django.contrib import admin
from .models import (
    User, Author, Genre, Series, Book, Review,
    Order, OrderItem, Cart, Promotion, PromoBook, Category
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'address')
    search_fields = ('name', 'email', 'phone', 'address')
    readonly_fields = ('id',)
    list_display_links = ('name',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'short_biography')
    search_fields = ('full_name',)
    readonly_fields = ('id',)
    list_display_links = ('full_name',)

    def short_biography(self, obj):
        if obj.bio:  # Используем bio вместо biography, т.к. это поле в модели Author
            return obj.bio[:75] + '...' if len(obj.bio) > 75 else obj.bio
        return ''
    short_biography.short_description = 'Краткая биография'

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    readonly_fields = ('id',)
    list_display_links = ('name',)

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    readonly_fields = ('id',)
    list_display_links = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'genre', 'series', 'year', 'isbn', 'price', 'discount')
    list_filter = ('author', 'genre', 'series', 'year')
    search_fields = ('title', 'isbn', 'author__full_name', 'genre__name', 'series__name')
    raw_id_fields = ('author', 'genre', 'series')
    readonly_fields = ('id',)
    list_display_links = ('title',)
    ordering = ('price',)  # Можно добавить сортировку по цене

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('book__title', 'user__name', 'text')
    raw_id_fields = ('book', 'user')
    readonly_fields = ('id',)
    date_hierarchy = 'date'
    list_display_links = ('id',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'status', 'delivery_address', 'payment_method')
    list_filter = ('status', 'payment_method', 'date')
    search_fields = ('user__name', 'delivery_address')
    raw_id_fields = ('user',)
    readonly_fields = ('id',)
    date_hierarchy = 'date'
    list_display_links = ('id',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('book',)
    extra = 1
    readonly_fields = ('id',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'book', 'quantity', 'price')
    raw_id_fields = ('order', 'book')
    search_fields = ('order__id', 'book__title')
    readonly_fields = ('id',)
    list_display_links = ('id',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'quantity')
    raw_id_fields = ('user', 'book')
    search_fields = ('user__name', 'book__title')
    readonly_fields = ('id',)
    list_display_links = ('id',)

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'promotion_type', 'start_date', 'end_date')
    search_fields = ('description', 'promotion_type')
    list_filter = ('promotion_type', 'start_date', 'end_date')
    readonly_fields = ('id',)
    list_display_links = ('description',)
    date_hierarchy = 'start_date'

@admin.register(PromoBook)
class PromoBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'promotion', 'book')
    raw_id_fields = ('promotion', 'book')
    search_fields = ('promotion__description', 'book__title')
    readonly_fields = ('id',)
    list_display_links = ('id',)

admin.site.register(Category)
