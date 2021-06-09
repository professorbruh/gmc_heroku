from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin


admin.site.site_header = "Admin"
admin.site.site_title = "Welcome to Admin's dashboard"
admin.site.index_title = "Welcome, Admin"

urlpatterns = [
    path('', views.login_view, name='home'),
    path('check', views.check_view, name='check'),
    path('logout', views.logout_view, name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_done.html'), name='password_reset_complete'),

    path('advisor/change_password',views.advisor_change_password_view,name = 'change_password_advisor'),
    path('advisor/view_profile', views.view_profile_advisor_view, name='view_profile_advisor'),
    path('advisor/class_details', views.class_details_view, name='class_details'),
    path('advisor/view_course', views.view_course_advisor_view, name='view_course_advisor'),
    path('advisor/view_grade/<str:course_title>', views.view_grade_advisor_view, name='view_grade_advisor'),
    path('advisor/view_marks', views.view_marks_advisor_view, name='view_marks_advisor'),
    path('advisor/approve_events', views.approve_events_view, name='approve_events'),

    path('student/view_profile', views.view_profile_student_view, name='view_profile_student'),
    path('student/view_marks', views.view_marks_view, name='view_marks'),
    path('student/change_password', views.student_change_password_view, name='change_password_student'),
    path('student/view_course', views.student_view_course_view, name='student_view_course'),
    path('student/view_grade/<str:course_title>', views.student_view_grade_view, name='student_view_grade'),
    path('student/event', views.events_form_view, name='events'),

    path('faculty/view_profile', views.view_profile_faculty_view, name='view_profile_faculty'),
    path('faculty/view_course', views.view_course_faculty_view, name='view_course_faculty'),
    path('faculty/view_course_update', views.view_course_update_faculty_view, name='view_course_update_faculty'),
    path('faculty/view_marks/<str:course_title>', views.view_marks_faculty_view, name='view_marks_faculty'),
    path('faculty/update_marks/<str:course_title>', views.update_marks_view, name='update_marks'),
    path('faculty/view_course_grade', views.view_course_grade_view, name='view_course_grade'),
    path('faculty/view_grade/<str:course_title>', views.view_grade_faculty_view, name='view_grade_faculty'),
    path('faculty/change_password', views.faculty_change_password_view, name='change_password_faculty'),

    path('coe/view_profile', views.view_profile_coe_view, name='view_profile_coe'),
    path('coe/view_course', views.view_course_coe_view, name='view_course_coe'),
    path('coe/update_grade/<str:course_title>', views.update_grade_view, name='update_grade'),
    path('coe/change_password', views.coe_change_password_view, name='change_password_coe'),
    path('coe/view_year', views.view_year_view, name='view_level'),
    path('coe/grace_mark_calculate/<str:year>', views.grace_mark_calculate_view, name='grace_mark_calculate')
]
