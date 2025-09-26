from rest_framework import serializers
from .models import Book, Author, Category, Review

# Сериализатор для книги
class BookSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()  # вычисляемое поле
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author_name', 'category_name',
            'price', 'discount', 'discounted_price', 'status'
        ]

    def get_discounted_price(self, obj):
        # Через context можно передавать request или дополнительные данные
        request = self.context.get('request')
        return obj.discounted_price

# Сериализатор для аннотированной книги
class BookAnnotatedSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)
    sold_count = serializers.IntegerField(read_only=True)
    favorites_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 
                  'avg_rating', 'sold_count', 'favorites_count']

# Сериализатор для автора
class AuthorSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'full_name', 'books_count']

    def get_books_count(self, obj):
        # Считаем количество книг у автора
        return obj.books.count()


# Сериализатор для отзывов
class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_name', 'text', 'rating', 'date']
