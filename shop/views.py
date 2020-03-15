from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order,OrderUpdate,Bank
from math import ceil
import json
from shop.forms import UserForm, UserProfileInfoForm
from . import models
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from shop.paymentform import djangopay



def index(request):
    # products = Product.objects.all()


    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.description.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')
@login_required
def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        description = request.POST.get('description', '')
        contact = Contact(name=name, email=email, phone=phone, description= description)
        contact.save()
        thank = True
        return render(request, 'shop/contact.html', {'thank': thank})
    return render(request, 'shop/contact.html')
@login_required
def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status": "success", "updates": updates, "itemsJson": order[0].items_json},
                                          default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)


    return render(request, 'shop/productView.html', {'product':product[0]})

@login_required
def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        address = request.POST.get('address1', '')
        del_address = request.POST.get('del_address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json, name=name,  address=address,del_address=del_address,  city=city,
                       state=state, zip_code=zip_code,amount = amount,  phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id

        #djangopayform
        form = djangopay(request.POST)
        DOB = request.POST.get('dob')
        cardnumber = request.POST.get('cardnumber')
        gmail = request.POST.get('email')
        print(gmail)
        print(DOB)
        print(cardnumber)
        q = Bank.objects.get(email=gmail, birthdate=DOB, creditcardno=cardnumber)
        print(q)
        print(q.balance)
        print(amount)
        if (q):

            if q.balance >= int(amount):
                q.balance = int(q.balance) - int(amount)
                q.save()
                print(q.balance)
                return render(request, 'shop/success.html', {"price": amount})
            else:
                return render(request, 'shop/declined.html')

        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    else:
        form = djangopay()
    return render(request, 'shop/checkout.html',{'form':form})


def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            name = user_form.cleaned_data['firstname']
            subject = 'message from eshop'
            comment = 'Hi! I am a new user'
            message = '%s %s' % (comment, name)
            emailFrom = user_form.cleaned_data['email']
            emailTo = [settings.EMAIL_HOST_USER]
            send_mail(
                subject,
                message,
                emailFrom,
                emailTo,
                fail_silently=True,
            )

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'shop/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))

            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print('Someone tried to login and failed!')
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("invalid login details supplied!")
    else:
        return render(request, 'shop/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def success(request):
    return render(request,'shop/success.html')

def declined(request):
    return render(request,'shop/declined.html')

@login_required
def djangopayment(request):

    if request.method == "POST":
        form = djangopay(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            DOB = request.POST.get('DOB')
            cardnumber = request.POST.get('cardnumber')
            q = Bank.objects.filter(email = email, birthdate = DOB, creditcardno = cardnumber)
            if(q):
                
                if q.balance >=150 :
                    new = Bank.objects.filter(email=email, birthdate=DOB, creditcardno=cardnumber).update(balance = q.balance - 150)
                    new.save()
                    return render(request, 'shop/success.html', {"price":"150"})
                else:
                    message = "You dont have sufficient balance . Please recharge for the payment"
                    return render(request,'shop/declined.html',{"message":message})
    else:
        form = djangopay()
    return render(request,'shop/djangopay.html',{'form':form})



