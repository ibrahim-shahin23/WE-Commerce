from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import CategoryForm, ProductForm
from .models import Cart, CartItem, Product, Category
from django.views.generic import ListView, DetailView ,CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin ,UserPassesTestMixin
from django.contrib.auth.decorators import login_required


class ProductListView(ListView):
    model = Product  # Specify the model to use
    template_name = "products/products.html"  # Specify the template
    context_object_name = "products"  # Name of the context variable in the template

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)

        # Add additional context (e.g., error_message)
        if not context["products"]:
            context["error_message"] = "No products found"
        else:
            context["error_message"] = ""
        return context

class SingleProductView(DetailView):
    model = Product
    template_name = "products/product_info.html"
    context_object_name = 'product' 
    pk_url_kwarg = 'product_id'


class CategoryListView(ListView):
    model=Category
    template_name='products/categories.html'
    context_object_name = "categories"
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)

        # Add additional context (e.g., error_message)
        if not context["categories"]:
            context["error_message"] = "No categories found"
        else:
            context["error_message"] = ""
        return context

class SingleCategoryView(DetailView):
    model = Category
    template_name = 'products/products.html'
    context_object_name = 'category'
    pk_url_kwarg = 'category_id'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        # Add the products to the context
        category_id = self.kwargs.get("category_id")  # Assuming the URL uses `category_id` for category ID
        context["products"] = self.object.products.all()
        if not context["products"]:
            context["error_message"] = "No products found"
        else:
            context["error_message"] = ""
        return context


class ProductSearchView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    def get_queryset(self):
        # Get the search query from the URL parameter 'title'
        query = self.request.GET.get("title")
        if query:
            # Filter products by title (case-insensitive)
            return Product.objects.filter(title__icontains=query)
        else:
            # Return an empty queryset if no query is provided
            return Product.objects.none()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        # Add the search query to the context
        context["query"] = self.request.GET.get("title", "")
        return context

class CreateProductView(LoginRequiredMixin, CreateView):
    template_name = "products/forms/form.html"
    form_class = ProductForm
    success_url = "/products/"
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Add New Product"
        return context
    def form_valid(self, form):
        print("product added successfully")
        return super().form_valid(form)
    
    
class EditProductView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "products/forms/form.html"
    form_class = ProductForm
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy("all_products")
    extra_context = {"form_title" : "Edit Product"}

class CreateCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = "products/forms/form.html"
    form_class = CategoryForm
    success_url = "/products/categories/"
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Add New Category"
        return context
    
class EditCategoryView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = "products/forms/form.html"
    form_class = CategoryForm
    pk_url_kwarg = 'category_id'
    extra_context = {"form_title" : "Edit Category"}
    success_url = reverse_lazy("all_categories")

class DeleteProductView(UserPassesTestMixin,DeleteView):
    model = Product
    success_url = reverse_lazy("all_products")
    pk_url_kwarg = 'product_id'

    def test_func(self):
        return self.request.user.is_superuser
    
class DeleteCategoryView(UserPassesTestMixin,DeleteView):
    model = Category
    success_url = reverse_lazy("all_categories")
    pk_url_kwarg = 'category_id'

    def test_func(self):
        return self.request.user.is_superuser
    
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if(product):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return JsonResponse({"success":True},status=200)
    else:
        return JsonResponse({"success":False},status=404)
# redirect('view_cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    return render(request, 'cart/view_cart.html', {'cart_items': cart_items})

@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    return redirect('view_cart')