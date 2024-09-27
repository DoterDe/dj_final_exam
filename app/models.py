from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import migrations



class Post(models.Model):
    title = models.CharField(max_length=200)  
    content = models.TextField()               
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  

    def __str__(self):
        return self.title

    def get_like_count(self):
        return self.likes.count() 


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True) 
    
    class Meta:
        unique_together = ('user', 'post') 

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

class UserProfile1(User):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    avatar = models.ImageField(upload_to = 'photo' ,null = True, default = 'photo/sbcf-default-avatar.webp' )
    code = models.IntegerField(default=0, null=True)
    # cv = models.FileField(upload_to='cv/photos')
    # photo = models.ImageField(upload_to ='photo/photos' )
    # id_photo = models.ImageField(upload_to = 'id_photo/photos')
    def __str__(self) -> str:
        return f'{self.first_name}'

class UserProfile(User):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    avatar = models.ImageField(upload_to ='id_photo/photos' )

    # cv = models.FileField(upload_to='cv/photos')
    # photo = models.ImageField(upload_to ='photo/photos' )
    # id_photo = models.ImageField(upload_to = 'id_photo/photos')
    def __str__(self) -> str:
        return f'{self.first_name}'


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def str(self):
        return self.name
    

