from django.urls import path
from customer import views

app_name = "customer"
urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('forgotpassword/', views.ForgotPasswordView.as_view(), name="forgotpassword"),
]