from django.db.models import Avg, Count, Sum
from rest_framework import generics
from .models import Book, Author, Review, OrderItem, Favorite
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter
from .serializers import (
    BookSerializer,
    AuthorSerializer,
    ReviewSerializer,
    BookAnnotatedSerializer
)

filter_backends = [DjangoFilterBackend]


# Список книг с аннотациями
class BookAnnotatedListAPI(generics.ListAPIView):
    queryset = Book.objects.all().annotate(
        avg_rating=Avg('review__rating'),            # средний рейтинг
        sold_count=Sum('orderitem__quantity'),       # сколько купили (если есть OrderItem)
        favorites_count=Count('favorite', distinct=True)  # сколько раз в избранное
    )
    serializer_class = BookAnnotatedSerializer


# Список книг
class BookListAPI(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_context(self):
        # Передаем request в сериализатор
        return {'request': self.request}


# Список авторов
class AuthorListAPI(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


# Список отзывов для книги
class ReviewListAPI(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        book_id = self.kwargs.get('book_id')
        return Review.objects.filter(book_id=book_id)
