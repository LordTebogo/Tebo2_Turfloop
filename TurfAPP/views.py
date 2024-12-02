from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import ProductImage, UserProfile, Business, ProductDetail
from django.contrib import messages
from .forms import ProductDetailForm, ProductImageForm
from django.db.models import Q


# Updated register view

def register(request):
    if request.method == "POST":
        # User fields
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        # UserProfile fields
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        date_of_birth = request.POST.get("date_of_birth")
        
        # Business fields
        business_name = request.POST.get("business_name")
        business_description = request.POST.get("business_description")
        logo = request.FILES.get("logo")

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "register.html", request.POST)  # Re-render with the submitted data

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken!")
            return render(request, "register.html", request.POST)
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return render(request, "register.html", request.POST)

        # Create the User
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        # Create the UserProfile
        user_profile = UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            address=address,
            date_of_birth=date_of_birth,
        )

        # Create the Business
        Business.objects.create(
            user_profile=user_profile,
            name=business_name,
            description=business_description,
            logo=logo,
        )

        messages.success(request, "Registration successful! Please log in.")
        return redirect("login")

    return render(request, "register.html")

# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("homepage")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")

# Edit product view

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(ProductDetail, id=product_id, business__user_profile=request.user.profile)
    ProductImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=1, can_delete=True)

    if request.method == "POST":
        # Handle product details
        product_form = ProductDetailForm(request.POST, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, queryset=product.images.all())

        if product_form.is_valid() and formset.is_valid():
            product_form.save()
            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    form.instance.delete()
                elif form.cleaned_data:
                    form.instance.product = product
                    form.save()

            messages.success(request, "Product updated successfully.")
            return redirect("dashboard")
    else:
        product_form = ProductDetailForm(instance=product)
        formset = ProductImageFormSet(queryset=product.images.all())

    return render(request, "edit_product.html", {
        "product_form": product_form,
        "formset": formset,
        "product": product
    })



# Delete product view
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(ProductDetail, id=product_id, business__user_profile=request.user.profile)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect("dashboard")



def homepage(request):
    query = request.GET.get("q", "")
    products = ProductDetail.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(business__name__icontains=query) |
            Q(product_type__icontains=query)  # Assuming category field is present
        )

    # Check if the request is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return only the HTML for the filtered products
        return render(request, "partials/product_grid.html", {"products": products})

    # Return full page when not an AJAX request
    return render(request, "homepage.html", {"products": products, "query": query})



# Dashboard view with enhanced error handling
@login_required
def dashboard(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found. Please complete your profile.")
        return redirect("register")

    try:
        business = Business.objects.get(user_profile=user_profile)
    except Business.DoesNotExist:
        messages.error(request, "You must register a business to manage products.")
        return redirect("register")

    products = ProductDetail.objects.filter(business=business)

    return render(request, "dashboard.html", {"products": products})


# Add product with product_type
@login_required
def add_product(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found. Please complete your profile.")
        return redirect("register")

    try:
        business = Business.objects.get(user_profile=user_profile)
    except Business.DoesNotExist:
        messages.error(request, "You must register a business to add products.")
        return redirect("register")
    
    ProductImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=3)

    if request.method == "POST":
        product_form = ProductDetailForm(request.POST)
        formset = ProductImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())

        if product_form.is_valid() and formset.is_valid():
            product = product_form.save(commit=False)
            product.business = business
            product.save()

            for form in formset:
                if form.cleaned_data:
                    image = form.save(commit=False)
                    image.product = product
                    image.save()

            messages.success(request, "Product added successfully.")
            return redirect("dashboard")
    else:
        product_form = ProductDetailForm()
        formset = ProductImageFormSet(queryset=ProductImage.objects.none())

    return render(request, "add_product.html", {
        "product_form": product_form,
        "formset": formset,
    })


# Product detail view
def product_detail(request, product_id):
    product = get_object_or_404(ProductDetail, id=product_id)
    images = product.images.all()

    return render(request, "product_detail.html", {"product": product, "images":images})