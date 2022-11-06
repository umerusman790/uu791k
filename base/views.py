from cProfile import label
import re
from unicodedata import category
from django.shortcuts import render, redirect
from sklearn.preprocessing import label_binarize
from .models import Room, Topic, Message, User, Media
from .forms import RoomForm
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserForm, CustomUserCreationForm, MediaForm
from joblib import load

# Create your views here.

gpa_fields_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K','L', 'M', 'N', 'O']
category_fields_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K','L', 'M', 'N', 'O','P']
label_fields = {
    "A": 'Your Fsc/Ics marks percentage?',
    "B": 'Kindly choose your current semester.',
    "C": 'Please mention your NTS score?',
    "D": 'Please provide your current CGPA?',
    "E": 'Please select your father/guardian monthly Income from these options.',
    "F": 'Please select your monthly Income ?',
    "G": 'Are you satisfied with your program selection?',
    "H": 'What you did previously in intermediate?',
    "I": 'Your matric marks percentage?',
    "J": 'Do you feel any risk of failing to Graduate in your degree?',
    "K": 'Kindly tell us does your family supports you in education?',
    "L": 'Kindly select, how much time you spend on physical exercise e.g., gym, sports, running etc. ?',
    "M": 'Do you love to socialize with other?',
    "N": 'Do you have depression of study?',
    "O": 'How much you have interest in this domain?',
    "P": 'Do you love your subjects',
}

user_response_object = {
    "A": '',
    "B": {
        "1":'5 semsester',
        "2":'6 semsester',
        "3":'7 semsester',
        "4":'4 semsester',
        "6":'2 semsester',
        "7":'3 semsester', 
    },
    "C": '',
    "D": '',
    "E": {
        "6":'Father dont do any job',
        "17":'Less than 10k',
        "9":'Between 10k to 25k',
        "7":'Between 25k to 50k',
        "2":'Between 50k to 75k',
        "1":'Between 75k to 100k',
        "3":'Between 100k to 150k',
        "4":'Between 150k to 200k',
        "8" :'Between 200k to 250k',
        "5" :'Between 250k to 300k',
        "13":'Between 300k to 350k',
        "18":'Between 350k to 400k',
        "12":'Between 400k to 450k',
        "16":'Between 450k to 500k',
        "20":'Between 500k to 550k',
        "14":'Between 550k to 600k',
        "15":'Between 600k to 650k',
        "19":'Between 750k to 800k',
        "11":'Between 950k to 1M',
        "10":'More than 1M',
    },
    "F": {
        "6":'Between 50k to 75k',
        "9":'more than 1M',
        "7":'Between 75k to 100k',
        "2":'Dont do freelancing',
        "1":'Between 10k to 25k',
        "3":'Between 100k to 150k',
        "4":'Less than 10k',
        "8" :'Between 150k to 200k',
        "5" :'Between 25k to 50k',
        
    },
    "G":  {
       "1":'1',
       "2":'2',
       "3":'3',
       "4":'4',
       "5":'5',
        
    },
    "H":  {
        "6":'O level',
        "2":'FSC (pre engineering)',
        "1":'ICS (Physics)',
        "3":'ICS (Stats)',
        "4":'A level',
        "5" :'Fsc (pre medical)',
        
    },
    "I": '',
    "J": {
        "2":'Sometimes',
        "1":'Never',
        "3":'Rarely',
        "4":'Always',
        "5" :'Often',
        
    },
    "K": {
        "2":'Often',
        "1":'Always',
        "3":'Sometimes',
        "4":'Rarely',
        "5" :'Never',
        
    },
    "L": {
        "2":'Moderate',
        "1":'Less',
        "3":'Very less',
        "4":'None',
        "5" :'Extremely',
        
    },
    "M": {
        "2":'Often',
        "1":'Sometimes',
        "3":'Always',
        "4":'Rarely',
        "5" :'Never',
        
    },
    "N": {
        "2":'Always',
        "1":'Often',
        "3":'Rarely',
        "4":'Never',
        "5" :'Sometimes',
        
    },
    "O": {
         "1":'1',
       "2":'2',
       "3":'3',
       "4":'4',
       "5":'5',
    },
    "P": {
        "1":'1',
       "2":'2',
       "3":'3',
       "4":'4',
       "5":'5',
    },
}
good_responses = {
     "A": '83.21',
    "B": '1 Semester',
    "C": '80.96',
    "D": '3.26',
    "E": "Don't do freelancing",
    "F": 'Between 100k to 150k',
    "G": '5',
    "H": 'FSC (Pre-engineering)',
    "I": '88.64',
    "J": 'Never',
    "K": 'Always',
    "L": 'Moderate',
    "M": 'Sometimes',
    "N": 'Sometimes',
    "O": '5.0',
    "P": '3',
}
# //////// Login/////////

def Log_in(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
             messages.error(request, 'username or password is incorrect')
            
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'username or password is incorrect')

    context = { 'page': page} 
    return render(request, 'base/login_register_page.html', context)



# //////// Logout /////////

def Log_out(request):
    logout(request)
    return HttpResponseRedirect('/')



# //////// Register //////////

