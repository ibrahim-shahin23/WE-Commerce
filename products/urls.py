from django.urls import path
from .views import DeleteCategoryView, DeleteProductView, EditCategoryView, ProductListView, CategoryListView, SingleProductView, SingleCategoryView , ProductSearchView ,CreateProductView, CreateCategoryView, EditProductView# Import the views

urlpatterns = [
    path('', ProductListView.as_view(), name='all_products'),
    path("<int:product_id>/", SingleProductView.as_view(), name="one_product"),
    path("categories/", CategoryListView.as_view(), name="all_categories"),
    path("categories/<int:category_id>/", SingleCategoryView.as_view(), name="one_category") , 
    path('search/', ProductSearchView.as_view(), name='search_products'),
    path('add_product/', CreateProductView.as_view(), name='add_product'),
    path('edit_product/<int:product_id>/', EditProductView.as_view(), name='edit_product'),
    path('delete_product/<int:product_id>/', DeleteProductView.as_view(), name='delete_product'),
    path('edit_category/<int:category_id>/', EditCategoryView.as_view(), name='edit_category'),
    path('delete_category/<int:category_id>/', DeleteCategoryView.as_view(), name='delete_category'),
    path('add_category/', CreateCategoryView.as_view(), name='add_category')
]
