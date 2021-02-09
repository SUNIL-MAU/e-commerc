from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from django.views import View
from .middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator
import razorpay

# Create your views here.
class home(View):

    def post(self, request):
        # print(request.POST.get('product'))
        product = request.POST.get('product')
        print(product)
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1                  
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1    
            
        else:
            cart = {}    
            cart[product] = 1
        request.session['cart'] = cart
        print(cart)    
        return redirect('home')
        

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        Products = None
        categorys = Category.get_all_product()
        catogeryID = request.GET.get('catogery')
        if catogeryID:
            Products = Product.get_all_product_by_id(catogeryID)
        else:
            Products = Product.get_all_product() 

        user_name = request.session.get('firstname')

        context= {'Products':Products,'categorys':categorys,'user_name':user_name}
        return render(request ,'index/index.html', context)






def registerUser(request):
    postdata = request.POST
    # print(postdata)
    first_name = postdata.get('firstname')
    last_name = postdata.get('lastname')
    email = postdata.get('email')
    phone = postdata.get('phone')
    password = postdata.get('password')
    password2 = postdata.get('password2')
    con_pass = make_password(password2)
    print(password2, type(password2))
    print(password, type(password))
    
     # print(firstname, lastname, email, phone, password)
    value = {'first_name':first_name, 'last_name':last_name, 'email':email, 'phone':phone}
    
    customer = Customer(first_name=first_name, last_name=last_name, email=email, phone=phone, password=password, confirm_password=password2 )
    # print(customer.last_name)
        
    error_message = validateCustomer(customer)
    if not error_message:
        customer.password = make_password(customer.password)
        customer.confirm_password = make_password(customer.confirm_password)
        customer.save()
        return redirect('home')
    data = {'error': error_message, 'values':value}    
    return render(request, 'index/signup.html', data)


def validateCustomer(customer):
    error_message = {}
    if not customer.first_name:
        error_message = 'First Name Required !!'            
    elif len(customer.first_name)<3:
        error_message = 'First name must be greater than 3 word!!'
    elif not customer.last_name:
        error_message = 'Last Name Required!!'    
    elif len(customer.last_name)<3:
        error_message= 'Last name must be greater than 3 word!!'
    elif not customer.phone:
        error_message = 'Phone Number Requires'        
    elif len(customer.phone)<10:
        error_message = 'Phone Number must be 10 digit!!'
    elif len(customer.password)<5:
        error_message = 'Input valid password!!'
    elif customer.password != customer.confirm_password:
        error_message = 'Password doesn\'t match'             
    elif len(customer.email)<3:
        error_message = 'Input valid mail !!'
    elif customer.isExists():

        error_message = 'Email Address Already Registered!!'
         
    return error_message        

def signup(request):
    # print(request)
    if request.method =='GET':
        return render(request, 'index/signup.html', )
    else:
        return registerUser(request)

 
#  ----- For user login -----       
class login(View):
    
    def get(self, request):
        
        return render(request, 'index/login.html')

    def post(self, request):
        # print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        error_message = {}
        # if not email:
        #     print('email nhi h')
        #     error_message = 'Please input email!!'
        
        # elif not password:
        #     error_message = 'please input password!!'    
        # print(email, password)
        customer = Customer.get_customer_by_email(email)
        
      
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['email'] = customer.email
                request.session['firstname'] = customer.first_name
                return redirect('home')
            else:
                error_message = 'Email or Password invalid!!' 
        else:
            error_message = 'Email or Password invalid!!'
          
        return render(request, 'index/login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')
    
        
class cart(View):
    @method_decorator(auth_middleware)
    def get(self, request):
        # print(list(request.session.get('cart').keys()))
        ids = list(request.session.get('cart').keys())
        # print(ids)
        products = Product.get_products_by_id(ids)
        # print(pro)
        return render(request, 'index/cart.html', {'products':products})


    
class CheckOut(View):
    @method_decorator(auth_middleware)
    def post(self, request):
        
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cus = Customer.objects.get(id=customer)
        
        cart = request.session.get('cart')
        products = Product.objects.filter(id__in=list(cart))

        
        
        for product in products:
            
            # print(product)
            order = Order(product=product,customer=Customer(id=customer),quantity=cart.get(str(product.id)), price=product.price,address=address,phone=phone)
            
            order.save()
        request.session['cart'] = {}            
        return redirect('order')


class OrderView(View):
    @method_decorator(auth_middleware)
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.objects.filter(customer=customer)
        
        c = Order.objects.all().values_list()
        
        total = []
        for i in range(0,len(c)):
            p = c[i][3]*c[i][4]
            total.append(p)
        totol_price = sum(total)  

        return render(request, 'index/order.html',{'orders':orders,'count':c.count(), 'total_price':totol_price})

    def post(self, request):
        key_id = 'rzp_test_RFRahJ9fHePOkp'
        key_secret = 'PRY5Km7Zn9eM4qZzAi7khOQI'
        totalamount = request.POST.get('totalPrice')
        print(totalamount)
        client = razorpay.Client(auth=(key_id, key_secret))
        data = {
                "amount": int(totalamount)*100,
                "currency":"INR",
                "receipt": "receipt id of order",
                "notes": {
                "email":"sunilmaurya71297@gmail.com",
                "name":"anuj MAURYA",
                "Purchese_for":"shoot shalwar"
            } 
        } 
        order = client.order.create(data=data) 

        orderdata = {}
        for key, value in order.items():
            orderdata[key]= value
        order_id = orderdata['id']    
        customer = request.session.get('customer')
        orders = Order.objects.filter(customer=customer)
        
        c = Order.objects.all().values_list()
        
        total = []
        for i in range(0,len(c)):
            p = c[i][3]*c[i][4]
            total.append(p)
        totol_price = sum(total)  

        return render(request, 'index/order.html',{'orders':orders,'count':c.count(), 'total_price':totol_price,'order_id':order_id})
    

def Search(request):
    query = request.POST.get('search')
    product = Product.objects.filter(name__icontains=query)      
    
    return render(request, 'index/search.html',{'Products':product})


def Product_disc(request, id):
    if request.method=='GET':
        product = Product.objects.get(pk=id)
        context = {'Products':product}
    else:
        return HttpResponse('post')    
    return render(request, 'index/prod_disc.html', context)



   
