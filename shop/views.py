from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from django.db.models import Q
from shop.models import Shop, Product, Category, Order, OrderItem, PageSettings, WishlistItem, Banner, Comment, RecentViewedProduct
import math


class IndexView(View):
    shops = Shop.objects.all()
    categories = Category.objects.all()
    settings = PageSettings.objects.first()
    banners = Banner.objects.all()
    bestseller_products = Product.objects.order_by("-sale_number")[:4]
    featured_products = Product.objects.filter(is_featured=True)

    def get(self, request):
        self.order = Order.objects.get(customer=request.user)
        self.orderitems = OrderItem.objects.filter(order__customer=request.user)
        self.wishlist_number = len(WishlistItem.objects.filter(customer=request.user))
        self.wishlistitems = WishlistItem.objects.filter(customer=request.user)
        query = request.GET.get("q")
        if query:
            self.searching_products = Product.objects.filter(name__icontains=query).values()
            data = list(self.searching_products)
            return JsonResponse(data, safe=False)

        orderitemid = request.GET.get("orderitemid")
        if orderitemid:
            orderitem = OrderItem.objects.get(id=orderitemid)
            orderitem.delete()

            data = {
                "productprice": orderitem.product.price,
                "orderitemquantity": orderitem.quantity,
            }
            return JsonResponse(data)

        self.context = {
            "shops": self.shops,
            "categories": self.categories,
            "settings": self.settings,
            "bestseller_products": self.bestseller_products,
            "featured_products": self.featured_products,
            "order": self.order,
            "wishlist_number": self.wishlist_number,
            "orderitems": self.orderitems,
            "banners": self.banners,
            "wishlistitems": self.wishlistitems,
        }

        return render(request, 'index.html', self.context)

    def post(self, request):
        choice = request.POST.get("choice")
        if choice == "addtocard":
            id = request.POST.get("productid")
            color = request.POST.get("color")
            size = request.POST.get("size")
            quantity = request.POST.get("count")

            product = Product.objects.get(id=id)
            order = Order.objects.get(customer=request.user)

            orderitem = OrderItem.objects.create(
                product = product,
                order = order,
                quantity = quantity,
                color = color,
                size = size
            )

            data = {
                "productname": product.name,
                "productid": product.id,
                "productprice": product.price,
                "orderitemid": orderitem.id,
                "orderitemsize": orderitem.size,
                "orderitemcolor": orderitem.color,
                "quantity": quantity,
                "color": color,
                "size": size,
            }

            return JsonResponse(data)

        elif choice == "wishlist":
            productid = request.POST.get("productid")
            product = Product.objects.get(id=productid)
            if WishlistItem.objects.filter(customer=request.user, product=product).exists():
                data = {
                    "warning": "Product is already in wishlist. Go to product detail or wishlist page to remove it.", 
                }
            else:
                WishlistItem.objects.create(customer=request.user, product=product)
                data = {
                    "wishlistcount": len(WishlistItem.objects.all()),
                }

            return JsonResponse(data)



class ProductsView(View):
    shops = Shop.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all()

    def get(self, request):
        self.order = Order.objects.get(customer=request.user)
        self.orderitems = OrderItem.objects.filter(order__customer=request.user)
        self.wishlist_number = len(WishlistItem.objects.filter(customer=request.user))
        query = request.GET.get("q")
        if query:
            self.searching_products = Product.objects.filter(name__icontains=query).values()
            data = list(self.searching_products)
            return JsonResponse(data, safe=False)

        orderitemid = request.GET.get("orderitemid")
        if orderitemid:
            orderitem = OrderItem.objects.get(id=orderitemid)
            orderitem.delete()

            data = {
                "productprice": orderitem.product.price,
                "orderitemquantity": orderitem.quantity,
            }
            return JsonResponse(data)

        minprice = request.GET.get("minprice")
        maxprice = request.GET.get("maxprice")

        if minprice and maxprice:
            self.products = Product.objects.filter(Q(discount_price__gte=minprice), Q(discount_price__lte=maxprice))
            
            data = {
                "products": list(self.products.values()),
            }

            return JsonResponse(data)

        self.context = {
            "shops": self.shops,
            "categories": self.categories,
            "wishlist_number": self.wishlist_number,
            "products": self.products,
            "order": self.order,
            "orderitems": self.orderitems,
        }

        return render(request, 'products.html', self.context)

    def post(self, request):
        choice = request.POST.get("choice")
        if choice == "addtocard":
            id = request.POST.get("productid")
            color = request.POST.get("color")
            size = request.POST.get("size")
            quantity = request.POST.get("count")

            product = Product.objects.get(id=id)
            order = Order.objects.get(customer=request.user)

            orderitem = OrderItem.objects.create(
                product = product,
                order = order,
                quantity = quantity,
                color = color,
                size = size
            )

            data = {
                "productname": product.name,
                "productid": product.id,
                "productprice": product.price,
                "orderitemid": orderitem.id,
                "orderitemsize": orderitem.size,
                "orderitemcolor": orderitem.color,
                "quantity": quantity,
                "color": color,
                "size": size,
            }

            return JsonResponse(data)

        elif choice == "wishlist":
            productid = request.POST.get("productid")
            product = Product.objects.get(id=productid)
            if WishlistItem.objects.filter(customer=request.user, product=product).exists():
                data = {
                    "warning": "Product is already in wishlist. Go to product detail or wishlist page to remove it.", 
                }
            else:
                WishlistItem.objects.create(customer=request.user, product=product)
                data = {
                    "wishlistcount": len(WishlistItem.objects.all()),
                }

            return JsonResponse(data)


