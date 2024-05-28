from django.shortcuts import render,redirect, HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.




def home(request):
    products = Product.objects.all()

    context = {'product': products}
    return render(request, 'pages/index.html', context)


def product_view(request, slug):
    try: 
        products = Product.objects.get(slug=slug)
        context = {'product': products}

        return render(request, 'pages/product.html', context)

    except:
        return HttpResponse('Sorry Page not found ')


def login_page(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)
        if not user_obj.exists():
            messages.warning(request, "Email seems New to me, Plz First register.")
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.success(request, "Naughty !! Naughty !! Your account is not Verified till yet")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = authenticate(username = email, password= password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')
        

        messages.success(request, "Opps, hey you made some mistake. Try again")
        return HttpResponseRedirect(request.path_info)
    return redirect('/')



def register(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)
        if user_obj.exists():
            messages.warning(request, "Email is allready reigstered, check your mail box for more info.")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create(first_name= first_name, last_name= last_name, email = email, username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, "Success, Now lets see Weather you are real, Check your mail plz")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')