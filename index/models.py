from django.db import models
import datetime

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    confirm_password = models.CharField(max_length=500, default='')
    

    def __str__(self):
        return self.first_name

    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False    

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False    




class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_product():
       return Category.objects.all()


class Product(models.Model):
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField()
    disc = models.CharField(max_length=200, null=True)
    images = models.ImageField(null=True, blank=True)
    


    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.images.url
        except:
            url = ''    
        return url    

    @staticmethod
    def get_all_product():
        return Product.objects.all()


    @staticmethod
    def get_all_product_by_id(category_id):
        if category_id:
            return Product.objects.filter(category__id=category_id)
        else:
            return Product.get_all_product()        



    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)        


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=500, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    