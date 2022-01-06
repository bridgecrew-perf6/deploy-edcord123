from django.db import models
from django.db.models import Q
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room, Topic
from .form import RoomForm

# Create your views here.

# rooms=[
#     {'id':1, 'name':'Lets learn python'},
#     {'id':2, 'name':'Lets play a game'},
#     {'id':3, 'name':'Lets learn frontend'},
# ]
def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        
        )
    room_count=rooms.count()
    topics=Topic.objects.all()
    context={'rooms':rooms,'topics':topics,'room':room_count}
    return render(request,'base/home.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    context={'room':room}
    
    return render(request,'base/room.html',context)

def CreateRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)

def UpdateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)

def DeleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    context={'obj':room}
    return render(request,'base/delete.html',context)