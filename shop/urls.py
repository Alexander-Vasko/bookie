from django.urls import path, include
from .api_views import BookAnnotatedListAPI
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Главная + поиск
    path('', views.index, name='index'),
    path('search/', views.search_books, name='search_books'),

    # Список книг / фильтры / детали
    path('books/', views.book_list, name='book_list'),
    path('books/available/', views.available_books, name='available_books'),
    path('books/category/<int:category_id>/', views.category_books, name='category_books'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),

    # CRUD автора 
    path('authors/', views.author_list, name='author_list'),
    path('authors/create/', views.create_author, name='create_author'),
    path('authors/<int:pk>/edit/', views.edit_author, name='edit_author'),
    path('authors/<int:pk>/delete/', views.delete_author, name='delete_author'),

    # CRUD книги (форма редактирования/создания) 
    path('books/create/', views.create_book, name='create_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),

    # Корзина
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Избранное
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('favorites/add/<int:book_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:book_id>/', views.remove_from_favorites, name='remove_from_favorites'),

    # Отзывы
    path('books/<int:book_id>/review/add/', views.add_review, name='add_review'),
    
    # Авторизация
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration_view, name='registration'),
    
    # API urls 
    path('api/', include('shop.api_urls')),
    path('books-annotated/', BookAnnotatedListAPI.as_view(), name='books_annotated_api'),

]

# Подключение медиа-файлов для разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
