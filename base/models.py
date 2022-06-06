from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Roomy(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True) #null field is allowed
    participants = models.ManyToManyField(User,related_name='participants',blank=True)
    updated = models.DateTimeField(auto_now=True) #takes a snapshot on everytime we save the room
    created = models.DateTimeField(auto_now_add=True) #takes snapshot when we first create the room

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Roomy,on_delete=models.CASCADE) #if a room gets deleted all the messages gets deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) #takes a snapshot on everytime we save/edit the post
    created = models.DateTimeField(auto_now_add=True) #takes snapshot when we first create the post

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.body[0:50] #display only 1st 50 characters of the msg in the preview
