from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.auth, name = "authorization"),
    path('auth', views.auth, name = "authorization"),
    path('spamtype/', views.spamtype, name = "spamtype"),
    path('spamtype/textspam', views.textspam, name = "textspam"),
    path('spamtype/wordspam', views.wordspam, name = "textspam"),
    path('spamtype/emailspam', views.emailspam, name = "textspam"),
    path('textspam', views.spamone, name = "textspam"),
    path('spamtype/check', views.checkSpam, name = "TextCheckSpam"),
    path('logout', views.logout, name = "Logout"),
    path('spamtype/spam', views.spam),
    url('home', views.Home,name='home'),
    url('text',views.hompage,name='hompage'),
    url(r'result', views.result, name='result'),
]
