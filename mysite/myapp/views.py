from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.db.models import Q
from cities_light.models import Country, City
import re, string
import geoip2.database
import geopy.distance
from geopy.geocoders import Nominatim
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
from sklearn.metrics import r2_score
from sklearn import svm
import seaborn as sns
from imblearn.over_sampling import SMOTE

from django.core import serializers

from . import forms
from myapp.forms import AgencyForm, ProfileForm, HideCompletedRequestsForm, AddVolunteerRequestForm
from myapp.models import Profile, Cause, News_Articles, Agencies, Request_Fulfilled, Request_In_Progress, Volunteering, Social_Media_Post, Agency_Social_Media_Post
from . import models


import json



# Helper functions
def checkAuth(request):
    if(request.user.is_authenticated):
        return True
    else:
        return False


# Create your views here.
def home(request):
    # df = pd.DataFrame(list(Request_In_Progress.objects.all().values()))
    # filt = Request_In_Progress.objects.all().values_list('cause_id', flat=True)
    # df2 = pd.DataFrame(list(Cause.objects.all().filter(id__in = filt)))


    #cs = Cause.objects.all().filter(id__in=filt)

    #cause = models.Cause.objects.all().filter(id__in=cause)
    #.values_list('')

    #print(cause.type_of_cause)
    #cause = list(cause.cause_id.type_of_cause)
    #df2 = pd.DataFrame(list(cause))
    # print("df first: ")
    # print(df)
    # print(df2)
    #
    # X = df[['type_of_cause']]
    # y = df[['cause_id']]
    # #
    # # sns.countplot(x='item',data=X)
    # # plt.title('Items Requested')
    # # plt.show()
    # #
    # # X = A.loc[:,A.columns != 'cause_id']
    # # y = A.loc[:,A.columns == 'cause_id']
    # X.item = le.fit_transform(X.item)
    # print(X.item)
    #
    # from imblearn.over_sampling import SMOTE
    #
    # # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    # #
    # # smt = SMOTE(random_state=0)
    # # data_X,data_y=smt.fit_sample(X_train, y_train)
    #
    # # sns.countplot(x='cause_id',data=data_y)
    # # plt.title("Cause ID's")
    # # plt.show()
    # #
    #
    #
    #
    #
    #
    # X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3, random_state=0)
    # #
    # # # Fit or Train the Model
    # lr_model = LogisticRegression()
    # lr_model.fit(X_train,y_train)
    #
    # score = lr_model.score(X_train,y_train)
    # print(f"Accuracy with train data : {score:0.2f}")
    #
    # # Evaluate Model using test data
    # y_pred =lr_model.predict(X_test)
    #
    # # Find out accuracy with test data
    # r2score = r2_score(y_test,y_pred)
    # print(f"Accuracy with test data :  {r2score:0.2f}")
    #
    # # Pickle model
    # pd.to_pickle(lr_model,'lr_model.pickle')



    title = "Home "
    articles = models.News_Articles.objects.all().order_by('-picture')
    articles = articles[:4]
    Agenciess = models.Agencies.objects.all()[:6]
    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    #
    # if x_forwarded_for:
    #     ip = x_forwarded_for.split(',')[0]
    # else:
    #     ip = request.META.get('REMOTE_ADDR')
    # #try:
    #
    # reader = geoip2.database.Reader('../GeoLite2-City_20201013/GeoLite2-City.mmdb')
    # ip = '24.94.15.83'
    # response = reader.city(ip)
    #
    # # print(response.country.iso_code)
    # # print(response.country.name)
    # # print(response.country.names['zh-CN'])
    # # print(response.subdivisions.most_specific.name)
    # # print(response.subdivisions.most_specific.iso_code)
    # # print(response.city.name)
    # # print(response.postal.code)
    # # print(response.location.latitude)
    # # print(response.location.longitude)
    # location1 = (response.location.latitude, response.location.longitude)
    #
    # geolocator = Nominatim(user_agent="my_user_agent")
    # loc = geolocator.geocode("Cleveland, OH", exactly_one=False)[0]
    #
    # location2 = (loc.latitude, loc.longitude)
    #
    # print(City.objects.filter(latitude=46.97537))
    #
    # distance = geopy.distance.distance(location1, location2).miles
    # print(distance)
    # reader.close()
    # except:
    #     pass

    context = {
        "user" : request.user,
        "title": title,
        "articles": articles,
        "agencies": Agenciess,
        "ranger": range(0, 5),
        "is_user": checkAuth(request),
    }
    return render(request, 'main/index.html', context=context)




def agencies(request):
    # # Unpickle model
    # model = pd.read_pickle('lr_model.pickle')
    #
    # # Take input from user
    # gre = int(input("Enter Item    : "))
    # tof = int(input("Enter Amount Total  : "))
    #
    # # Predict chances
    # result = model.predict([[gre,tof,cgpa]])  # input must be 2D array
    # print(f"Chances are : {result[0] * 100:.2f}%")

    title = "Agencies "
    Agenciess = models.Agencies.objects.all()
    agency_cities = Agencies.objects.values_list('city', flat=True)
    cities = City.objects.all().filter(id__in = agency_cities)

    if request.method == 'POST':

        city_id = request.POST['city_id']
        if city_id is not "":
            selected_item = get_object_or_404(City, pk=request.POST.get('city_id'))
            Agenciess = Agencies.objects.filter(city=selected_item)

    context = {
        "title": title,
        "cities": cities,
        "agencies": Agenciess,
        "ranger": range(0, 3),
        "is_user": checkAuth(request),
    }
    return render(request, 'main/agencies.html', context=context)




