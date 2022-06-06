from django.contrib import admin

# Register your models here.
from .models import Roomy, Topic, Message
admin.site.register(Roomy)
admin.site.register(Topic)
admin.site.register(Message)