from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    # Create rdv
    path('new/', views.create_appointment_view, name='create'),
    # Update rdv
    path('<int:pk>/update/', views.update_appointment_view, name='update'),
    path('<int:pk>/delete/', views.delete_appointment_view, name='delete'),

    #### Doctor
    path('<int:pk>/process/', views.process_appointment_view, name='process'), # pour voir les détails et décider
    path('<int:pk>/confirm/', views.confirm_appointment_action, name='confirm_action'),
    path('<int:pk>/refuse/', views.refuse_appointment_action, name='refuse_action'),
]