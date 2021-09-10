from django.shortcuts import render, redirect, render_to_response
from .forms import DetectForm
from .ml import machine
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.cache import cache_control
from .forms import SearchForm
import os
import joblib
import requests
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
model1 = joblib.load(os.path.dirname(__file__) + "\\mySVCModel1.pkl")
model2 = joblib.load(os.path.dirname(__file__) + "\\myModel.pkl")
# model3 = joblib.load(os.path.dirname(__file__) + "\\model.pkl")

# Create your views here.
def homepage(request):
    return render(request, 'home.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def auth(request):
    if(request.method == "POST"):
        un = request.POST.get('username')
        up = request.POST.get('password')

        if(un == "sahil" and up == "sahil"):
            request.session['authdetails'] = "sahil"
            if(request.session['authdetails'] == "sahil"):
                print("Session for SAHIL started")
                return render(request, 'home.html')
            else:
                return redirect('/auth')
        elif(un == "guest" and up == "guest"):
            request.session['authdetails'] = "guest"
            if(request.session['authdetails'] == "guest"):
                print("GUEST SESSION STARTED")
                return render(request, 'home.html')
            else:
                return redirect('/auth')
        else:
            return render(request, 'auth.html')
    else:
        return render(request, 'auth.html')
            
#Function for TEXT SPAM is as follows
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkSpam(request):
    if(request.method == "POST"):
        if(request.session.has_key('authdetails') == True):
            algo = request.POST.get("algo")
            rawData = request.POST.get("rawdata")

            if(algo == "Algo-1"):
                return render(request, 'outputalgo1.html', {"answer" : model1.predict([rawData])[0]})
            elif(algo == "Algo-2"):
                return render(request, 'outputalgo2.html', {"answer" : model2.predict([rawData])[0]})
            # elif(algo == "Algo-3"):
                # return render(request, 'output.html', {"answer" : model3.predict([rawData])[0]})
        else:
            return redirect('/')
    else:
        return render(request, 'home.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if(request.session.has_key('authdetails') == True):
        request.session.clear()
        print("Session Destroyed Successfully")
        # request.session.flush()
        return redirect('/')
    else:
        return redirect('/')
        
def spamtype(request):
    return render(request, 'spamtype.html')
    
def selectspamtype(request):
    if(request.method == "POST"):
        if(request.session['authdetails'] == "sahil"):
            spamtype = request.POST.get("spam")
        else:
            return redirect('/')
    else:
        print("No Spam Type Selected")
        return render(request, 'spamtype.html')
        
def spamone(request):
    return render(request, 'textspam.html')
    
def Home(request):
    form = SearchForm(request.POST or None)
    response = None
    if form.is_valid():
        value = form.cleaned_data.get("q")

        df = pd.read_csv('spam.csv', encoding="latin-1")
        df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
        df['label'] = df['v1'].map({'ham': 0, 'spam': 1})
        X = df['v2']
        y = df['label']
        cv = CountVectorizer()
        X = cv.fit_transform(X) 
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
        clf = MultinomialNB()
        clf.fit(X_train,y_train)
        clf.score(X_test,y_test)
        y_pred = clf.predict(X_test)
        message = value
        data = [message]
        vect = cv.transform(data).toarray()
        my_prediction = clf.predict(vect)

        if(my_prediction== 1):
            print("Spam")
            response = "Spam"
        else:
            print("Not Spam")
            response = "Not Spam" 

        return render(request, 'result.html', {"response": response})
    return render(request, 'form.html', {"form": form})
    
def spam(request):
    msg1 = request.POST['msg']
    model = joblib.load('Email_Spam_detector.pkl')
    message = model.predict([msg1])[0]
    if message==0:
        ans = "Mail sent successfully"
        return render(request,'email.html',{'ans':ans})
    else:
        ans = "Looking like, you sent a spam email!!!"
        return render(request, 'email.html', {'ans': ans})
        
def textspam(request):
    return render(request,'textspam.html')
    
def wordspam(request):
    return render(request,'form.html')

def emailspam(request):
    return render(request,'email.html')
    
def hompage(request):
    form = DetectForm(request.POST)
    return render(request, 'index.html', {'form': form})

def result(request):
    form=DetectForm(request.POST)
    if form.is_valid():
        x=form.cleaned_data['msg']
        y=machine(x)
    return render_to_response('index.html',{'message':y,'form':form})