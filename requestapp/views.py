from django.shortcuts import render,get_object_or_404,redirect
from profileapp.models import *
from requestapp.models import Requesting_tutor
from django.contrib import messages
from django.core.exceptions import ValidationError
from categories.models import subjects_list

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile_Tutor, Profile_Student, Requesting_tutor, subjects_list

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile_Tutor, Profile_Student, Requesting_tutor, subjects_list
from django.contrib.auth.decorators import login_required

@login_required(login_url='log_in')
def tutor_session_request(request, id):
    tutor = get_object_or_404(Profile_Tutor, id=id)
    student = Profile_Student.objects.get(user=request.user)

    # Extract subject names from tutor's education_data JSON
    subject_names = set()
    for level in tutor.education_data:
        subject_names.update(level.get('subjects', []))

    # Get subject objects matching those names
    subjects = subjects_list.objects.filter(subject_name__in=subject_names)

    if request.method == 'POST':
        try:
            selected_subject_ids = request.POST.getlist('subjects')
            selected_subject_ids = [int(sid) for sid in selected_subject_ids if sid.strip().isdigit()]
            mode = request.POST.get('mode')
            time_from = request.POST.get('time_from')
            time_to = request.POST.get('time_to')
            start_date = request.POST.get('date_start')
            end_date = request.POST.get('date_end')
            priceperhour = request.POST.get('perhour')
            desc = request.POST.get('desc')

            data = Requesting_tutor(
                proposed_rate=priceperhour,
                session_start_date=start_date,
                session_end_date=end_date,
                session_time_from=time_from,
                session_time_to=time_to,
                student_user=student,
                tutor_user=tutor,
                desc = desc,
                mode = mode,
            )
            data.full_clean()  # Validate before saving
            data.save()
            data.subject.set(selected_subject_ids)  # Set ManyToMany subjects

            messages.success(request, 'Request sent successfully!')
            return redirect('tutor_session_request', id)

        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('tutor_session_request', id)

    context = {
        'tutor': tutor,
        'subjects': subjects,
    }
    return render(request, 'request_session/request_tutor.html', context)

def tutor_request(request):
    tutor = Profile_Tutor.objects.get(user=request.user)
    if tutor:
        list_req_tutor = Requesting_tutor.objects.filter(tutor_user=tutor)
    context = {
        'req_list' : list_req_tutor,
    } 
    return render(request,'request_session/request_view_tutor.html',context)
    
def student_request(request):
    student = Profile_Student.objects.get(user=request.user)
    if student:
        list_req = Requesting_tutor.objects.filter(student_user_id=student)
    context = {
        'list_req' : list_req,
    } 
    return render(request,'request_session/request_view.html',context)

def counter_offer(request,id):
    data2 = get_object_or_404(Requesting_tutor,id=id)
    data = data2.student_user
    if request.method == 'POST':
        data2.counter_start_date = request.POST.get('counter_start_date')
        data2.counter_end_date = request.POST.get('counter_end_date')
        data2.counter_time_from = request.POST.get('counter_time_from')
        data2.counter_time_to = request.POST.get('counter_time_to')
        data2.counter_proposed_rate = request.POST.get('counter_proposed_rate')
        data2.desc = request.POST.get('desc')
        data2.status = 'counter offered'
        data2.save()
        messages.success(request,'counter offer sent succesfully!')
        return redirect('request_list_tutor')
        
    context = {
        'data': data,
        'data2' : data2,
    }
    return render(request,'request_session/counter_offer.html',context)

def accept_request(request,id):
    if request.method == 'POST':
        value = request.POST.get('submit_btn')
        data2 =get_object_or_404(Requesting_tutor,id=id)
        if value == 'accepted':
            data2.status = 'accepted'
        else:
            data2.status = 'rejected'
        data2.save()
        messages.success(request,'accepted successfully!')
        return redirect('request_list_tutor')
    
def edit_accept_request(request,id):
    if request.method == 'POST':
        value = request.POST.get('submit_btn')
        data2 =get_object_or_404(Requesting_tutor,id=id)
        if value == 'accepted':
            data2.status = 'accepted'
            data2.is_edit = True
        else:
            data2.status = 'rejected'
            data2.is_edit = True
        data2.save()
        messages.success(request,'accepted successfully!')
        return redirect('request_list_tutor')

def edit_request(request,id):
    data2 = get_object_or_404(Requesting_tutor,id=id)
    data = data2.student_user
    if request.method == 'POST':
        data2.counter_start_date = request.POST.get('counter_start_date')
        data2.counter_end_date = request.POST.get('counter_end_date')
        data2.counter_time_from = request.POST.get('counter_time_from')
        data2.counter_time_to = request.POST.get('counter_time_to')
        data2.counter_proposed_rate = request.POST.get('counter_proposed_rate')
        data2.desc = request.POST.get('desc')
        data2.status = 'counter offered'
        data2.is_edit = True
        data2.save()
        messages.success(request,'counter offer sent succesfully!')
        return redirect('request_list_tutor')
        
    context = {
        'data': data,
        'data2' : data2,
    }
    return render(request,'request_session/edit_request.html',context)

def counter_offer_view(request,id):
    data2 = get_object_or_404(Requesting_tutor,id=id)
    data = data2.student_user
    if request.method == 'POST':
        value = request.POST.get('submit_btn')
        data2 = get_object_or_404(Requesting_tutor,id=id)
        data = data2.student_user
        if value == 'accepted':
            data2.status = 'accepted'
        else:
            data2.status = 'rejected'
        data2.save()
        messages.success(request,'offer successfully!')
        return redirect('request_list')
    context = {
        'data' : data,
        'data2' : data2,
    }
        
    return render(request,'request_session/counter_offer_view.html',context)