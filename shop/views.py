
from django.shortcuts import redirect, render
from django.http import Http404, JsonResponse
from django.views import View
from django.utils import timezone
from django.db.models import Q
from shop.models import Shop, Product, Category, Order, OrderItem, PageSettings, WishlistItem, Banner, Comment, RecentViewedProduct
from customer.models import Message
import math


class IndexView(View):
    shops = Shop.objects.all()
    categories = Category.objects.all()
    settings = PageSettings.objects.first()
    banners = Banner.objects.all()
    bestseller_products = Product.objects.order_by("-sale_number")[:4]
    featured_products = Product.objects.filter(is_featured=True)

    def get(self, request):
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
            "banners": self.banners,
        }

        if request.user.is_authenticated:
            self.order = Order.objects.get(customer=request.user)
            self.orderitems = OrderItem.objects.filter(order__customer=request.user)
            self.wishlist_number = len(WishlistItem.objects.filter(customer=request.user))
            self.wishlistitems = WishlistItem.objects.filter(customer=request.user)
            self.wishlistproducts = Product.objects.filter(product_wishlistitems__customer=request.user)

            self.context["order"] = self.order
            self.context["orderitems"] = self.orderitems
            self.context["wishlist_number"] = self.wishlist_number
            self.context["wishlistitems"] = self.wishlistitems
            self.context["wishlistproducts"] = self.wishlistproducts
            
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
            wishlistitem = WishlistItem.objects.filter(customer=request.user, product=product)
            if wishlistitem.exists():
                wishlistitem.delete()
                data = {
                    "stat": "bi bi-heart",
                    "wishlistcount": len(WishlistItem.objects.filter(customer=request.user)),
                }
            else:
                WishlistItem.objects.create(customer=request.user, product=product)
                data = {
                    "stat": "bi-heart-fill whishListBackground",
                    "wishlistcount": len(WishlistItem.objects.filter(customer=request.user)),
                }


            return JsonResponse(data)



class ProductsView(View):
    shops = Shop.objects.all()
    categories = Category.objects.all()
    settings = PageSettings.objects.first()
    products = Product.objects.all()
    toptitle = "All shoes"

    def get(self, request):
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

        gender = request.GET.get("gender")
        shopname = request.GET.get("shop")
        categoryname = request.GET.get("category")

        if gender:
            self.products = Product.objects.filter(gender=gender.capitalize())
            self.toptitle = gender.capitalize()
        if shopname:
            self.products = Product.objects.filter(shop__name=shopname.capitalize())
            self.toptitle = shopname.capitalize()
        if categoryname:
            self.products = Product.objects.filter(categories__name=categoryname.capitalize())
            self.toptitle = categoryname.capitalize()

        self.context = {
            "shops": self.shops,
            "categories": self.categories,
            "settings": self.settings,
            "products": self.products,
            "toptitle": self.toptitle,
        }

        if request.user.is_authenticated:
            self.order = Order.objects.get(customer=request.user)
            self.orderitems = OrderItem.objects.filter(order__customer=request.user)
            self.wishlist_number = len(WishlistItem.objects.filter(customer=request.user))
            self.wishlistitems = WishlistItem.objects.filter(customer=request.user)
            self.wishlistproducts = Product.objects.filter(product_wishlistitems__customer=request.user)

            self.context["order"] = self.order
            self.context["orderitems"] = self.orderitems
            self.context["wishlist_number"] = self.wishlist_number
            self.context["wishlistitems"] = self.wishlistitems
            self.context["wishlistproducts"] = self.wishlistproducts

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
            wishlistitem = WishlistItem.objects.filter(customer=request.user, product=product)
            if wishlistitem.exists():
                wishlistitem.delete()
                data = {
                    "stat": "bi bi-heart",
                    "wishlistcount": len(WishlistItem.objects.filter(customer=request.user)),
                }
            else:
                WishlistItem.objects.create(customer=request.user, product=product)
                data = {
                    "stat": "bi-heart-fill whishListBackground",
                    "wishlistcount": len(WishlistItem.objects.filter(customer=request.user)),
                }


            return JsonResponse(data)


