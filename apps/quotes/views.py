from __future__ import unicode_literals
from . models import *
from django.shortcuts import render, redirect #HttpResponse
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'quotes/index.html')

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/success')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully logged in!")
    return redirect('/success')

def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'quotes/success.html', context)

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')

def add(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/{{user_id}}')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'quotes/add.html', context)