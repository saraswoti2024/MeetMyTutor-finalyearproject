from django.shortcuts import render,redirect,get_object_or_404
from profileapp.models import *
from requestapp.models import *
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm
from django.db.models import Exists, OuterRef
from .models import Feedback
def my_tutors_view(request):
    student = Profile_Student.objects.get(user=request.user)
    if student:
        list_req = Requesting_tutor.objects.filter(student_user_id=student,status='accepted')
    context = {
        'list_req' : list_req,
        'active_tab': 'all_tutors',
    } 
    return render(request,'mytutors/my_tutors.html',context)

def mytutors_ongoing(request):
    student = Profile_Student.objects.get(user=request.user)
    if student:
        list_req = Requesting_tutor.objects.filter(student_user_id=student,status='accepted',is_complete=False)
    context = {
        'list_req' : list_req,
        'active_tab': 'incomplete',
    } 
    return render(request,'mytutors/incomplete_my_tutors.html',context)

def mytutors_complete(request):
    student = Profile_Student.objects.get(user=request.user)
    if student:
        list_req = Requesting_tutor.objects.filter(student_user_id=student,status='accepted',is_complete=True)
        list_req = list_req.annotate(
        feedback_given=Exists(
            Feedback.objects.filter(
                req_tutor=OuterRef('pk'),
                student_user=student
            )
        )
    )
    context = {
        'list_req' : list_req,
        'active_tab': 'completed',
    } 
    return render(request,'mytutors/complete_my_tutors.html',context)


@login_required(login_url='log_in')
def feedback_view(request, id):
    req_tutor = get_object_or_404(Requesting_tutor, id=id)
    tutor_profile = req_tutor.tutor_user  # Assuming FK to Profile_Tutor
    student_profile = Profile_Student.objects.get(user=request.user)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.tutor_user = tutor_profile
            feedback.student_user = student_profile
            feedback.req_tutor = req_tutor
            feedback.user = request.user
            feedback.is_feedback = True
            feedback.save()
            return redirect('feedback_thankyou')
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback_tutor.html', {
        'form': form,
    })
    
def feedback_thankyou(request):
    return render(request, 'feedback/feedback_thankyou.html')

def student_feedback_view(request,id):
    tutors = Requesting_tutor.objects.get(id=id)
    student = Profile_Student.objects.get(user=request.user)
    show = Feedback.objects.filter(tutor_user = tutors.tutor_user, student_user = student,req_tutor = tutors).first()
    if request.method == 'POST':
        tutors = Requesting_tutor.objects.get(id=id)
        student = Profile_Student.objects.get(user=request.user)
        show = Feedback.objects.filter(tutor_user = tutors.tutor_user, student_user = student,req_tutor = tutors).first()
        show.delete()
        return redirect('my_tutors_complete')
    context = {
        'show' : show,
    }
    return render(request,'feedback/view_feedback_student.html',context)

def tutor_feedback_view(request,id):
    student = Requesting_tutor.objects.get(id=id)
    tutors = Profile_Tutor.objects.get(user=request.user)
    show = Feedback.objects.filter(student_user = student.student_user, tutor_user = tutors,req_tutor = student).first()
    context = {
        'show' : show,
    }
    return render(request,'feedback/view_feedback_tutor.html',context)