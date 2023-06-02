from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.

# rooms= [
#     {'id': 1, 'name': 'Full Stack Developer'},
#     {'id': 2, 'name': 'Backend Developer'},
#     {'id': 3, 'name': 'Frontend Developer'},
#     {'id': 4, 'name': 'Python/Django Development'},
#     {'id': 5, 'name': 'C++ Development'}    
# ]
def loginUser(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        try:
        
            user=request.get(User, username=username, password=password)
            # messages.error(request, 'User does not exit') 
        except:
            # messages.error(request, 'User does not exit')
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
            else:
                messages.error(request, 'Invalid username or password') 
    context={'page':page}
    return render(request,  'tunde/login_register.html', context)


@login_required(login_url='login')
def home(request):
   
    q= request.GET.get('q') if request.GET.get('q') else ''
    rooms=Room.objects.filter(Q(topic__name__icontains=q)|
                              Q(name__icontains=q)|
                              Q(description__icontains=q))
    topics=Topic.objects.all()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context={'rooms':rooms, 'topics':topics, 'room_messages':room_messages }
    return render(request, 'tunde/home.html', context)



def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form=UserCreationForm()
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
           
            return redirect('home')
        else:
            messages.error(request, 'An error occurred while creating a new user')
    context={'form': form}
    return render(request, 'tunde/login_register.html', context)

@login_required(login_url='login')
def room(request, pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all()
    participants=room.participants.all()
    if request.method == 'POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    # for i in rooms:
    #     if i['id']==int(pk):
    #         room=i
        
    context={'room':room, 'room_messages':room_messages, 'participants':participants }
    return render(request, 'tunde/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm(request.POST)
    if form.is_valid():
        room=form.save(commit=False)
        room.host=request.user
        room.save()
        return redirect('home')
    context={'form':form}
    return render(request, 'tunde/form_create.html', context)

@login_required(login_url='login')
def editRoom(request, pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You cant edit this message')
    form=RoomForm(instance=room)
    if request.method == 'POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form': form}
    return render(request, 'tunde/form_create.html', context)



@login_required(login_url='login')
def deleteRoom(request, pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You cant delete this message')
    if request.method=='POST':
        room=room.delete()
        return redirect('home')
    return render(request, 'tunde/delete_room.html', {'obj' : room})





@login_required(login_url='login')
def deleteMessage(request, pk):
    message=Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You cant delete this message')
    if request.method=='POST':
        message=message.delete()
        return redirect('home')
    return render(request, 'tunde/delete_room.html', {'obj' : message})




def userProfile(request, pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user': user, 'rooms': rooms, 'topics': topics, 'room_messages': room_messages}
    return render(request, 'tunde/profile.html', context)