def register(request):

    if request.method == 'POST':
        print("checking")
        form = CustomUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit= False) 
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    form = CustomUserCreationForm()
    context = {'form': form }
    return render(request, 'base/login_register_page.html', context)


# //////// HOME /////////

def home(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.all()
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms':rooms, 'topics':topics, 'room_count':count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)

# //////// profile /////////

def profile(request, id):
    topics = Topic.objects.all()
    user = User.objects.get(id=id)
    rooms = user.rooms.all()
    room_messages = user.messages.all()
    context = {'user':user, 'room_messages':room_messages, 'rooms':rooms, 'topics':topics}
    return render(request, 'base/profile.html', context)




# //////// ROOM //////////////////////////////////

def room(request, id):
    room = Room.objects.get(id=id)
    room_messages = room.messages.all().order_by('-createdAt')
    participants = room.participants.all()
    print(participants)
    if request.method == 'POST':
        message = room.messages.create(
            user=request.user,
            room= room,
            body= request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', id=id)
    context = {'room':room, 'room_messages':room_messages, 'participants':participants}

    return render(request, 'base/room.html', context)




# //////// CREATE-----ROOM /////////
@login_required(login_url='home')
def create_room(request):
    topics = Topic.objects.all()
    form = RoomForm()
    print(form)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        print(topic_name)
        topic, created = Topic.objects.get_or_create(name=topic_name)
        print(created)
        Room.objects.create(
            name= request.POST.get('name'),
            topic = topic,
            description = request.POST.get('description'),
            host = request.user,

        )


        return HttpResponseRedirect('/')


    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)   

# //////// UPDATE-----ROOM /////////
@login_required(login_url='home')
def update_room(request, id):
    room = Room.objects.get(id=id)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        print(topic_name)
        topic, created = Topic.objects.get_or_create(name=topic_name)
        print(created)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return HttpResponseRedirect('/')

    context = {'room': room, 'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

# //////// DELETE-----ROOM /////////
@login_required(login_url='home')
def delete_room(request, id):
    room = Room.objects.get(id=id)
    if request.method == 'POST':
        room.delete()
        return HttpResponseRedirect('/')
    context = {'room': room, 'obj': room}
    return render(request, 'base/delete.html', context)






 # //////// DELETE-----MESSAGE /////////
@login_required(login_url='home')
def delete_msg(request, id):
    message = Message.objects.get(id=id)
    if request.method == 'POST':
        message.delete()
        return HttpResponseRedirect('/')
    context = {'message': message, 'obj':message}
    return render(request, 'base/delete.html', context)


# //////// DELETE-----MESSAGE /////////
@login_required(login_url='home')
def user_update(request):
    user = request.user

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES,instance=user)
        print(form)
        if form.is_valid(): 
            form.save()
            return redirect('profile', id=user.id)

    form  = UserForm(instance=user)

    return render(request, 'base/update-user.html', {'form': form})


# //////// UPLOAD-----FILE IN ROOM /////////

@login_required(login_url='home')
def upload_file(request, id):
    room = Room.objects.get(id=id)
    print(room)
    if request.method == 'POST':
        form  = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.user = request.user
            media.room  = room
            print(media)
            media.save()
            return redirect('room', id =id)
            


    else:
        form = MediaForm()
    
    context = {'form': form}
    return render(request, 'base/upload_file.html', context)


@login_required(login_url='home')
def room_files(request, id):
    files = Media.objects.filter(room__id=id)
    print(files)
    context = {'files': files}
    return render(request, 'base/all_files.html', context)


def predict_gpa(request):
    model = load('model1.sav')
    user_values = []
    gpa = None
    if request.method == 'POST':
        for name in gpa_fields_names:
            user_values.append(float(request.POST.get(name)))
        gpa = model.predict([user_values])

        return render(request, 'base/gpa_page.html', {'gpa': gpa[0]})

    context = {'gpa': gpa}
    return render(request, 'base/gpa_form.html', context)




model = load('svc_trained_model.pkl')
def predict_category(request):
    user_values = []
    category = None
    print(request.POST)
    if request.method == 'POST':
        for name in ['CP', 'RESTECG', 'CA', 'THAL']:
            user_values.append(int(request.POST.get(name)))

        print(user_values)
        category = model.predict([user_values])
        text = 'Yes' if category[0] == 1 else 'NO'
        context = {'category': text}

        return render(request, 'base/category_page.html', context)

    context = {} 
    return render(request, 'base/marks_form.html', context)

    # model = load('model2.sav')
    # user_values = []
    # user_response_label = []
    # category = None
    # if request.method == 'POST':
    #     for name in category_fields_names:
    #         user_values.append(float(request.POST.get(name)))
    #         user_response_label.append(request.POST.get(name) if user_response_object[name]=='' else user_response_object[name][request.POST.get(name)])

    #     print(user_values)
    #     category = model.predict([user_values])

    #     zipped = list(zip(label_fields.values(), good_responses.values(), user_response_label))
    #     print(zipped)
    #     context = {'category': category[0], 'zipped': zipped}

    #     return render(request, 'base/category_page.html', context)

    # context = {} 
    # return render(request, 'base/marks_form.html', context)
