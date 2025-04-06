from django.contrib import admin
from .models import Comment, News

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','fname', 'lname', 'email', 'comment')
    

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id','head')
