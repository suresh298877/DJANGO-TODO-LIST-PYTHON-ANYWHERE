from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, JsonResponse
from . import serializers
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .forms import *

from django.core.mail import send_mail
from . import forms
from . import models

# Create your views here.


def landing_view(request):
    users = User.objects.all()
    return render(request, 'landingpage.html', {'users': users, 'images': profile.objects.all()})


@login_required(login_url="login")
def home_view(request):
    todos = None
    form = forms.TodoForm()
    if request.user.is_authenticated:
        todos = models.TODO.objects.filter(
            user=request.user).order_by('priority')

    return render(request, 'home.html', {'form': form, 'todos': todos})


def login_view(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login', {'form': form})


def signup_view(request):
    if request.method == 'GET':
        form = CustomUserCreationForm(None)
        return render(request, 'signup.html', {'form': form})
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database
            post = form.save(commit=False)

            post.save()
            try:
                subject = 'TODO LIST WEB APP'

                user_id = User.objects.get(
                    username=form.cleaned_data['username']).id
                message = f'Hi {form.cleaned_data["username"]}, thank you for registering in Todo Web Application.Please click here to verify your Account https://suresh298877.pythonanywhere.com/app/gverify/{user_id}'
                email_from = 'suresh.p19212033cvv@gmail.com'
                recipient_list = [form.cleaned_data['email'], ]
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse('Failed to send mail verification link.contact administrator suresh.p19212033cvv@gmail.com')
            return HttpResponse("<h1>We have sent an email verification link to your gmail.Please verify the link</h1>")
        else:
            return render(request, 'signup.html', {'form': form})


def gverify_view(request, user_id):
    uo = User.objects.get(id=user_id)
    if request.method == 'GET':
        img_form = UserImageForm()
        return render(request, 'profilepic.html', {'img_form': img_form, 'user_id': user_id})
    elif request.method == 'POST':
        try:
            img_form = UserImageForm(request.POST, request.FILES)
            if img_form.is_valid():
                f = img_form.save()
                f.user = uo
                f.save()
            uo.is_active = True
            uo.save()
            return HttpResponse('<h1>Your account has been verified.please login in the home page</h1>')
        except Exception as e:
            return HttpResponse('<h1>Failed to verify your account.Please contact to `suresh.p19212033cvvv@gmail.com`</h1>')


def logout_view(request):
    logout(request)
    return redirect('home')


def add_todo_view(request):
    form = forms.TodoForm(request.POST)
    todo = form.save(commit=False)
    todo.user = request.user
    todo.save()
    return redirect('home')


def delete_todo_view(request, id):
    todo = TODO.objects.get(id=id).delete()
    return redirect('home')


def change_todo_status(request, id, status):
    todo = TODO.objects.get(pk=id)
    todo.status = status
    todo.save()
    return redirect('home')


# DJANGO REST FRAMEWORK


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
@csrf_exempt
def todo_get_post(request):
    if request.method == 'GET':
        todos = models.TODO.objects.filter(
            user=request.user).order_by('priority')
        serializer = serializers.TodoSerializer(todos, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        data = request.data
        data['user'] = request.user
        print(data)

        serializer = serializers.TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            # s=serializer.save(commit=False)
            # s.user=request.user
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@csrf_exempt
def todo_delete(request, id):
    obj = models.TODO.objects.get(id=id).delete()
    return Response({'msg': 'deleted'})