def trending(request):
    title = "Trending News "
    articles = models.News_Articles.objects.all().order_by('-picture')
    # articles = articles[:10]

    context = {
        "title": title,
        "articles": articles,
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
            user = request.user
            context = {
                "user":user,
                "signedIn": True,
                "is_user": checkAuth(request),
            }
            return HttpResponseRedirect("/")

    else:
        form_instance = forms.RegistrationForm()

    context = {
        "form":form_instance,
        "title": title,
        "is_user": checkAuth(request),
    }
    return render(request, "registration/signUp.html", context = context)






def agencyProfile(request, uname=None):
    delete = request.GET.get('delete', 0)

    if delete != 0:
        Request_In_Progress.objects.filter(id=delete).delete()

    title = "Agency Profile"
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")
    agency = Agencies.objects.get(username=uname)
    try:
        posts = Agency_Social_Media_Post.objects.filter(author=agency).order_by('-date_posted')
        if posts:
            has_posts = True
        else:
            has_posts=False
    except:
        has_posts = False

    try:
        agency = Agencies.objects.get(username=uname)
        proportion = Request_In_Progress.objects.filter(agency=agency).values_list('amount_fulfilled', 'amount_total')
        amount_fulfilled_total = 0
        amount_requested_total = 0
        amount_not_fulfilled = 0
        for p in proportion:
            amount_fulfilled_total += p[0]
            amount_requested_total += p[1]

        if amount_requested_total:
            amount_not_fulfilled = round((amount_requested_total-amount_fulfilled_total)*100/amount_requested_total, 2)
            amount_fulfilled_total = round(amount_fulfilled_total*100/amount_requested_total, 2)
        requests_in_progress = Request_In_Progress.objects.filter(is_complete=True, agency=agency).count()
        requests_completed = Request_In_Progress.objects.filter(is_complete=False, agency=agency).count()
        volunteering_request = Volunteering.objects.filter(agency=agency)[:6]
        if request.user not in agency.admin_users.all():
            is_admin = False
        else:
            is_admin = True


        if request.method == "POST":
            profile = Profile.objects.get(user=request.user)
            completed_form = HideCompletedRequestsForm(request.POST, instance=profile)
            if(completed_form.is_valid()):
                completed_form.save()
        try:
            profile = Profile.objects.get(user=request.user)
            is_hidden = HideCompletedRequestsForm(instance=profile)
        except:
            is_hidden = HideCompletedRequestsForm()
        hidden_checked = is_hidden['requests_view_hide_completed'].value()

        if hidden_checked:
            requests = Request_In_Progress.objects.filter(is_complete=False, agency=agency)[:6]
        else:
            requests = Request_In_Progress.objects.filter(agency=agency)[:6]

        instance  = models.Profile.objects.get(user=request.user)
        causes = agency.causes

        if  request.user in agency.admin_users.all():
            is_personal_agency = True
        else:
            is_personal_agency = False
        is_agency = True

        if agency.only_volunteer:
            volunteer_only = True
        else:
            volunteer_only = False

        is_follower = False

        prof = Profile.objects.get(user=request.user)

        follow = request.GET.get('follow', 0)
        if follow != 0:
             if(agency in prof.agencies_following.all()):
                 profile.agencies_following.remove(agency)
             else:
                 profile.agencies_following.add(agency)

        if(agency in prof.agencies_following.all()):
            is_follower = True

        context = {
            "title": title,
            "is_follower": is_follower,
            "amount_fulfilled_total": amount_fulfilled_total,
            "amount_not_fulfilled": amount_not_fulfilled,
            "volunteer_only": volunteer_only,
            "is_user": checkAuth(request),
            "user": request.user,
            "username": uname,
            "has_posts": has_posts,
            "posts": posts,
            "requests": requests,
            "is_agency":is_agency,
            "is_admin": is_admin,
            "requests_in_progress": requests_in_progress,
            "requests_completed": requests_completed,
            "volunteering_request": volunteering_request,
            "is_hidden": is_hidden,
            "agency": agency,
             "causes": causes,
            "is_personal_agency": is_personal_agency
        }
        return render(request, 'main/agencyProfile.html', context=context)

    except models.Agencies.DoesNotExist:
        is_agency = False
        is_personal_agency = False
    context = {
        "title": title,
        "is_user": checkAuth(request),
        "user": request.user,
        "has_posts": has_posts,
        "posts": posts,
        "is_agency": is_agency,
        "is_personal_agency": is_personal_agency,
        "username": uname,
    }
    return render(request, 'main/agencyProfile.html', context=context)





def agencySignUp(request):
    signedIn = True
    is_user = request.POST.get('is_user')
    passw = request.POST.get("pass")

    user = authenticate(request, is_user=is_user, password=passw)

    if request.method == "POST":
        form_instance = forms.AgencyForm(request.POST, request.FILES)

        if form_instance.is_valid():
            instance = form_instance.save(commit = False)
            instance.user = request.user

            name = string.capwords(instance.name)
            uname = re.sub(r"\s+", "", name)
            instance.username = uname
            instance.save()
            instance.admin_users.add(request.user)
            return redirect('agencyProfile', uname=uname)
            #return redirect("main/agencySignUp.html")
    else:
        form_instance = forms.AgencyForm()
    context = {
        "form" : form_instance,
        "e": is_user,
        "signedIn": signedIn,
        "is_user": checkAuth(request),
    }
    return render(request, 'main/agencySignUp.html', context=context)




def profile(request, username=None):
    title = "Profile"
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")

    profile = Profile.objects.get(user=request.user)
    all_profiles = models.Profile.objects.exclude(user=request.user)
    number_of_profiles = all_profiles.count()

    denominator = number_of_profiles+1
    num_donations_numerator = 0
    num_volunteer_numerator = 0
    num_items_numerator = 0
    num_cause_numerator = 0
    num_agency_numerator = 0

    number_of_donations = profile.number_of_donations
    number_of_volunteering_participations = profile.number_of_volunteering_participations
    number_of_items_donated = profile.number_of_items_donated
    number_of_causes_contributed_to = profile.number_of_causes_contributed_to.count()
    number_of_agencies_contributed_to = profile.number_of_agencies_contributed_to.count()

    for p in all_profiles:
        if p.number_of_donations <= number_of_donations:
            num_donations_numerator += 1
        if p.number_of_volunteering_participations <= number_of_volunteering_participations:
            num_volunteer_numerator += 1
        if p.number_of_items_donated <= number_of_items_donated:
            num_items_numerator += 1
        if p.number_of_causes_contributed_to.count() <= number_of_causes_contributed_to:
            num_cause_numerator += 1
        if p.number_of_agencies_contributed_to.count() <= number_of_agencies_contributed_to:
            num_agency_numerator += 1

    num_donations_percentile = round(num_donations_numerator*100/denominator, 2)
    num_items_percentile = round(num_items_numerator*100/denominator, 2)
    num_volunteer_percentile = round(num_volunteer_numerator*100/denominator, 2)
    num_cause_percentile = round(num_cause_numerator*100/denominator, 2)
    num_agency_percentile = round(num_agency_numerator*100/denominator, 2)

    #or prof in

    is_follower = False
    has_posts = False
    posts = []
    has_agency = False
    user_agency = []
    has_event = False
    user_events = []
    try:
        user_info = models.User.objects.get(username=username)
        if user_info == request.user:
            is_personal_profile = True
            user = request.user
            profile = Profile.objects.get(user=request.user)
            all_agencies = Agencies.objects.all()
            for agency in all_agencies:
                if request.user in agency.admin_users.all():
                    has_agency = True
                    user_agency.append(agency)
            user_volunteering = Volunteering.objects.all()
            for v in user_volunteering:
                if request.user in v.volunteers.all():
                    has_event = True
                    user_events.append(v)
            try:
                posts = Social_Media_Post.objects.filter(author=request.user).order_by('-date_posted')
                if posts:
                    has_posts = True
            except:
                has_posts = False

        else:

           is_personal_profile = False
           profile = Profile.objects.get(user=user_info)
           prof = Profile.objects.get(user=request.user)

           number_of_donations = profile.number_of_donations
           number_of_volunteering_participations = profile.number_of_volunteering_participations
           number_of_items_donated = profile.number_of_items_donated
           number_of_causes_contributed_to = profile.number_of_causes_contributed_to.count()
           number_of_agencies_contributed_to = profile.number_of_agencies_contributed_to.count()

           delete = request.GET.get('follow', 0)
           if delete != 0:
                if(prof in profile.followers.all()):
                    profile.followers.remove(prof)
                    prof.following.remove(profile)
                else:
                    profile.followers.add(prof)
                    prof.following.add(profile)
           if(prof in profile.followers.all()):
               is_follower = True

           all_agencies = Agencies.objects.all()
           for agency in all_agencies:
               if user_info in agency.admin_users.all():
                   has_agency = True
                   user_agency.append(agency)
           user_volunteering = Volunteering.objects.all()
           for v in user_volunteering:
               if user_info in v.volunteers.all():
                   has_event = True
                   user_events.append(v)
           try:
               posts = Social_Media_Post.objects.filter(author=user_info).order_by('-date_posted')[:15]
               if posts:
                   has_posts = True
           except:
               has_posts = False


        is_an_account = True
        context = {
            "title": title,
            "is_user": checkAuth(request),
            "user": request.user,
            "has_posts": has_posts,
            "posts": posts,
            "username": username,
            "is_follower": is_follower,
            "has_event": has_event,
            "user_events": user_events,
            "user_agency": user_agency,
            "is_an_account":is_an_account,
            "user_info": user_info,
            "num_volunteer_percentile": num_volunteer_percentile,
            "num_donations_percentile": num_donations_percentile,
            "num_cause_percentile": num_cause_percentile,
            "num_agency_percentile": num_agency_percentile,
            "num_items_percentile": num_items_percentile,
            "has_agency": has_agency,
            "is_personal_profile": is_personal_profile,
            "number_of_donations": number_of_donations,
            "number_of_volunteering_participations": number_of_volunteering_participations,
            "number_of_items_donated": number_of_items_donated,
            "number_of_causes_contributed_to": number_of_causes_contributed_to,
            "number_of_agencies_contributed_to": number_of_agencies_contributed_to
        }
        return render(request, 'main/profile.html', context=context)
    except models.User.DoesNotExist:
        return HttpResponseRedirect("/")



def createProfile(request):
    title = "Create Profile"
    signedIn = True
    is_user = request.POST.get('is_user')
    passw = request.POST.get("pass")
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")

    user = authenticate(request, is_user=is_user, password=passw)
    instance  = get_object_or_404(Profile, user=request.user)
    data = {'city': instance.city, 'picture': instance.picture, 'bio': instance.bio}
    if request.method == "POST":
        form_instance = forms.ProfileForm(request.POST, request.FILES, initial=data, instance=instance)
        if form_instance.is_valid():
            instance = form_instance.save(commit=False)
            instance.user = request.user
            username = instance.user.username
            instance.save()
            return redirect('profile', username=username)
    else:
        form_instance = forms.ProfileForm(initial=data)
    context = {
        "form":form_instance,
        "title": title,
        "is_user": checkAuth(request),
    }
    return render(request, "main/createProfile.html", context = context)



def createCause(request):
    title = "Create Cause"
    signedIn = True
    is_user = request.POST.get('is_user')
    passw = request.POST.get("pass")
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")

    if request.method == "POST":
        form_instance = forms.CauseForm(request.POST)
        if form_instance.is_valid():
            instance = form_instance.save(commit=False)
            title = instance.title
            instance.username = re.sub(r"\s+", "", title)
            print(instance.username)
            instance.save()
            return HttpResponseRedirect("/")
    else:
        form_instance = forms.CauseForm()
    context = {
        "form" : form_instance,
        "e": is_user,
        "signedIn": signedIn,
        "is_user": checkAuth(request),
    }
    return render(request, 'main/createCause.html', context=context)



def pledgeSupport(request,  username=None):
    agency = Agencies.objects.get(username=username)
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")

    if request.user not in agency.admin_users.all():
        return HttpResponseRedirect("/")


    if request.method == "POST":
        form_instance = forms.PledgeSupportForm(request.POST, instance=agency)
        if form_instance.is_valid():
            ids = request.POST.get('causes')
            for id in ids:
                agency.causes.add(id)

                cs = Cause.objects.filter(id=id)[0]
                txt = agency.name + " pledged their support for "+ cs.title + " on " + str(datetime.now())
                agency_url = agency.username
                agency_name = agency.name
                cause_url = cs.username
                cause_name = cs.title
                type="agency pledge"
                Agency_Social_Media_Post.objects.create(author=agency, text=txt, agency_profile=agency_url, agency_name=agency_name, cause_profile=cause_url, cause_name=cause_name, type=type)


            causes = agency.causes.all()
            if request.user in agency.admin_users.all():
                is_admin = True
            else:
                is_admin = False
            context = {
                "username": username,
                "is_agency": True,
                "is_admin": is_admin,
                "user": request.user,
                "agency": agency,
                "is_user": checkAuth(request),
                "causes": causes,
                "is_personal_agency": True
            }
            return render(request, 'main/agencyProfile.html', context=context)
    else:
        form_instance = forms.PledgeSupportForm()
    context = {
        "form" : form_instance,
        "username": username,
        "is_user": checkAuth(request),
    }
    return render(request, 'main/pledgeSupport.html', context=context)



def addAgency(request, username=None):
    agency = Agencies.objects.get(username=username)
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")

    if request.method == "POST":
        form_instance = forms.AddAgencyForm(request.POST, instance=agency)
        if form_instance.is_valid():
            f_instance = form_instance.save(commit=False)
            users = form_instance.cleaned_data['admin_users']
            for user in users:
                agency.admin_users.add(user)
            agency.save()
            return redirect('/')
    else:
        form_instance = forms.AddAgencyForm()
    context = {
        "form" : form_instance,
        "instance": agency,
        "username": username,
        "is_user": checkAuth(request),
    }
    #return redirect(addAgency, username=username)
    return render(request, 'main/addAgency.html', context=context)




def activeCauses(request):
    # reader = geoip2.database.Reader('../GeoLite2-City_20201013/GeoLite2-City.mmdb')
    # ip = '24.94.15.83'
    # response = reader.city(ip)
    # print(response.city.geoname_id)
    #
    # location1 = (response.location.latitude, response.location.longitude)
    #
    # geolocator = Nominatim(user_agent="my_user_agent")
    # loc = geolocator.geocode("Chico, CA", exactly_one=False)[0]
    #
    # location2 = (loc.latitude, loc.longitude)
    #
    #
    # distance = geopy.distance.distance(location1, location2).miles
    # print(distance)
    # reader.close()

    cause = Cause.objects.all()
    cause_type = Cause.objects.values_list('type_of_cause', flat=True)
    #print(cause_type)
    cause_cities = Cause.objects.values_list('location', flat=True)
    cities = City.objects.all().filter(id__in = cause_cities)
    if request.method == 'POST':
        city_id = request.POST.get('city_id')
        type_id = request.POST.get('type_id')
        if city_id is not "":
            if type_id is not "":
                selected_item = get_object_or_404(City, pk=request.POST.get('city_id'))
                cause = Cause.objects.filter(location=selected_item, type_of_cause=type_id)
            else:
                selected_item = get_object_or_404(City, pk=request.POST.get('city_id'))
                cause = Cause.objects.filter(location=selected_item)
        elif type_id is not "":
            cause = Cause.objects.filter(type_of_cause=type_id)



    context = {
        "Cause": cause,
        "cities": cities,
        "cause_type": cause_type,
        "is_user": checkAuth(request)
    }
    return render(request, 'main/activeCauses.html', context=context)




def causePage(request, uname=None):
    title = "Cause"
    username = re.sub(r"\s+", "", uname)
    try:
        cause_info = Cause.objects.get(username=username)
        requests = Request_In_Progress.objects.filter(cause=cause_info.id)
        volunteer_requests = Volunteering.objects.filter(cause=cause_info.id)
        article1 = News_Articles.objects.filter(description__contains=uname)
        article2  = News_Articles.objects.filter(title__contains=uname)
        agencies = Agencies.objects.filter(causes=cause_info)

        #if request.user not in agency.admin_users.all():
        if request.method == 'POST':
            agency_id = request.POST.get('agency_id')
            if agency_id is not "":
                selected_item = get_object_or_404(Agencies, pk=request.POST.get('agency_id'))
                requests = Request_In_Progress.objects.filter(agency=selected_item, cause=cause_info.id)
                volunteer_requests = Volunteering.objects.filter(agency=selected_item, cause=cause_info.id)
        articles = article1 | article2
        is_cause = True
        context = {
            "title": title,
            "is_user": checkAuth(request),
            "user": request.user,
            "volunteer_requests": volunteer_requests,
            "uname": uname,
            "agencies": agencies,
            "is_cause": is_cause,
            "articles": articles,
            "requests": requests,
            "cause_info": cause_info,
        }
        return render(request, 'main/cause.html', context=context )

    except models.Cause.DoesNotExist:
        return redirect('activeCauses')



def agencyRequestedDonations(request, username=None):
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")
    if(username is None):
        requests = Request_In_Progress.objects.all()
        is_admin = False
        agency = "All Agency"
    else:
        agency = Agencies.objects.filter(username=username)[0]
        if request.user in agency.admin_users.all():
            is_admin = True
        else:
            is_admin = False
        requests = Request_In_Progress.objects.filter(agency=agency)

    delete = request.GET.get('delete', 0)
    context = {
        "agency": agency,
        "username": username,
        "user": request.user,
        "is_admin": is_admin,
        "is_user": checkAuth(request),
        "requests": requests,
    }
    if delete != 0:
        Request_In_Progress.objects.filter(id=delete).delete()

    return render(request, 'main/agencyRequestedDonations.html', context=context)



def addRequests(request, username):
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")
    agency = Agencies.objects.filter(username=username)[0]
    if request.user not in agency.admin_users.all():
        return HttpResponseRedirect("/")
    if request.method == "POST":
        form_instance = forms.AddRequestForm(request.POST)
        if form_instance.is_valid():
          instance = form_instance.save(commit=False)
          cause = form_instance.cleaned_data['cause']
          if cause not in agency.causes.all():
              agency.causes.add(cause)
          instance.agency = agency


          amt = str(form_instance.cleaned_data['amount_total'])
          txt = agency.name + " requested " + amt + " " + form_instance.cleaned_data['item'] + " on " + str(datetime.now()) + " for " + cause.title
          agency_url = agency.username
          agency_name = agency.name
          cause_url = cause.username
          cause_name = cause.title
          type="agency add request"
          Agency_Social_Media_Post.objects.create(author=agency, text=txt, agency_profile=agency_url, agency_name=agency_name, cause_profile=cause_url, cause_name=cause_name, type=type)



          instance.save()
          return redirect('activeDonations')
    else:
        form_instance = forms.AddRequestForm()

    context = {
      "form":form_instance,
      "username": username,
      "agency": agency,
      "is_user": checkAuth(request),
    }
    return render(request, 'main/addRequests.html', context=context)



def agencyRequestedVolunteers(request, username=None):
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")
    if(username is None):
        requests = Volunteering.objects.all()
        is_admin = False
        agency = "All Agency"
    else:
        agency = Agencies.objects.filter(username=username)[0]
        if request.user in agency.admin_users.all():
            is_admin = True
        else:
            is_admin = False
        requests = Volunteering.objects.filter(agency=agency)

    delete = request.GET.get('delete', 0)
    context = {
        "agency": agency,
        "username": username,
        "user": request.user,
        "is_admin": is_admin,
        "is_user": checkAuth(request),
        "requests": requests,
    }
    if delete != 0:
        Volunteering.objects.filter(id=delete).delete()

    return render(request, 'main/agencyRequestedVolunteers.html', context=context)


def addVolunteerRequest(request, username):
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")
    agency = Agencies.objects.filter(username=username)[0]
    if request.user not in agency.admin_users.all():
        return HttpResponseRedirect("/")
    if request.method == "POST":
        form_instance = AddVolunteerRequestForm(request.POST)
        if form_instance.is_valid():
          instance = form_instance.save(commit=False)
          cause = form_instance.cleaned_data['cause']
          if cause not in agency.causes.all():
              agency.causes.add(cause)
          instance.agency = agency

          amt = str(form_instance.cleaned_data['number_of_volunteers'])
          txt = agency.name + " requested " + amt + " volunteers on " + str(datetime.now()) + " for " + cause.title
          agency_url = agency.username
          agency_name = agency.name
          cause_url = cause.username
          date_p = form_instance.cleaned_data['date_needed']
          cause_name = cause.title
          type="agency add volunteer request"
          Agency_Social_Media_Post.objects.create(author=agency, text=txt, agency_profile=agency_url, agency_name=agency_name, cause_profile=cause_url, cause_name=cause_name, type=type, date_posted=date_p)


          instance.save()
          context = {
            "form":form_instance,
            "username": username,
            "agency": agency,
            "is_user": checkAuth(request),
          }
          return redirect('activeVolunteerRequests')
    else:
        form_instance = AddVolunteerRequestForm()

    context = {
      "form":form_instance,
      "username": username,
      "agency": agency,
      "is_user": checkAuth(request),
    }
    return render(request, 'main/addVolunteerRequest.html', context=context)



def activeDonations(request):
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")

    agencies = Agencies.objects.all()
    causes = Cause.objects.all()
    requests = Request_In_Progress.objects.filter(is_complete=False).order_by('-date_requested')


    if request.method == 'POST':
        agency_id = request.POST.get('agency_id')
        cause_id = request.POST.get('cause_id')
        if agency_id is not "":
            if cause_id is not "":
                selected_item = get_object_or_404(Agencies, pk=request.POST.get('agency_id'))
                selected_cause = get_object_or_404(Cause, pk=request.POST.get('cause_id'))
                requests = Request_In_Progress.objects.filter(agency=selected_item, cause=selected_cause, is_complete=False).order_by('-date_requested')
            else:
                selected_item = get_object_or_404(Agencies, pk=request.POST.get('agency_id'))
                requests = Request_In_Progress.objects.filter(agency=selected_item, is_complete=False).order_by('-date_requested')

        elif cause_id is not "":
            selected_cause = get_object_or_404(Cause, pk=request.POST.get('cause_id'))
            requests = Request_In_Progress.objects.filter(cause=selected_cause, is_complete=False).order_by('-date_requested')



    user = request.user
    context = {
        "user": user,
        "agencies": agencies,
        "causes": causes,
        "is_user": checkAuth(request),
        "requests": requests
    }

    return render(request, 'main/activeDonations.html', context = context)




def activeVolunteerRequests(request):
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")


    agencies = Agencies.objects.all()
    causes = Cause.objects.all()
    requests = Volunteering.objects.all().order_by('-date_needed')


    request_cities = Volunteering.objects.values_list('location', flat=True)
    cities = City.objects.all().filter(id__in = request_cities)

    if request.method == 'POST':
        agency_id = request.POST.get('agency_id')
        cause_id = request.POST.get('cause_id')
        city_id = request.POST.get('city_id')
        if agency_id is not "":
            if cause_id is not "":
                if city_id is not "":
                    selected_item = get_object_or_404(Agencies, pk=request.POST.get('agency_id'))
                    selected_cause = get_object_or_404(Cause, pk=request.POST.get('cause_id'))
                    selected_location = get_object_or_404(City, pk=request.POST.get('city_id'))
                    requests = Volunteering.objects.filter(agency=selected_item, cause=selected_cause, location=selected_location).order_by('-date_needed')
                else:
                    selected_item = get_object_or_404(Agencies, pk=request.POST.get('agency_id'))
                    selected_cause = get_object_or_404(Cause, pk=request.POST.get('cause_id'))
                    requests = Volunteering.objects.filter(agency=selected_item, cause=selected_cause).order_by('-date_needed')
            elif city_id is not "":
                selected_location = get_object_or_404(City, pk=request.POST.get('city_id'))
                selected_item = get_object_or_404(Agencies, pk=request.POST.get('agency_id'))
                requests = Volunteering.objects.filter(agency=selected_item, location=selected_location).order_by('-date_needed')
            else:
                selected_item = get_object_or_404(Agencies, pk=request.POST.get('agency_id'))
                requests = Volunteering.objects.filter(agency=selected_item).order_by('-date_needed')
        elif cause_id is not "":
            if city_id is not "":
                selected_cause = get_object_or_404(Cause, pk=request.POST.get('cause_id'))
                selected_location = get_object_or_404(City, pk=request.POST.get('city_id'))
                requests = Volunteering.objects.filter(cause=selected_cause, location=selected_location).order_by('-date_needed')
            else:
                selected_cause = get_object_or_404(Cause, pk=request.POST.get('cause_id'))
                requests = Volunteering.objects.filter(cause=selected_cause).order_by('-date_needed')
        elif city_id is not "":
                selected_location = get_object_or_404(City, pk=request.POST.get('city_id'))
                requests = Volunteering.objects.filter(location=selected_location).order_by('-date_needed')


    user = request.user
    context = {
        "user": user,
        "agencies": agencies,
        "causes": causes,
        "cities": cities,
        "is_user": checkAuth(request),
        "requests": requests
    }

    return render(request, 'main/activeVolunteerRequests.html', context = context)




def finalSubmitDonation(request, id):

    if checkAuth(request) == False:
        return HttpResponseRedirect("/")
    donation = Request_In_Progress.objects.filter(id=id)[0]

    if request.method == "POST":
        form_instance = forms.MakeDonation(request.POST)
        if form_instance.is_valid():

          instance = form_instance.save(commit=False)
          instance.user = request.user
          instance.request_in_progress = donation
          instance.fulfilled_amount = 0
          instance.save()

          pledged = form_instance.cleaned_data['promised_amount']
          fulfilled = donation.amount_fulfilled
          total = donation.amount_total



          prof = Profile.objects.filter(user=request.user)[0]
          prof.number_of_donations+=1
          prof.number_of_items_donated += pledged
          agency = donation.agency
          cause = donation.cause
          if prof.number_of_agencies_contributed_to:
              if agency not in prof.number_of_agencies_contributed_to.all():
                  prof.number_of_agencies_contributed_to.add(agency)
          else:
              prof.number_of_agencies_contributed_to.add(agency)
          if prof.number_of_causes_contributed_to:
               if cause not in prof.number_of_causes_contributed_to.all():
                   prof.number_of_causes_contributed_to.add(cause)
          else:
              prof.number_of_causes_contributed_to.add(cause)


          prof.save()

          donation.amount_fulfilled = pledged+fulfilled
          donation.percent_complete = ((pledged+fulfilled)/total)*100

          user = request.user

          txt = user.first_name + user.last_name + "pledged to donate "+  str(pledged) + " " + donation.item +" for " + donation.agency.name + "'s help with " + donation.cause.title + " on" + str(datetime.now())
          agency_url=donation.agency.username
          agency_name=donation.agency.name
          cause_url = donation.cause.username
          cause_name = donation.cause.title
          number_pledged = pledged
          item = donation.item
          date_p = datetime.now()
          type="donation"
          Social_Media_Post.objects.create(author=request.user, text=txt, agency_profile=agency_url, agency_name=agency_name, date_posted=date_p, cause_profile=cause_url, cause_name=cause_name, type=type, number_pledged=number_pledged, item=item)


          if(donation.amount_fulfilled == donation.amount_total):
              donation.is_complete = True
              donation.percent_complete = 100


              txt = donation.agency.name + " successfully fulfilled their request for " + str(donation.amount_total) +  " " + donation.item + " on " + str(datetime.now()) + " for " + donation.cause.title

              type="agency complete donation"
              Agency_Social_Media_Post.objects.create(author=donation.agency, text=txt, agency_profile=agency_url, agency_name=agency_name, cause_profile=cause_url, cause_name=cause_name, type=type)


          donation.save()
          return redirect('activeDonations')
          #return render(request, 'main/activeDonations.html', context=context)
    else:
        form_instance = forms.MakeDonation()

    user = request.user
    context = {
        "user": user,
        "id": id,
        "is_user": checkAuth(request),
        "form": form_instance,
        "donation": donation
    }

    return render(request, 'main/finalSubmitDonation.html', context = context)




def PledgeToVolunteer(request, id):
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")
    VolunteerPledge = Volunteering.objects.filter(id=id)[0]
    user = request.user
    if request.user not in VolunteerPledge.volunteers.all():
        prof = Profile.objects.filter(user=request.user)[0]
        prof.number_of_volunteering_participations+=1
        agency = VolunteerPledge.agency
        cause = VolunteerPledge.cause
        if prof.number_of_agencies_contributed_to:
            if agency not in prof.number_of_agencies_contributed_to.all():
                prof.number_of_agencies_contributed_to.add(agency)
        else:
            prof.number_of_agencies_contributed_to.add(agency)
        if prof.number_of_causes_contributed_to:
            if cause not in prof.number_of_causes_contributed_to.all():
                prof.number_of_causes_contributed_to.add(cause)
        else:
            prof.number_of_causes_contributed_to.add(cause)
        prof.save()

        VolunteerPledge.volunteers.add(request.user)
        num_total = VolunteerPledge.number_of_volunteers
        VolunteerPledge.amount_fulfilled += 1;
        amnt_fulfilled = VolunteerPledge.amount_fulfilled
        VolunteerPledge.percent_complete = (amnt_fulfilled/num_total)*100


        txt = user.first_name + user.last_name + "pledged to attend "+ VolunteerPledge.agency.name + "'s volunteering event for " + VolunteerPledge.cause.title + " on"
        agency_url=VolunteerPledge.agency.username
        agency_name=VolunteerPledge.agency.name
        cause_url = VolunteerPledge.cause.username
        cause_name = VolunteerPledge.cause.title
        date_p = VolunteerPledge.date_needed
        type="volunteer"
        Social_Media_Post.objects.create(author=request.user, text=txt, agency_profile=agency_url, agency_name=agency_name, date_posted=date_p, cause_profile=cause_url, cause_name=cause_name, type=type)



        if(VolunteerPledge.amount_fulfilled == VolunteerPledge.number_of_volunteers):
          #donation.is_complete = True
           VolunteerPledge.percent_complete = 100


           txt = VolunteerPledge.agency.name + " successfully fulfilled their request for " + str(VolunteerPledge.number_of_volunteers) +  " volunteers on " + str(datetime.now()) + " for " + VolunteerPledge.cause.title

           type="agency complete volunteer"
           Agency_Social_Media_Post.objects.create(author=VolunteerPledge.agency, text=txt, agency_profile=agency_url, agency_name=agency_name, cause_profile=cause_url, cause_name=cause_name, type=type)


        VolunteerPledge.save()

    context = {
        "user": user,
        "id": id,
        "is_user": checkAuth(request),
        "volunteer": VolunteerPledge
    }

    return render(request, 'main/PledgeToVolunteer.html', context = context)





def search(request):
    if request.method == 'GET' and 'q' in request.GET:
        keyword = request.GET.get("q")
        print(keyword)
    else:
        keyword is None

    if keyword is not None and keyword != '':
        agencies = Agencies.objects.filter(Q(name__contains=keyword) | Q(username__contains=keyword))
        causes = Cause.objects.filter(Q(title__contains=keyword))
        users = User.objects.filter(Q(first_name__contains = keyword) | Q(last_name__contains = keyword) | Q(username__contains = keyword))
        news_articles = News_Articles.objects.filter(Q(title__contains = keyword) | Q(description__contains = keyword))

    else:
        agencies = None
        causes = None
        users = None
        news_articles = None

    context = {
        "agencies": agencies,
        "news_articles": news_articles,
        "users": users,
        "is_user": checkAuth(request),
        "causes": causes,
    }
    return render(request, 'main/search.html', context=context)



def donationPredictor(request):
    if request.method == 'POST':
        city_id = request.POST.get('city_id')
        type_of_cause = request.POST.get('cause_type_id')
        result = 0
        if city_id:
            city = City.objects.filter(display_name=city_id).values_list('population', flat=True)
            #print(city)
            if not type_of_cause:
                df8 = pd.DataFrame()

        if type_of_cause:
            df = pd.DataFrame(list(Cause.objects.all().filter(type_of_cause=type_of_cause).values()))

            #for i in df.iterrows():
            cause_ids = (df['id'])
            cause_location_ids = (df['location_id'])
            df1 = pd.DataFrame(list(City.objects.all().filter(id__in=cause_location_ids).values()))
            #print("here's the new dataframe with city info to join on:")
            #print(df1)

            df3 = pd.merge(df, df1, left_on='location_id', right_on='id')
            #print("here's the joined dataframe:")
            #print(df3)

            requests = Request_In_Progress.objects.all().filter(cause__in=cause_ids).values()
            volunteers = Volunteering.objects.all().filter(cause__in=cause_ids).values()
            if requests:
                if volunteers:
                    df4 = pd.DataFrame(list(requests))
                    df5 = pd.merge(df4, df3, left_on='cause_id', right_on='id_x')
                    df5.columns = ['quantity' if x=='amount_total' else x for x in df5.columns]

                    df6 = pd.DataFrame(list(volunteers))
                    df6.columns = ['quantity' if x=='number_of_volunteers' else x for x in df6.columns]
                    df6['item']='Volunteers'
                    df7 = pd.merge(df6, df3, left_on='cause_id', right_on='id_x')

                    df8 = pd.concat([df5, df7])
                else:
                    df4 = pd.DataFrame(list(requests))
                    df8 = pd.merge(df4, df3, left_on='cause_id', right_on='id_x')
                    df8.columns = ['quantity' if x=='amount_total' else x for x in df8.columns]

            elif volunteers:
                    df6 = pd.DataFrame(list(volunteers))
                    df6.columns = ['quantity' if x=='number_of_volunteers' else x for x in df6.columns]
                    df6['item']='Volunteers'
                    df8 = pd.merge(df6, df3, left_on='cause_id', right_on='id_x')



            else:
                df8 = pd.DataFrame()


        if not city_id:
            if not type_of_cause:
                df8 = pd.DataFrame()

    else:
        df8 = pd.DataFrame()
        result=0

    cause_types = Cause.objects.values_list('type_of_cause', flat=True).distinct()
    cities = City.objects.values_list('display_name', flat=True)

    if not df8.empty:
        #x_train = dataTrain[['Temperature(K)', 'Pressure(ATM)']].to_numpy().reshape(-1,2)
        df8['name'] = le.fit_transform(df8['name'])
        X = df8[['population', 'name']].to_numpy().reshape(-1,2)
        y = df8[['item']]
        y = le.fit_transform(y)

        lr_model = LogisticRegression()
        lr_model.fit(X,y)
        preds = lr_model.predict(X)
        counter = 0
        answer = (le.inverse_transform(preds))
        word_counter = {}
        for word in answer:
            if word in word_counter:
                word_counter[word] += 1
            else:
                word_counter[word] = 1

        popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
        result = popular_words[:1]


    context = {
        "is_user": checkAuth(request),
        "cause_types": cause_types,
        "cities": cities,
        "result": result,
        "df": df8,
    }
    return render(request, "main/donationPredictor.html", context=context)



def followingFeed(request):
    users = Profile.objects.filter(user=request.user).values_list('following')
    has_user_posts = False
    has_agency_posts = False
    user_posts = []
    agency_posts = []
    agencies_followed = Profile.objects.filter(user=request.user).values_list('agencies_following')
    #print(agencies_followed)
    try:

        for u in users:
            prof = User.objects.filter(profile=u[0])[0]
            #us = User.objects.filter(username=prof.user.username)
            usp = Social_Media_Post.objects.filter(author=prof)

            for p in usp:
                #print(p)
                user_posts.append(p)
    except:
        has_user_posts=False
    try:
        for a in agencies_followed:
            asp = Agency_Social_Media_Post.objects.filter(author=a)
            for a in asp:
                #print(a)
                agency_posts.append(a)
    except:
        has_agency_posts=False


    if user_posts:
        has_user_posts = True
        user_posts = sorted(user_posts, key=lambda Social_Media_Post: Social_Media_Post.date_posted, reverse=True)
    if agency_posts:
        has_agency_posts = True
        agency_posts = sorted(agency_posts, key=lambda Agency_Social_Media_Post: Agency_Social_Media_Post.date_posted, reverse=True)


    context = {
        "is_user": checkAuth(request),
        "user_posts": user_posts,
        "agency_posts": agency_posts,
        "has_user_posts": has_user_posts,
        "has_agency_posts": has_agency_posts,
    }
    return render(request, "main/followingFeed.html", context=context)
