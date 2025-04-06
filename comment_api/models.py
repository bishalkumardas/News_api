from django.db import models

# Create your models here.

# Comment table 
class Comment(models.Model):
    
    # user see bad, good and db stores 1, 4
    EXPERIENCE_CHOICES = [
    (1, 'Bad'),
    (2, 'Average'),
    (3, 'Decent'),
    (4, 'Good'),
    (5, 'Excellent'),
    ]
    
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    exp= models.IntegerField(choices=EXPERIENCE_CHOICES, default=5)
    comment = models.TextField()
    
    def __str__(self):
        return self.fname
    
# news with sentiment table
class News(models.Model):
    
    SENTIMENT_CHOICES= [
        ('Positive','Positive'),
        ('Negative','Negative'),
        ('Neutral','Neutral'),
    ]
    
    date=models.DateField()
    head=models.CharField(max_length=100)
    sub_head=models.CharField(max_length=200)
    image_link=models.URLField()
    content=models.TextField()
    sentiment=models.CharField(max_length=8, choices=SENTIMENT_CHOICES, blank=True, null=True)
    
    def __str__(self):
        return self.head
