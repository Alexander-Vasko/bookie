from django.shortcuts import render, get_object_or_404
from .models import Book, Category
from django.core.paginator import Paginator

# Представление для отображения всех книг
def book_list(request):
    books = Book.objects.all()  # Получаем все книги
    for book in books:
        book.discount_price = book.price - book.discount()  # Вычисляем цену со скидкой

    # Пагинация (по 10 книг на странице)
    paginator = Paginator(books, 10)  # Показываем 10 книг на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/book_list.html', {'page_obj': page_obj})

# Представление для фильтрации доступных книг
def available_books(request):
    books = Book.objects.filter(status='available')  # Фильтруем книги с доступным статусом
    for book in books:
        book.discount_price = book.price - book.discount()  # Вычисляем цену со скидкой

    # Пагинация (по 10 книг на странице)
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/book_list.html', {'page_obj': page_obj})

# Представление для отображения книг по категории
def category_books(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = category.books.all()  # Получаем все книги этой категории
    for book in books:
        book.discount_price = book.price - book.discount()  # Вычисляем цену со скидкой

    # Пагинация (по 10 книг на странице)
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/category_books.html', {'category': category, 'page_obj': page_obj})

# Представление для отображения информации о книге
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.discount_price = book.price - book.discount()  # Вычисляем цену со скидкой
    return render(request, 'shop/book_detail.html', {'book': book})

