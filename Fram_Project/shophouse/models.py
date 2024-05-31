from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid
from authenticate.models import *

class Categories(models.Model):
    slug = models.SlugField(unique=True, null=True, blank=True)
    categories_name=  models.CharField(max_length=100)
    discription = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.categories_name)
        super(Categories, self).save(*args, **kwargs)

    def __str__(self):
        return self.categories_name

class Product(models.Model):
    slug = models.SlugField(unique=True, null=True, blank=True)
    categories= models.ForeignKey(Categories, on_delete=models.CASCADE)
    framer_user= models.ForeignKey(FramerUser, on_delete=models.CASCADE)
    title= models.CharField(max_length=100)
    price= models.FloatField()
    discription = models.TextField()
    on_sale = models.BooleanField(default=False)
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    Rate= models.IntegerField(choices=RATING_CHOICES,  default=5)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product') 
    alt_text= models.CharField(max_length=100)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    STATUS_CHOICES = (
        ('cart', 'In Cart'),
        ('purchased', 'Purchased'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart Item: {self.product.title}"
    


class CheckOutInfo(models.Model):
    user = models.ForeignKey(BuyerUser, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart)

    s_ph_num = models.CharField(max_length=20)
    s_email = models.EmailField()

    Order_Notes=  models.CharField(max_length=350, null=True, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)



    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return str(f"Shipping Info for {self.s_email}")



class ShippingInfo(models.Model):
    checkout_info = models.OneToOneField(CheckOutInfo, on_delete=models.CASCADE)

    PAYMENT_OPTIONS = [('cash_payment', 'Cash Payment'),]
    payment_option = models.CharField(max_length=20, choices=PAYMENT_OPTIONS, default='cash_payment')

    shipping_number= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ordered_Date= models.DateField(auto_now_add=True)
    deliver_Date_on= models.DateField(null=True)
    recived_items= models.BooleanField(default=False)
    paid_money= models.BooleanField(default=False)

    def __str__(self):
        return f"Shipping Info for Order: {self.shipping_number}"

