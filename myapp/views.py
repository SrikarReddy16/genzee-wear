from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.utils.timezone import now
from .models import offer , arrivals , StoreItem , Cart
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password2 == password:
            if User.objects.filter(email=email).exists():
                messages.info(request,'E-mail is already in use')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username is already in use')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'Password is not same')
            return redirect('register')
    else:        
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    else:    
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def home(request):
    offerobj = offer.objects.filter(isactive=True,startdate__lte=now(),enddate__gte=now())
    arrival = arrivals.objects.all()
    return render(request,'home.html',{'offer':offerobj , 'arrivals':arrival})


def store(request):
    items = StoreItem.objects.all()

    search_res = request.GET.get('search','')
    if search_res:
        items = items.filter(Q(name__icontains=search_res) | Q(description__icontains=search_res))

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        items = items.filter(price__gte = min_price)
    
    if max_price:
        items = items.filter(price__lte = max_price)
    
    gender = request.GET.get('gender')
    if gender:
        items = items.filter(gender=gender)

    
    return render(request,'store.html',{'materials':items})


def add_to_cart(request, item_id):
    product = get_object_or_404(StoreItem, id=item_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1  
        cart_item.save()

    return redirect('cart')

def cart(request):

    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request,'cart.html',{'cart_items':cart_items,'total_price':total_price})

def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart')