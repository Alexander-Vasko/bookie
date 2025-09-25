from django.urls import path
from . import views

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
]
