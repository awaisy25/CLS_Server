from django.urls import path
from . import views

urlpatterns = [
   path("jobs/", views.Jobs.as_view()),
   path('university/', views.Universities.as_view()),
   path('university/<int:pk>', views.UniversityById.as_view()),
   path('salary/', views.Salaries.as_view()),
   path('calculations/', views.PayOffEstimate.as_view()),
]