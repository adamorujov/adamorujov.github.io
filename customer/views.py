from django.shortcuts import render, redirect
from django.views import View
from shop.models import PageSettings, Shop, Product, Category, Order, OrderItem, WishlistItem
from django.contrib.auth import views as auth_views
from customer.forms import LoginForm, RegisterForm, RecoverPasswordForm
from customer.models import Customer
from django.http import JsonResponse, Http404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail

class LoginView(auth_views.LoginView):
    settings = PageSettings.objects.first()

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        if request.user.is_authenticated:
            raise Http404
        self.shops = Shop.objects.all()
        self.categories = Category.objects.all()

        query = request.GET.get("q")
        if query:
            self.searching_products = Product.objects.filter(name__icontains=query).values()
            data = list(self.searching_products)
            return JsonResponse(data, safe=False)

        self.context = {
            "shops": self.shops,
            "categories": self.categories,
            "settings": self.settings,
            "form": form,
        }
        return render(request, 'login.html', self.context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, email=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                messages.info(request, "Please, enter correct email and password.")
                return redirect("customer:login")
        messages.info(request, "Invalid username or password.")
        return redirect("customer:login")


class RegisterView(View):
    settings = PageSettings.objects.first()

    def get(self, request):
        self.shops = Shop.objects.all()
        self.categories = Category.objects.all()
        if request.user.is_authenticated:
            raise Http404

        form = RegisterForm()
        self.context = {
            "shops": self.shops,
            "categories": self.categories,
            "settings": self.settings,
            "form": form,
        }
        return render(request, 'register.html', self.context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            username = form.cleaned_data.get("username")
            phone_number = form.cleaned_data.get("phone_number")
            password = form.cleaned_data.get("password1")

            user = authenticate(request, email=username, password=password)

            if user is not None or Customer.objects.filter(email=username).exists():
                messages.info(request, "This account is already exists.")
                return redirect("customer:register")
            else:
                newUser = Customer.objects.create_user(
                    email=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                )
                Order.objects.create(customer=newUser)
                login(request, newUser)
                return redirect("index")
        messages.info(request, "Please, enter valid data.")
        return redirect("customer:register")

class ForgotPasswordView(View):
    settings = PageSettings.objects.first()
    def get(self, request):
        self.shops = Shop.objects.all()
        self.categories = Category.objects.all()

        form = RecoverPasswordForm()

        self.context = {
            "shops": self.shops,
            "categories": self.categories,
            "settings": self.settings,
            "form": form,
        }

        if request.user.is_authenticated:
            self.order = Order.objects.get(customer=request.user)
            self.orderitems = OrderItem.objects.filter(order__customer=request.user)
            self.wishlist_number = len(WishlistItem.objects.filter(customer=request.user))

            self.context["order"] = self.order
            self.context["orderitems"] = self.orderitems
            self.context["wishlist_number"] = self.wishlist_number

        return render(request, 'forgotpassword.html', self.context)

    def post(self, request, *args, **kwargs):
        form = RecoverPasswordForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            if Customer.objects.filter(email=username).exists():
                send_mail(
                    'Change Password',
                    'Change your password here.',
                    'ademorujov@gmail.com',
                    [username],
                    fail_silently=False,
                )
                messages.info(request, "Please, check out your mail and change your password.")
                return redirect("customer:forgotpassword")
            else:
                messages.info(request, "Please, enter your correct mail address.")
                return redirect("customer:forgotpassword")
        messages.info(request, "Please, enter your correct mail address.")
        return redirect("customer:forgotpassword")

