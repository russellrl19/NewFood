# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from photosleuth.models import User,
from django.contrib.auth import authenticate, login, logout
import re
from django.shortcuts import redirect
from django.conf import settings
from forms import UserForm
from django.core.mail import EmailMessage
import django_smtp_ssl
import os
import requests
import urllib

# Create your views here.

def index(request):
    # user must be logged in
    if not request.user.is_authenticated:
        if request.method == 'GET':
            subscribe = request.GET.get('subscribe')
        return render(request, "homepage_temp.html", {'base_url': settings.BASE_URL, 'subscribe': subscribe } )

    return render(request, "dashboard.html", {'base_url': settings.BASE_URL})

def login_page(request):
    if 'username' not in request.POST or 'password' not in request.POST:
        return render(request, "login.html")

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(settings.BASE_URL)
    else:
        return render(request, "login.html", {'base_url': settings.BASE_URL})

def register_page(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            userprofile = profile_form.save(commit=False)
            userprofile.user = user
            userprofile.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user) # log them in
            profile_form.save()

            # send registration email
            if user_form.cleaned_data.get('first_name'):
                body = "Dear " + user_form.cleaned_data.get('first_name') + ",\n\n"
            else:
                body = "Hello,\n\n"
            body += "You have successfully registered for the early beta of Civil War Photo Sleuth! \n\n Your username is:\n\n " + username + "\n\n and your password is:\n\n " + password + "\n\n To log in, visit www.civilwarphotosleuth.com and click the 'Log In' button on the top menu.\n\n Please feel free to reply to this message with any problems or questions. This is an early beta version of the software, so there will be a few glitches. We welcome both bug reports and feature requests.\n\n Thanks, and happy sleuthing!\n\n --Kurt Luther and the CWPS Team"
            email = EmailMessage(
                'Welcome to Civil War Photo Sleuth!',
                body,
                settings.EMAIL_HOST_USER,
                [user_form.cleaned_data.get('email')],
                #reply_to=['photosleuthmi+register@gmail.com']
            )
            #email.send()

            return redirect(settings.BASE_URL)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'base_url': settings.BASE_URL })


def logout_page(request):
    logout(request)
    return redirect(settings.BASE_URL)


def add_photo(request):
    # user must be logged in
    if not request.user.is_authenticated:
        return redirect(settings.BASE_URL)

    return render(request, "add_photo.html", { 'base_url': settings.BASE_URL })


def search_filters(request):
    # user must be logged in
    if not request.user.is_authenticated:
        return redirect(settings.BASE_URL)

    return render(request, "search_filters.html", { 'base_url': settings.BASE_URL })


def search_results(request):
    # user must be logged in
    if not request.user.is_authenticated:
        return redirect(settings.BASE_URL)

    face_id = request.GET.get('face_id')
    if face_id:
        face = Face.objects.get(pk=face_id)
        view = View.objects.get(pk=face.view_id)
        return render(request, "search_results.html",
                  { 'face_id': face_id, 'photo_id': view.photo_id, 'view_id': view.id, 'base_url': settings.BASE_URL})
    else:
        return render(request, "search_results_no_face.html",
                  { 'base_url': settings.BASE_URL})


def help(request):
    return render(request, "help.html")
