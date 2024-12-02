from django.contrib.auth.models import User
from django.db import models

# UserProfile model extending the Django User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

# Business model linking only to UserProfile
class Business(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

# ProductDetail model for products under a Business
class ProductDetail(models.Model):  
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=100)  # e.g., 'Electronics', 'Food', etc.
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ProductImage model for handling multiple images per product
class ProductImage(models.Model):
    product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    
    def __str__(self):
        return f"Image for {self.product.name}"
