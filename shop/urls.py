from django.urls import path
from shop import views

app_name = "shop"
urlpatterns = [
    path('products/', views.ProductsView.as_view(), name="products"),
    path('detail/<int:id>/', views.DetailView.as_view(), name="detail"),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('wishlist/', views.WishlistView.as_view(), name="wishlist"),
    path('checkout/', views.checkout, name="checkout"),
    path('removeorderitem/<int:id>/', views.removeOrderItem, name="removeorderitem"),
]
