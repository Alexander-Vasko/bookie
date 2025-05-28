from django.contrib import admin
from django.urls import path
from shop import views

urlpatterns = [
    # Главная страница с книгами
    path('', views.book_list, name='book_list'),  
    
    # Страница с доступными книгами
    path('available/', views.available_books, name='available_books'),  
    
    # Страница категории, при передаче id категории
    path('category/<int:category_id>/', views.category_books, name='category_books'),  
    
    # Страница конкретной книги по первичному ключу (pk)
    path('book/<int:pk>/', views.book_detail, name='book_detail'),  
]
