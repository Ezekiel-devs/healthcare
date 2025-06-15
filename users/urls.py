from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('inscription/', views.register_patient_view, name='register'),
    path('connexion/', views.login_view, name='login'),
    path('deconnexion/', views.logout_view, name='logout'),
    path('profil/modifier/', views.profile_update_view, name='profile_update'),
    path('dashboard/', views.dashboard_redirect_view, name='dashboard-redirect'),
    path('dashboard/patient/', views.patient_dashboard_view, name='patient_dashboard'),
    path('dashboard/medecin/', views.doctor_dashboard_view, name='doctor_dashboard'),
    path('patient/<int:pk>/', views.patient_profile_view_for_doctor, name='patient_profile'),
    path('schedule/', views.doctor_schedule_view, name='doctor_schedule'),
]