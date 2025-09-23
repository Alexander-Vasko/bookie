from django.contrib import admin
from django.urls import path
from shop import views

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),

    # Страница поиска
    path('search/', views.search_books, name='search_books'),

    # Книги
    path('books/', views.book_list, name='book_list'),
    path('available/', views.available_books, name='available_books'),
    path('category/<int:category_id>/', views.category_books, name='category_books'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),

    # CRUD Author
    path('authors/', views.author_list, name='author_list'),
    path('authors/create/', views.create_author, name='create_author'),
    path('authors/<int:pk>/edit/', views.edit_author, name='edit_author'),
    path('authors/<int:pk>/delete/', views.delete_author, name='delete_author'),

    # Админка
    path('admin/', admin.site.urls),
]
