from django import forms
from .models import Author, Book

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['full_name', 'bio', 'photo']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'aria-label': 'Полное имя автора'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'aria-label': 'Биография автора'}),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'series', 'year', 'isbn', 'price', 'discount', 'description', 'cover', 'file', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'aria-label': 'Название книги'}),
            'author': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Автор'}),
            'genre': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Жанр'}),
            'series': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Серия'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'aria-label': 'Год издания'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'aria-label': 'ISBN'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'aria-label': 'Цена'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'aria-label': 'Скидка'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'aria-label': 'Описание'}),
        }
