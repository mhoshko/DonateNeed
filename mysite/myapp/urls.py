from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
  url(r'^$', views.home, name='home'),
  url(r'^agencies$', views.agencies, name='agencies'),
  url(r'^trending$', views.trending, name='trending'),
  url(r'^about$', views.about, name='about'),
  url('login/', auth_views.LoginView.as_view(), name='login'),
  url(r'^postSignIn/', views.postSignIn, name='postsignin'),
  url('logout/', views.logout_view, name='logout'),
  url(r'^signUp$', views.signUp, name='signUp'),
  url(r'^donation/(?P<username>.+)/', views.donation, name='donation'),
  url(r'^fetch_donation/', views.fetch_donation, name='fetch_donation'),
  url(r'^agencySignUp/', views.agencySignUp, name='agencySignUp'),
  url(r'^profile/(?P<username>.+)/', views.profile, name='profile'),
  url(r'^agencyRequestedDonations/(?P<username>.+)/', views.agencyRequestedDonations, name='agencyRequestedDonations'),
  url(r'^agencyRequestedDonations/', views.agencyRequestedDonations, name='agencyRequestedDonations'),
  url(r'^addRequests/(?P<username>.+)/', views.addRequests, name='addRequests'),
  url(r'^createProfile/', views.createProfile, name='createProfile'),
  url(r'^agencyProfile/(?P<uname>.+)', views.agencyProfile, name='agencyProfile'),
  url(r'^createCause/', views.createCause, name='createCause'),
  url(r'^addAgency/(?P<username>.+)', views.addAgency, name='addAgency'),
  url(r'^pledgeSupport/(?P<username>.+)/', views.pledgeSupport, name='pledgeSupport'),
  url(r'^activeCauses/', views.activeCauses, name='activeCauses'),
  url(r'^cause/(?P<uname>.+)', views.causePage, name='causePage'),
  url(r'^activeDonations/', views.activeDonations, name='activeDonations'),
  url(r'^search/', views.search, name='search'),
  url(r'^finalSubmitDonation/(?P<id>.+)/', views.finalSubmitDonation, name='finalSubmitDonation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
