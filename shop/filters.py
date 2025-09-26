import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    author = django_filters.CharFilter(field_name='author__full_name', lookup_expr='icontains')
    genre = django_filters.CharFilter(field_name='genre__name', lookup_expr='icontains')
    status = django_filters.ChoiceFilter(field_name='status', choices=Book.STATUS_CHOICES)

    class Meta:
        model = Book
        fields = ['min_price', 'max_price', 'author', 'genre', 'status']
