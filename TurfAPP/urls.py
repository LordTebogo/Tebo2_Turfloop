from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.homepage, name='homepage'),

    # Registration
    path('register/', views.register, name='register'),

    # Login
    path('login/', views.login_view, name='login'),

    # Logout
    path('logout/', views.logout_view, name='logout'),

    # Dashboard (requires login)
    path('dashboard/', views.dashboard, name='dashboard'),

    # Add Product
    path('add_product/', views.add_product, name='add_product'),

    # Edit Product (with ID)
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),

    # Delete Product (with ID)
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

    # Product Detail (with ID)
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
]
