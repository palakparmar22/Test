from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.signin, name='signin_'),
    path("signup", views.signup, name='signup'),
    path("signin/", views.signin, name='signin'),
    path('signout', views.signout, name="signout"),
    path('force_signout_test', views.force_signout_test, name="force_signout_test"),
    path('force_signout_tech_test', views.force_signout_tech_test, name="force_signout_tech_test"),
    path('parse_data/<int:id>/', views.parse_data, name="parse_data"),
    path('hr/', views.hr, name='hr'),
    path('candidate/', views.candidate, name='candidate'),
    path('employee/', views.employee, name='employee'),
    path('dataview/<int:id>/', views.dataview, name='dataview'),
    path("delete/<int:id>/ ", views.delete, name='delete'),
    path("test/", views.test, name='test'),
    path('test_check/<int:id>/', views.test_check, name='test_check'),
    path('test_result/<int:id>/', views.test_result, name='test_result'),
    path('tech_test_result/<int:id>/', views.tech_test_result, name='tech_test_result'),
    path("result", views.result, name='result'),
    path("contactus/", views.contactus, name='contactus'),
    path("delete_query", views.delete_query, name='delete_query'), 
    path("about/", views.about, name='about'), 
    path("current_openings/", views.current_openings, name='current_openings'),
    path("tech_test/", views.tech_test, name='technical_test'),
    path("test_complete/", views.test_complete, name='test_complete'),
    path("tech_test_check/<int:id>/", views.tech_test_check, name='tech_test_check'),
    path("tech_test_result/<int:id>/", views.tech_test_result, name='tech_test_result'),
    path("thanks/", views.thanks, name='thanks'),
    path("verification/", views.verification, name='verification'),
    path("success_otp/", views.success_otp, name='success_otp'),
    path("forgot_pwd/", views.forgot_pwd, name='forgot_pwd'),
    path("reset_pwd/", views.reset_pwd, name='reset_pwd'),
    path("reset_success/", views.reset_success, name='reset_success'),
    path("resend1/", views.resend1, name='resend1'),
    path("resend2/", views.resend2, name='resend2'),
    path("apt_info/", views.apt_info, name='apt_info'),
    path("test_complete/", views.test_complete, name='test_complete'),
    path("delete_ufm", views.delete_ufm, name='delete_ufm'),
    path("delete_job", views.delete_job, name='delete_job'),
    path("add_job", views.add_job, name='add_job'),
    path("usermgnt", views.usermgnt, name='usermgnt'),
    path('editadmin/<int:id>',views.editadmin,name='editadmin'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)