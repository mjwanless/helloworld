# pages/views.py
import os

from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
import pickle
import pandas as pd
import pdb

from django.conf import settings


def homePageView(request):
    # return request object and specify page.
    return render(request, 'home.html', {
        'mynumbers':[1,2,3,4,5,6,],
        'firstName': 'Malcolm',
        'lastName': 'Wanless',})

def aboutPageView(request):
    # return request object and specify page.
    return render(request, 'about.html')

def malcolmPageView(request):
    return render(request, 'malcolm.html')

def homePost(request):
    # Use request object to extract choice.

    choice = 8
    gmat = 100  # Initialize gmat variable.

    try:
        # Extract value from request object by control name.
        currentChoice = request.POST['choice']
        gmatStr = request.POST['gmat']
        print("Just before Malcolm's breakpoint")
        # pdb.set_trace()
        # breakpoint()
        print("Just after breakpoint")
        # Crude debugging effort.
        print("*** Years work experience: " + str(currentChoice))

    except:
        return render(request, 'home.html', {
            'errorMessage':'*** The data submitted is invalid. Please try again.',
            'mynumbers': [1, 2, 3, 4, 5, 6, ]})
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', kwargs={'choice':choice,'gmat':gmatStr},))


def results(request, choice, gmat):
    print("*** Inside results()")
    # load saved model

    with open('model_pkl', 'rb') as f:
        loadedModel = pickle.load(f)

    # Create a single prediction.
    singleSampleDf = pd.DataFrame(columns=['gmat', 'work_experience'])

    workExperience = float(choice)
    print("*** GMAT Score: " + str(gmat))
    print("*** Years experience: " + str(workExperience))
    singleSampleDf = singleSampleDf._append({'gmat':gmat,
                                             'work_experience':workExperience},
                                            ignore_index=True)

    singlePrediction = loadedModel.predict(singleSampleDf)

    print("Single prediction: " + str(singlePrediction))

    return render(request, 'results.html', {'choice': workExperience, 'gmat':gmat,
                                            'prediction':singlePrediction})