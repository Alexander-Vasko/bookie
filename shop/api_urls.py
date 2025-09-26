from django.urls import path
from .api_views import BookListAPI, AuthorListAPI, ReviewListAPI

urlpatterns = [
    path('books/', BookListAPI.as_view(), name='api_books'),
    path('authors/', AuthorListAPI.as_view(), name='api_authors'),
    path('books/<int:book_id>/reviews/', ReviewListAPI.as_view(), name='api_reviews'),
]
