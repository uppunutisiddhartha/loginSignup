# models.py

from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import User


class Student(models.Model):
    firstname = models.CharField(max_length=25, null=False, blank=False)
    lastname = models.CharField(max_length=25, null=False, blank=False)
    mail = models.EmailField(null=False, blank=False)
    photo = models.ImageField(upload_to='uploads/students/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # Set when created
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('library', 'E.Library'),
        ('BTech', 'B.Tech'),
        ('MBA', 'MBA'),
        ('MCA', 'MCA'),
        ('Degree', 'Degree'),
    ]

    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to='uploads/books/covers/', blank=True, null=True)
    rating = models.IntegerField(default=0)
    pdf = models.FileField(upload_to='books/pdfs/', null=True, blank=True)
    
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="library", null=False, blank=False)
    selected_item = models.CharField(max_length=100, default="history", null=True, blank=True)
    
    # New Fields for Approval Workflow
    is_approved = models.BooleanField(default=False)
    approval_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title
    
    
    
    #cart
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='cart')
    is_paid=models.BooleanField(default=False)


class CartItems(models.Model):
    cart=models. ForeignKey(Cart,on_delete=models.CASCADE,related_name='CartItems')
    book=models.ForeignKey(Book,on_delete=models.SET_NULL,null=True,blank=True)   
    
    






















from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='notes')  # Made non-nullable
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'book'], name='unique_user_book_note')
        ]
        ordering = ['-updated_at']

    def __str__(self):
        return f"Note by {self.user.username} on {self.book.title}"
