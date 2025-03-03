from django import forms

from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta():
        model = Product
        exclude = ("created_at","updated_at")

class CategoryForm(forms.ModelForm):
    class Meta():
        model = Category
        exclude = ("created_at","updated_at")