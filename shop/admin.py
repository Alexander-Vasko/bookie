from django.contrib import admin
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import (
    User, Author, Genre, Series, Book, Review,
    Order, OrderItem, Cart, Promotion, PromoBook, Category
)

# =====================
# Экспорт книг в PDF
# =====================
def export_books_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=books.pdf"
    p = canvas.Canvas(response)

    y = 800
    for book in queryset:
        p.drawString(100, y, "{} - {} - {}".format(book.title, book.author.full_name, book.price))
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    return response

export_books_pdf.short_description = "Экспортировать книги в PDF"

# =====================
# Скидка 10%
# =====================
def apply_discount(modeladmin, request, queryset):
    for book in queryset:
        book.price *= 0.9
        book.save()
    # Django не ждёт HttpResponse для обычного действия
    # return ничего не делаем

apply_discount.short_description = "Сделать скидку 10 процентов"


# =====================
# Админки
# =====================
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
        if obj.bio:
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
    list_display = ('id', 'title', 'author_name', 'genre_name', 'series_name', 'year', 'isbn', 'price', 'discount')
    list_filter = ('author', 'genre', 'series', 'year')
    search_fields = ('title', 'isbn', 'author__full_name', 'genre__name', 'series__name')
    raw_id_fields = ('author', 'genre', 'series')
    readonly_fields = ('id',)
    list_display_links = ('title',)
    ordering = ('price',)
    actions = [export_books_pdf, apply_discount]

    def author_name(self, obj):
        return obj.author.full_name if obj.author else "-"
    author_name.short_description = 'Автор'

    def genre_name(self, obj):
        return obj.genre.name if obj.genre else "-"
    genre_name.short_description = 'Жанр'

    def series_name(self, obj):
        return obj.series.name if obj.series else "-"
    series_name.short_description = 'Серия'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_title', 'user_name', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('book__title', 'user__name', 'text')
    raw_id_fields = ('book', 'user')
    readonly_fields = ('id',)
    date_hierarchy = 'date'
    list_display_links = ('id',)

    def book_title(self, obj):
        return obj.book.title if obj.book else "-"
    book_title.short_description = 'Книга'

    def user_name(self, obj):
        return obj.user.name if obj.user else "-"
    user_name.short_description = 'Пользователь'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'date', 'status', 'delivery_address', 'payment_method')
    list_filter = ('status', 'payment_method', 'date')
    search_fields = ('user__name', 'delivery_address')
    raw_id_fields = ('user',)
    readonly_fields = ('id',)
    date_hierarchy = 'date'
    list_display_links = ('id',)

    def user_name(self, obj):
        return obj.user.name if obj.user else "-"
    user_name.short_description = 'Пользователь'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('book',)
    extra = 1
    readonly_fields = ('id',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'book_title', 'quantity', 'price')
    raw_id_fields = ('order', 'book')
    search_fields = ('order__id', 'book__title')
    readonly_fields = ('id',)
    list_display_links = ('id',)

    def order_id(self, obj):
        return obj.order.id if obj.order else "-"
    order_id.short_description = 'Заказ #'

    def book_title(self, obj):
        return obj.book.title if obj.book else "-"
    book_title.short_description = 'Книга'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'book_title', 'quantity')
    raw_id_fields = ('user', 'book')
    search_fields = ('user__name', 'book__title')
    readonly_fields = ('id',)
    list_display_links = ('id',)

    def user_name(self, obj):
        return obj.user.name if obj.user else "-"
    user_name.short_description = 'Пользователь'

    def book_title(self, obj):
        return obj.book.title if obj.book else "-"
    book_title.short_description = 'Книга'

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
    list_display = ('id', 'promotion_desc', 'book_title')
    raw_id_fields = ('promotion', 'book')
    search_fields = ('promotion__description', 'book__title')
    readonly_fields = ('id',)
    list_display_links = ('id',)

    def promotion_desc(self, obj):
        return obj.promotion.description if obj.promotion else "-"
    promotion_desc.short_description = 'Акция'

    def book_title(self, obj):
        return obj.book.title if obj.book else "-"
    book_title.short_description = 'Книга'

admin.site.register(Category)
