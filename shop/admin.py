from django.contrib import admin, messages
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from shop.models import Banner, PageSettings, SocialMediaAccount, Shop, Product, Sale, ProductImage, ProductDescriptionImage, Color, Size, Category, Comment, WishlistItem, Order, OrderItem, RecentViewedProduct

class BannerAdmin(admin.TabularInline):
    model = Banner
    extra = 1
    show_change_link = True

class SocialMediaAccountAdmin(admin.TabularInline):
    model = SocialMediaAccount
    extra = 1

@admin.register(PageSettings)
class SettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (_("HOME PAGE META DATA"), {'fields': ('home_title', 'home_meta_description', 'home_meta_keywords')}),
        (_('PRODUCTS PAGE META DATA'), {'fields': ('products_title', 'products_meta_description', 'products_meta_keywords')}),
        (_('HOME PAGE FIRST BESTSELLER FIELD'), {'fields': ('first_field_image', 'first_field_title', 'first_field_description',
                                       'first_field_link', 'first_field_link_name')}),
        (_('HOME PAGE TRENDING FIELD'), {'fields': ('trending_image', 'trending_title', 'trending_description',
                                        'trending_link', 'trending_link_name')}),
        (_('HOME PAGE MIDDLE FIELD'), {'fields': ('middle_image', 'middle_title', 'middle_description',
                                        'middle_link', 'middle_link_name')}),
        (_('HOME PAGE LAST BESTSELLER FIELD'), {'fields': ('last_field_image', 'last_field_title', 'last_field_description',
                                        'last_field_link', 'last_field_link_name')}),
        (_('CONTACT INFORMATION'), {'fields': ('about', 'address', 'email', 'telephone')}),
    )
    inlines = [BannerAdmin, SocialMediaAccountAdmin]

    def save_model(self, request, obj, form, change):
        super(SettingsAdmin, self).save_model(request, obj, form, change)
        if obj != PageSettings.objects.first():
            messages.set_level(request, messages.ERROR)
            messages.error(request, "Sorry! You cannot add more than one setting model.")

class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductDescriptionImageAdmin(admin.TabularInline):
    model = ProductDescriptionImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'shop', 'discount_price', 'get_star_point', 'sale_number', 'in_stock', 'is_featured')
    list_filter = ('star_point', 'in_stock', 'gender', 'is_featured', 'pub_date', 'modified_date')
    search_fields = ('name', 'shop__name', 'description')
    date_hierarchy = 'modified_date'
    fieldsets = (
        (_("PRODUCT META DATA"), {'fields': ('product_meta_description', 'product_meta_keywords')}),
        (_('PRODUCT'), {'fields': ('shop', 'name', 'price', 'discount_price', 
                                   'star_point','in_stock', 'number_in_stock', 
                                   'sale_number', 'description', 'sale', 
                                   'colors', 'sizes', 'categories',
                                   'gender', 'is_featured', 'pub_date', 'modified_date')}),
    )
    inlines = [ProductImageAdmin, ProductDescriptionImageAdmin]
    actions = ['mark_in_stock', 'mark_out_of_stock', 'mark_featured', 'mark_non_featured']

    def get_star_point(self, obj):
        return obj.get_star_point()

    @admin.action(description="Mark selected products as in stock")
    def mark_in_stock(self, request, queryset):
        updated = queryset.update(in_stock=True)
        self.message_user(request, ngettext(
            "%d product was successfully marked as in stock.",
            "%d products were successfully marked as in stock.",
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description="Mark selected products as out of stock")
    def mark_out_of_stock(self, request, queryset):
        updated = queryset.update(in_stock=False)
        self.message_user(request, ngettext(
            "%d product was successfully marked as out of stock.",
            "%d products were successfully marked as out of stock.",
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description="Mark selected products as featured")
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, ngettext(
            "%d product was successfully marked as featured.",
            "%d products were successfully marked as in featured.",
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description="Mark selected products as non-featured")
    def mark_non_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, ngettext(
            "%d product was successfully marked as in non-featured.",
            "%d products were successfully marked as in non-featured.",
            updated,
        ) % updated, messages.SUCCESS)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "product", "name", "email", "rating")
    search_fields = ("comment", "name")
    list_filter = ("product__shop__name", "product__name")
    date_hierarchy = "pub_date"

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("__str__", "code")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("__str__", "get_subtotal")
    list_filter = ("created_date",)
    search_fields = ("customer__email",)
    date_hierarchy = "created_date"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("__str__", "quantity")
    list_filter = ("purchase_date",)
    search_fields = ("product__name",)
    date_hierarchy = "purchase_date"

@admin.register(WishlistItem)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("customer_email", "product__name")

@admin.register(RecentViewedProduct)
class RecentViewedzProductAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("customer_email", "product__name")

class CustomAdminSite(AdminSite):
    site_title = _("Djangoo site admin")
    site_header = _("Djangoo administration")
    index_title = _("Sitee administration")


admin.site.register(Shop)
admin.site.register(Sale)
admin.site.register(Size)
admin.site.register(Category)

AdminSite.site_title = _("Djangoo site admin")
AdminSite.site_header = _("Djangoo administration")
AdminSite.index_title = _("Sitee administration")