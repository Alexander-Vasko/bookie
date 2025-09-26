from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count
from decimal import Decimal

from django.contrib.auth import logout

from .models import Book, Category, Author, PromoBook, Cart, Favorite, Review
from .forms import AuthorForm, BookForm, ReviewForm


# ======================
# Основные views для книг
# ======================

def index(request):
    # 1. Популярные книги: top-5 по количеству заказов
    popular_books = Book.objects.annotate(order_count=Count('orderitem')).order_by('-order_count')[:5]

    # 2. Новые поступления: последние 5 добавленных книг
    new_books = Book.objects.all().order_by('-id')[:5]

    # 3. Акции и скидки: книги с активными промо
    promo_books = PromoBook.objects.select_related('book').all()[:5]

    return render(request, 'shop/index.html', {
        'popular_books': popular_books,
        'new_books': new_books,
        'promo_books': promo_books,
    })
    

# =====================
# Регистрация
# =====================
def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматически логиним после регистрации
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'shop/registration.html', {'form': form})

# =====================
# Вход (логин)
# =====================
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

# =====================
# Выход (logout)
# =====================
def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect('index')
    
# Добавление книги в корзину
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'quantity': 1}  # если объект новый, сразу ставим quantity = 1
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

# Удаление книги из корзины
def remove_from_cart(request, book_id):
    cart_item = get_object_or_404(Cart, user=request.user, book_id=book_id)
    cart_item.delete()
    return redirect('cart_detail')

# Просмотр корзины
def cart_detail(request):
    items = Cart.objects.filter(user=request.user)
    for item in items:
        item.total_price = item.book.discounted_price * item.quantity

    total = sum(item.total_price for item in items)

    return render(request, 'shop/cart.html', {
        'items': items,
        'total': total,
    })


# Добавление книги в избранное
def add_to_favorites(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    Favorite.objects.get_or_create(user=request.user, book=book)
    return redirect('favorites_list')

# Удаление книги из избранного
def remove_from_favorites(request, book_id):
    fav = get_object_or_404(Favorite, user=request.user, book_id=book_id)
    fav.delete()
    return redirect('favorites_list')



# Список избранного
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('book')
    return render(request, 'shop/favorites.html', {'favorites': favorites})

# Добавление отзыва
def add_review(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = ReviewForm()
    return render(request, 'shop/add_review.html', {'form': form, 'book': book})

# Поиск книг по названию
def search_books(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(title__icontains=query) if query else []
    for book in books:
        book.discount_price = book.price - book.calculate_discount()
    return render(request, 'shop/book_list.html', {
        'page_obj': books,
        'query': query
    })


def book_list(request):
    books = Book.objects.all()
    for book in books:
        book.discount_price = book.price - book.calculate_discount()
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/book_list.html', {'page_obj': page_obj})


def available_books(request):
    books = Book.objects.filter(status='available')
    for book in books:
        book.discount_price = book.price - book.calculate_discount()
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/book_list.html', {'page_obj': page_obj})


def category_books(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = category.books.all()
    for book in books:
        book.discount_price = book.price - book.calculate_discount()
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/category_books.html', {
        'category': category,
        'page_obj': page_obj
    })


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.discount_price = book.price - book.calculate_discount()
    reviews = book.review_set.all()        # связанные отзывы
    promos = book.promobook_set.all()      # связанные акции
    return render(request, 'shop/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'promos': promos,
    })



# ======================
# CRUD для Book
# ======================

def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'shop/book_form.html', {'form': form})


def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'shop/book_form.html', {'form': form, 'book': book})


def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'shop/book_confirm_delete.html', {'book': book})


# ======================
# Примеры select_related / prefetch_related
# ======================

def books_with_author_genre(request):
    books = Book.objects.select_related('author', 'genre').all()
    return render(request, 'shop/book_list.html', {'page_obj': books})


def books_with_promotions(request):
    books = Book.objects.prefetch_related('promotions').all()
    return render(request, 'shop/book_list.html', {'page_obj': books})


# ======================
# Примеры Django ORM для части 4
# ======================

# values() и values_list()
def books_values(request):
    books = Book.objects.values('title', 'price')
    return render(request, 'shop/books_values.html', {'books': books})


def books_values_list(request):
    books = Book.objects.values_list('title', 'price')
    return render(request, 'shop/books_values_list.html', {'books': books})


# count() и exists()
def books_stats(request):
    total_books = Book.objects.count()
    has_available = Book.objects.filter(status='available').exists()
    return render(request, 'shop/books_stats.html', {
        'total_books': total_books,
        'has_available': has_available
    })


# update() и delete()
def apply_discount(request):
    Book.objects.update(discount=10)
    return redirect('book_list')


def delete_old_books(request):
    Book.objects.filter(year__lt=2000).delete()
    return redirect('book_list')


# ======================
# CRUD Author
# ======================

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'shop/author_list.html', {'authors': authors})


def create_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()
    return render(request, 'shop/author_form.html', {'form': form})


def edit_author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'shop/author_form.html', {'form': form, 'author': author})


def delete_author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        author.delete()
        return redirect('author_list')
    return render(request, 'shop/author_confirm_delete.html', {'author': author})
