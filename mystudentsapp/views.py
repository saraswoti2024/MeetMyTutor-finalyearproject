from django.shortcuts import render,redirect
from profileapp.models import *
from requestapp.models import Requesting_tutor
from django.contrib import messages
from mytutorapp.models import Feedback
from django.db.models import Exists, OuterRef
# Create your views here.

#incomplete students
def mystudents(request):
    tutor = Profile_Tutor.objects.get(user=request.user)
    data = Requesting_tutor.objects.filter(status='accepted',tutor_user=tutor,is_complete=False)
    context = {
        'data' : data,
        'active_tab': 'incomplete',
    }
    return render(request,'student/incomplete_tutor_students.html',context)

#complete in table button
def is_complete_view(request,id):
    try:
        data = Requesting_tutor.objects.get(id=id)
        if request.method == 'POST':
                data.is_complete = True
                data.save()
                return redirect('mystudents')
    except Exception as e:
        messages.error(request,f'{str(e)}')
        return redirect('mystudents')

#completed session 
def completed_view(request):
    tutor = Profile_Tutor.objects.get(user=request.user)
    value = Requesting_tutor.objects.filter(status='accepted',is_complete=True)
    value = value.annotate(
        feedback_given=Exists(
            Feedback.objects.filter(
                req_tutor=OuterRef('pk'),
                tutor_user=tutor
            )
        )
    )
    context = {
        'value' : value,
        'active_tab': 'completed'
    }
    return render(request,'student/complete_tutor_students.html',context)

#all_students
def all_students(request):
    value = Requesting_tutor.objects.filter(status='accepted')
    context = {
        'value' : value,
        'active_tab': 'all_students',
    }
    return render(request,'student/all_tutor_students.html',context)