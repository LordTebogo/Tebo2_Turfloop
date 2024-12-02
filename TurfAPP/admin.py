from django.contrib import admin
from .models import UserProfile, Business, ProductDetail, ProductImage

# UserProfile Admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', 'date_of_birth')
    search_fields = ('user__username', 'phone_number', 'address')
    list_filter = ('date_of_birth',)


# Business Admin
@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_profile', 'created_at', 'logo_preview')
    search_fields = ('name', 'user_profile__user__username')
    list_filter = ('created_at',)

    def logo_preview(self, obj):
        if obj.logo:
            return f'<img src="{obj.logo.url}" style="width: 50px; height: auto;" />'
        return "No logo"
    logo_preview.allow_tags = True
    logo_preview.short_description = 'Logo'


# Inline for ProductImage to manage images directly from ProductDetail
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms for additional images
    fields = ('image', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="width: 50px; height: auto;" />'
        return "No image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'


# ProductDetail Admin
@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'product_type', 'date_added')
    search_fields = ('name', 'product_type', 'business__name')
    list_filter = ('product_type', 'date_added')
    inlines = [ProductImageInline]


# ProductImage Admin
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview')
    search_fields = ('product__name',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="width: 50px; height: auto;" />'
        return "No image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'
