from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Conversation
from django.core import serializers

import random
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import json
import os
import numpy as np

# Create your views here.

classifier = joblib.load('C:\\Users\\ALAMEEN\\Documents\\Documents\\my_projects\\Customer-service-agent\\CSAProject\\DataAndBrain\\text_classifier_model.joblib')
vectorizer = joblib.load('C:\\Users\\ALAMEEN\\Documents\\Documents\\my_projects\\Customer-service-agent\\CSAProject\\DataAndBrain\\vectorizer.joblib')
    
def predict_and_respond(sentence, user):

    sentence_vector = vectorizer.transform([sentence])
    
    predicted_probabilities = classifier.predict_proba(sentence_vector)
    predicted_category = classifier.classes_[np.argmax(predicted_probabilities)]
    confidence = np.max(predicted_probabilities)

    # print(f"Confidence: {confidence}")
    
    # Set a confidence threshold
    threshold = 0.1  # Adjust this value as needed
    if confidence < threshold:
        new_con = Conversation.objects.create(
            user=user, user_question=sentence, bot_response=f"I'm sorry I don't have response for '{sentence}', try asking in another way.",
            status=False
        )
        
        new_con.save()
    
    else:
        new_con = Conversation.objects.create(
            user=user, user_question=sentence, bot_response=predicted_category,
            status=True
        )
        
        new_con.save()
        
def ask_Q(request):
    current_user = User.objects.get(username=request.user)
    if request.method == 'POST':
        msg = request.POST.get("message")
        
        if msg is None:
            return JsonResponse({'success': False})
        else:
            predict_and_respond(msg, current_user)
            return JsonResponse({'success': True})
    return redirect('/')

@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def fetch_conversation_data(request):
    # Get the current logged-in user
    current_user = request.user
    
    # Fetch the user's conversations
    conversation = Conversation.objects.filter(user=current_user)

    # Convert conversation queryset to JSON format
    conversation_json = serializers.serialize('json', conversation)

    # Return a JSON response
    return JsonResponse({
        'conversation': conversation_json,
        'status': 'success'
    })

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return JsonResponse({'success': True, 'message': 'loginin......'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid Login Credentials!!'})
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("cpassword")

        # Check if passwords match
        if confirm_password != password:
            msg = "Password and Confirm password mismatched."
            return JsonResponse({'success': False, 'message': msg})
        
        # Check if email or username already exists
        if User.objects.filter(email=email).exists():
            msg = "Email already exists."
            return JsonResponse({'success': False, 'message': msg})

        if User.objects.filter(username=username).exists():
            msg = "Username already exists."
            return JsonResponse({'success': False, 'message': msg})

        # Create new user
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        msg = 'Signup completed successfully.'
        return JsonResponse({'success': True, 'message': msg})

    return render(request, 'signup.html')
