from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True,blank=True,null=True)
    # slug = models.SlugField(unique=True)


    def __str__(self):
        return self.name


class Book(models.Model):
    title=models.CharField(max_length=256)
    description=models.TextField()
    image=models.ImageField(upload_to='books/')
    price=models.PositiveIntegerField()
    categories=models.ManyToManyField(Category, related_name="categories")
    borrower=models.ManyToManyField(User,blank=True)
    def __str__(self):
        return f"{self.title}"

class Review(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=False,null=False)
    body=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reviewed By {self.user.first_name} {self.user.last_name}"