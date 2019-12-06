from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

from django.core import serializers

from . import forms
from myapp.forms import AgencyForm

from . import models


# For Testing
class Card:
  def __init__(self, name, url, picUrl, address, phone):
    self.name = name
    self.url = url
    self.picUrl = picUrl
    self.address = address
    self.phone = phone

newCard = [
    Card("Red Cross", "https://www.redcross.org", "media/redCross.jpg", "2125 East Onstott Road Yuba City, CA 95991","(530) 673-1460"),
    Card("Neighborhood Church of Chico", "http://www.ncchico.org/", "media/NC.jpg", "2801 Notre Dame Boulevard Chico, CA 95928", "(530) 343-6006"),
    Card("Northern Valley Catholic Social Service", "https://www.redcross.org", "media/NVCSS.png", "2400 Washington Ave Redding, CA 96001-2832", "(530) 345-1600")
  ]
# End testing block 



# Helper funstions
def checkAuth(request):

  if(request.user.is_authenticated):
      return True
  else:
      return False


# Create your views here.
def home(request):
  title = "Home "
  articles = models.News_Articles.objects.all()[:3]

  context = {
    "title": title,
    "cards": newCard,
    "articles": articles,
    "range": range(0, 5),
    "is_user": checkAuth(request),
  }

  return render(request, 'main/index.html', context=context)


def agencies(request):
  title = "Agencies "

  context = {
    "title": title,
    "cards": newCard,
    "ranger": range(0, 3),
    "is_user": checkAuth(request),
  }

  return render(request, 'main/agencies.html', context=context)




def trending(request):
  title = "Trending News "

  context = {
    "title": title,
    "articles": newArticle,
    "ranger": range(0, 5),
    "is_user": checkAuth(request),
  }

  return render(request, 'main/trending.html', context=context)




def about(request):
  title = "About Us "

  context = {
    "title": title,
    "is_user": checkAuth(request),
  }

  return render(request, 'main/about.html', context = context)




def signIn(request):
  title = "Sign In "

  context = {
    "title": title,
    "is_user": checkAuth(request),
  }

  return render(request, "main/signIn.html", context = context)




def postSignIn(request):
  signedIn = True
  title = "Welcome "
  is_user = request.POST.get('is_user')
  passw = request.POST.get("pass")

  user = authenticate(request, is_user=is_user, password=passw)

  if user is None:
    title = "Invalid "
    message = "invalid credentials"
    signedIn = False

    context = {
      "title": title,
      "msg": message,
      "is_user": checkAuth(request),
    }

    return render(request, "main/signIn.html", context = context)

  context = {
    "title": title,
    "e": is_user,
    "signedIn": signedIn,
    "is_user": checkAuth(request),
  }

  #get.session['uid']=str(session_id)
  return HttpResponseRedirect("main/index.html")




def logout_view(request):

  logout(request)
  return HttpResponseRedirect("/login/")




def signUp(request):
  title = "registration"

  if request.method == "POST":

    form_instance = forms.RegistrationForm(request.POST)
    if form_instance.is_valid():

      form_instance.save()
      return HttpResponseRedirect("/postSignIn/")
  else:

    form_instance = forms.RegistrationForm()

  context = {
    "form":form_instance,
    "title": title,
    "is_user": checkAuth(request),
  }

  return render(request, "registration/signUp.html", context = context)




def postsignup(request):
  title = "Welcome "
  name = request.POST.get('name')
  email = request.POST.get('email')
  passw = request.POST.get('pass')

  context = {
    "title": title,
    "e": email,
    "is_user": checkAuth(request),
  }

  return render(request, "main/welcome.html", context = context)




def agencySignUp(request):
  signedIn = True
  is_user = request.POST.get('is_user')
  passw = request.POST.get("pass")

  user = authenticate(request, is_user=is_user, password=passw)

  if request.method == "POST":
    form_instance = forms.AgencyForm(request.POST)
    if form_instance.is_valid():
      Agencies = form_instance.save(commit=False)
      Agencies.user = request.user
      Agencies.save()
      return HttpResponseRedirect("/")

  else:
    form_instance = forms.AgencyForm()

  context = {
    "form" : form_instance,
    "e": is_user,
    "signedIn": signedIn,
    "is_user": checkAuth(request),
  }
  return render(request, 'main/agencySignUp.html', context=context)




def profile(request):
   title = "Profile"
   context = {
     "title": title,
     "is_user": checkAuth(request),
     "user": request.user,
     #Subject to have more things - Calvin
   }

   return render(request, 'main/profile.html', context=context)
