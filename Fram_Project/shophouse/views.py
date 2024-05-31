from django.shortcuts import render,redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from authenticate.models import *
from shophouse.models import *
from base.simple_pgrm import *

# Create your views here.

def list_on_sale(product_list):
    sorted_list = sorted(product_list, key=lambda x: x.on_sale, reverse=True)
    return sorted_list

def list_higest_price(product_list):
    sorted_list= sorted(product_list, key= lambda x: x.price, reverse=True )
    return sorted_list

def list_lowest_price(product_list):
    sorted_list= sorted(product_list, key= lambda x: x.price, reverse=False )
    return sorted_list

def list_rating(product_list):
    sorted_list= sorted(product_list, key= lambda x: x.Rate, reverse=True )
    return sorted_list

def short_request(request, short_id):
    if short_id == 'none':
        return redirect('home')
    else:
        return home(request, short_on=short_id )




def home(request, short_on='none'):

    products = list(Product.objects.all())
    if short_on == 'sale':
        products= list_on_sale(products)
    elif short_on == 'H_price':
        products= list_higest_price(products)    
    elif short_on == 'L_price':
        products= list_lowest_price(products) 
    elif short_on == 'rate':
        products= list_rating(products) 

    total_items_num=0
    identify_farmer_=None
    
    if request.user.is_authenticated:
        carts_info = Cart.objects.filter(user=request.user, status= 'cart')
        for each in carts_info:
            total_items_num += each.quantity
        
        identify_farmer_= identify_farmer(request.user)
        total_items_num=total_items_num
    

    if request.method == 'GET':
    
        query = request.GET.get('query')
        if query:
            products = Product.objects.filter(title__icontains=query) 
   
    context = {'product': products, 'identify_farmer': identify_farmer_, "total_items_num":total_items_num}  
    
    return render(request, 'pages/index.html', context)


def product_view(request, slug):
    try: 
        products = Product.objects.get(slug=slug)
        context = {'product': products}
        total_items_num = 0
        if request.user.is_authenticated:
            carts_info = Cart.objects.filter(user=request.user, status= 'cart')
            for each in carts_info:
                total_items_num += each.quantity
            context = {'product': products, "total_items_num":total_items_num, 'identify_farmer': identify_farmer(request.user)}
            
            
        return render(request, 'pages/product.html', context)

    except:
        return HttpResponse('Sorry Page not found ')

@login_required(login_url="login_page")
def dashboard(request):
    # Fetch data for the overview page
    user = request.user
    if identify_farmer(user):
        framer = FramerUser.objects.get(Profile__user_m=user)
        products = Product.objects.filter(framer_user=framer)
        orders = Cart.objects.filter(product__framer_user=framer, status='purchased')
        revenue = sum(order.product.price * order.quantity for order in orders)

        checkout_orders_placed = CheckOutInfo.objects.filter(cart__product__framer_user=framer)
        pending_orders = checkout_orders_placed.filter(shippinginfo__recived_items=False)
        
        categories = Categories.objects.all()
        
        
        context = {
            'products': products,
            'checkout_orders_placed': checkout_orders_placed,
            'revenue': revenue,
            'pending_orders': pending_orders,
            'categories':categories,
            'farmer':framer
        }
        return render(request, 'pages/dashboard.html', context)
    return HttpResponse('Sorry Dashboard features is only for farmer at the movement')


@login_required(login_url="login_page")
def product_upload(request):
    user = request.user  
    if identify_farmer(user):
        if request.method == 'POST':
            name = request.POST['name']
            description = request.POST['description']
            category_id = request.POST['category']
            new_category = request.POST['new_category']
            price = request.POST['price']
            on_sale = 'on_sale' in request.POST
            images = request.FILES.getlist('images')


            category = None
            if new_category:
                category, created = Categories.objects.get_or_create(categories_name=new_category)
            elif category_id:
                category = Categories.objects.get(id=category_id)

            profile= Profile.objects.get(user_m=request.user)
            framer_user=FramerUser.objects.get(Profile=profile)
            product = Product.objects.create(
                categories=category,
                framer_user=framer_user,
                title=name,
                discription=description,
                price=price,
                on_sale=on_sale,
                )
            for image in images:
                ProductImages.objects.create(product=product, image=image, alt_text=name )

            return redirect('home')
        categories = Categories.objects.all()
        return render(request, 'pages/dashboard.html', {'categories': categories})
    return redirect('home')