class DetailView(View):
    shops = Shop.objects.all()
    categories = Category.objects.all()

    def get(self, request, id):
        self.order = Order.objects.get(customer=request.user)
        self.orderitems = OrderItem.objects.filter(order__customer=request.user)
        self.wishlist_number = len(WishlistItem.objects.filter(customer=request.user))
        self.product = Product.objects.get(id=id)
        self.comments = self.product.comments.all()
        self.starpoint_int = int(self.product.get_star_point())
        self.startpoint_rest = 5 - math.ceil(self.product.get_star_point())
        self.has_rest = False
        self.recently_viewed_products = RecentViewedProduct.objects.filter(customer=request.user)
        product_categories = self.product.categories.all()
        wishlisted = False

        if WishlistItem.objects.filter(product=self.product).exists():
            wishlisted = True

        query = request.GET.get("q")
        if query:
            self.searching_products = Product.objects.filter(name__icontains=query).values()
            data = list(self.searching_products)
            return JsonResponse(data, safe=False)

        for category in product_categories:
            also_like_products = Product.objects.filter(categories=category).exclude(name=self.product.name)

        if not RecentViewedProduct.objects.filter(customer=request.user, product=self.product).exists():
            RecentViewedProduct.objects.create(customer=request.user, product=self.product)
        else:
            recent_viewed_product = RecentViewedProduct.objects.get(customer=request.user, product=self.product)
            recent_viewed_product.viewed_date = timezone.now()
            recent_viewed_product.save()

        if self.product.star_point != self.starpoint_int:
            self.has_rest = True

        self.context = {
            "shops": self.shops,
            "categories": self.categories,
            "wishlist_number": self.wishlist_number,
            "product": self.product,
            "order": self.order,
            "orderitems": self.orderitems,
            "comments": self.comments,
            "starpoint_int": range(self.starpoint_int),
            "starpoint_rest": range(self.startpoint_rest),
            "has_rest": self.has_rest,
            "also_like_products": also_like_products,
            "recently_viewed_products": self.recently_viewed_products,
            "wishlisted": wishlisted,
        }

        return render(request, 'detail.html', self.context)



class ContactView(View):
    shops = Shop.objects.all()
    categories = Category.objects.all()

    def get(self, request):
        self.order = Order.objects.get(customer=request.user)
        self.orderitems = OrderItem.objects.filter(order__customer=request.user)
        self.wishlist_number = len(WishlistItem.objects.filter(customer=request.user))
        self.pagesettings = PageSettings.objects.first()

        self.context = {
            "shops": self.shops,
            "categories": self.categories,
            "order": self.order,
            "orderitems": self.orderitems,
            "wishlist_number": self.wishlist_number,
            "pagesettings": self.pagesettings,
        }

        return render(request, 'contact.html', self.context)
        
class WishlistView(View):
    shops = Shop.objects.all()
    categories = Category.objects.all()

    def get(self, request):
        self.order = Order.objects.get(customer=request.user)
        self.orderitems = OrderItem.objects.filter(order__customer=request.user)
        self.wishlist_number = len(WishlistItem.objects.filter(customer=request.user))
        self.wishlistitems = WishlistItem.objects.filter(customer=request.user)

        self.context = {
            "shops": self.shops,
            "categories": self.categories,
            "order": self.order,
            "orderitems": self.orderitems,
            "wishlist_number": self.wishlist_number,
            "wishlistitems": self.wishlistitems,
        }

        return render(request, 'wishlist.html', self.context)


def wishlist(request):
    return render(request, 'wishlist.html')

def checkout(request):
    return render(request, 'checkout.html')


def removeOrderItem(request, id):
    orderitem = OrderItem.objects.get(id=id)
    orderitem.delete()
    return redirect("index")

