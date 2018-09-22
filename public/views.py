# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from photosleuth.models import HDS_Data, Person, Military, Photo, View, Face_Person, User, Face, Temp_Face_CWID, Annotation, Profile
from django.contrib.auth import authenticate, login, logout
import re
from django.shortcuts import redirect
from django.conf import settings
from forms import UserForm
from forms import UserProfileForm
from forms import UpdateUserProfileForm
from forms import NewProfileUserForm
from forms import myProfileUserForm
from forms import NewProfileForm
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

def my_profile(request):
    # user must be logged in
    if not request.user.is_authenticated:
        return redirect(settings.BASE_URL)

    if request.method == 'POST':
        user_form = myProfileUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            userprofile = profile_form.save(commit=False)
            userprofile.user = user
            userprofile.save()
            profile_form.save()
    else:
        user_form = myProfileUserForm()
        profile_form = NewProfileForm()
    return render(request, 'my_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'base_url': settings.BASE_URL })

def public_profile(request, username):
    # user must be logged in
    if not request.user.is_authenticated:
        return redirect(settings.BASE_URL)

    profile_username = User.objects.get(username=username).username
    id = User.objects.get(username=username).id
    first_name = User.objects.get(username=username).first_name
    last_name = User.objects.get(username=username).last_name
    email = User.objects.get(username=username).email
    user_id = Profile.objects.get(user_id=id).user_id
    bio = Profile.objects.get(user_id=id).bio
    interests = Profile.objects.get(user_id=id).interests

    return render(request, 'public_profile.html', {'profile_username': profile_username, 'id': id, 'first_name': first_name, 'last_name': last_name, 'email': email, 'user_id': user_id, 'bio': bio, 'interests': interests, 'base_url': settings.BASE_URL })

def logout_page(request):
    logout(request)
    return redirect(settings.BASE_URL)


def add_photo(request):
    # user must be logged in
    if not request.user.is_authenticated:
        return redirect(settings.BASE_URL)

    return render(request, "add_photo.html", { 'base_url': settings.BASE_URL })

def add_identity(request):
    if not request.user.is_authenticated:
        return redirect(settings.BASE_URL + '/login')
    if request.method == 'POST':
        # submission page

        # get POST vars
        fname = request.POST.get('First Name')
        mname = request.POST.get('Middle Name')
        lname = request.POST.get('Last Name')
        gender = request.POST.get('Gender')
        race = request.POST.get('Race')
        birthYear = request.POST.get('Birth Year')
        personSource = request.POST.get('Person Source')

        side = request.POST.getlist('Side')
        unitNumber = request.POST.getlist('Unit Number')
        unitName = request.POST.getlist('Unit Name')
        branch = request.POST.getlist('Branch')
        company = request.POST.getlist('Company')
        rankIn = request.POST.getlist('Rank In')
        rankOut = request.POST.getlist('Rank Out')
        #militarySource = request.POST.getlist('Military Source')

        counter = request.POST.getlist('counter')
        face_id = request.POST.get('face_id')

        # first, create the Person
        person = Person()
        person.creator = request.user

        person.first_name = fname
        person.middle_name = mname
        person.last_name = lname

        person.gender = gender
        person.race = race
        if birthYear:
            person.birth_year = birthYear
        person.source = personSource

        person.save()
        #print "person saved "

        # now create Military items for this person
        for i in range(len(counter)):
            m = Military()
            m.person = person
            m.creator = request.user

            m.side = side[i]
            if unitNumber[i]:
                m.unit_number = unitNumber[i]
            m.unit_name = unitName[i]
            m.branch = branch[i]
            m.company = company[i]
            m.rank = rankIn[i]
            #m.source = militarySource[i]
            m.save()
            #print "military saved "

            # if rank out provided (and different), duplicate it and save second rank
            if rankOut[i] and (rankOut[i] != rankIn[i]):
                m.pk = None
                m.rank = rankOut[i]
                m.save()
                #print "military 2 saved "

        # finally, if a Face was provided, attach to this person
        if face_id:
            fp = Face_Person()
            fp.creator = request.user
            fp.face = Face.objects.get(pk=face_id)
            fp.person = person
            fp.save()
            #print "face_person saved "
            photo_id = View.objects.get(pk=fp.face.view_id).photo_id
            #print "done - redirect to photo page"
            return redirect(settings.BASE_URL + 'photos/view/' + str(photo_id))
        else:
            # eventually point someone to the Person page, once such a thing exists
            #print "done - redirect to home page"
            return redirect(settings.BASE_URL)

    else:
        face_id = request.GET.get('face_id')
        if face_id:
            api_endpoint = settings.BASE_URL + 'api/v1/faces/' + face_id
            params = { 'api_key': 123456 }
            response = requests.get(api_endpoint, params)
            json_response = response.json()
            if json_response['success'] == 'success':
                photo_id = json_response['photo_id']
                face_thumb_src = json_response['face_thumb']['src'][0]

            api_endpoint = settings.BASE_URL + 'api/v1/photos/' + str(photo_id)
            response = requests.get(api_endpoint, params)
            json_response = response.json()
            if json_response['success'] == 'success':
                front_img_src = json_response['views'][0]['img_url'][0]
                back_img_src = None
                if len(json_response['views']) > 1:
                    back_img_src = json_response['views'][1]['img_url'][0]

            #face = Face.objects.get(pk=face_id)
            #view = View.objects.get(pk=face.view_id)
            return render(request, "add_identity.html", {
                    'base_url': settings.BASE_URL,
                    'face_id': face_id,
                    'photo_id': photo_id,
                    'front_img_src': front_img_src,
                    'back_img_src': back_img_src,
                    'thumb_src': face_thumb_src
                })
        else:
            return render(request, "add_identity.html", {'base_url': settings.BASE_URL})

def view_photo(request, photo_id):
    # user must be logged in
    if not request.user.is_authenticated:
        return redirect(settings.BASE_URL)

    photo = Photo.objects.get(pk=photo_id)
    views = View.objects.filter(photo__id=photo_id)
    faces = Face.objects.filter(view__photo__id=photo_id)
    people = Person.objects.filter(face_person__face__view__photo_id=photo_id)
    fps = Face_Person.objects.filter(face__view__photo_id=photo_id)
    annotations = Annotation.objects.filter(photo_id=photo_id, face_id=None)


    return render(request, "view_photo.html", {'photo': photo, 'views': views, 'faces': faces, 'people': people, 'fps': fps, 'annotations': annotations, 'base_url': settings.BASE_URL })

def tag_photo(request, photo_id):
    # user must be logged in
    if not request.user.is_authenticated:
        return redirect(settings.BASE_URL)

    photo = Photo.objects.get(pk=photo_id)
    views = View.objects.filter(photo_id=photo.id)
    view_type = request.GET.get('view')
    remaining = request.GET.get('remaining', 0)

    # view = views[0]
    return render(request, "tag_photo.html", { 'photo': photo, 'view_type': view_type, 'remaining': remaining, 'base_url': settings.BASE_URL })

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
