from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.




class FramerInfo(models.Model):
    user_m = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to='profile_pic')
    ph_num = models.ImageField(null=True)
    def __str__(self):
        return self.user_m

class BuyersInfo(models.Model):
    user_m = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to='profile_pic')
    ph_num = models.ImageField(null=True)
    def __str__(self):
        return self.user_m

class Product(models.Model):
    title= models.CharField(max_length=100)
    price= models.FloatField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    discription = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product') 


