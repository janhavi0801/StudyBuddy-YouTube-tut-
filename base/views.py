from multiprocessing import context
from unicodedata import name
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Roomy,Topic,Message
from .forms import RoomForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
# rooms=[
#     {'id':1,'name':'Lets learn python!'},
#     {'id':2,'name':'Janhavi ka server'},
#     {'id':3,'name':'god help me'}
# ]

def loginPage(request):

    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'Document Deleted, u no user.')

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect(home)
        else:
            messages.error(request,'Username or password does not exist')

    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error Occurred :(')

    context={'form':form}
    return render(request,'base/login_register.html',context)

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ''
    rm = Roomy.objects.filter(

        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        
        )

    topics=Topic.objects.all()
    room_count = rm.count()

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rm,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request, 'base/home.html',context)

def room(request,p):
    rm2 = Roomy.objects.get(id=p)
    msg=rm2.message_set.all().order_by('-created') #give us a set of messages that are related to this specific room
    participants = rm2.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=rm2,
            body=request.POST.get('body')
        )
        rm2.participants.add(request.user)
        return redirect('room',p=rm2.id)

    context = {'room':rm2,'room_messages':msg,'participants':participants}
    return render(request, 'base/room.html',context)

def userProfile(request,p):
    user = User.objects.get(id=p)
    rooms = user.roomy_set.all()
    room_messages = user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='login') #restrict non-users
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST)

        Roomy.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        return redirect('home')

    context = {'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login') 
def updateRoom(request,p):
    room = Roomy.objects.get(id=p)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save(
            
        )
        return redirect('home')

    context={'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def DelRoom(request,p):
    rom = Roomy.objects.get(id=p)

    if request.user != rom.host:
        return HttpResponse('You are not allowed!')

    if request.method == 'POST':
        rom.delete()
        return redirect('home')
    
    context={'obj':rom}
    return render(request,'base/delete.html',context)

@login_required(login_url='login')
def Delmsg(request,p):
    msg = Message.objects.get(id=p)

    if request.user != msg.user:
        return HttpResponse('You are not allowed!')

    if request.method == 'POST':
        msg.delete()
        return redirect('home')
    
    context={'obj':msg}
    return render(request,'base/delete.html',context)