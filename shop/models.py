from django.db import models
from django.contrib import messages
from customer.models import Customer
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import math

class Banner(models.Model):
    setting = models.ForeignKey("shop.PageSettings", on_delete=models.CASCADE, related_name="banners")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    link = models.URLField(max_length=250, blank=True, null=True)
    link_name = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField()

    class Meta:
        ordering = ("-id", )

    def __str__(self):
        return self.title

class PageSettings(models.Model):
    home_title = models.CharField(max_length=300)
    home_meta_description = models.TextField()
    home_meta_keywords = models.TextField()

    products_title = models.CharField(max_length=300)
    products_meta_description = models.TextField()
    products_meta_keywords = models.TextField()

    first_field_image = models.ImageField("Image", blank=True, null=True)
    first_field_title = models.CharField("Title", max_length=100, blank=True, null=True)
    first_field_description = models.CharField("Description", max_length=250, blank=True, null=True)
    first_field_link = models.URLField("Link", max_length=250, blank=True, null=True)
    first_field_link_name = models.CharField("Link name", max_length=50, blank=True, null=True)

    trending_image = models.ImageField("Image", blank=True, null=True)
    trending_title = models.CharField("Title", max_length=100, blank=True, null=True)
    trending_description = models.CharField("Description", max_length=250, blank=True, null=True)
    trending_link = models.URLField("Link", max_length=250, blank=True, null=True)
    trending_link_name = models.CharField("Link name", max_length=50, blank=True, null=True)

    middle_image = models.ImageField("Image", blank=True, null=True)
    middle_title = models.CharField("Title", max_length=100, blank=True, null=True)
    middle_description = models.CharField("Description", max_length=250, blank=True, null=True)
    middle_link = models.URLField("Link", max_length=250, blank=True, null=True)
    middle_link_name = models.CharField("Link name", max_length=50, blank=True, null=True)

    last_field_image = models.ImageField("Image", blank=True, null=True)
    last_field_title = models.CharField("Title", max_length=100, blank=True, null=True)
    last_field_description = models.CharField("Description", max_length=250, blank=True, null=True)
    last_field_link = models.URLField("Link", max_length=250, blank=True, null=True)
    last_field_link_name = models.CharField("Link name", max_length=50, blank=True, null=True)

    about = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True)
    telephone = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"

    def save(self, *args, **kwargs):
        settings = PageSettings.objects.all()
        if len(settings) == 0 or self == PageSettings.objects.first():
            return super(PageSettings, self).save(*args, **kwargs)
        else:
            pass
        

    def __str__(self):
        return "Settings"

class SocialMediaAccount(models.Model):
    setting = models.ForeignKey(PageSettings, on_delete=models.CASCADE, related_name="socialmediaaccounts")
    name = models.CharField("Social media name", max_length=25)
    link = models.URLField("Account link", max_length=250)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(blank=True, null=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.name

class Product(models.Model):
    
    GENDER = [
        ("Men", "Men"),
        ("Women", "Women"),
        ("Kid", "Kid"),
        ("Unisex", "Unisex")
    ]

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_products")
    name = models.CharField(max_length=250)
    price = models.FloatField(default=0)
    discount_price = models.FloatField(default=0)
    star_point = models.FloatField(default=0)
    in_stock = models.BooleanField(default=True)
    number_in_stock = models.IntegerField(default=0)
    sale_number = models.IntegerField(default=0)
    description = models.TextField()
    sale = models.ForeignKey("shop.Sale", on_delete=models.SET_NULL, blank=True, null=True)
    colors = models.ManyToManyField("shop.Color", related_name="color_products", blank=True)
    sizes = models.ManyToManyField("shop.Size", related_name="size_products", blank=True)
    categories = models.ManyToManyField("shop.Category", related_name="category_products", blank=True)
    gender = models.CharField(max_length=6, choices=GENDER, default="Unisex")
    is_featured = models.BooleanField(default=False)
    pub_date = models.DateTimeField("Publication date", default=timezone.now)
    modified_date = models.DateTimeField("Modified date",  default=timezone.now)

    product_meta_description = models.TextField(default="")
    product_meta_keywords = models.TextField(default="")

    def get_star_point(self):
        sum = 0
        for comment in self.comments.all():
            sum += comment.rating

        if self.comments.all():
            return sum / (len(self.comments.all()))
        else:
            return sum

    class Meta:
        ordering = ("-id",)


    def save(self, *args, **kwargs):
        if not Product.objects.filter(id=self.id).exists():
            self.pub_date = timezone.now()
        self.modified_date = timezone.now()
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Sale(models.Model):
    percent = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ("-id", )

    def __str__(self):
        return str(self.percent) + "%"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()

    class Meta:
        ordering = ("-id",)
        verbose_name = "Product image"
        verbose_name_plural = "Product images"

    def __str__(self):
        return self.product.name + " | " + self.id

class ProductDescriptionImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()

    class Meta:
        ordering = ("-id",)
        verbose_name = "Product description image"
        verbose_name_plural = "Product description images"

    def __str__(self):
        return self.product.name + " | " + self.id
    
class Color(models.Model):
    name = models.CharField(max_length=15)
    code = models.CharField(max_length=6)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.name

class Size(models.Model):
    number = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ("number",)

    def __str__(self):
        return str(self.number)

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.comment[:25] + "..."


class WishlistItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_wishlistitems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_wishlistitems")
    
    class Meta:
        ordering = ("-id", )

    def __str__(self):
        return self.product.name

class Order(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="order", blank=True, null=True)
    subtotal = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)

    def get_subtotal(self):
        subtotal = 0
        for orderitem in OrderItem.objects.filter(order=self):
            subtotal += orderitem.product.price * orderitem.quantity

        return subtotal

    def __str__(self):
        return self.customer.email

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, related_name="product_orderitems")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_orderitems")
    quantity = models.SmallIntegerField(default=0)
    color = models.CharField(max_length=20, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id", )
        verbose_name = "Order item"
        verbose_name_plural = "Order items"

    def __str__(self):
        return self.product.name

class RecentViewedProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="recentviewedproducts")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products_recentviewedproducts")
    viewed_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-viewed_date", )

    def __str__(self):
        return self.product.name