@login_required(login_url="login_page")
def profile_change(request):
    if request.method == 'POST':
        profile_img= request.FILES.get('profile_img')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        bio = request.POST.get('bio')
        user = request.user
        user.first_name= first_name
        user.last_name= last_name
        user.save()

        framer = FramerUser.objects.get(Profile__user_m=user)
        framer.Bio = bio
        framer.ph_num= phone_number
        framer.profile_img= profile_img
        framer.save()

    return redirect(dashboard)


@login_required(login_url="login_page")
def cart(request):
    total_items_num = 0
    if request.user.is_authenticated:
        carts_info = Cart.objects.filter(user=request.user, status= 'cart')
        for each_cart in carts_info:
            total_items_num += each_cart.quantity
    each_total_price=[]
    total_price=0
    for each_cart in carts_info:
        each_total_price.append(each_cart.product.price * each_cart.quantity)
        total_price+=(each_cart.product.price * each_cart.quantity)

    
    context = {"total_items_num":total_items_num, 'carts_info':carts_info, 'each_total_price':each_total_price, 'total_price':total_price, 'identify_farmer': identify_farmer(request.user)}
    return render(request, 'pages/cart.html', context)

@login_required(login_url="login_page")
def add_cart(request,product_slug):
    product_instance= get_object_or_404(Product, slug = product_slug)
    cartsinfo, created= Cart.objects.get_or_create(user = request.user, product = product_instance)
    cartsinfo.quantity +=1

    cartsinfo.save()
    return redirect('home')

@login_required(login_url="login_page")
def rmv_cart(request,product_slug):
        product_instance= get_object_or_404(Product, slug = product_slug)
        cartsinfo, created= Cart.objects.get_or_create(user = request.user, product = product_instance)
        cartsinfo.delete()
        return redirect('cart')

@login_required(login_url="login_page")
def checkout(request):
    if request.method == 'POST':
        s_ph_num = request.POST.get('s_ph_num')
        s_email = request.POST.get('s_email')

        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        Order_Notes = request.POST.get('Order_Notes')

        payment_option = request.POST.get('payment_option')

        profile= Profile.objects.get(user_m=request.user)
        buyer_user=BuyerUser.objects.get(Profile=profile)



        checkoutinfo = CheckOutInfo.objects.create(
            user=buyer_user,
            s_ph_num=s_ph_num,
            s_email=s_email,
            address=address,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            Order_Notes=Order_Notes,
        )
        carts_info = Cart.objects.filter(user=request.user, status= 'cart')

        for each_cart in carts_info:
            checkoutinfo.cart.add(each_cart)
        for each_cart in carts_info:
            each_cart.status = 'purchased'
            each_cart.save()
        checkoutinfo.save()


        Shippinginfo = ShippingInfo.objects.create(
            checkout_info=checkoutinfo,
        )

        return redirect('/history/')


    total_items_num = 0
    if request.user.is_authenticated:
        carts_info = Cart.objects.filter(user=request.user)
        for each_cart in carts_info:
            total_items_num += each_cart.quantity
    each_total_price=[]
    total_price=0
    for each_cart in carts_info:
        each_total_price.append(each_cart.product.price * each_cart.quantity)
        total_price+=(each_cart.product.price * each_cart.quantity)
    
    context = {"total_items_num":total_items_num, 'carts_info':carts_info, 'each_total_price':each_total_price, 'total_price':total_price,'identify_farmer': identify_farmer(request.user)}

    return render(request, 'pages/checkout.html', context)


def history_view(request):
    profile= Profile.objects.get(user_m=request.user)
    buyer_user=BuyerUser.objects.get(Profile=profile)

    checkouts = CheckOutInfo.objects.filter(user=buyer_user)

    shipping_info = []
    for checkout in checkouts:
        shipping_info.extend(ShippingInfo.objects.filter(checkout_info=checkout))

    context = {
        'checkouts': checkouts,
        'shipping_info': shipping_info
    }
    return render(request, 'pages/history.html', context)