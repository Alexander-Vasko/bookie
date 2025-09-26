from django.test import TestCase, Client
from django.urls import reverse
from .models import Book, Author, Category, Cart, OrderItem, Favorite, Review
from decimal import Decimal
from django.contrib.auth.models import User

class ShopTests(TestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

        # Создаем автора и категорию
        self.author = Author.objects.create(full_name="Автор Тест")
        self.category = Category.objects.create(name="Категория Тест")
        
        # Создаем книгу
        self.book = Book.objects.create(
            title="Книга Тест",
            author=self.author,
            category=self.category,
            price=Decimal('500.00'),
            discount=10,
            status='available'
        )

    # 1. Тест get_discounted_price
    def test_get_discounted_price(self):
        discounted = self.book.price - (self.book.price * self.book.discount / 100)
        self.assertEqual(self.book.discounted_price, discounted)

    # 2. Тест добавления книги в корзину
    def test_add_to_cart(self):
        response = self.client.post(reverse('add_to_cart', args=[self.book.id]))
        cart_item = Cart.objects.get(user=self.user, book=self.book)
        self.assertEqual(cart_item.quantity, 1)
        self.assertEqual(response.status_code, 302)  # редирект на корзину

    # 3. Тест удаления книги из корзины
    def test_remove_from_cart(self):
        Cart.objects.create(user=self.user, book=self.book, quantity=1)
        response = self.client.post(reverse('remove_from_cart', args=[self.book.id]))
        self.assertFalse(Cart.objects.filter(user=self.user, book=self.book).exists())
        self.assertEqual(response.status_code, 302)

    # 4. Тест просмотра списка книг
    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    # 5. Тест добавления книги в избранное
    def test_add_to_favorites(self):
        response = self.client.post(reverse('add_to_favorites', args=[self.book.id]))
        fav = Favorite.objects.get(user=self.user, book=self.book)
        self.assertIsNotNone(fav)
        self.assertEqual(response.status_code, 302)

    # 6. Тест удаления книги из избранного
    def test_remove_from_favorites(self):
        Favorite.objects.create(user=self.user, book=self.book)
        response = self.client.post(reverse('remove_from_favorites', args=[self.book.id]))
        self.assertFalse(Favorite.objects.filter(user=self.user, book=self.book).exists())

    # 7. Тест создания отзыва
    def test_add_review(self):
        response = self.client.post(reverse('add_review', args=[self.book.id]), {
            'text': 'Отличная книга',
            'rating': 5
        })
        review = Review.objects.get(user=self.user, book=self.book)
        self.assertEqual(review.text, 'Отличная книга')
        self.assertEqual(review.rating, 5)

    # 8. Тест API фильтрации книг по цене
    def test_filter_books_api(self):
        url = reverse('book_list') + f'?min_price=100&max_price=1000'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    # 9. Тест API аннотированных данных книги
    def test_book_annotated_api(self):
        from rest_framework.test import APIClient
        api_client = APIClient()
        api_client.force_authenticate(user=self.user)
        response = api_client.get(reverse('book_annotated_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('avg_rating', response.data[0])

    # 10. Тест валидации OrderItem (нельзя создать с отрицательной суммой)
    def test_order_item_validation(self):
        from django.core.exceptions import ValidationError
        order_item = OrderItem(book=self.book, quantity=-1, user=self.user)
        with self.assertRaises(ValidationError):
            order_item.full_clean()