class DetailView(View):
    shops = Shop.objects.all()
    categories = Category.objects.all()
    settings = PageSettings.objects.first()

    def get(self, request, id):
        self.product = Product.objects.get(id=id)
        self.comments = self.product.comments.all()
        self.starpoint_int = int(self.product.get_star_point())
        self.starpoint_rest = 5 - math.ceil(self.product.get_star_point())
        self.has_rest = False
        product_categories = self.product.categories.all()
        wishlisted = False
        
        if WishlistItem.objects.filter(product=self.product).exists():
            wishlisted = True

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

        for category in product_categories:
            also_like_products = Product.objects.filter(categories=category).exclude(name=self.product.name)

        if self.product.get_star_point() != self.starpoint_int:
            self.has_rest = True

        self.context = {
            "shops": self.shops,
            "categories": self.categories,
            "settings": self.settings,
            "product": self.product,
            "comments": self.comments,
            "starpoint_int": range(self.starpoint_int),
            "starpoint_rest": range(self.starpoint_rest),
            "has_rest": self.has_rest,
            "also_like_products": also_like_products,
            "wishlisted": wishlisted,
        }

        if request.user.is_authenticated:
            self.order = Order.objects.get(customer=request.user)
            self.orderitems = OrderItem.objects.filter(order__customer=request.user)
            self.wishlist_number = len(WishlistItem.objects.filter(customer=request.user))
            self.wishlistitems = WishlistItem.objects.filter(customer=request.user)
            self.wishlistproducts = Product.objects.filter(product_wishlistitems__customer=request.user)
            self.recently_viewed_products = RecentViewedProduct.objects.filter(customer=request.user)

            if not RecentViewedProduct.objects.filter(customer=request.user, product=self.product).exists():
                RecentViewedProduct.objects.create(customer=request.user, product=self.product)
            else:
                recent_viewed_product = RecentViewedProduct.objects.get(customer=request.user, product=self.product)
                recent_viewed_product.viewed_date = timezone.now()
                recent_viewed_product.save()

            self.context["order"] = self.order
            self.context["orderitems"] = self.orderitems
            self.context["wishlist_number"] = self.wishlist_number
            self.context["wishlistitems"] = self.wishlistitems
            self.context["wishlistproducts"] = self.wishlistproducts
            self.context["recently_viewed_products"] = self.recently_viewed_products

        return render(request, 'detail.html', self.context)


    def post(self, request, id):
        choice = request.POST.get("choice")
        if choice == "addtocard":
            productid = request.POST.get("productid")
            color = request.POST.get("color")
            size = request.POST.get("size")
            quantity = request.POST.get("count")

            product = Product.objects.get(id=productid)
            order = Order.objects.get(customer=request.user)

            to_product = Product.objects.get(id=id)

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
            wishlistitem = WishlistItem.objects.filter(customer=request.user, product=product)
            if wishlistitem.exists():
                wishlistitem.delete()
                data = {
                    "stat": "bi bi-heart",
                    "wishlistcount": len(WishlistItem.objects.filter(customer=request.user)),
                }
            else:
                WishlistItem.objects.create(customer=request.user, product=product)
                data = {
                    "stat": "bi-heart-fill whishListBackground",
                    "wishlistcount": len(WishlistItem.objects.filter(customer=request.user)),
                }


            return JsonResponse(data)

        elif choice == "wishlisted":
            productid = request.POST.get("productid")
            product = Product.objects.get(id=productid)

            if not WishlistItem.objects.filter(customer=request.user, product=product).exists():
                WishlistItem.objects.create(customer=request.user, product=product)
                data = {
                    "itemclass" : "w bi-heart-fill whishListBackground",
                    "switch": "on",
                    "wishlistcount": len(WishlistItem.objects.filter(customer=request.user))
                }
            else:
                wishlistitem = WishlistItem.objects.get(customer=request.user, product=product)
                wishlistitem.delete()
                data = {
                    "itemclass" : "w bi bi-heart whishListIcon",
                    "switch": "off",
                    "wishlistcount": len(WishlistItem.objects.filter(customer=request.user))
                }

            return JsonResponse(data)

        elif choice == "comment":
            productid = request.POST.get("productid")
            product = Product.objects.get(id=productid)

            if request.user.is_authenticated:
                name = request.user.first_name + " " + request.user.last_name
                email = request.user.email
            else:
                name = request.POST.get("name")
                email = request.POST.get("email")
            
            rating = request.POST.get("rating")
            comment = request.POST.get("comment")

            newComment = Comment.objects.create(
                product = product,
                name = name,
                email = email,
                rating = rating,
                comment = comment,
            )


            data = {
                "name": newComment.name,
                "email": newComment.email,
                "rating": newComment.rating,
                "comment": newComment.comment,
                "pub_date": newComment.pub_date.strftime("%b %d, %Y"),
                "comments_number": len(Comment.objects.filter(product=product)),
                "starpoint_int": int(product.get_star_point()),
                "has_rest": True if product.get_star_point() != int(product.get_star_point()) else False,
                "starpoint_rest":  5 - math.ceil(product.get_star_point()),
            }

            return JsonResponse(data)



        


