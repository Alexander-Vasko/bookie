import os
import django
import random
from decimal import Decimal
from faker import Faker
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookie.settings')
django.setup()

from shop.models import Author, Genre, Book, Category

fake = Faker()

# Очистка старых данных
Author.objects.all().delete()
Genre.objects.all().delete()
Category.objects.all().delete()
Book.objects.all().delete()

# Создаём категории
categories = [Category.objects.create(name=fake.word().capitalize()) for _ in range(5)]

# Создаём жанры
genres = [Genre.objects.create(name=fake.word().capitalize()) for _ in range(5)]

# Создаём авторов
authors = [Author.objects.create(full_name=fake.name()) for _ in range(5)]

# Создаём 30 книг
for _ in range(30):
    Book.objects.create(
        title=fake.sentence(nb_words=3),
        author=random.choice(authors),
        genre=random.choice(genres),
        category=random.choice(categories),
        price=Decimal(random.randint(100, 1000)),
        year=random.randint(1990, datetime.now().year),
        isbn=fake.unique.isbn13()  # уникальный ISBN
    )

print("База данных успешно заполнена!")
