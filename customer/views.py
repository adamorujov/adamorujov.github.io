from django.shortcuts import render
from django.views import View
from shop.models import Shop, Category, Order, OrderItem, WishlistItem

class LoginView(View):
    def get(self, request):
        self.shops = Shop.objects.all()
        self.categories = Category.objects.all()
        self.order = Order.objects.get(customer=request.user)
        self.orderitems = OrderItem.objects.filter(order__customer=request.user)
        self.wishlist_number = len(WishlistItem.objects.filter(customer=request.user))

        self.context = {
            "shops": self.shops,
            "categories": self.categories,
            "order": self.order,
            "orderitems": self.orderitems,
            "wishlist_number": self.wishlist_number,
        }
        return render(request, 'login.html', self.context)

class RegisterView(View):
    def get(self, request):
        self.shops = Shop.objects.all()
        self.categories = Category.objects.all()
        self.order = Order.objects.get(customer=request.user)
        self.orderitems = OrderItem.objects.filter(order__customer=request.user)
        self.wishlist_number = len(WishlistItem.objects.filter(customer=request.user))

        self.context = {
            "shops": self.shops,
            "categories": self.categories,
            "order": self.order,
            "orderitems": self.orderitems,
            "wishlist_number": self.wishlist_number,
        }
        return render(request, 'register.html', self.context)

class ForgotPasswordView(View):
    def get(self, request):
        self.shops = Shop.objects.all()
        self.categories = Category.objects.all()
        self.order = Order.objects.get(customer=request.user)
        self.orderitems = OrderItem.objects.filter(order__customer=request.user)
        self.wishlist_number = len(WishlistItem.objects.filter(customer=request.user))

        self.context = {
            "shops": self.shops,
            "categories": self.categories,
            "order": self.order,
            "orderitems": self.orderitems,
            "wishlist_number": self.wishlist_number,
        }
        return render(request, 'forgotpassword.html', self.context)

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def forgotpassword(request):
    return render(request, 'forgotpassword.html')