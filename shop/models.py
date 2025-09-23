from django.db import models
from django.utils import timezone
from decimal import Decimal

# Модель категории книг
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Кастомный менеджер для доступных книг
class BookManager(models.Manager):
    def available(self):
        return self.filter(status='available')


# Модель книги
class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
        ('discontinued', 'Discontinued'),
    ]
    
    title = models.CharField("Название книги", max_length=200)
    author = models.ForeignKey('Author', verbose_name="Автор", on_delete=models.CASCADE, related_name='books')
    genre = models.ForeignKey('Genre', verbose_name="Жанр", on_delete=models.CASCADE, related_name='books')
    series = models.ForeignKey('Series', verbose_name="Серия", null=True, blank=True, on_delete=models.SET_NULL)
    year = models.PositiveIntegerField("Год издания")
    isbn = models.CharField("ISBN", max_length=20, unique=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    discount = models.DecimalField("Скидка", max_digits=5, decimal_places=2, default=0)
    description = models.TextField("Описание", blank=True)
    cover = models.ImageField("Обложка", upload_to='books/', null=True, blank=True)
    file = models.FileField("Файл книги (PDF)", upload_to="books/files/", null=True, blank=True)  # <── добавлено
    published_date = models.DateField("Дата публикации", default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)  # Дата добавления книги
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    category = models.ForeignKey(Category, related_name='books', on_delete=models.CASCADE)

    objects = BookManager()  # Используем кастомный менеджер

    promotions = models.ManyToManyField(
        'Promotion',
        through='PromoBook',
        through_fields=('book', 'promotion'),
        related_name='books'
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['price']

    def __str__(self):
        return self.title

    # Метод для расчета скидки
    def calculate_discount(self):
        if not self.price:  # проверка на None
            return Decimal('0.0')
        days_on_shelf = (timezone.now() - self.created_at).days
        if days_on_shelf > 30:
            return self.price * Decimal('0.1')  # 10% скидка
        return Decimal('0.0')

    # Метод для получения абсолютного URL книги
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('book_detail', kwargs={'pk': self.pk})


class User(models.Model):
    name = models.CharField("Имя", max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=20)
    address = models.CharField("Адрес", max_length=255)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name


class Author(models.Model):
    full_name = models.CharField("ФИО", max_length=200)
    bio = models.TextField("Биография", blank=True)
    photo = models.ImageField("Фото", upload_to='authors/', null=True, blank=True)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.full_name


class Genre(models.Model):
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField("Название серии", max_length=100)

    class Meta:
        verbose_name = "Серия"
        verbose_name_plural = "Серии"

    def __str__(self):
        return self.name


class Review(models.Model):
    book = models.ForeignKey(Book, verbose_name="Книга", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    text = models.TextField("Текст отзыва")
    rating = models.PositiveSmallIntegerField("Рейтинг")
    date = models.DateTimeField("Дата отзыва", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв на {self.book} от {self.user}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    date = models.DateTimeField("Дата заказа", auto_now_add=True)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='new')
    delivery_address = models.CharField("Адрес доставки", max_length=255)
    payment_method = models.CharField("Способ оплаты", max_length=50)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id} от {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name="Заказ", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name="Книга", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Количество")
    price = models.DecimalField("Цена на момент покупки", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Состав заказа"

    def __str__(self):
        return f"{self.book} x {self.quantity}"


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name="Книга", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Количество")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user} - {self.book} x {self.quantity}"


class Promotion(models.Model):
    description = models.TextField(verbose_name='Описание')
    promotion_type = models.CharField(max_length=50, verbose_name='Тип акции')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'


class PromoBook(models.Model):
    promotion = models.ForeignKey(Promotion, verbose_name="Акция", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name="Книга", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Книга в акции"
        verbose_name_plural = "Книги в акциях"

    def __str__(self):
        return f"{self.book} - {self.promotion}"
