# shop/forms.py
from django import forms
from .models import Author, Book

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

class BookForm(forms.ModelForm):  # <-- добавляем эту форму
    class Meta:
        model = Book
        fields = '__all__'
