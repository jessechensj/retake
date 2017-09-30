from django.shortcuts import render, HttpResponse, redirect
from django.contrib.sessions.models import Session
from models import User, Quote
from django.contrib import messages
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
  return render(request, 'index.html')


def login(request):
  if request.method == "POST":
    if re.match(EMAIL_REGEX, request.POST['email']) != None:
      user = User.objects.filter(email=request.POST['email'])
      if user:
        if user[0].password == request.POST["password"]:
          request.session['user_id'] = user[0].id
          return redirect('/success')
        else:
          messages.error(request, "Invalid E-mail or Password")
          return redirect('/')
      else:
        messages.error(request, "Invalid E-mail or Password")
        return redirect('/')
    else:
      messages.error(request, "Invalid E-mail or Password")
      return redirect('/')
  return redirect('/')


def register(request):
  if request.method == "POST":
    if len(User.objects.validation(request.POST)) > 0:
      messages.error(request, User.objects.validation(request.POST))
      return redirect('/')
    else:
      User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=request.POST['password'], dob=request.POST['dob'])
      messages.error(request, "successfully registered")
      request.session['user_id'] = User.objects.last().id
      return redirect('/success')
  return redirect('/')


def success(request):
  messages.error(request, User.objects.get(id=request.session['user_id']).name + " logged in!")
  return redirect('/quotes')


def logout(request):
  request.session.flush()
  messages.error(request, "logged out!")
  return redirect('/')


def quotes(request):
  request.session['name'] = User.objects.get(id=request.session['user_id']).name
  quotes = {
    'quotes':Quote.objects.all(),
    'favorites':Quote.objects.filter(favoritedby=request.session['user_id'])
  }
  return render(request, 'quotes.html', quotes)

def add(request):
  print Quote.objects.validation(request.POST)
  if len(Quote.objects.validation(request.POST)) > 0:
    messages.error(request, Quote.objects.validation(request.POST))
    return redirect('/quotes') 
  user = User.objects.get(id=request.session['user_id'])
  Quote.objects.create(message=request.POST['message'], quotedby=request.POST['quotedby'], user=user)
  return redirect('/quotes')

def add_favorite(request, id):
  quote = Quote.objects.get(id=id)
  quote.save()
  quote.favoritedby.add(User.objects.get(id=request.session['user_id']))
  return redirect('/quotes')

def remove_favorite(request, id):
  quote = Quote.objects.get(id=id)
  user = User.objects.get(id=request.session['user_id'])
  quote.favoritedby.remove(user)
  return redirect('/quotes')

def user(request, id):
  user = {
    'username':User.objects.get(id=id).name,
    'count':Quote.objects.filter(user=id).count(),
    'quotes':Quote.objects.filter(user=id)
  }
  return render(request, 'user.html', user)
