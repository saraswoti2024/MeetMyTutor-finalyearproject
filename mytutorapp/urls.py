from django.urls import path
from mytutorapp import views

urlpatterns = [
     path('my_tutors/',views.my_tutors_view,name="my_tutors"), 
     path('ongoing_sessions/',views.mytutors_ongoing,name="my_tutors_ongoing"), 
     path('complete_sessions/',views.mytutors_complete,name="my_tutors_complete"), 
     path('feedback/<int:id>', views.feedback_view, name='feedback_form'),
     path('feedback/thank-you/', views.feedback_thankyou, name='feedback_thankyou'),
     path('view_feedback/<int:id>', views.student_feedback_view, name='feedback_view_student'),
     path('view_feedback_tutor/<int:id>', views.tutor_feedback_view, name='feedback_view_tutor'),
]

  