class ContactView(View):
    shops = Shop.objects.all()
    categories = Category.objects.all()
    settings = PageSettings.objects.first()

    def get(self, request):

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
        }

        if request.user.is_authenticated:
            self.order = Order.objects.get(customer=request.user)
            self.orderitems = OrderItem.objects.filter(order__customer=request.user)
            self.wishlist_number = len(WishlistItem.objects.filter(customer=request.user))

            self.context["order"] = self.order
            self.context["orderitems"] = self.orderitems
            self.context["wishlist_number"] = self.wishlist_number

        return render(request, 'contact.html', self.context)

    def post(self, request):
        choice = request.POST.get("choice")
        if choice == "message":
            if request.user.is_authenticated:
                name = request.user.first_name + " " + request.user.last_name
                email = request.user.email
                tel = request.user.phone_number
            else:
                name = request.POST.get("name")
                email = request.POST.get("email")
                tel = request.POST.get("tel")
            message = request.POST.get("message")

            Message.objects.create(
                name = name,
                email = email,
                phone_number = tel,
                message = message,
            )

            data = {
                "stat": "Sent",
            }

            return JsonResponse(data)



        
class WishlistView(View):
    shops = Shop.objects.all()
    categories = Category.objects.all()
    settings = PageSettings.objects.first()

    def get(self, request):

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
        }

        if request.user.is_authenticated:
            self.order = Order.objects.get(customer=request.user)
            self.orderitems = OrderItem.objects.filter(order__customer=request.user)
            self.wishlist_number = len(WishlistItem.objects.filter(customer=request.user))
            self.wishlistitems = WishlistItem.objects.filter(customer=request.user)

            self.context["order"] = self.order
            self.context["orderitems"] = self.orderitems
            self.context["wishlist_number"] = self.wishlist_number
            self.context["wishlistitems"] = self.wishlistitems

        return render(request, 'wishlist.html', self.context)

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
            wishlistitemid = request.POST.get("wishlistitemid")
            wishlistitem = WishlistItem.objects.get(id=wishlistitemid)
            wishlistitem.delete()

            data = {
                "info": wishlistitem.product.name + " removed from wishlist.",
                "wishlistcount": len(WishlistItem.objects.filter(customer=request.user)),
            }

            return JsonResponse(data)

class CheckoutView(View):
    shops = Shop.objects.all()
    categories = Category.objects.all()
    settings = PageSettings.objects.first()
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
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

        self.context = {
            "shops": self.shops,
            "categories": self.categories,
            "settings": self.settings,
            "order": self.order,
            "orderitems": self.orderitems,
            "wishlist_number": self.wishlist_number,
        }

        return render(request, 'checkout.html', self.context)




