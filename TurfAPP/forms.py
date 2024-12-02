from django import forms
from .models import ProductDetail, ProductImage

class ProductDetailForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = ["name", "product_type", "description", 'price']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image"]
